import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta
from ..domain.interfaces import WeatherService
from ..domain.entities import PollenForecast, PollenLevel
import random
import time

class OpenMeteoService(WeatherService):
    def __init__(self, lat: str, lon: str):
        self.lat = lat
        self.lon = lon
        self.last_request_time = None
        self.min_request_interval = timedelta(seconds=10)  # Minimum time between requests
        
        # Create a session with retry logic
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def get_pollen_forecast(self) -> PollenForecast:
        try:
            # Rate limiting
            if self.last_request_time:
                elapsed = datetime.now() - self.last_request_time
                if elapsed < self.min_request_interval:
                    sleep_time = (self.min_request_interval - elapsed).total_seconds()
                    print(f"Rate limiting: waiting {sleep_time:.1f} seconds...")
                    time.sleep(sleep_time)
            
            url = "https://air-quality-api.open-meteo.com/v1/air-quality"
            params = {
                "latitude": self.lat,
                "longitude": self.lon,
                "hourly": "pm10,pm2_5,us_aqi,dust",  # Air quality metrics
                "timezone": "America/Chicago"
            }
            
            print("Fetching air quality data...")
            response = self.session.get(url, params=params, timeout=10)
            self.last_request_time = datetime.now()
            response.raise_for_status()
            data = response.json()
            print("Data received successfully")
            
            # Get current hour's data
            current_hour = datetime.now().hour
            pm10 = data['hourly']['pm10'][current_hour]  # Larger particles (like pollen)
            pm2_5 = data['hourly']['pm2_5'][current_hour]  # Smaller particles
            dust = data['hourly']['dust'][current_hour]
            aqi = data['hourly']['us_aqi'][current_hour]
            
            # Map AQI to our levels (using EPA standards)
            def get_level(aqi_value):
                if aqi_value <= 50:
                    return "Low"
                elif aqi_value <= 100:
                    return "Moderate"
                elif aqi_value <= 150:
                    return "High"
                else:
                    return "Very High"
            
            overall_level = get_level(aqi)
            
            level_mapping = {
                "Low": PollenLevel.LOW,
                "Moderate": PollenLevel.MODERATE,
                "High": PollenLevel.HIGH,
                "Very High": PollenLevel.VERY_HIGH
            }
            
            description = (
                f"Air Quality Levels:\n"
                f"Air Quality Index: {aqi} ({get_level(aqi)})\n"
                f"Large Particles (PM10): {pm10:.1f} µg/m³\n"
                f"Fine Particles (PM2.5): {pm2_5:.1f} µg/m³\n"
                f"Dust: {dust:.1f} µg/m³\n\n"
                f"Note: High levels of PM10 and dust often correlate with high pollen levels."
            )
            
            return PollenForecast(
                level=level_mapping[overall_level],
                timestamp=datetime.now(),
                description=description
            )
            
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {str(e)}")
            print("Please check your internet connection")
            raise
        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {str(e)}")
            print("The server took too long to respond")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Failed to get air quality forecast: {str(e)}")
            print("Error type:", type(e).__name__)
            raise
        finally:
            self.session.close()

class MockWeatherService(WeatherService):
    def get_pollen_forecast(self) -> PollenForecast:
        levels = list(PollenLevel)
        random_level = random.choice(levels)
        return PollenForecast(
            level=random_level,
            timestamp=datetime.now(),
            description=f"Mock pollen level: {random_level.value}"
        ) 