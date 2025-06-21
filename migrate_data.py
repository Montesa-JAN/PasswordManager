import json
import os

DATA_FILE = "dist/main/data.json"

def migrate():
    if not os.path.exists(DATA_FILE):
        print("No data.json found to migrate.")
        return

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print("Error reading data.json:", e)
            return

    # If already a list of dicts, do nothing
    if isinstance(data, list):
        print("data.json is already in the correct format.")
        return

    # If it's a dict (old format), convert to list of dicts
    migrated = []
    if isinstance(data, dict):
        for key, value in data.items():
            # If value is a list (dict-of-lists format)
            if isinstance(value, list):
                for entry in value:
                    entry_copy = entry.copy()
                    entry_copy["website"] = key
                    migrated.append(entry_copy)
            # If value is a dict (single entry per website)
            elif isinstance(value, dict):
                entry_copy = value.copy()
                entry_copy["website"] = key
                migrated.append(entry_copy)
    else:
        print("Unknown data.json format. No migration performed.")
        return

    # Write migrated data back
    with open(DATA_FILE, "w") as f:
        json.dump(migrated, f, indent=4)
    print("Migration complete. data.json is now in the new format.")

if __name__ == "__main__":
    migrate()