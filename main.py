from sys import argv
from PyQt5.QtWidgets import QApplication
from classes.window import *
import classes.globals as glb

if __name__ == '__main__':
    window = Window()
    window.show()
    glb.app.exec()
