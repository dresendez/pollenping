import os
import sys
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.weather_service import OpenMeteoService
from src.infrastructure.email_service import GmailService
from src.config import (
    EMAIL_ADDRESS, 
    EMAIL_APP_PASSWORD,
    LATITUDE, 
    LONGITUDE
)

def test_weather_notification():
    # Initialize services
    weather_service = OpenMeteoService(
        lat=LATITUDE,
        lon=LONGITUDE
    )
    
    email_service = GmailService(
        email=EMAIL_ADDRESS,
        app_password=EMAIL_APP_PASSWORD
    )
    
    # Email to receive notifications
    recipient_email = os.getenv('RECIPIENT_EMAIL')  # Get from .env
    
    try:
        # Get the forecast
        print("\nGetting air quality forecast...")
        forecast = weather_service.get_pollen_forecast()
        
        # Print the results
        print("\nForecast Results:")
        print(f"Level: {forecast.level.value}")
        print(f"Time: {forecast.timestamp}")
        print(f"Description: {forecast.description}")
        
        # Send email notification
        print(f"\nSending email notification to {recipient_email}...")
        email_service.send_notification(
            to_email=recipient_email,  # Send to different email
            subject=f"Air Quality Alert: {forecast.level.value}",
            body=forecast.description
        )
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error in test: {str(e)}")
        raise

if __name__ == "__main__":
    test_weather_notification() 