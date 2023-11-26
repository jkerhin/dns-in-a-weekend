"""Updating now to actually handle the returned packet

Still a clunky print, but better than before
"""
import socket

import weekend_dns


def main():
    site = "www.example.com"  # Works fine
    # site = "www.metafilter.com"  # Bombs out. Record type = 5 (not implemented yet)

    query = weekend_dns.build_query(site, weekend_dns.TYPE_A)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(query, ("1.1.1.1", 53))  # Cloudflare

    response, _ = sock.recvfrom(1024)

    pkt = weekend_dns.DNSPacket.parse_bytes(response)
    print("DNS Packet:", pkt)
    print("IP Address:", weekend_dns.io.ip_to_string(pkt.answers[0].data))


if __name__ == "__main__":
    main()
