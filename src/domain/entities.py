from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class PollenLevel(Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

@dataclass
class PollenForecast:
    level: PollenLevel
    timestamp: datetime
    description: str 