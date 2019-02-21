import os
from requests import post


class MailException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Mailer:
    """Send's an email using the mailgun API to verify A user's account"""
    
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    FROM_EMAIL = os.environ.get('FROM_EMAIL')
    FROM_TITLE = 'Flask Blog API'

    @classmethod
    def send(cls, email, subject, text, html):
        if cls.MAILGUN_API_KEY is None:
            raise MailException('Failed to get Mailgun api key.')

        if cls.MAILGUN_DOMAIN is None:
            raise MailException('Failed to get Mailgun domain.')

        res = post(
            f'https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages',
            auth=('api', cls.MAILGUN_API_KEY),
            data={
              'from': f'{cls.FROM_TITLE} <{cls.FROM_EMAIL}>',
              'to': email,
              'text': text,
              'html': html,
              'subject': subject
            }
        )
        if res.status_code != 200:
            raise MailException('Failed to send email via Mailgun, user registration failed.')

        return res

