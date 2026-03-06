"""
Модуль для збору мережевих пакетів з pcap файлу.
Використовує Scapy для читання трафіку.
"""

from scapy.all import rdpcap
from config import PCAP_FILE
from logger import logger_collector


def collect_packets():
    """
    Зчитує всі пакети з pcap файлу, вказаного в конфігурації.
    
    Returns:
        list: Список пакетів у форматі Scapy.
    """
    logger_collector.info(f"Початок читання pcap файлу: {PCAP_FILE}")
    
    try:
        packets = rdpcap(PCAP_FILE)
        logger_collector.info(f"Успішно прочитано {len(packets)} пакетів з {PCAP_FILE}")
        
        # Логуємо перші 5 типів пакетів для діагностики
        if len(packets) > 0:
            packet_types = set(type(p).__name__ for p in packets[:5])
            logger_collector.debug(f"Типи пакетів: {packet_types}")
        
        return packets
        
    except FileNotFoundError:
        logger_collector.error(f"pcap файл не знайдено: {PCAP_FILE}")
        raise
    except Exception as e:
        logger_collector.error(f"Помилка читання pcap файлу: {str(e)}", exc_info=True)
        raise


def extract_packet_info(packet):
    """
    Виділяє основну інформацію з мережевого пакета.
    
    Args:
        packet: Об'єкт пакета з Scapy
        
    Returns:
        dict: Словник з інформацією про пакет (src_ip, dst_ip, src_port, dst_port)
    """
    info = {
        'src_ip': None,
        'dst_ip': None,
        'src_port': None,
        'dst_port': None,
    }
    
    try:
        if packet.haslayer('IP'):
            info['src_ip'] = packet['IP'].src
            info['dst_ip'] = packet['IP'].dst
            
            if packet.haslayer('TCP'):
                info['src_port'] = packet['TCP'].sport
                info['dst_port'] = packet['TCP'].dport
                logger_collector.debug(f"TCP пакет: {info['src_ip']}:{info['src_port']} -> {info['dst_ip']}:{info['dst_port']}")
    except Exception as e:
        logger_collector.warning(f"Помилка при аналізі пакета: {str(e)}")
    
    return info