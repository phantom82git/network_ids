"""
Модуль email-сповіщень про виявлені атаки.
Використовує SMTP для надсилання повідомлень адміністратору.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, ADMIN_EMAIL
from logger import logger_notifier
import re


def send_email(subject, body):
    """
    Відправляє email через SMTP-сервер.
    
    Args:
        subject: Тема листа
        body: Текст листа (plain text)
        
    Returns:
        bool: True, якщо лист відправлено успішно, інакше False
    """
    logger_notifier.info(f"Підготовка до відправки email: '{subject[:50]}...'")
    logger_notifier.debug(f"SMTP конфігурація: {SMTP_SERVER}:{SMTP_PORT}, відправник={SMTP_USER}, отримувач={ADMIN_EMAIL}")
    
    try:
        # Створення повідомлення
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Підключення до SMTP сервера
        logger_notifier.debug("Підключення до SMTP сервера...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls()
        
        # Логування
        logger_notifier.debug(f"Аутентифікація користувача {SMTP_USER}")
        server.login(SMTP_USER, SMTP_PASSWORD)
        
        # Відправка
        server.send_message(msg)
        server.quit()
        
        logger_notifier.info("Email відправлено успішно")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger_notifier.error(f"Помилка аутентифікації SMTP: {str(e)}")
        return False
        
    except smtplib.SMTPException as e:
        logger_notifier.error(f"SMTP помилка: {str(e)}")
        return False
        
    except ConnectionError as e:
        logger_notifier.error(f"Помилка з'єднання: {str(e)}")
        return False
        
    except Exception as e:
        logger_notifier.error(f"Неочікувана помилка при відправці email: {str(e)}", exc_info=True)
        return False


def send_alert(alert):
    """
    Відправляє сповіщення про виявлену атаку.
    Приймає як рядок з повідомленням про атаку.
    
    Args:
        alert: Рядок з інформацією про атаку
        
    Returns:
        bool: True, якщо сповіщення відправлено, інакше False
    """
    if isinstance(alert, dict):
        # Якщо це словник (для сумісності)
        attack_type = alert.get('type', 'Unknown')
        source = alert.get('source', 'Unknown')
        alert_str = f"{attack_type} attack detected from {source}"
    else:
        # Якщо це рядок
        alert_str = str(alert)
        # Визначаємо тип атаки з рядка
        if "DoS" in alert_str:
            attack_type = "DoS"
        elif "PortScan" in alert_str or "Port Scan" in alert_str:
            attack_type = "PortScan"
        elif "Brute force" in alert_str or "bruteforce" in alert_str:
            attack_type = "BruteForce"
        else:
            attack_type = "Unknown"
    
    logger_notifier.info(f"Обробка сповіщення: {alert_str[:50]}...")
    
    # Формування теми
    subject = f"Виявлено атаку: {attack_type}"
    
    # Формування тіла листа
    body = f"""
    ВИЯВЛЕНО МЕРЕЖЕВУ АТАКУ!
    
    Тип: {attack_type}
    Час: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Деталі:
    {alert_str}
    """
    
    logger_notifier.debug(f"Тема сповіщення: {subject}")
    result = send_email(subject, body)
    
    if result:
        logger_notifier.info(f"Сповіщення відправлено для {attack_type} атаки")
    else:
        logger_notifier.error(f"Не вдалося відправити сповіщення для {attack_type} атаки")
    
    return result