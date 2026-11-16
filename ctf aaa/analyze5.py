# Try 2-byte XOR keys for the two remaining ciphertexts
hex_strings = ["654a465b731a6232722d727574335f76307263333132345d10", "7a687a52696464656e52696e523f7830665263617365"]

for hex_str in hex_strings:
    print("=== Hex:", hex_str)
    data = bytes.fromhex(hex_str)
    print("Length:", len(data))
    
    found = False
    for k0 in range(256):
        for k1 in range(256):
            key = bytes([k0, k1])
            result = bytes(data[i] ^ key[i % 2] for i in range(len(data)))
            if all(32 <= b < 127 or b in (9,10,13) for b in result):
                text = result.decode('ascii')
                if 'flag' in text.lower() or 'ctf' in text.lower() or 'hidden' in text.lower():
                    print("  FOUND 2-byte key", key.hex(), ":", text)
                    found = True
    if not found:
        print("  No 2-byte key found with flag/ctf/hidden")
    print()
