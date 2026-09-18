import hashlib

SECRET = "IRISH_HUB_2024_X9K2"
CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def make_checksum(payload):
    # CRC32 in Python
    import binascii
    h = binascii.crc32((SECRET + payload).encode()) & 0xFFFFFFFF
    s = ""
    for _ in range(4):
        s += CHARSET[h % 36]
        h //= 36
    return s

def generate_key(index):
    h = hashlib.sha256(f"{SECRET}:{index}".encode()).hexdigest()
    payload = ""
    for i in range(8):
        payload += CHARSET[int(h[i * 2:(i + 1) * 2], 16) % 36]
    check = make_checksum(payload)
    return f"IRISH-{payload[:4]}-{payload[4:8]}-{check}"

# Python keys
py_keys = [generate_key(i) for i in range(10)]
print("Python keys:")
for k in py_keys:
    print(f"  {k}")

# JS FNV-1a simulation
def js_generate_key(index):
    import struct
    input_str = SECRET + ":" + str(index)
    h1 = 0x811c9dc5
    h2 = 0x01000193
    for c in input_str:
        b = ord(c)
        h1 = (h1 ^ b) * 0x01000193 & 0xFFFFFFFF
        h2 = (h2 ^ b) * 0x811c9dc5 & 0xFFFFFFFF
    hex_str = format(h1, '08x') + format(h2, '08x')
    payload = ""
    for i in range(8):
        idx = int(hex_str[i*2:(i+1)*2], 16) % 36
        payload += CHARSET[idx]
    check = make_checksum(payload)
    return f"IRISH-{payload[:4]}-{payload[4:8]}-{check}"

js_keys = [js_generate_key(i) for i in range(10)]
print("\nJS keys:")
for k in js_keys:
    print(f"  {k}")

print("\nMatch:", py_keys == js_keys)
