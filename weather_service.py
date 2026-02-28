"""
This Module manages the weather data retrieval process.
"""
import executor
import queries
import geocoding
import weather_report


def create_schema(connection_object):
    """
    Create the tables from the database table. Should be declared at first run
    :param connection_object: psycopg2.connection object
    :return: None
    """
    executor.execute_query(connection_object,queries.create_weather_table)
    executor.execute_query(connection_object,queries.create_locations_table)
    executor.execute_query(connection_object,queries.create_weather_snapshots_table)
    executor.execute_query(connection_object,queries.create_weather_forecast_table)

def get_location_data(connection_object,loc):
    """ Retrieve location information from the database.
    :param connection_object: psycopg2.connection object
    :param loc: A tuple containing city name and country code
    :return: A tuple containing location data in database column order if exist else None"""
    return executor.fetch_one(connection_object, queries.select_location_id, loc)

def get_current_weather_data(connection_object,loc_id):
    """ Retrieve current weather data from the database.
    :param connection_object: psycopg2.connection object
    :param loc_id: ID from locations table
    :return: A tuple containing current weather data in database column order if exist else None"""
    return executor.fetch_one(connection_object, queries.select_current_weather_snapshot, (loc_id,))

def get_predicted_weather_data(connection_object, loc_id):
    """Retrieve the weather prediction closest to the current time.
    :param connection_object: psycopg2.connection object
    :param loc_id: ID from locations table
    :return: A tuple containing current weather data in database column order if exist else None"""
    return executor.fetch_one(connection_object, queries.select_nearest_weather_forecast_snapshot, (loc_id,))

def check_weather_code(connection_object,weather_info):
    """
    Checks if a weather condition code is already in the database. If not,inserts it.
    :param connection_object: psycopg2.connection object
    :param weather_info: tuple of weather condition (weather_id, main, description)
    :return: None
    """
    weather = executor.fetch_one(connection_object, queries.select_weather_code, (weather_info[0],))
    if weather is None:
        executor.execute_query(connection_object,queries.insert_into_weather_table,weather_info)


def get_weather_data(connection, loc: tuple[str,str], comparison: bool, api_key:str):
    """
    Retrieve weather data from the database.
    :param connection: psycopg2.connection object
    :param loc: tuple containing city name and country code
    :param comparison: bool for comparison between current weather data and predicted weather data
    :param api_key: API key from OpenWeatherMap
    :return: tuple of current weather data and predicted if comparison is true else tuple of just current weather data
    """
    location_data = get_location_data(connection,loc) # Check if location exists in database
    if location_data is None: # If location not found, fetch from geocoding API and insert
        location_info = geocoding.main(loc,api_key)
        executor.execute_query(connection,queries.insert_into_locations_table,location_info)
        location_data = get_location_data(connection,loc)

    # Extract location ID and coordinates
    location_id = location_data[0]
    cty = (location_data[1], location_data[2])

    current_data = get_current_weather_data(connection,location_id) # Check if we have recent cached weather data (within last hour)
    predicted_data = get_predicted_weather_data(connection,location_id)  # Check if prediction data exists (for comparison mode)
    hourly_weather = None
    if current_data is None: # If no cached current weather, fetch from API
        present_weather, hourly_weather = weather_report.main(cty,location_id,api_key)
        check_weather_code(connection,present_weather.weather_info)
        executor.execute_query(connection, queries.insert_into_weather_snapshots_table, present_weather.to_tuple())
        current_data = get_current_weather_data(connection,location_id)

    if comparison and predicted_data is None: # If comparison requested and no predictions exist
        if hourly_weather is None: # Reuse hourly data if already fetched, otherwise fetch from API
            hourly_weather = weather_report.main(cty,location_id,api_key)[1]
            for hour in hourly_weather: # Ensure all weather codes exist before insert
                check_weather_code(connection,hour.weather_info)
        executor.execute_many(connection,queries.insert_into_weather_forecast_table,[data.to_tuple() for data in hourly_weather])
        predicted_data = get_predicted_weather_data(connection,location_id)

    return (current_data,predicted_data) if comparison else (current_data,)