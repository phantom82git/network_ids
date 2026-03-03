"""
Модуль для збору мережевих пакетів з pcap файлу.

Використовує Scapy для читання трафіку.
"""

from scapy.all import rdpcap
from config import PCAP_FILE


def collect_packets():
    """
    Зчитує всі пакети з pcap файлу, вказаного в конфігурації.

    Returns:
        list: Список пакетів у форматі Scapy.
    """
    return rdpcap(PCAP_FILE)
