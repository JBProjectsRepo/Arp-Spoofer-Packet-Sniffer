def pkt_payload(scapy_packet):
    if "ICMP" in scapy_packet:
        print("Payload inserted!")
    else:
        print("Payload not inserted!")
    return scapy_packet
