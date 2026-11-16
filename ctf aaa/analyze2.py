# Let's try different approaches for the remaining two ciphertexts
hex_strings = ["654a465b731a6232722d727574335f76307263333132345d10", "7a687a52696464656e52696e523f7830665263617365"]

for hex_str in hex_strings:
    print("=== Hex:", hex_str)
    data = bytes.fromhex(hex_str)
    print("Length:", len(data))
    
    # Try common CTF XOR keys (words)
    common_keys = [b'key', b'ctf', b'flag', b'secret', b'password', b'admin', b'hello', b'xor', b'hidden', b'case', b'ridden', b'rin', b'x0f']
    for key in common_keys:
        result = bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))
        try:
            text = result.decode('ascii')
            print("  Key", key, ":", text)
        except:
            pass
    
    # Try repeating key brute force (key length 2-10, find key by frequency)
    for keylen in range(2, 11):
        key = bytearray(keylen)
        for i in range(keylen):
            # For each position, try all 256 keys and pick the one that produces most printable
            best_k = 0
            best_score = -1
            for k in range(256):
                chars = [data[j] ^ k for j in range(i, len(data), keylen)]
                score = sum(1 for c in chars if 32 <= c < 127)
                if score > best_score:
                    best_score = score
                    best_k = k
            key[i] = best_k
        result = bytes(data[j] ^ key[j % keylen] for j in range(len(data)))
        try:
            text = result.decode('ascii')
            if all(32 <= b < 127 or b in (9,10,13) for b in result):
                print("  Repeating key len", keylen, "key=", key.hex(), ":", text)
        except:
            pass
    print()
