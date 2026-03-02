from collections import defaultdict
from config import *


class Detector:

    def __init__(self):
        self.dos_counter = defaultdict(list)
        self.portscan_counter = defaultdict(set)
        self.bruteforce_counter = defaultdict(int)

    def process(self, packet_info):
        src = packet_info["src"]
        port = packet_info["port"]
        timestamp = packet_info["time"]

        # ---- DoS detection ----
        self.dos_counter[src].append(timestamp)
        self.dos_counter[src] = [
            t for t in self.dos_counter[src] if timestamp - t <= TIME_WINDOW
        ]

        # ---- Port scan detection ----
        self.portscan_counter[src].add(port)

        # ---- Brute force detection ----
        if port == 22:
            self.bruteforce_counter[src] += 1

    def detect(self):
        alerts = []

        # DoS
        for src, times in self.dos_counter.items():
            if len(times) > DOS_THRESHOLD:
                alerts.append(f"DoS attack detected from {src}")

        # Port scan
        for src, ports in self.portscan_counter.items():
            if len(ports) > PORTSCAN_THRESHOLD:
                alerts.append(f"Port scan detected from {src}")

        # Brute force
        for src, attempts in self.bruteforce_counter.items():
            if attempts > BRUTEFORCE_THRESHOLD:
                alerts.append(f"Brute force attack detected from {src}")

        return alerts
