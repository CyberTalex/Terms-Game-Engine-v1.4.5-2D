from tkinter import Tk
from tkinter import filedialog
import tkinter as tk
import sys
import os
import json
from PyQt5.QtWidgets import QWidget,QMainWindow,QTextEdit,QVBoxLayout,QApplication,QAction,QFileDialog,QInputDialog
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import pygame
from pygame.locals import *
from constants import *
from subprocess import call
#from subprocess import Popen
from ursina.prefabs.grid_editor import PixelEditor
from PIL import Image
#import leveleditor      #Level Editörü Başta Çalıştırmak İçin
from ursina import *

pencere=tk.Tk()
pencere.title("Terms Game Engine v1.4.3 2D")
pencere.geometry("400x100")

def dosyaYap():
    dosya = open("Kayıtlı_Kod_Dosyası.py", "w")
    
dugme = tk.Button(text = "Yeni Proje", command=dosyaYap())
dugme.pack()

pencere.mainloop()

def openFile():
    options=QFileDialog.Options()
    data=QFileDialog.getOpenFileName(widget,"Dosya Seç","","All Files(*)",options=options)
    fileopen=open(data[0],"r")
    textbox.setPlainText(fileopen.read())
    fileopen.close()


def saveactionFun():
    options=QFileDialog.Options()
    data=QFileDialog.getSaveFileName(widget,"Dosya Kaydet","",options=options)
    fileopen=open(data[0],"w")
    fileopen.write(textbox.toPlainText())
    fileopen.close()

def initNotePad():
    if os.path.exists("./config.json"):
        data=open("./config.json","r")
        dictdata=json.loads(data.read())
        data.close()
        return dictdata
    else:
        openfile=open("./config.json","w")
        dictdata={"size":15}
        openfile.write(json.dumps(dictdata))
        openfile.close()
        return dictdata

def fontActionFun():
    data=QInputDialog.getInt(widget,"Yazı Boyutu","Yazı Boyutu",initData['size'],12,48,1)
    if data[1]:
        initData['size']=data[0]
        openfile=open("./config.json","w")
        openfile.write(json.dumps(initData))
        openfile.close()

        textdata=textbox.toPlainText()
        textbox.setPlainText("")
        textbox.setFontPointSize(data[0])
        textbox.setPlainText(textdata)




app=QApplication(sys.argv)

mainwindow=QMainWindow()
mainwindow.setWindowTitle("Kod Editörü")
widget=QWidget()

#menu
menubar=mainwindow.menuBar()
filemenu=menubar.addMenu("Dosya")
openaction=QAction("Aç")
openaction.triggered.connect(openFile)
filemenu.addAction(openaction)

saveaction=QAction("Kaydet")
saveaction.triggered.connect(saveactionFun)
filemenu.addAction(saveaction)

setting=menubar.addMenu("Ayarlar")
fontaction=QAction("Yazı Boyutu")
fontaction.triggered.connect(fontActionFun)
setting.addAction(fontaction)


layout=QVBoxLayout()
layout.setContentsMargins(0,0,0,0)

textbox=QTextEdit()

initData=initNotePad()


textbox.setFontPointSize(initData['size'])
layout.addWidget(textbox)
widget.setLayout(layout)

mainwindow.setCentralWidget(widget)

mainwindow.show()
mainwindow.showMaximized()

#ÖNEMLİ pixel.py Burada Çalıştırılıyor Aynı Anda İki İşlem Gerçekleştiriliyor bu Oyun Motoru'nun Kurucusu Malesef ki 32-bit bilgisayarı olduğu için iki tane işlemi yaparken kasıyor bu oyun motorunu 32-bit bir bilgisayar ile geliştirildiği için iki işlemi yapacak kadar kaldıramıyor.
call(["python", "pxeditor.py"])

exec(open('leveleditor.py').read())

sys.exit(app.exec_())