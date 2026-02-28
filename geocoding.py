"""
This module handles geocoding operations by converting city names to geographic
coordinates using the OpenWeatherMap Geocoding API.
"""

import requests

def city_cleaner(geo_json_data:dict) -> tuple:
    """
    Takes the raw JSON response from the geocoding API and extracts the first
    matching location, formatting it into a standardized tuple for database storage.
    :param geo_json_data: JSON response from the API containing location data
    :return: A tuple containing (longitude, latitude, city_name, state, country_code)
    """
    city = geo_json_data[0]
    if 'state' not in city:
        city['state'] = None
    city_info = (city['lon'], city['lat'], city['name'], city['state'], city['country'])
    return city_info

def crawler(loc:tuple, api_key:str) -> dict:
    """
    Fetch geographic coordinates for a city from OpenWeatherMap Geocoding API.
    Makes a GET request to the OpenWeatherMap Geocoding API to retrieve
    location data for the specified city and country.
    :param api_key: API key from OpenWeatherMap
    :param loc: A tuple containing(city name, country code)
    :return: JSON response from the API containing location data
    """
    city,country = loc[0],loc[1]
    location = city + "," + country
    with requests.Session() as session:
        param = {"q": location, "appid": api_key}
        response = session.get("https://api.openweathermap.org/geo/1.0/direct", params=param)
        print(response.status_code)
        response.raise_for_status()
        data = response.json()
    return data

def main(location:tuple[str,str],api_key:str) -> tuple:
    """
    Convert a location tuple containing a city name and country code to relevant location detail for storage.
    :param api_key: API key from OpenWeatherMap
    :param location: A tuple containing(city_name, Two-letter ISO country code)
    :return: A tuple containing location data in database column order
    """
    city_data = city_cleaner(crawler(location,api_key))
    return city_data





