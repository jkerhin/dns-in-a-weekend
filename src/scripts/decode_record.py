from io import BytesIO

import weekend_dns

# Pulled this from wireshark
my_response = bytes.fromhex(
    "44cb8180000100010000000003777777076578616d706c6503636f6d0000010001c00c0001000100014c7500045db8d822"
)
# From the walkthrough
julia_response = b'`V\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00R\x9b\x00\x04]\xb8\xd8"'


def main():
    hdl = BytesIO(my_response)
    h = weekend_dns.DNSHeader.read(hdl)
    q = weekend_dns.DNSQuestion.read(hdl)
    r = weekend_dns.DNSRecord.read(hdl)

    print("Header:", h)
    print("Question:", q)
    print("Record:", r)


if __name__ == "__main__":
    main()
