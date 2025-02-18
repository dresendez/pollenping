import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.weather_service import OpenMeteoService
from src.config import LATITUDE, LONGITUDE

def test_pollen_forecast():
    # Initialize the weather service
    weather_service = OpenMeteoService(
        lat=LATITUDE,
        lon=LONGITUDE
    )
    
    try:
        # Get the forecast
        forecast = weather_service.get_pollen_forecast()
        
        # Print the results
        print("\nAir Quality Forecast Results:")
        print(f"Level: {forecast.level.value}")
        print(f"Time: {forecast.timestamp}")
        print(f"Description: {forecast.description}")
        
    except Exception as e:
        print(f"Error getting forecast: {str(e)}")

if __name__ == "__main__":
    test_pollen_forecast() 