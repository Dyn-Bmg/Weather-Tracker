"""
This module formats and prints weather information in human-readable formats
"""
def print_result(data,location):
    """
    Prints result in easily understable format.
    :param data: tuple containing current weather data tuple and optionally predicted weather data tuple
    :param location: tuple containing city name and country code
    :return: None
    """
    location = location[0].upper() + ',' + location[1]
    if len(data) == 1:
        result = data[0]
        dt = result[0].strftime("%Y-%m-%d %H:%M:%S %Z")
        desc = str(result[6]).title()
        print(f"\n=== CURRENT WEATHER FOR {location} ===")
        print(f"Time:        {dt}")
        print(f"Temperature: {result[1]}°C")
        print(f"Feels like: {result[2]}°C")
        print(f"Humidity:    {result[3]}%")
        print(f"Pressure:    {result[4]} hPa")
        print(f"Wind Speed:  {result[5]} m/s")
        print(f"Weather Description: {desc}")
    else:
        current,predicted = data[0],data[1]
        ct,pt = current[0].strftime("%Y-%m-%d %H:%M:%S %Z"),predicted[0].strftime("%Y-%m-%d %H:%M:%S %Z")
        desc,desp = str(current[6]).title(),str(predicted[6]).title()
        print(f"\n=== COMPARISON WEATHER(CURRENT TO PREDICTED) FOR {location} ===")
        print(f"Time:        {ct}              |     {pt}")
        print(f"Temperature: {current[1]}°C    |     {predicted[1]}°C")
        print(f"Feels like: {current[2]}°C     |     {predicted[2]}°C")
        print(f"Humidity:    {current[3]}%    |     {predicted[3]}%")
        print(f"Pressure:    {current[4]} hPa    |     {predicted[4]} hPa")
        print(f"Wind Speed:  {current[5]} m/s    |     {predicted[5]} m/s")
        print(f"Weather Description: {desc}        |     {desp}")
