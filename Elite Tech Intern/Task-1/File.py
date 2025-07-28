import os
import hashlib
import json
import time

# Directory to monitor
MONITOR_DIR = "files_to_monitor"
HASH_DB_FILE = "hashes.json"

def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def build_hash_database(directory):
    """Build a dictionary of file paths and their hashes"""
    hash_db = {}
    for root, _, files in os.walk(directory):
        for fname in files:
            fpath = os.path.join(root, fname)
            file_hash = calculate_file_hash(fpath)
            if file_hash:
                relative_path = os.path.relpath(fpath, directory)
                hash_db[relative_path] = file_hash
    return hash_db

def save_hash_database(hash_db):
    """Save hash database to a file"""
    with open(HASH_DB_FILE, "w") as f:
        json.dump(hash_db, f, indent=4)

def load_hash_database():
    """Load existing hash database"""
    if not os.path.exists(HASH_DB_FILE):
        return {}
    with open(HASH_DB_FILE, "r") as f:
        return json.load(f)

def monitor_changes():
    """Check for file changes compared to stored hash values"""
    print(f"\n📂 Monitoring directory: {MONITOR_DIR}")
    old_hashes = load_hash_database()
    new_hashes = build_hash_database(MONITOR_DIR)

    added = set(new_hashes) - set(old_hashes)
    deleted = set(old_hashes) - set(new_hashes)
    modified = {f for f in new_hashes if f in old_hashes and new_hashes[f] != old_hashes[f]}

    if not added and not deleted and not modified:
        print("✅ No changes detected.")
    else:
        if added:
            print("➕ Files Added:")
            for f in added:
                print(f"  - {f}")
        if deleted:
            print("❌ Files Deleted:")
            for f in deleted:
                print(f"  - {f}")
        if modified:
            print("✏️Files Modified:")
            for f in modified:
                print(f"  - {f}")

    # Update the hash database
    save_hash_database(new_hashes)

if __name__ == "__main__":
    os.makedirs(MONITOR_DIR, exist_ok=True)
    print("🛡️ File Integrity Monitor Started.")
    while True:
        monitor_changes()
        print("🔁 Checking again in 10 seconds...\n")
        time.sleep(10)
