import socket

from weekend_dns import DNSPacket, build_query


def send_query(ip_address: str, domain_name: str, record_type: int) -> DNSPacket:
    query = build_query(domain_name=domain_name, record_type=record_type)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(query, (ip_address, 53))
        data, _ = sock.recvfrom(1024)

    return DNSPacket.parse_bytes(data)
