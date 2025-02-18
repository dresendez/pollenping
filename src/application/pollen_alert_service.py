from ..domain.interfaces import WeatherService, NotificationService
from ..domain.entities import PollenLevel

class PollenAlertService:
    def __init__(
        self, 
        weather_service: WeatherService,
        notification_service: NotificationService,
        alert_threshold: PollenLevel = PollenLevel.HIGH
    ):
        self.weather_service = weather_service
        self.notification_service = notification_service
        self.alert_threshold = alert_threshold

    def check_and_send_alert(self, phone_number: str) -> bool:
        forecast = self.weather_service.get_pollen_forecast()
        
        if forecast.level.value >= self.alert_threshold.value:
            message = (
                f"Pollen Alert: {forecast.level.value} levels detected.\n"
                f"Details: {forecast.description}"
            )
            return self.notification_service.send_alert(message, phone_number)
        
        return False 