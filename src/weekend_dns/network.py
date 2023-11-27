import socket

from weekend_dns import DNSPacket, build_query


def send_query(server: str, domain_name: str, record_type: int) -> DNSPacket:
    query = build_query(domain_name=domain_name, record_type=record_type)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(query, (server, 53))
        data, _ = sock.recvfrom(1024)

    return DNSPacket.parse_bytes(data)


def resolve(domain_name: str, record_type: int) -> str:
    nameserver = "198.41.0.4"
    while True:
        print(f"Querying {nameserver} for {domain_name}")
        response = send_query(
            server=nameserver, domain_name=domain_name, record_type=record_type
        )
        if ip := response.get_answer():
            return ip
        elif nsIP := response.get_nameserver_ip():
            nameserver = nsIP
        elif ns_domain := response.get_nameserver():
            nameserver = resolve(ns_domain, 1)  # TYPE_A
        else:
            raise Exception("Something went wrong")
