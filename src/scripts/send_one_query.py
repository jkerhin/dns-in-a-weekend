"""Quick send-only test

Use wireshark to capture network traffic and decode the response
"""
import socket

import weekend_dns


def main():
    query = weekend_dns.build_query("www.example.com", weekend_dns.TYPE_A)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(query, ("1.1.1.1", 53))  # Cloudflare

    response, _ = sock.recvfrom(1024)

    print(response.hex())


if __name__ == "__main__":
    main()
