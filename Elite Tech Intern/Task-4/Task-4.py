from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64, os

def generate_key(password: str, salt: bytes) -> bytes:
    """Derives a key using PBKDF2 from password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(file_path, password):
    salt = os.urandom(16)
    key = generate_key(password, salt)
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        original_data = file.read()

    encrypted_data = fernet.encrypt(original_data)

    with open(file_path + ".enc", 'wb') as file:
        file.write(salt + encrypted_data)

    print(f"✅ File encrypted: {file_path}.enc")

def decrypt_file(file_path, password):
    with open(file_path, 'rb') as file:
        data = file.read()
        salt, encrypted_data = data[:16], data[16:]

    key = generate_key(password, salt)
    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        original_name = file_path.replace(".enc", ".dec")

        with open(original_name, 'wb') as file:
            file.write(decrypted_data)

        print(f"✅ File decrypted: {original_name}")
    except Exception as e:
        print("❌ Decryption failed. Wrong password or file corrupted.")

if __name__ == "__main__":
    import sys

    print("=== AES-256 FILE ENCRYPTOR / DECRYPTOR ===")
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").lower()

    file_path = input("Enter file path: ").strip()
    password = input("Enter password: ").strip()

    if choice == 'e':
        encrypt_file(file_path, password)
    elif choice == 'd':
        decrypt_file(file_path, password)
    else:
        print("❌ Invalid option.")
