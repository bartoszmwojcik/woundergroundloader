# Wunderground Weather Station Data Loader

This tool fetches weather data from a Weather Underground personal weather station and stores it in a SQLite database.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your Weather Underground API credentials:
```
WUNDERGROUND_API_KEY=your_api_key_here
STATION_ID=your_station_id_here
```

## Usage

To start collecting weather data:
```bash
python main.py
```

The script will:
- Create a SQLite database if it doesn't exist
- Fetch weather data from your station every 5 minutes
- Store new data points in the database
- Skip any duplicate data points
- Log all activities to the console

## Data Structure

The weather data is stored in a SQLite database with the following fields:
- timestamp: Date and time of the observation
- temperature: Temperature in Celsius
- humidity: Relative humidity percentage
- pressure: Atmospheric pressure
- wind_speed: Wind speed
- wind_direction: Wind direction in degrees
- precipitation: Precipitation amount
- solar_radiation: Solar radiation level
- uv_index: UV index
- station_id: Weather station identifier

## Configuration

You can modify the following settings in `config.py`:
- UPDATE_INTERVAL: Time between data fetches (default: 300 seconds / 5 minutes)
- DATABASE_URL: SQLite database location
- API endpoints and other configuration

## Error Handling

The tool includes comprehensive error handling and logging:
- Failed API requests are logged with error details
- Database connection issues are caught and logged
- Duplicate data entries are detected and skipped
- All activities are logged to the console with timestamps 