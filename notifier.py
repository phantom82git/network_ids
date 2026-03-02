import smtplib
from email.mime.text import MIMEText
from config import *


def send_alert(message):
    msg = MIMEText(message)
    msg["Subject"] = "IDS Alert"
    msg["From"] = SMTP_USER
    msg["To"] = ADMIN_EMAIL

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(SMTP_USER, ADMIN_EMAIL, msg.as_string())
    server.quit()
