hex_strings = ["654a465b731a6232722d727574335f76307263333132345d10", "7a687a52696464656e52696e523f7830665263617365"]

for hex_str in hex_strings:
    print("=== Hex:", hex_str)
    data = bytes.fromhex(hex_str)
    print("Length:", len(data))
    
    # Try assuming plaintext starts with various known prefixes
    prefixes = [b"flag{", b"ctf{", b"hidden", b"secret", b"password", b"admin", b"root", b"test", b"hello", b"world", b"key", b"xor", b"case", b"ridden", b"rin", b"hidden_", b"flag_", b"ctf_"]
    for prefix in prefixes:
        if len(data) >= len(prefix):
            key = bytes(data[i] ^ prefix[i] for i in range(len(prefix)))
            # Try repeating this key
            for kl in range(1, len(prefix) + 1):
                k = key[:kl]
                result = bytes(data[i] ^ k[i % kl] for i in range(len(data)))
                try:
                    text = result.decode('ascii')
                    if all(32 <= b < 127 or b in (9,10,13) for b in result):
                        if 'flag' in text.lower() or 'ctf' in text.lower() or 'hidden' in text.lower() or 'secret' in text.lower():
                            print("  FOUND! prefix:", prefix, "keylen:", kl, "key:", k.hex(), "->", text)
                except:
                    pass
    
    # Try Vigenere-like: key is a single word repeated
    words = [b"key", b"ctf", b"flag", b"secret", b"password", b"admin", b"root", b"test", b"hello", b"world", b"hidden", b"cipher", b"crypto", b"xor", b"case", b"ridden", b"rin", b"hidden_flag", b"hidden_case"]
    for word in words:
        result = bytes(data[i] ^ word[i % len(word)] for i in range(len(data)))
        try:
            text = result.decode('ascii')
            if all(32 <= b < 127 or b in (9,10,13) for b in result):
                print("  Word key", word, ":", text)
        except:
            pass
    
    print("Done")
    print()
