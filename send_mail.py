import smtplib

from email.mime.text import MIMEText
from email.header import Header
from config import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER, RECEIVER


def send_mail(title, body):
    try:
        message = MIMEText('<h1>' + body + '</h1>', 'html', 'utf-8')
        message['From'] = SENDER
        message['To'] = RECEIVER
        message['Subject'] = Header(title, 'utf-8')

        smtpObj = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        smtpObj.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtpObj.sendmail(SENDER, [RECEIVER], message.as_string())
        smtpObj.quit()
    except Exception:
        print(f'Sending failed\n[title]\n{title}\n[body]\n{body}')


if __name__ == '__main__':
    send_mail('Hello from Mars', '来自火星的问候')
