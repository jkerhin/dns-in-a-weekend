import struct
from typing import BinaryIO


def encode_dns_name(domain_name: str) -> bytes:
    encoded = b""
    for part in domain_name.encode("ascii").split(b"."):
        encoded += struct.pack("!B", len(part)) + part
    return encoded + b"\x00"


def read_dns_name_simple(hdl: BinaryIO) -> bytes:
    """Does not handle or even check for compression"""
    parts = []
    # Stops on length 0 as "0" is False-y
    while length := struct.unpack("!B", hdl.read(1))[0]:
        parts.append(hdl.read(length))
    return b".".join(parts)


def read_dns_name(hdl: BinaryIO) -> bytes:
    """Read DNS name from buffered IO handle, handling compression appropriately"""
    parts = []
    while length := struct.unpack("!B", hdl.read(1))[0]:
        if length & 0b1100_0000:
            parts.append(read_compressed_name(length, hdl))
            break
        else:
            parts.append(hdl.read(length))
    return b".".join(parts)


def read_compressed_name(length: int, hdl: BinaryIO) -> bytes:
    """Oh fun it uses lookbacks, and absolute indexes into the message buffer"""
    pointer_bytes = struct.pack("!B", length & 0b0011_1111) + hdl.read(1)
    (pointer,) = struct.unpack("!H", pointer_bytes)
    current_pos = hdl.tell()
    hdl.seek(pointer)
    result = read_dns_name(hdl=hdl)
    hdl.seek(current_pos)
    return result


def ip_to_string(ip: bytes) -> str:
    octets = struct.unpack("!4B", ip)
    return ".".join(str(o) for o in octets)
