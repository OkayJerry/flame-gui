from PyQt5 import QtWidgets
from classes.tree import *
from classes.canvas import *
from classes.legend import *

class PrimaryWorkspace(QtWidgets.QWidget):
    def __init__(self,graph,parent=None):

        super(QtWidgets.QWidget,self).__init__(parent)

        # components
        self.layout = QtWidgets.QVBoxLayout()
        self.graph = graph
        self.lat_tree = LatTree(self)

        self.layout.addWidget(self.graph,3)
        self.layout.addWidget(self.lat_tree,2)

        self.setLayout(self.layout)

class SecondaryWorkspace(QtWidgets.QWidget):
    def __init__(self,graph,parent=None):
        super(QtWidgets.QWidget,self).__init__(parent)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.legend = Legend(graph,self)
        
        self.layout.addWidget(self.legend)
        
        self.setLayout(self.layout)



class Workspace(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(QtWidgets.QWidget,self).__init__(parent)

        self.graph = FmMplCanvas()
        self.primary = PrimaryWorkspace(self.graph,self)
        self.secondary = SecondaryWorkspace(self.graph,self)

        # components
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.primary,3)
        self.layout.addWidget(self.secondary,1)
        self.setLayout(self.layout)
