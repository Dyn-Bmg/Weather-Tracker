"""
This module handles fetching weather data from the OpenWeatherMap API.
It retrieves both current weather observations and hourly forecasts for
a given location.
"""

import requests
import os
from weather_snapshot import WeatherSnapshot



def crawler(info:tuple, api_key:str) -> dict:
    """
    Fetch comprehensive weather data from OpenWeatherMap One Call API 3.0.
    :param api_key: API key from OpenWeatherMap
    :param info: A tuple containing (longitude, latitude)
    :return: JSON response from OpenWeatherMap
    """
    lon = info[0]
    lat = info[1]
    with requests.Session() as session:
        param = {"lat": lat, "lon": lon, "appid": api_key,"units": 'metric'}
        response = session.get("https://api.openweathermap.org/data/3.0/onecall", params=param)
        data = response.json()
    return data

def main(info,city_id,api_key) -> tuple[WeatherSnapshot, list[WeatherSnapshot]]:
    """
    Retrieves weather data from the API and converts it into structured
    WeatherSnapshot objects suitable for database storage
    :param api_key: API key from OpenWeatherMap
    :param info: A tuple containing (longitude, latitude)
    :param city_id: ID from the locations table
    :return: A tuple containing (current_snapshot, hourly_snapshots)
              - current_snapshot: Current WeatherSnapshot object
              - hourly_snapshots: List of 48 hours of WeatherSnapshot objects
    """
    data = crawler(info,api_key)
    offset = data['timezone_offset']
    current = WeatherSnapshot(data['current'], offset,city_id)
    hourly = [WeatherSnapshot(hour, offset,city_id) for hour in data['hourly']]

    return current, hourly
