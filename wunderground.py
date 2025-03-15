import requests
from datetime import datetime, timedelta
import logging
from config import API_KEY, STATION_ID, BASE_URL
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WundergroundClient:
    def __init__(self, api_key=API_KEY, station_id=STATION_ID):
        self.api_key = api_key
        self.station_id = station_id
        if not api_key or not station_id:
            raise ValueError("API key and station ID are required")

    def get_historical_data(self, start_date, end_date=None):
        """
        Fetch historical hourly data for a date range.
        Args:
            start_date (datetime): Start date for historical data
            end_date (datetime, optional): End date for historical data. Defaults to current date.
        """
        if end_date is None:
            end_date = datetime.now()

        current_date = start_date
        while current_date <= end_date:
            logger.info(f"Fetching hourly data for {current_date.date()}")
            try:
                # Weather Underground API endpoint for hourly data
                url = f"{BASE_URL}/pws/history/hourly"
                params = {
                    "apiKey": self.api_key,
                    "stationId": self.station_id,
                    "format": "json",
                    "units": "m",  # metric units
                    "date": current_date.strftime("%Y%m%d")
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                observations = data.get('observations', [])
                
                # Process each hourly observation
                for observation in observations:
                    metric = observation.get('metric', {})
                    imperial = observation.get('imperial', {})  # some fields might be in imperial
                    
                    parsed_data = {
                        'timestamp': datetime.fromtimestamp(observation.get('epoch', 0)),
                        'temp_avg': metric.get('tempAvg'),
                        'temp_high': metric.get('tempHigh'),
                        'temp_low': metric.get('tempLow'),
                        'windchill_avg': metric.get('windchillAvg'),
                        'windchill_high': metric.get('windchillHigh'),
                        'windchill_low': metric.get('windchillLow'),
                        'windgust_avg': metric.get('windgustAvg'),
                        'windgust_high': metric.get('windgustHigh'),
                        'windgust_low': metric.get('windgustLow'),
                        'windspeed_avg': metric.get('windspeedAvg'),
                        'windspeed_high': metric.get('windspeedHigh'),
                        'windspeed_low': metric.get('windspeedLow'),
                        'winddir_avg': observation.get('winddirAvg'),  # wind direction is usually in degrees
                        'precip_rate': metric.get('precipRate'),
                        'pressure_max': metric.get('pressureMax'),
                        'pressure_min': metric.get('pressureMin'),
                        'station_id': self.station_id
                    }
                    
                    # Remove None values to allow database defaults to work
                    parsed_data = {k: v for k, v in parsed_data.items() if v is not None}
                    
                    yield parsed_data
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching weather data for {current_date.date()}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error processing data for {current_date.date()}: {e}")
            
            # Move to next day
            current_date += timedelta(days=1)
            
            # Add a small delay to avoid hitting rate limits
            time.sleep(0.1)

    def get_current_conditions(self):
        """
        Fetch current conditions from the weather station
        Documentation: https://www.wunderground.com/member/api-keys
        """
        try:
            url = f"{BASE_URL}/pws/observations/current"
            params = {
                "apiKey": self.api_key,
                "stationId": self.station_id,
                "format": "json",
                "units": "m"  # metric units
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse the response into our database format
            observation = data.get('observations', [{}])[0]
            metric = observation.get('metric', {})
            
            parsed_data = {
                'timestamp': datetime.fromtimestamp(observation.get('epoch', datetime.utcnow().timestamp())),
                'temperature': metric.get('temp'),
                'humidity': observation.get('humidity'),
                'pressure': metric.get('pressure'),
                'wind_speed': metric.get('windSpeed'),
                'wind_direction': observation.get('winddir'),
                'precipitation': metric.get('precipRate'),
                'solar_radiation': observation.get('solarRadiation'),
                'uv_index': observation.get('uv'),
                'station_id': self.station_id
            }
            
            return parsed_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return None

    def _safe_get(self, data, path):
        """
        Safely navigate nested dictionaries
        """
        for key in path:
            try:
                data = data[key]
            except (KeyError, IndexError, TypeError):
                return None
        return data 