import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(email, code):
    smtp_server = 'smtp.gmail.com'  # Пример для Gmail, замените на настройки своего почтового провайдера
    smtp_port = 587  # Порт для Gmail

    sender_email = 'maxzombigames@gmail.com'  # Ваш адрес электронной почты
    sender_password = 'xidwmofwpokpviqc'  # Ваш пароль

    recipient_email = email
    subject = 'Ваш код подтверждения'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    verification_text = f'Ваш код подтверждения: {code}'
    message.attach(MIMEText(verification_text, 'plain'))

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, recipient_email, message.as_string())
        smtp.quit()
        print('Письмо с кодом подтверждения отправлено успешно.')
        return True
    except Exception as e:
        print(f'Ошибка при отправке письма: {e}')
        return False

