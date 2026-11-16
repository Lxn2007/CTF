hex_strings = ["654a465b731a6232722d727574335f76307263333132345d10", "7a687a52696464656e52696e523f7830665263617365"]

for hex_str in hex_strings:
    print("=== Hex:", hex_str)
    data = bytes.fromhex(hex_str)
    print("Length:", len(data))
    
    # Try assuming plaintext starts with 'flag{'
    known = b'flag{'
    if len(data) >= 5:
        key_bytes = bytes(data[i] ^ known[i] for i in range(5))
        print("Key (if starts with flag{):", key_bytes.hex(), repr(key_bytes))
        # Try repeating this key
        for kl in range(1, 6):
            key = key_bytes[:kl]
            result = bytes(data[i] ^ key[i % kl] for i in range(len(data)))
            try:
                text = result.decode('ascii')
                print("  Repeating key len", kl, ":", text)
            except:
                print("  Repeating key len", kl, ":", "(non-ascii)")
    
    # Try all single-byte XOR
    print("  All printable single-byte results:")
    for k in range(256):
        result = bytes(b ^ k for b in data)
        if all(32 <= b < 127 or b in (9,10,13) for b in result):
            text = result.decode("ascii")
            print("    Key", k, "(0x%02x):" % k, text)
    print()
