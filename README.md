# 🌤️ Weather Tracker

A Python CLI application that fetches, stores, and compares real-time and forecasted weather data using the OpenWeatherMap API and a PostgreSQL database.

---

## Features

- **Current weather lookup** — Fetch live weather conditions for any city worldwide
- **Forecast comparison** — Compare current weather against the nearest predicted forecast
- **Smart caching** — Avoids redundant API calls by caching results (current: 1 hour, forecast: 48 hours)
- **PostgreSQL persistence** — Stores weather snapshots, forecasts, and location data
- **Automatic geocoding** — Resolves city names to coordinates via the OpenWeatherMap Geocoding API

---

## Tech Stack

- **Python 3.10+**
- **PostgreSQL** via `psycopg2`
- **OpenWeatherMap API** (One Call API 3.0 + Geocoding API)
- `requests`, `python-dotenv`

---

## Project Structure

```
weather-tracker/
├── main.py               # Entry point — handles user input and orchestration
├── weather_service.py    # Core logic — coordinates DB checks and API calls
├── weather_report.py     # Fetches current weather and hourly forecast from OWM API
├── weather_snapshot.py   # WeatherSnapshot class — models a single weather observation
├── geocoding.py          # Converts city names to coordinates via Geocoding API
├── executor.py           # PostgreSQL connection and query execution helpers
├── queries.py            # All SQL queries and schema definitions
├── visual_output.py      # Formats and prints weather data to the terminal
└── requirements.txt
```

---

## Database Schema

```
locations            — City coordinates and metadata
weather              — Weather condition codes, names, and descriptions
weather_snapshots    — Current weather observations (timestamped)
weather_forecast     — 48-hour hourly forecast data (timestamped, deduped)
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Dyn-Bmg/Weather-Tracker.git
cd Weather-Tracker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
API_KEY=your_openweathermap_api_key
```

> Get a free API key at [openweathermap.org](https://openweathermap.org/api). Note that the One Call API 3.0 requires a paid subscription.

### 4. Initialize the database schema

On first run, call `create_schema` from `weather_service.py` to set up the tables:

```python
import weather_service
weather_service.create_schema(connection)
```

This only needs to be done once.

---

## Usage

```bash
python main.py
```

You will be prompted to:

1. Enter a **city name**
2. Enter a **2-letter country code** (e.g. `NG`, `US`, `GB`)
3. Choose an option:
   - `0` — Get current weather
   - `1` — Compare current weather with the nearest forecast

### Example output

```
=== CURRENT WEATHER FOR LAGOS,NG ===
Time:        2025-06-01 14:00:00 WAT
Temperature: 29.4°C
Feels like:  33.1°C
Humidity:    82%
Pressure:    1010 hPa
Wind Speed:  3.6 m/s
Weather Description: Moderate Rain
```

---

## Caching Behaviour

| Data type        | Cache duration |
|------------------|----------------|
| Current weather  | 1 hour         |
| Forecast data    | 48 hours       |
| Location data    | Permanent      |

The app checks the database before making any API call. If fresh data exists, it is returned directly without hitting the API.

---

## License

MIT