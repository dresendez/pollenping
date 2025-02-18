import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')

# Location configuration
LATITUDE = os.getenv('LATITUDE', '29.7604')  # Default Houston latitude
LONGITUDE = os.getenv('LONGITUDE', '-95.3698')  # Default Houston longitude

# Alert configuration
DEFAULT_ALERT_TIME = os.getenv('ALERT_TIME', "06:30")  # 6:30 AM by default
TIMEZONE = os.getenv('TIMEZONE', 'local') 