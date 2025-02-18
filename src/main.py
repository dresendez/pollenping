from infrastructure.weather_service import DummyWeatherService
from infrastructure.notification_service import EmailToSMSService
from infrastructure.scheduler_service import SchedulerService
from application.pollen_alert_service import PollenAlertService
from config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    CARRIER,
    DEFAULT_ALERT_TIME
)
from datetime import datetime

def create_alert_service():
    """Create and configure the alert service"""
    weather_service = DummyWeatherService()
    notification_service = EmailToSMSService(
        email=EMAIL_ADDRESS,
        password=EMAIL_PASSWORD,
        carrier=CARRIER
    )
    
    return PollenAlertService(
        weather_service=weather_service,
        notification_service=notification_service
    )

def check_and_send_alert(phone_number: str, alert_service: PollenAlertService) -> None:
    """Wrapper function for the alert service that will be scheduled"""
    print(f"Running scheduled check at {datetime.now()}")
    result = alert_service.check_and_send_alert(phone_number)
    print(f"Alert sent: {result}")

def main():
    # Initialize services
    alert_service = create_alert_service()
    scheduler = SchedulerService()
    
    # Phone number to send alerts to
    phone_number = "8324726640"  # Replace with actual phone number
    
    # Schedule the daily check
    scheduler.schedule_daily_job(
        lambda: check_and_send_alert(phone_number, alert_service),
        DEFAULT_ALERT_TIME
    )
    
    print(f"Starting scheduler. Will check pollen levels daily at {DEFAULT_ALERT_TIME}")
    scheduler.start()

if __name__ == "__main__":
    main() 