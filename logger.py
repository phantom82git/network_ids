"""
Модуль для логування подій та сповіщень у файл.

Забезпечує простий запис рядків з часовими мітками.
"""

from datetime import datetime
from config import LOG_FILE


def log_event(message):
    """
    Записує повідомлення у лог-файл з часовою міткою.

    Args:
        message (str): Текст повідомлення для запису.
    """
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")
