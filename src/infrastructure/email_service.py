import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class GmailService:
    def __init__(self, email: str, app_password: str):
        self.email = email
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.port = 587

    def send_notification(self, to_email: str, subject: str, body: str) -> None:
        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.email, self.app_password)
            server.send_message(message) 