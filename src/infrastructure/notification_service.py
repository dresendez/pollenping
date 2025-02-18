import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import platform
from src.domain.interfaces import NotificationService

class EmailService(NotificationService):
    def __init__(self, sender_email: str, app_password: str):
        self.email = sender_email
        self.password = app_password

    def send_alert(self, message: str, to: str) -> bool:
        try:
            # Create MIME message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to
            msg['Subject'] = "Pollen Alert"
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to Gmail's SMTP server
            print("Connecting to Gmail SMTP server...")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            
            # Login and send
            print("Attempting to login...")
            server.login(self.email, self.password)
            print("Login successful, sending message...")
            server.send_message(msg)
            server.quit()
            print("Message sent, SMTP connection closed")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            print(f"Error type: {type(e)}")
            return False

class EmailToSMSService(NotificationService):
    CARRIERS = {
        "att": "@txt.att.net",  # Primary gateway
        "att2": "@text.att.net",  # Alternative gateway
        "tmobile": "@tmomail.net",
        "verizon": "@vzwpix.com",  # Changed to Verizon's MMS gateway
        "sprint": "@messaging.sprintpcs.com"
    }

    def __init__(self, email: str, app_password: str, carrier: str):
        self.email = email
        self.password = app_password
        self.carrier = carrier.lower()
        if self.carrier not in self.CARRIERS:
            raise ValueError(f"Unsupported carrier. Must be one of: {', '.join(self.CARRIERS.keys())}")

    def send_alert(self, message: str, to: str) -> bool:
        try:
            # Remove the "1" prefix - not needed for Verizon
            recipient = to + self.CARRIERS[self.carrier]
            print(f"Sending message to: {recipient}")
            
            # Create MIME message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = recipient
            msg['Subject'] = "Pollen Alert"
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to Gmail's SMTP server
            print("Connecting to Gmail SMTP server...")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.set_debuglevel(1)  # Add debug output
            server.starttls()
            
            # Login and send
            print("Attempting to login...")
            server.login(self.email, self.password)
            print("Login successful, sending message...")
            server.send_message(msg)
            server.quit()
            print("Message sent, SMTP connection closed")
            return True
            
        except Exception as e:
            print(f"Failed to send SMS: {str(e)}")
            print(f"Error type: {type(e)}")
            return False

class iMessageService(NotificationService):
    def __init__(self):
        if platform.system() != 'Darwin':  # Darwin is macOS
            raise RuntimeError("iMessage service only works on macOS")

    def send_alert(self, message: str, to: str) -> bool:
        try:
            # AppleScript command to send iMessage
            apple_script = f'''
            tell application "Messages"
                send "{message}" to buddy "{to}" of service "iMessage"
            end tell
            '''
            
            # Execute the AppleScript
            subprocess.run(['osascript', '-e', apple_script])
            print(f"iMessage sent to {to}")
            return True
            
        except Exception as e:
            print(f"Failed to send iMessage: {str(e)}")
            return False 