import os
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

def encrypt_file(file_path, cipher):
    with open(file_path, "rb") as f:
        file_data = f.read()

    encrypted_data = cipher.encrypt(file_data)

    with open(file_path, "wb") as f:
        f.write(encrypted_data)

    base, ext = os.path.splitext(file_path)
    new_file_path = base + "_encrypted" + ext
    os.rename(file_path, new_file_path)
    print(f"Encrypted and renamed: {new_file_path}")

folder_path = "C:\\Users\\mehta\\Desktop\\impfiles"

for root, dirs, files in os.walk(folder_path):
    for filename in files:
        file_path = os.path.join(root, filename)
        
        if os.path.isfile(file_path):
            print(f"Encrypting {file_path}")
            encrypt_file(file_path, cipher)

print("All files and subfolder files have been encrypted and renamed!")
