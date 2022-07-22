from sys import argv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from classes.window import *
import classes.globals as glb

if __name__ == '__main__':
    window = Window()
    window.setWindowIcon(QIcon('frib.jpg'))
    window.show()
    glb.app.exec()
