"""
This module defines the WeatherSnapshot class, which represents a single weather
observation at a specific location and time.
"""
from datetime import datetime, timezone, timedelta
class WeatherSnapshot:
    """
    Represents a single weather observation at a specific location and time.
    """
    def __init__(self, dict_data: dict,offset: int,location_id:int) -> None:
        """
        Initialize a WeatherSnapshot object from OpenWeatherMap API response
        with relevant attributes for database insertion.
        :param dict_data: Weather data from OpenWeatherMap API
        :param offset: Timezone offset from UTC
        :param location_id: ID from the locations table
        """
        tz = timezone(timedelta(seconds=offset))
        self.location_id = location_id
        self.timestamp = datetime.fromtimestamp(dict_data['dt'], tz=tz)
        self.temp = float(dict_data['temp'])
        self.feels_like = float(dict_data['feels_like'])
        self.humidity = int(dict_data['humidity'])
        self.pressure = int(dict_data['pressure'])
        self.wind_speed = float(dict_data['wind_speed'])
        weather = dict_data['weather'][0]
        self.weather_id = int(weather['id'])
        self.weather_info = (weather['id'], weather['main'], weather['description'])

    def to_tuple(self) -> tuple:
        """
        Convert the weather snapshot to a tuple for database insertion.
        :return: Weather data in database column order
        """
        return self.location_id, self.timestamp, self.temp, self.feels_like, self.humidity, self.pressure, self.wind_speed, self.weather_id



