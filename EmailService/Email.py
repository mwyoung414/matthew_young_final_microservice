
import smtplib
from email.message import EmailMessage


class EmailService:
    """A class to handle email sending using Gmail's SMTP server."""

    def __init__(self, gmail_address: str = None, gmail_app_password: str = None):
        self.GMAIL_ADDRESS = gmail_address
        self.GMAIL_APP_PASSWORD = gmail_app_password   

        if not (self.GMAIL_ADDRESS and self.GMAIL_APP_PASSWORD):
            raise RuntimeError("Please set GMAIL_ADDRESS and GMAIL_APP_PASSWORD env vars")

    def send_email(self, to_addr: str, subject: str, body: str):
        msg = EmailMessage()
        msg["From"]    = self.GMAIL_ADDRESS
        msg["To"]      = to_addr
        msg["Subject"] = subject
        msg.set_content(body)

        # Connect to Gmail’s SMTP server over SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(self.GMAIL_ADDRESS, self.GMAIL_APP_PASSWORD)
            smtp.send_message(msg)