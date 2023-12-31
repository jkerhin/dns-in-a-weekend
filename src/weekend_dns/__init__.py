"""Implementing DNS in a weekend!"""
import random

from .io import encode_dns_name
from .models import DNSHeader, DNSPacket, DNSQuestion, DNSRecord

__version__ = "0.1.0"

random.seed(1)  # TODO: Need a better place for this
CLASS_IN = 1


def build_query(domain_name: str, record_type) -> bytes:
    name = encode_dns_name(domain_name=domain_name)
    id = random.randint(0, 65535)
    # RECURSION_DESIRED = 1 << 8
    # header = DNSHeader(id=id, num_questions=1, flags=RECURSION_DESIRED)
    header = DNSHeader(id=id, num_questions=1, flags=0)
    question = DNSQuestion(name=name, type_=record_type, class_=CLASS_IN)
    return header.to_bytes() + question.to_bytes()
