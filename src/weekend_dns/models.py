import struct

from pydantic import BaseModel


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


class DNSQuestion(BaseModel):
    name: bytes
    type_: int
    class_: int

    def to_bytes(self) -> bytes:
        return self.name + struct.pack("!2H", self.type_, self.class_)
