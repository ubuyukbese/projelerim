from datetime import datetime
start = datetime.now()
import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtWidgets import QAction, qApp, QMainWindow, QComboBox, QLineEdit
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
mid1 = datetime.now()

class Mail(MIMEMultipart):
    def __init__(self):
        super().__init__()

    def mailbilesen(self,fromfrom,toto,subject,body,sifre):
        self["From"] = fromfrom
        self["To"] = toto
        self["Subject"] = subject
        self.sifre = sifre
        self.text = body
        self.body = MIMEText(self.text, "plain")
        self.attach(self.body)

    def mailattachment(self,aclick):
        filename = QFileDialog.getOpenFileName(aclick,"Dosya Aç",os.getenv("HOME"))
        filename = filename[0]
        attachment = open(filename,"rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        self.attach(p)
        self.attachmentname = filename

    def mailgonder(self):
        try:
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login(self["From"], self.sifre)
            mail.sendmail(self["From"], self["To"], self.as_string())
            print("Mail Başarıyla Gönderildi")
            mail.close()

        except:
            sys.stderr.write("Bir sorun oluştu, mailiniz gönderilemedi")
            sys.stderr.flush()

class Mailuygulama(QWidget):
    def __init__(self):
        super().__init__()
        self.mail = Mail()
        self.init_ui()
        self.uitasarim()

    def init_ui(self):
        self.c1 = QLabel("Kimden:")
        self.c2 = QLabel("Kime:")
        self.c3 = QLabel("Şifre:")
        self.c4 = QLabel("Konu:")
        self.c5 = QLabel("Gövde:")
        self.d1 = QLineEdit()
        self.d2 = QLineEdit()
        self.d3 = QLineEdit()
        self.d3.setEchoMode(QLineEdit.Password)
        self.d4 = QLineEdit()
        self.d5 = QTextEdit()
        self.aclick = QPushButton("Dosya Ekle")
        self.fclick = QPushButton("Mail Gönder")
        self.attachlabel = QLabel()
        self.runningattachlabel = ""
        self.aclick.clicked.connect(lambda : self.mailattachment(self.aclick))
        self.fclick.clicked.connect(lambda: self.mailgonder(self.d1.text(),self.d2.text(),self.d4.text(),self.d5.toPlainText(),self.d3.text()))
        self.widgets1 = []
        self.widgets2 = []
        for i in range(1,6):
            self.widgets1.append(eval("self.c" + str(i)))
        for i in range(1,6):
            self.widgets2.append(eval("self.d" + str(i)))
        self.formatting()

    def formatting(self):
        for i in self.widgets1:
            i.setAlignment(Qt.AlignRight)
            i.setFont(QFont("Arial", 16))

        for i in self.widgets2:
            i.setAlignment(Qt.AlignLeft)
            i.setFont(QFont("Arial", 16))
            i.setGeometry(0,0,500,500)

    def uitasarim(self):
        self.smallboxes1 = []
        self.smallboxes2 = []
        for i in self.widgets1:
            a = 1
            v_boxum = QVBoxLayout()
            v_boxum.addWidget(i)
            widgeting = QWidget()
            widgeting.setMinimumWidth(100)
            widgeting.setLayout(v_boxum)
            #v_boxum.setGeometry(QRect(0,0,4000,1000))
            self.smallboxes1.append(widgeting)
            v_boxum.setObjectName("box for c"+ str(a))
            widgeting.setObjectName("box for cc"+ str(a))
            a += 1
        for i in self.widgets2:
            v_boxum = QVBoxLayout()
            v_boxum.addWidget(i)
            widgeting = QWidget()
            widgeting.setMinimumWidth(300)
            widgeting.setLayout(v_boxum)
            #v_boxum.setGeometry(QRect(0,0,4000,1000))
            self.smallboxes2.append(widgeting)
            v_boxum.setObjectName("box for d"+ str(a))
            widgeting.setObjectName("box for dd"+ str(a))
            a += 1

        self.ortabox = []
        for i in range(1,6):
            h_boxum = QHBoxLayout()
            self.ortabox.append(h_boxum)
            h_boxum.setObjectName("h_box" + str(i))

        for i in range(len(self.ortabox)):
            self.ortabox[i].addWidget(self.smallboxes1[i])
            self.ortabox[i].addWidget(self.smallboxes2[i])

        v_box1 = QVBoxLayout()
        h_box = QHBoxLayout()
        h_boxattach = QHBoxLayout()

        h_box.addWidget(self.fclick)

        for i in self.ortabox:
            v_box1.addLayout(i)

        v_box1.addLayout(h_box)

        v_box = QVBoxLayout()
        v_box.addStretch()
        v_box.addLayout(v_box1)
        v_box.addWidget(self.aclick)
        v_box.addWidget(self.attachlabel)
        v_box.addStretch()

        self.setLayout(v_box)
        self.setWindowTitle("Mail Uygulaması")

    def mailattachment(self,aclick):
        self.mail.mailattachment(aclick)
        self.runningattachlabel += self.mail.attachmentname + "\n"
        self.attachlabel.setText(self.runningattachlabel)

    def mailgonder(self,fromfrom,toto,subject,body,sifre):
        self.mail.mailbilesen(fromfrom,toto,subject,body,sifre)
        self.mail.mailgonder()

class Anapencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mailuygulama = Mailuygulama()
        self.setCentralWidget(self.mailuygulama)

        #self.menuleri_olustur()
        self.show()
        self.setWindowTitle("Mail Gönderme Uygulaması")


mid2 = datetime.now()
app = QApplication(sys.argv)
menu = Anapencere()
finish = datetime.now()
print(finish-start)
print(finish-mid2)
print(mid2-mid1)
print(mid1-start)
sys.exit(app.exec())
