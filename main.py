from sys import argv
from PyQt5.QtWidgets import QApplication
from classes.window import *
 
if __name__ == '__main__':
    app = QApplication(argv)
    window = Window()
    window.show()
    app.exec()
