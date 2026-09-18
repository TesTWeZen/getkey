import hashlib
import json
import secrets
import string

SALT = "IRISH_HUB_2024"
NUM_KEYS = 500
KEY_CHARS = string.ascii_uppercase + string.digits  # A-Z0-9

def generate_key(index):
    h = hashlib.sha256(f"{SALT}-{index}".encode()).hexdigest()
    # 3 groups of 4 chars from hash
    g1 = ''.join(KEY_CHARS[int(h[i], 16) % len(KEY_CHARS)] for i in range(0, 4))
    g2 = ''.join(KEY_CHARS[int(h[i], 16) % len(KEY_CHARS)] for i in range(4, 8))
    g3 = ''.join(KEY_CHARS[int(h[i], 16) % len(KEY_CHARS)] for i in range(8, 12))
    return f"IRISH-{g1}-{g2}-{g3}"

keys = [generate_key(i) for i in range(NUM_KEYS)]

# Save as JSON
with open("keys.json", "w") as f:
    json.dump(keys, f)

# Save as Lua table (for script)
with open("keys.luau", "w") as f:
    f.write("local KEYS = {\n")
    for k in keys:
        f.write(f'    ["{k}"] = true,\n')
    f.write("}\n")

# Save as plain list
with open("keys_list.txt", "w") as f:
    f.write("\n".join(keys))

print(f"Generated {NUM_KEYS} keys")
print(f"Example: {keys[0]}")
print(f"Example: {keys[1]}")
print(f"Example: {keys[2]}")
