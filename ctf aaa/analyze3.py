hex_strings = ["654a465b731a6232722d727574335f76307263333132345d10", "7a687a52696464656e52696e523f7830665263617365"]

for hex_str in hex_strings:
    print("=== Hex:", hex_str)
    data = bytes.fromhex(hex_str)
    print("Length:", len(data))
    
    # Try all possible multi-byte keys (2-4 bytes) by brute force
    for keylen in range(2, 5):
        for k0 in range(256):
            for k1 in range(256):
                if keylen == 2:
                    key = bytes([k0, k1])
                    result = bytes(data[i] ^ key[i % 2] for i in range(len(data)))
                    if all(32 <= b < 127 or b in (9,10,13) for b in result):
                        text = result.decode('ascii')
                        if 'flag' in text.lower() or 'ctf' in text.lower() or 'hidden' in text.lower():
                            print("  FOUND key", key.hex(), ":", text)
                if keylen >= 3:
                    for k2 in range(256):
                        key = bytes([k0, k1, k2])
                        result = bytes(data[i] ^ key[i % 3] for i in range(len(data)))
                        if all(32 <= b < 127 or b in (9,10,13) for b in result):
                            text = result.decode('ascii')
                            if 'flag' in text.lower() or 'ctf' in text.lower() or 'hidden' in text.lower():
                                print("  FOUND key", key.hex(), ":", text)
                        if keylen >= 4:
                            for k3 in range(256):
                                key = bytes([k0, k1, k2, k3])
                                result = bytes(data[i] ^ key[i % 4] for i in range(len(data)))
                                if all(32 <= b < 127 or b in (9,10,13) for b in result):
                                    text = result.decode('ascii')
                                    if 'flag' in text.lower() or 'ctf' in text.lower() or 'hidden' in text.lower():
                                        print("  FOUND key", key.hex(), ":", text)
    print("Done searching")
    print()
