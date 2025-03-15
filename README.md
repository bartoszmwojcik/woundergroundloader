# Weather Underground Data Loader

A Python tool to fetch and store weather data from a Weather Underground Personal Weather Station into a SQLite database.

## Features

- Fetches historical weather data from Weather Underground API
- Stores data in SQLite database with automatic deduplication
- Supports hourly data collection
- Calculates wind turbine power output based on wind speed
- Handles large date ranges efficiently with progress tracking
- Memory-efficient processing (processes one record at a time)

## Installation

1. Clone the repository:
```bash
git clone git@github.com:bartoszmwojcik/woundergroundloader.git
cd woundergroundloader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Weather Underground API credentials:
```bash
WUNDERGROUND_API_KEY=your_api_key_here
WUNDERGROUND_STATION_ID=your_station_id_here
```

## Usage

### Basic Usage

To fetch the last 30 days of data:
```bash
python main.py
```

### Specific Date Range

To fetch data for a specific date range:
```bash
python main.py --start-date 2023-01-01 --end-date 2023-12-31
```

### Last N Days

To fetch data for the last N days:
```bash
python main.py --days 365
```

## Data Storage

Weather data is stored in a SQLite database (`weather_data.db`) with the following measurements:
- Temperature (°C)
- Wind Speed (km/h)
- Wind Direction (degrees)
- Wind Chill (°C)
- Wind Gusts (km/h)
- Precipitation (mm)
- Pressure (hPa/mb)
- Calculated Wind Power (W)

## Wind Power Calculation

The tool calculates theoretical wind power output based on wind speed:
- Below 2 km/h: 0W (no power generation)
- Above 12 km/h: 1600W (maximum power)
- Between 2-12 km/h: Power = 16 * (windspeed_ms - 2)²
  where windspeed_ms is wind speed in meters per second

## Contributing

Feel free to submit issues and enhancement requests! 