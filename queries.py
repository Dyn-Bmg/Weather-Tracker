"""
This module contains all SQL queries used by the weather tracking application,
including table creation statements and data manipulation queries.

Weather-Tracker Database Schema:
    - weather: weather condition data
    - locations: location data
    - weather_snapshots: Current weather data
    - weather_prediction: Forecasted weather data
"""


create_weather_table = """
CREATE TABLE weather (
    weather_id SMALLINT PRIMARY KEY NOT NULL,
    main TEXT NOT NULL,
    description TEXT NOT NULL
);
"""

create_locations_table = """
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    city TEXT,
    state TEXT,
    country_code CHAR(2) NOT NULL,
    CONSTRAINT unique_location_coords UNIQUE (latitude, longitude)
);
"""

create_weather_snapshots_table = """
CREATE TABLE weather_snapshots (
    id BIGSERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations(id),
    weather_timestamp TIMESTAMPTZ NOT NULL,
    temperature REAL NOT NULL,
    feels_like REAL NOT NULL,
    humidity INTEGER NOT NULL,
    pressure INTEGER NOT NULL,
    wind_speed REAL NOT NULL,
    weather_code INTEGER NOT NULL REFERENCES weather(weather_id), 
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

create_weather_forecast_table = """CREATE TABLE weather_forecast (
    id BIGSERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations(id),
    weather_timestamp TIMESTAMPTZ NOT NULL,
    temperature REAL NOT NULL,
    feels_like REAL NOT NULL,
    humidity INTEGER NOT NULL,
    pressure INTEGER NOT NULL,
    wind_speed REAL NOT NULL,
    weather_code INTEGER NOT NULL REFERENCES weather(weather_id),
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_location_timestamp UNIQUE (location_id, weather_timestamp)
);
"""

insert_into_weather_table = """
INSERT INTO weather (weather_id, main, description)
VALUES (%s, %s, %s)
"""

insert_into_locations_table = """
INSERT INTO locations (longitude, latitude, city, state, country_code)
VALUES (%s, %s, %s, %s, %s)"""

insert_into_weather_snapshots_table = """
INSERT INTO weather_snapshots 
(location_id, weather_timestamp, temperature, feels_like, humidity, pressure, 
 wind_speed, weather_code) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

insert_into_weather_forecast_table = """
INSERT INTO weather_forecast
(location_id, weather_timestamp, temperature, feels_like, humidity, pressure, 
 wind_speed, weather_code) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (location_id,weather_timestamp) DO NOTHING
"""

select_weather_code = """
SELECT * FROM weather
WHERE weather_id = %s
"""

select_location_id = """
SELECT id, longitude, latitude FROM locations
WHERE city = %s and country_code = %s
LIMIT 1
"""

select_current_weather_snapshot ="""
SELECT weather_timestamp, temperature, feels_like, humidity, pressure, 
wind_speed, weather.description FROM weather_snapshots
LEFT OUTER JOIN weather ON weather_snapshots.weather_code = weather.weather_id
WHERE location_id = %s 
AND fetched_at >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
LIMIT 1
"""

select_nearest_weather_forecast_snapshot = """
SELECT weather_timestamp, temperature, feels_like, humidity, pressure, 
wind_speed, weather.description FROM weather_forecast
LEFT OUTER JOIN weather ON weather_forecast.weather_code = weather.weather_id
WHERE location_id = %s AND fetched_at >= CURRENT_TIMESTAMP - INTERVAL '48 hour'
ORDER BY ABS(EXTRACT(EPOCH FROM (weather_timestamp - NOW())))
LIMIT 1
"""

