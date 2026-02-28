from dotenv import load_dotenv
load_dotenv()

import os
import executor
import visual_output
import weather_service

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
api_key = os.getenv("API_KEY")

connection = executor.create_connection(db_name, db_user, db_password, db_host, db_port)


try:
    print("WELCOME!!!!")
    city,country = (input("Enter city: ").title(), input("Enter country: ").upper())
    print("Option 0: Get current weather")
    print("Option 1: Compare current weather with predicted weather")
    compare =  bool(int(input("Select Option: ")))
    weather_data = weather_service.get_weather_data(connection,(city, country), compare, api_key)
    visual_output.print_result(weather_data,(city,country))

finally: # Ensures database connection is closed even if errors occur
    if connection is not None:
        connection.close()