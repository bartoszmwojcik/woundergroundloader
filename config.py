import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_KEY = os.getenv('WUNDERGROUND_API_KEY')
STATION_ID = os.getenv('STATION_ID')

# Database Configuration
DATABASE_URL = 'sqlite:///weather_data.db'

# API Endpoints
BASE_URL = 'https://api.weather.com/v2'  # We'll update this with the correct base URL

# Time settings
UPDATE_INTERVAL = 300  # 5 minutes in seconds 