import os
import hashlib
import json
from pymongo import MongoClient
import tkinter as tk
from tkinter import messagebox
import time


def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_all_file_hashes(folder_path):
    file_hashes = {}
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                file_hashes[file_path] = calculate_file_hash(file_path)
    return file_hashes

def save_hashes_to_file(file_hashes, file_name="file_hashes.json"):
    with open(file_name, "w") as f:
        json.dump(file_hashes, f, indent=4)

def load_hashes_from_file(file_name="file_hashes.json"):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    else:
        return None

def compare_hashes(old_hashes, new_hashes):
    changed_files = 0
    for file_path, old_hash in old_hashes.items():
        new_hash = new_hashes.get(file_path)
        if new_hash is None or new_hash != old_hash:
            changed_files += 1
    return changed_files

def monitor_folder(folder_path, max_changes=5):
    stored_hashes = load_hashes_from_file()

    if stored_hashes is None:
        print("No stored hashes found. Calculating initial hashes and saving them...")
        initial_hashes = get_all_file_hashes(folder_path)
        save_hashes_to_file(initial_hashes)
        print("Initial hashes saved. Monitoring will start next time you run the program.")
        return str("First time hash detected")

    current_hashes = get_all_file_hashes(folder_path)

    changed_files_count = compare_hashes(stored_hashes, current_hashes)

    if changed_files_count > max_changes:
        print(f"Attack detected! More than {max_changes} files have been modified.")
        
        myclient = MongoClient(
            "mongodb+srv://jainam:7sjssduBdkrndj@finalproject.q4jsbp.mongodb.net/Ransomware?retryWrites=true&w=majority&appName=finalproject",
            tls=True, 
            tlsAllowInvalidCertificates=True
            )
        mydb = myclient["Ransomware"]
        mycol = mydb["machines"]
        myquery = { "ipaddress": "10.0.2.15" }
        newvalues = { "$set": { "status": "Attack" } }
        mycol.update_one(myquery, newvalues)     
        messagebox.showwarning("Ransomware Detector", "Your system has been Attacked")
        save_hashes_to_file(current_hashes)
        print("Current hashes saved for future comparison.")
        return str("Attack detected")

    else:
        print(f"{changed_files_count} files changed. No attack detected.")
        save_hashes_to_file(current_hashes)
        print("Current hashes saved for future comparison.")
        return str("System is safe")

folder_path = "C:\\Users\\mehta\\OneDrive\\Desktop\\impfiles"

while True:
    ret = monitor_folder(folder_path, max_changes=5)
    if ret == "Attack detected":
        break
    else:
        time.sleep(2)
        print("Scanning file hashes...")
        continue
    



