from abc import ABC, abstractmethod
from .entities import PollenForecast

class WeatherService(ABC):
    @abstractmethod
    def get_pollen_forecast(self) -> PollenForecast:
        pass

class NotificationService(ABC):
    @abstractmethod
    def send_alert(self, message: str, to: str) -> bool:
        pass 