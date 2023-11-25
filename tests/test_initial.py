import weekend_dns


def test_encode_dns_name():
    encoded = weekend_dns.encode_dns_name("google.com")
    assert encoded == b"\x06google\x03com\x00"
