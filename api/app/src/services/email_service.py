import os
import smtplib
from email.mime.text import MIMEText


def send_emails(initiator, client):
    smtp = smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
    smtp.starttls()
    smtp.login(os.getenv("SMTP_LOGIN_EMAIL"), os.getenv("SMTP_LOGIN_PASSWORD"))

    msg = MIMEText(f"Вы понравились {initiator.first_name}! Почта участника: {initiator.email}.")
    msg['Subject'] = 'New match!'
    msg['From'] = os.getenv("SMTP_LOGIN_EMAIL")
    msg['To'] = client.email
    smtp.sendmail(os.getenv("SMTP_LOGIN_EMAIL"), client.email, msg=msg.as_string())

    msg = MIMEText(f"Вы понравились {client.first_name}! Почта участника: {client.email}.")
    msg['Subject'] = 'New match!'
    msg['From'] = os.getenv("SMTP_LOGIN_EMAIL")
    msg['To'] = initiator.email
    smtp.sendmail(os.getenv("SMTP_LOGIN_EMAIL"), initiator.email, msg=msg.as_string())

    smtp.quit()
