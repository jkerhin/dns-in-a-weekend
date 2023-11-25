"""Implementing DNS in a weekend!"""
import struct

from .models import DNSHeader, DNSQuestion

__version__ = "0.0.1"


def encode_dns_name(domain_name: str) -> bytes:
    encoded = b""
    for part in domain_name.encode("ascii").split(b"."):
        encoded += struct.pack("!B", len(part)) + part
    return encoded + b"\x00"
