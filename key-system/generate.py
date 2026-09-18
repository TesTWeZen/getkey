import string, hashlib, json, os

SECRET = "IRISH_HUB_2024_X9K2"
CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
CSET_LEN = 36

def crc32_custom(data):
    crc = 0xFFFFFFFF
    for b in data:
        byte = ord(b) if isinstance(b, str) else b
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
    return crc ^ 0xFFFFFFFF

def make_checksum(payload_8chars):
    data = SECRET + payload_8chars
    h = crc32_custom(data)
    s = ""
    for _ in range(4):
        s += CHARSET[h % CSET_LEN]
        h //= CSET_LEN
    return s

def generate_key(index):
    h = hashlib.sha256(f"{SECRET}:{index}".encode()).hexdigest()
    payload = ""
    for i in range(8):
        payload += CHARSET[int(h[i * 2:(i + 1) * 2], 16) % CSET_LEN]
    check = make_checksum(payload)
    return f"IRISH-{payload[:4]}-{payload[4:8]}-{check}"

def validate_key(key):
    if not key.startswith("IRISH-"):
        return False
    parts = key.split("-")
    if len(parts) != 4:
        return False
    for p in parts[1:]:
        if len(p) != 4:
            return False
        for c in p:
            if c not in CHARSET:
                return False
    payload = parts[1] + parts[2]
    expected = make_checksum(payload)
    return parts[3] == expected

keys = [generate_key(i) for i in range(500)]

print(f"Generated {len(keys)} keys")
print(f"First: {keys[0]}, Validate: {validate_key(keys[0])}")
print(f"Fake: {validate_key('IRISH-AAAA-BBBB-CCCC')}")

with open(r"C:\Users\aerux\OneDrive\Documents\Default Project\key-system\keys.json", "w") as f:
    json.dump(keys, f)
print("Saved keys.json")
