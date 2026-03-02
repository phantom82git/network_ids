from scapy.all import rdpcap
from config import PCAP_FILE


def collect_packets():
    return rdpcap(PCAP_FILE)
