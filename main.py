"""
Головний модуль системи виявлення мережевих атак.

Координує збір пакетів, аналіз, виявлення, логування та сповіщення.
"""

from collector import collect_packets
from analyzer import analyze_packet
from detector import Detector
from logger import log_event
from notifier import send_alert


def main():
    """
    Основний цикл роботи системи IDS.

    Читає пакети з файлу, аналізує кожен, передає детектору,
    виводить результати, логує та надсилає сповіщення.
    """
    packets = collect_packets()
    detector = Detector()

    for packet in packets:
        info = analyze_packet(packet)
        if info:
            detector.process(info)

    alerts = detector.detect()

    if alerts:
        for alert in alerts:
            print(alert)
            log_event(alert)
            send_alert(alert)
    else:
        print("No attacks detected.")


if __name__ == "__main__":
    main()
