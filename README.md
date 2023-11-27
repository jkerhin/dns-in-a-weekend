# Implementing DNS in a weekend

Following along with Julia Evans' tutorial:
    https://implement-dns.wizardzines.com/

I'm keeping the language as Python, but hopefully this will be an opportunity to learn
a bit more about Pydantic rather than just dataclasses (which I am comfortable with)

## Design pattern changes

If you index into a bytestring/bytearray, Python will return each individual byte as an
unsigned 8-bit integer. You can also construct bytestrings/bytearrays from sequences of
integers. i.e.:

```python
assert b"\x01"[0] == 1
assert b"\xFF"[0] == 255
```

This makes sense if you know what's going on, but IMHO it's _not_ very "discoverable" -
it's hard to identify the behavior that's going on under the hood when you see it in the
context of a script/function.

Since multiple fields in a DNS packet encode length as an 8-bit integer, Julia leveraged
this pattern pretty heavily in her examples. Instead, in the spirit of PEP-0020, I'm
taking the approach that "Explicit is better than Implicit" and using `struct` to unpack
a 1-byte integer each time we need a length.

```python
# Used in Julia's examples. Read one byte, giving a bytestring with length of one. Then,
# get the 0th element which is returned as an 8-bit uint
length = reader.read(1)[0]

# Used throughout my code
# Explicitly use "B" format - unsigned char
length, = struct.unpack("!B", reader.read(1))
```

## Self Assessment

Well, I got it working, but with a significant amount of copy/paste and with minimal "own
work" modifications. There are more exercises remaining, and I've got a couple TODOs
throughout the code. Not sure when I'll have time to get back to this, but these are
things I was thinking of as next steps:

 - [ ] Actually use `Enum`s throughout the code instead of raw integers
- [ ] Make it work with `CNAME` records
- [ ] cache DNS records
- [ ] Support other record types by name (e.g. A, AAAA, TXT, etc.)
    - This ties in to the "use Enums" item
- [ ] The other items on [the "exercises" list](https://implement-dns.wizardzines.com/book/exercises)
