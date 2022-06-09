from PyQt5 import QtWidgets
from classes.tree import *
from classes.canvas import *

class Workspace(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)

        # initialize
        self.layout = QtWidgets.QVBoxLayout()
        self.graph = FmMplCanvas()
        self.lat_tree = LatTree(self)

        # set
        self.layout.addWidget(self.graph,3)
        self.layout.addWidget(self.lat_tree,2)

        # add widgets to layout
        self.setLayout(self.layout)

