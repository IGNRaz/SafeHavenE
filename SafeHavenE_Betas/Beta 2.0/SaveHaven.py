import sys
import os
import hashlib
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QFileDialog, QHBoxLayout, QToolButton 
from PyQt5.QtCore import QTimer, QSize, Qt
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
        self.setWindowIcon(QIcon(r'C:\Users\DELL\Downloads\shield-keyhole.png'))
        self.initUI()
        self.attempts = 0
        self.max_attempts = 3
        self.timer_duration = 60 * 5
        db()
    def initUI(self):
        self.setWindowTitle("SaveHavenE V:1.0")
        self.setGeometry(500, 350, 500, 300)
        
        
        
        image_label = QLabel(self)
        
        pixmap = QPixmap("C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\Frame 13.png")
        scaled_pixmap = pixmap.scaled(500, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setGeometry(0,0,500,300)
        image_label.setPixmap(scaled_pixmap)


    
       

        self.encrypt_button = QPushButton(' Encrypt  ', self)
        self.encrypt_button.setIcon(QIcon(r'C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\binary-lock.png'))
        self.encrypt_button.setStyleSheet('background-color:#E85555; color:black; font-size:19px; border:1px solid black ; border-radius:6px;')
        self.encrypt_button.clicked.connect(self.wencrypt)
        self.encrypt_button.setGeometry(126,250,121,31)
        self.encrypt_button.setToolTip('تشفير')

        self.decrypt_button = QPushButton('Decrypt', self)
        self.decrypt_button.setIcon(QIcon(r'C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\lock-open-alt.png'))
        self.decrypt_button.setStyleSheet('background-color:#B6EEC6; color:black; font-size:19px; border:1px solid black ; border-radius:6px;')
        self.decrypt_button.clicked.connect(self.wdecrypt)
        self.decrypt_button.setGeometry(257,250,121,31)
        self.decrypt_button.setToolTip('فك تشفير')
        self.show() 
        
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


    def createe(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.folder_input1.setText(folder)


    def wencrypt(self):
        
        self.hide()  
        page1 = QWidget()
        page1.setWindowTitle("SaveHavenE V:1.0")
        page1.setWindowIcon(QIcon('C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\shield-keyhole'))
        page1.setGeometry(500, 350, 500, 300)
    
        image_label = QLabel(page1)
        pixmap = QPixmap("C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\Frame 14.png")
        scaled_pixmap = pixmap.scaled(500, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setGeometry(0, 0, 500, 300)
        image_label.setPixmap(scaled_pixmap)

        self.folder_input1 = QLineEdit(page1)
        self.folder_input1.setToolTip('ادخل مسار الملف')
        self.folder_input1.setPlaceholderText('Enter Folder Name')
        self.folder_input1.setStyleSheet('background-color:#B6EEC6; color:black; font-size:17px; border:0.5px solid black ; border-radius:5px;')
        self.folder_input1.setGeometry(290, 95, 160, 33)

        self.choos = QPushButton('', page1)
        self.choos.setIcon(QIcon(r'C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\folder-open.png'))
        self.choos.setStyleSheet('background-color:#B6EEC6; color:black; font-size:17px; border:0.5px solid black ; border-radius:5px;')
        self.choos.setGeometry(440, 95, 38, 33)
        self.choos.setToolTip('اضغط لتحميل ملف')
        self.choos.clicked.connect(self.createe)

        self.pass_input1 = QLineEdit(page1)
        self.pass_input1.setEchoMode(QLineEdit.Password)
        self.pass_input1.setToolTip('ادخل كلمة السر')
        self.pass_input1.setPlaceholderText('Enter Password')
        self.pass_input1.setStyleSheet('background-color:#B6EEC6; color:black; font-size:17px; border:0.5px solid black ; border-radius:5px;')
        self.pass_input1.setGeometry(290, 140, 190, 33)

        button1 = QPushButton(" Encrypt", page1)
        button1.setGeometry(325, 182, 121, 29)
        button1.setIcon(QIcon(r'C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\binary-lock.png'))
        button1.setStyleSheet('background-color:#E85555; color:black; font-size:20px; border:1px solid black ; border-radius:6px;')
        button1.clicked.connect(self.encrypt)

        back_button2 = QPushButton("Back", page1)
        back_button2.setGeometry(35, 264, 121, 29)
        back_button2.clicked.connect(lambda: self.back(page1))  

        page1.show()

    def wdecrypt(self):
        
        self.hide()  
        page2 = QWidget()
        page2.setWindowTitle("SaveHavenE V:1.0")
        page2.setWindowIcon(QIcon('C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\shield-keyhole'))
        page2.setGeometry(500, 350, 500, 300)

        image_label = QLabel(page2)
        pixmap = QPixmap("C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\Frame 133.png")
        scaled_pixmap = pixmap.scaled(500, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setGeometry(0, 0, 500, 300)
        image_label.setPixmap(scaled_pixmap)

        self.folder_input1 = QLineEdit(page2)
        self.folder_input1.setToolTip('ادخل مسار الملف')
        self.folder_input1.setPlaceholderText('Enter Folder Name')
        self.folder_input1.setStyleSheet('background-color:#B6EEC6; color:black; font-size:17px; border:0.5px solid black ; border-radius:5px;')
        self.folder_input1.setGeometry(15, 95, 160, 33)

        self.choos = QPushButton('', page2)
        self.choos.setIcon(QIcon(r'C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\folder-open.png'))
        self.choos.setStyleSheet('background-color:#B6EEC6; color:black; font-size:17px; border:0.5px solid black ; border-radius:5px;')
        self.choos.setGeometry(165, 95, 38, 33)
        self.choos.setToolTip('اضغط لتحميل ملف')
        self.choos.clicked.connect(self.createe)

        self.pass_input1 = QLineEdit(page2)
        self.pass_input1.setEchoMode(QLineEdit.Password)
        self.pass_input1.setToolTip('ادخل كلمة السر')
        self.pass_input1.setPlaceholderText('Enter Password')
        self.pass_input1.setStyleSheet('background-color:#B6EEC6; color:black; font-size:17px; border:0.5px solid black ; border-radius:5px;')
        self.pass_input1.setGeometry(15, 140, 190, 33)

        button2 = QPushButton(" Decrypt", page2)
        button2.setGeometry(45, 182, 121, 29)
        button2.setIcon(QIcon(r'C:\\Users\\DELL\\Desktop\\SafeHavenE\\Used pics\\lock-open-alt.png'))
        button2.setStyleSheet('background-color:#B6EEC6; color:black; font-size:20px; border:1px solid black ; border-radius:6px;')
        button2.clicked.connect(self.decrypt)

        back_button2 = QPushButton("Back", page2)
        back_button2.setGeometry(350, 264, 121, 29)
        back_button2.clicked.connect(lambda: self.back(page2))  

        page2.show()

 
    def back(self, current_page):
        current_page.close()  
        self.show()  


    def encrypt(self):
        folder = self.folder_input1.text()
        password = self.pass_input1.text()

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
        

        folder = self.folder_input1.text()
        password = self.pass_input1.text()

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
            if decrypt and file.endswith(".azm"):
                files.append(file_path)
            elif not decrypt and not file.endswith(".azm") and file not in ["thekey.key"]:
                files.append(file_path)
        return files

    def encrypt_files(self, files, key):
        for file in files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
            contents_encrypted = Fernet(key).encrypt(contents)
            with open(file + ".azm", "wb") as thefile:
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
    app = QApplication(sys.argv)
    w = SafeHavenE()
    sys.exit(app.exec_())