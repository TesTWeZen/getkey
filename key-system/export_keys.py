import json, os

keys_path = r"C:\Users\aerux\OneDrive\Documents\Default Project\key-system\keys.json"
with open(keys_path) as f:
    keys = json.load(f)

out_path = r"C:\Users\aerux\OneDrive\Documents\Default Project\key-system\keys_data.js"
with open(out_path, "w") as f:
    f.write("const VALID_KEYS = ")
    json.dump(keys, f)
    f.write(";\n")

print(f"Wrote {len(keys)} keys to keys_data.js")
