import struct
from typing import BinaryIO

from pydantic import BaseModel

from weekend_dns import io


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
        data = hdl.read(data_len)
        return cls(name=name, type_=type_, class_=class_, ttl=ttl, data=data)
