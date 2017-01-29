# https://alexwlchan.net/2016/05/python-smtplib-and-fastmail/

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class FastMailSMTP(smtplib.SMTP_SSL):
    """A wrapper for handling SMTP connections to FastMail."""

    def __init__(self, username, password):
        super().__init__('mail.messagingengine.com', port=465)
        self.login(username, password)

    def send_message(self, from_addr, to_addrs, msg,
                     subject):
        msg_root = MIMEMultipart()
        msg_root['Subject'] = subject
        msg_root['From'] = from_addr
        msg_root['To'] = ', '.join(to_addrs)

        msg_alternative = MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)

        msg_alternative.attach(MIMEText(msg))
        msg_alternative.attach(MIMEText(msg, 'html'))

        self.sendmail(from_addr, to_addrs, msg_root.as_string())
