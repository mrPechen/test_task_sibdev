import smtplib
from environs import Env

"""
Отправка писем со списком превышенных ПЗ.
"""


def send_email(email: str, message: list) -> None:
    env = Env()
    env.read_env()
    host = env.str('EMAIL_HOST')
    user = env.str('EMAIL_USER')
    password = env.str('EMAIL_PASSWORD')
    smtp_obj = smtplib.SMTP(f'{host}', 587)
    smtp_obj.starttls()
    smtp_obj.login(f'{user}', f'{password}')
    smtp_obj.sendmail(f'{user}', f'{email}',
                      f'The threshold value was exceeded for: {message}')
    smtp_obj.quit()
