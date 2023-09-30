from PyQt5.QtCore import Qt
import os
from PyQt5.QtWidgets import ( QApplication, QFileDialog, QListWidget ,QButtonGroup, QGroupBox, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox, QHBoxLayout,  QRadioButton )
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageFilter import SHARPEN


app = QApplication([])
window = QWidget()
window.resize(1200,900)
window.setWindowTitle('Easy Editor')
lwfiles = QListWidget()

knop_papka = QPushButton('Папка')
knop_levo = QPushButton('Лево')
knop_pravo = QPushButton('Право')
knop_zerkalo = QPushButton('Зеркало')
knop_rezkost = QPushButton('Резкость')
knop_bw = QPushButton('Ч/Б')
kartina = QLabel('Картинка')

glav = QHBoxLayout()
lay_1 = QVBoxLayout()
lay_1.addWidget(knop_papka)
lay_1.addWidget(lwfiles)
lay_2 = QVBoxLayout()
lay_2.addWidget(kartina, 90)
lay_tools = QHBoxLayout()
lay_tools.addWidget(knop_levo)
lay_tools.addWidget(knop_pravo)
lay_tools.addWidget(knop_zerkalo)
lay_tools.addWidget(knop_rezkost)
lay_tools.addWidget(knop_bw)
lay_2.addLayout(lay_tools)

glav.addLayout(lay_1, 20)
glav.addLayout(lay_2, 80)
window.setLayout(glav)
window.show()



workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenameList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    lwfiles.clear()
    for filename in filenames:
        lwfiles.addItem(filename)



class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modifield/'

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        kartina.hide()
        pixmapimage = QPixmap(path)
        w, h = kartina.width(), kartina.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        kartina.setPixmap(pixmapimage)
        kartina.show()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_rezkost(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    




workimage = ImageProcessor()

def showChosenImage():
    if lwfiles.currentRow() >= 0:
        filename = lwfiles.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

lwfiles.currentRowChanged.connect(showChosenImage)
knop_papka.clicked.connect(showFilenameList)
knop_bw.clicked.connect(workimage.do_bw)
knop_zerkalo.clicked.connect(workimage.do_flip)
knop_levo.clicked.connect(workimage.do_left)
knop_pravo.clicked.connect(workimage.do_right)
knop_rezkost.clicked.connect(workimage.do_rezkost)


app.exec()

