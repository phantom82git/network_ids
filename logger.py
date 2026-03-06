"""
Модуль для логування подій та сповіщень у файл.
Забезпечує простий запис рядків з часовими мітками та розширене логування.
"""

from datetime import datetime
from config import LOG_FILE
import logging
import sys

# ===== НАЛАШТУВАННЯ ЛОГУВАННЯ =====
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Створюємо кореневий логер
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)  # Для розробки, можна змінити на INFO для продакшн

# Очищаємо попередні обробники (якщо є)
if root_logger.handlers:
    root_logger.handlers.clear()

# Створюємо обробник для виводу в консоль
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # В консоль виводимо INFO і вище

# Створюємо обробник для запису у файл
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)  # У файл пишемо все

# Створюємо форматувальник
formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Додаємо обробники до кореневого логера
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)

# Створюємо логери для різних модулів
logger_collector = logging.getLogger('collector')
logger_analyzer = logging.getLogger('analyzer')
logger_detector = logging.getLogger('detector')
logger_notifier = logging.getLogger('notifier')
logger_main = logging.getLogger('main')


# ===== СТАРА ФУНКЦІЯ (ЗАЛИШАЄМО ДЛЯ СУМІСНОСТІ) =====
def log_event(message):
    """
    Записує повідомлення у лог-файл з часовою міткою.
    
    Args:
        message (str): Текст повідомлення для запису.
    """
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"[{datetime.now()}] {message}\n")
    
    # Додатково логуємо через нову систему
    logging.info(f"[legacy] {message}")
