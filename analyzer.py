from scapy.layers.inet import IP, TCP


def analyze_packet(packet):
    if IP in packet and TCP in packet:
        return {
            "src": packet[IP].src,
            "dst": packet[IP].dst,
            "port": packet[TCP].dport,
            "time": float(packet.time),
        }
    return None
