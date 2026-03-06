"""
Головний модуль системи виявлення мережевих атак.
Координує збір пакетів, аналіз, виявлення, логування та сповіщення.
"""

from collector import collect_packets
from analyzer import analyze_packet
from detector import Detector
from logger import log_event, logger_main, logger_detector, logger_notifier
from notifier import send_alert
import sys
import traceback


def main():
    """
    Основний цикл роботи системи IDS.
    """
    logger_main.info("=" * 60)
    logger_main.info("ЗАПУСК СИСТЕМИ: Network Intrusion Detection System")
    logger_main.info("=" * 60)
    
    try:
        # Крок 1: Збір пакетів
        logger_main.info("Фаза 1: Збір мережевих пакетів")
        packets = collect_packets()
        logger_main.info(f"Зібрано {len(packets)} пакетів для аналізу")
        
        # Крок 2: Ініціалізація детектора
        detector = Detector()
        logger_main.debug("Детектор ініціалізовано успішно")
        
        # Крок 3: Аналіз пакетів
        logger_main.info("Фаза 2: Аналіз пакетів")
        attack_count = 0
        total_packets = len(packets)
        
        for i, packet in enumerate(packets):
            # Логуємо прогрес кожні 100 пакетів
            if i % 100 == 0 and i > 0:
                percent = (i / total_packets) * 100
                logger_main.debug(f"Оброблено {i}/{total_packets} пакетів ({percent:.1f}%)")
            
            info = analyze_packet(packet)
            if info:
                logger_detector.debug(f"Інформація про пакет: {info}")
                detector.process(info)
        
        logger_main.info(f"Аналіз завершено: оброблено {total_packets} пакетів")
        
        # Крок 4: Виявлення атак
        logger_main.info("Фаза 3: Виявлення атак")
        alerts = detector.detect()  # Це список рядків!
        
        # Крок 5: Обробка результатів
        if alerts:
            logger_main.warning(f"Виявлено {len(alerts)} потенційних атак!")
            
            for alert in alerts:
                # Вивід на екран
                print(f"⚠️ {alert}")
                
                # Логування в файл (стара функція)
                log_event(alert)
                
                # Відправка email (якщо alert це рядок, а не словник)
                logger_notifier.info(f"Відправка сповіщення: {alert[:50]}...")  # Перші 50 символів
                
                # Для сумісності з notifier.py, створюємо простий словник
                alert_dict = {'type': 'Unknown', 'source': 'Unknown'}
                
                # Спробуємо витягнути тип атаки з рядка
                if "DoS" in alert:
                    alert_dict['type'] = 'DoS'
                elif "PortScan" in alert or "Port Scan" in alert:
                    alert_dict['type'] = 'PortScan'
                elif "Brute force" in alert or "bruteforce" in alert:
                    alert_dict['type'] = 'BruteForce'
                
                # Спробуємо витягнути IP з рядка
                import re
                ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', alert)
                if ip_match:
                    alert_dict['source'] = ip_match.group()
                
                try:
                    send_alert(alert_dict)
                    logger_notifier.info(f"Сповіщення відправлено успішно: {alert_dict['type']}")
                except Exception as e:
                    logger_notifier.error(f"Помилка відправки сповіщення: {str(e)}")
        else:
            logger_main.info("Атак не виявлено - система безпечна")
        
        logger_main.info("=" * 60)
        logger_main.info("СИСТЕМА ЗУПИНЕНА: Штатне завершення")
        logger_main.info("=" * 60)
        
    except FileNotFoundError as e:
        logger_main.error(f"Критична помилка: Файл не знайдено - {str(e)}")
        print(f"Помилка: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger_main.warning("Система перервана користувачем (Ctrl+C)")
        print("\nСистема перервана користувачем")
        sys.exit(0)
        
    except Exception as e:
        logger_main.critical(f"Критична неочікувана помилка: {str(e)}")
        logger_main.critical(traceback.format_exc())
        print(f"Критична помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()