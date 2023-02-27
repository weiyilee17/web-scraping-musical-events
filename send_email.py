from smtplib import SMTP_SSL
from ssl import create_default_context
from os import getenv
from email.mime.text import MIMEText


def send_email(subject, message):
    host = 'smtp.gmail.com'
    port = 465

    username = getenv('EMAIL_SENDER')
    password = getenv('PORTFOLIO_APP_PASSWORD')
    receiver = getenv('EMAIL_RECEIVER')

    context = create_default_context()

    format_text = MIMEText(message, 'plain', 'utf-8')
    format_text['Subject'] = subject

    with SMTP_SSL(host, port, context=context) as email_server:
        email_server.login(username, password)
        email_server.sendmail(username, receiver, format_text.as_string())
    print('Email was sent!')
