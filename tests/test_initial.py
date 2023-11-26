import weekend_dns


def test_encode_dns_name():
    encoded = weekend_dns.encode_dns_name("google.com")
    assert encoded == b"\x06google\x03com\x00"


def test_build_query():
    query = weekend_dns.build_query("example.com", weekend_dns.TYPE_A)
    assert (
        query
        == b"D\xcb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01"
    )
