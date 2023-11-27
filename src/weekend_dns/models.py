import struct
from enum import Enum
from io import BytesIO
from typing import BinaryIO

from pydantic import BaseModel

from weekend_dns import io


class DNSType(Enum):
    A = 1
    NS = 2
    CNAME = 5
    MX = 15
    TXT = 16
    AAAA = 28


class DNSHeader(BaseModel):
    id: int
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

    def to_bytes(self) -> bytes:
        fields = (v for _, v in tuple(self))
        return struct.pack("!6H", *fields)

    @classmethod
    def read(cls, hdl: BinaryIO) -> "DNSHeader":
        i, f, nq, na, at, ad = struct.unpack("!6H", hdl.read(12))
        return cls(
            id=i,
            flags=f,
            num_questions=nq,
            num_answers=na,
            num_authorities=at,
            num_additionals=ad,
        )


class DNSQuestion(BaseModel):
    name: bytes
    type_: int
    class_: int

    def to_bytes(self) -> bytes:
        return self.name + struct.pack("!2H", self.type_, self.class_)

    @classmethod
    def read(cls, hdl: BinaryIO) -> "DNSQuestion":
        name = io.read_dns_name(hdl=hdl)
        type_, class_ = struct.unpack("!2H", hdl.read(4))
        return cls(name=name, type_=type_, class_=class_)


class DNSRecord(BaseModel):
    name: bytes
    type_: int
    class_: int
    ttl: int
    data: bytes

    @classmethod
    def read(cls, hdl: BinaryIO) -> "DNSRecord":
        name = io.read_dns_name(hdl=hdl)
        type_, class_, ttl, data_len = struct.unpack("!HHIH", hdl.read(10))
        if type_ == DNSType.NS.value:
            data = io.read_dns_name(hdl)
        elif type_ == DNSType.A.value:
            data = io.ip_to_string(hdl.read(data_len))
        else:
            data = hdl.read(data_len)
        return cls(name=name, type_=type_, class_=class_, ttl=ttl, data=data)


class DNSPacket(BaseModel):
    header: DNSHeader
    questions: list[DNSQuestion]
    answers: list[DNSRecord]
    authorities: list[DNSRecord]
    additionals: list[DNSRecord]

    def get_answer(self):
        for x in self.answers:
            if x.type_ == DNSType.A.value:
                return x.data

    def get_nameserver(self):
        for x in self.authorities:
            if x.type_ == DNSType.NS.value:
                return x.data.decode("utf-8")

    def get_nameserver_ip(self):
        for x in self.additionals:
            if x.type_ == DNSType.A.value:
                return x.data

    @classmethod
    def parse_bytes(cls, packet_bytes: bytes) -> "DNSPacket":
        hdl = BytesIO(packet_bytes)
        header = DNSHeader.read(hdl=hdl)
        questions = [DNSQuestion.read(hdl=hdl) for _ in range(header.num_questions)]
        answers = [DNSRecord.read(hdl=hdl) for _ in range(header.num_answers)]
        authorities = [DNSRecord.read(hdl=hdl) for _ in range(header.num_authorities)]
        additionals = [DNSRecord.read(hdl=hdl) for _ in range(header.num_additionals)]

        return cls(
            header=header,
            questions=questions,
            answers=answers,
            authorities=authorities,
            additionals=additionals,
        )
