import sys
import os
import hashlib
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QFileDialog, QHBoxLayout, QToolButton
from PyQt5.QtCore import QTimer, QSize , Qt
from PyQt5.QtGui import QPixmap, QIcon
import re
import sqlite3
 

def db():
    conn=sqlite3.connect('.password.db')
    c=conn.cursor()
    
    c.execute('''create table if not exists pass ( folder text primary key, hashed_password text)
                   
                   ''')
        
    conn.commit()
    conn.close()
     


class SafeHavenE(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('c:\\Users\\DELL\\Downloads\\shield-keyhole.png'))
        self.initUI()
        self.attempts = 0
        self.max_attempts = 3
        self.timer_duration = 60 * 5
        db()
    def initUI(self):
        self.setWindowTitle("SaveHavenE V:1.0")
        self.setGeometry(100, 100, 500, 300)
        
        layout = QVBoxLayout()
        
        image_label = QLabel(self)
        pixmap = QPixmap("C:/Users/DELL/Downloads/download.jpg")
        scaled_pixmap = pixmap.scaled(500, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        layout.addWidget(image_label)

        self.folder_label = QLabel('Enter Folder Name:')
        self.folder_input = QLineEdit(self)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        
        self.pass_label = QLabel('Enter Password:')
        self.pass_input = QLineEdit(self)
        self.pass_input.setEchoMode(QLineEdit.Password)
        
       
        self.eye_button = QToolButton(self)
        self.eye_button.setIcon(QIcon('C:/Users/DELL/Desktop/SafeHavenE/Used pics/hide.png'))
        self.eye_button.setIconSize(QSize(20, 20))
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(self.pass_input)
        pass_layout.addWidget(self.eye_button)
        
        layout.addWidget(self.pass_label)
        layout.addLayout(pass_layout)

        self.choos = QPushButton('Choose Folder', self)
        self.choos.setIcon(QIcon(r'C:\\Users\\DELL\\Downloads\\folder-open.png'))
        self.choos.clicked.connect(self.create)
        layout.addWidget(self.choos)

        self.encrypt_button = QPushButton(' Encrypt  ', self)
        self.encrypt_button.setIcon(QIcon(r'c:\\Users\\DELL\\Downloads\\binary-lock.png'))
        self.encrypt_button.clicked.connect(self.encrypt)
        layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('Decrypt', self)
        self.decrypt_button.setIcon(QIcon(r'c:\\Users\\DELL\\Downloads\\lock-open-alt.png'))
        self.decrypt_button.clicked.connect(self.decrypt)
        layout.addWidget(self.decrypt_button)

        self.timer_label = QLabel('')
        layout.addWidget(self.timer_label)

        self.setLayout(layout)
        self.show() 

    def create(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.folder_input.setText(folder)

    def passcheak(self, password):
        if len(password) < 8:
            QMessageBox.warning(self, 'Error', 'Password should be at least 8 characters.')
            return False

        if not re.search(r'[a-z]', password):
            QMessageBox.warning(self, 'Error', 'Password should have at least one lowercase letter.')
            return False

        if not re.search(r'[A-Z]', password):
            QMessageBox.warning(self, 'Error', 'Password should have at least one uppercase letter.')
            return False

        if not re.search(r'[!@#$%&]', password):
            QMessageBox.warning(self, 'Error', 'Password should have at least one symbol.')
            return False

        return True

    def encrypt(self):
        folder = self.folder_input.text()
        password = self.pass_input.text()

        if not self.passcheak(password):
            return

        if not os.path.exists(folder):
            os.makedirs(folder)

        conn = sqlite3.connect('.password.db')
        c = conn.cursor()

        
        c.execute("SELECT hashed_password FROM pass WHERE folder=?", (folder,))
        row = c.fetchone()

        if row is None:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            c.execute("INSERT INTO pass (folder, hashed_password) VALUES (?, ?)", (folder, hashed_password))
            conn.commit()

            key = Fernet.generate_key()
            with open(os.path.join(folder, "thekey.key"), "wb") as thekey:
                thekey.write(key)
        else:
            with open(os.path.join(folder, "thekey.key"), "rb") as thekey:
                key = thekey.read()

        files = self.get_files(folder)
        if not files:
            QMessageBox.information(self, 'Info', 'No new files to encrypt.')
            return

        self.encrypt_files(files, key)
        QMessageBox.information(self, 'Success', 'New files encrypted.')

    def decrypt(self):
        folder = self.folder_input.text()
        password = self.pass_input.text()

        if not os.path.exists(folder):
            QMessageBox.warning(self, 'Error', 'No folder with that name. Please create one or choose an existing one.')
            return

        if not os.path.exists(os.path.join(folder, "thekey.key")):
            QMessageBox.warning(self, 'Error', 'No encrypted files found.')
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        
        conn = sqlite3.connect('.password.db')
        c = conn.cursor()
        c.execute("SELECT hashed_password FROM pass WHERE folder=?", (folder,))
        row = c.fetchone()

        if row is None:
            QMessageBox.warning(self, 'Error', 'No password found for this folder.')
            conn.close()
            return

        stored_hashed_password = row[0]
        conn.close()
        if hashed_password == stored_hashed_password:
            self.attempts = 0
            with open(os.path.join(folder, "thekey.key"), "rb") as thekey:
                key = thekey.read()

            files = self.get_files(folder, decrypt=True)
            self.decrypt_files(files, key)
            QMessageBox.information(self, 'Success', 'Files decrypted successfully.')

        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.start_timer()
            else:
                QMessageBox.warning(self, 'Error', f'Wrong password. Attempts left: {self.max_attempts - self.attempts}')

    def start_timer(self):
        self.timer_label.setText(f'Please wait {self.timer_duration}s before the next try')
        QTimer.singleShot(self.timer_duration * 1000, self.reset_attempts)

    def reset_attempts(self):
        self.attempts = 0
        self.timer_label.setText('')

    def get_files(self, folder, decrypt=False):
        files = []
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if decrypt and file.endswith(".az"):
                files.append(file_path)
            elif not decrypt and not file.endswith(".az") and file not in ["thekey.key"]:
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

    def toggle_password_visibility(self):
        if self.pass_input.echoMode() == QLineEdit.Password:
            self.pass_input.setEchoMode(QLineEdit.Normal)
            self.eye_button.setIcon(QIcon('C:/Users/DELL/Desktop/SafeHavenE/Used pics/view.png'))
        else:
            self.pass_input.setEchoMode(QLineEdit.Password)
            self.eye_button.setIcon(QIcon('C:/Users/DELL/Desktop/SafeHavenE/Used pics/hide.png'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SafeHavenE()
    sys.exit(app.exec_())
