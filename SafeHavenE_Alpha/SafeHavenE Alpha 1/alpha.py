'''
import sys
import os
import hashlib
from cryptography.fernet import Fernet
import re 

class SafeHavenE:
    def __init__(self):
        self.attempts = 0
        self.max_attempts = 3
        self.timer_duration = 60*5

    def encrypt(self, folder, password):
        if not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(os.path.join(folder, "thekey.key")):
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            with open(os.path.join(folder, "password.txt"), "w") as passfile:
                passfile.write(hashed_password)

            key = Fernet.generate_key()
            with open(os.path.join(folder, "thekey.key"), "wb") as thekey:
                thekey.write(key)
        else:
            with open(os.path.join(folder, "thekey.key"), "rb") as thekey:
                key = thekey.read()

        files = self.get_files(folder)
        if not files:
            return

        self.encrypt_files(files, key)
        
    def decrypt(self, folder, password):
        if not os.path.exists(folder):
            return

        if not os.path.exists(os.path.join(folder, "thekey.key")):
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        with open(os.path.join(folder, "password.txt"), "r") as passfile:
            stored_hashed_password = passfile.read()

        if hashed_password == stored_hashed_password:
            self.attempts = 0
            with open(os.path.join(folder, "thekey.key"), "rb") as thekey:
                key = thekey.read()

            files = self.get_files(folder, decrypt=True)
            self.decrypt_files(files, key)
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.start_timer()

    def start_timer(self):
        QTimer.singleShot(self.timer_duration * 1000, self.reset_attempts)

    def reset_attempts(self):
        self.attempts = 0

    def get_files(self, folder, decrypt=False):
        files = []
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if decrypt and file.endswith(".az"):
                files.append(file_path)
            elif not decrypt and not file.endswith(".az") and file not in ["thekey.key", "password.txt"]:
                files.append(file_path)
        return files

    def encrypt_files(self, files, key):
        for file in files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
            contents_encrypted = Fernet(key).encrypt(contents)
            with open(file + ".az", "wb") as thefile:   
                thefile.write(contents_encrypted)
            os.remove(file)

    def decrypt_files(self, files, key):
        for file in files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
            contents_decrypted = Fernet(key).decrypt(contents)
            og_name = file[:-3]
            with open(og_name, "wb") as thefile:
                thefile.write(contents_decrypted)
            os.remove(file)

if __name__ == '__main__':
    app = SafeHavenE()
'''