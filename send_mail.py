import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config import *


def send_mail(title, body):
    message = MIMEText('<h1>' + body + '</h1>', 'html', 'utf-8')
    message['From'] = SENDER
    message['To'] = RECEIVER
    message['Subject'] = Header(title, 'utf-8')

    smtpObj = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    smtpObj.login(SMTP_USERNAME, SMTP_PASSWORD)
    smtpObj.sendmail(SENDER,
                     [RECEIVER], message.as_string())
    smtpObj.quit()


if __name__ == "__main__":
    # Test
    send_mail("title", "body")
