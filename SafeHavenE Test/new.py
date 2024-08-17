#امبوراتات

#مكتبة للنظام والتحكم بلملفات
import sys
import os
#مكتبة شان نسوي باسورد مشفرة عواض الداتا بيس
import hashlib
#مكتبة تشفير
from cryptography.fernet import Fernet
#مكاتب واجهات
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout , QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
import re 






#كلاسات و دوال
class SafeHavenE(QWidget):
    #main
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('c:\\Users\\DELL\\Downloads\\shield-keyhole.png'))
        self.initUI()
        #حماية شان مايصير spam
        self.attempts = 0
        self.max_attempts = 3
        #مؤقت بيشتغل بلثواني 
        self.timer_duration = 60*5 
    #ui
    def initUI(self):
        
        self.setWindowTitle("SaveHavenE V:1.0")
        self.setGeometry(100, 100, 500,300)
        
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
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)

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

    #pass cheak :3
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

    #تشفير
    def encrypt(self):
        folder = self.folder_input.text()
        password = self.pass_input.text()

        if not self.passcheak(password):
          return

        
        #بتسوي ملف او بتستعمله
        if not os.path.exists(folder):
            os.makedirs(folder)

        # التحقق من وجود المفتاح
        if not os.path.exists(os.path.join(folder, "thekey.key")):
            # إنشاء كلمة سر مشفرة
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
           # with open(os.path.join(folder, "password.txt"), "w") as passfile:
              #  passfile.write(hashed_password)

            # إنشاء مفتاح
            key = Fernet.generate_key()
            with open(os.path.join(folder, "thekey.key"), "wb") as thekey:
                thekey.write(key)
        else:
            with open(os.path.join(folder, "thekey.key"), "rb") as thekey:
                key = thekey.read()

        # جلب الملفات التي لم يتم تشفيرها بعد
        files = self.get_files(folder)
        if not files:
            QMessageBox.information(self, 'Info', 'No new files to encrypt.')
            return

        self.encrypt_files(files, key)
        QMessageBox.information(self, 'Success', 'New files encrypted.')
        
    #فك تشفير
    def decrypt(self):
        folder = self.folder_input.text()
        password = self.pass_input.text()
        
        #في حال ماكان في ملف 
        if not os.path.exists(folder):
            QMessageBox.warning(self, 'Error', 'No Foolder with that name please create one or choose an exsiting one.')
            return
        #في حال ماكان في مفتاح
        if not os.path.exists(os.path.join(folder, "thekey.key")):
            QMessageBox.warning(self, 'Error', 'No encrypted files found.')
            return
        #التاكد من الكلمة اذا كانت نفس الكلمة المشفرة بلملف
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        #قي حال تحقق بفك
        with open(os.path.join(folder, "password.txt"), "r") as passfile:
            stored_hashed_password = passfile.read()

        if hashed_password == stored_hashed_password:
            self.attempts = 0
            with open(os.path.join(folder, "thekey.key"), "rb") as thekey:
                key = thekey.read()

            files = self.get_files(folder, decrypt=True)
            self.decrypt_files(files, key)
            QMessageBox.information(self, 'Success', 'Files decrypted successfully.')

        else:
            #هي شان اذا صار خطاء بلكلمة بمررها وبيرفع قيمة الحاولات لحتى يسكر لوب
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.start_timer()
            else:
                QMessageBox.warning(self, 'Error', f'Wrong password. Attempts left: {self.max_attempts - self.attempts}')

    def start_timer(self):
        self.timer_label.setText(f'Please wait {self.timer_duration}s before the next try')
        #مؤقت بستعمل الملي ثانية ضربتها بي 1000 شان يصير دقايق تقريبا
        QTimer.singleShot(self.timer_duration * 1000, self.reset_attempts)

    def reset_attempts(self):
        #بس خلص الوقت بيرجع بعيد المحاولات لمحل ماكانت لبشتغل الكود
        self.attempts = 0
        self.timer_label.setText('')
    #بتجيب الملفات 
    def get_files(self, folder, decrypt=False):
        #بتخزن مسارات
        files = []
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            #في حال كان مشفر بخزنه 
            if decrypt and file.endswith(".az"):
                files.append(file_path)
                #في حال مو مشفر بضيفه للقائمة ليشفره
            elif not decrypt and not file.endswith(".az") and file not in ["thekey.key", "password.txt"]:
                files.append(file_path)
                #بترجع ملفات
        return files
        
    #بتجيب الملفات المشفرة
    def encrypt_files(self, files, key):
        for file in files:
            #يقرا باينري
            with open(file, "rb") as thefile:
                #محتويات
                contents = thefile.read()
                #تشفير محتويات الملف باستخدام مفتاح التشفير
            contents_encrypted = Fernet(key).encrypt(contents)
            #بكتب امتداد ليضيف .az
            with open(file + ".az", "wb") as thefile:   
                #كتابة المحتويات المشفرة في الملف الجديد
                thefile.write(contents_encrypted)
                #حذف الملف الأصلي بعد تشفيره
            os.remove(file)
    #فك تشفير
    def decrypt_files(self, files, key):
        #تقريبا نفيس كلام فك التشفير
        for file in files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
                #فك تشفير
            contents_decrypted = Fernet(key).decrypt(contents)
            #لحذف ال .az
            og_name = file[:-3]
            with open(og_name, "wb") as thefile:
                #ترجيع محتويات
                thefile.write(contents_decrypted)
                #حذف الملف المشفر
            os.remove(file)

if __name__ == '__main__':
    #إنشاء تطبيق 
    app = QApplication(sys.argv)
    #إنشاء widget
    w = SafeHavenE()
    #تشغيل التطبيق
    sys.exit(app.exec_())
