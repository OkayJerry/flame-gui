
from PyQt5.QtWidgets import QApplication

import globals as glb
from classes.windows import MainWindow

if __name__ == '__main__':
    window = MainWindow()
    window.show()
    glb.app.exec()
