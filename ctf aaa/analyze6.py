# Let's try to crack the remaining two ciphertexts with better methods
hex_strings = ["654a465b731a6232722d727574335f76307263333132345d10", "7a687a52696464656e52696e523f7830665263617365"]

for hex_str in hex_strings:
    print("=== Hex:", hex_str)
    data = bytes.fromhex(hex_str)
    print("Length:", len(data))
    
    # Try repeating key with frequency analysis for key lengths 2-8
    for keylen in range(2, 9):
        key = bytearray(keylen)
        for i in range(keylen):
            # Try all 256 possible key bytes, pick best by English letter frequency
            best_k = 0
            best_score = -1
            for k in range(256):
                chars = [data[j] ^ k for j in range(i, len(data), keylen)]
                # Score: number of printable ASCII chars that are common English letters
                score = sum(1 for c in chars if chr(c).isalpha() or chr(c) in ' _{}0123456789')
                if score > best_score:
                    best_score = score
                    best_k = k
            key[i] = best_k
        
        result = bytes(data[j] ^ key[j % keylen] for j in range(len(data)))
        try:
            text = result.decode('ascii')
            if all(32 <= b < 127 or b in (9,10,13) for b in result):
                print("  Keylen", keylen, "key=", key.hex(), ":", text)
        except:
            pass
    
    # Also try: what if key is "hidden" repeated?
    for key in [b"hidden", b"flag", b"ctf", b"secret", b"key", b"password", b"admin", b"root", b"test", b"hello", b"world", b"case", b"ridden", b"rin"]:
        result = bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))
        try:
            text = result.decode('ascii')
            if all(32 <= b < 127 or b in (9,10,13) for b in result):
                print("  Word key", key, ":", text)
        except:
            pass
    
    print()
