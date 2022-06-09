from PyQt5 import QtWidgets
from classes.workspace import * 

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self,main_window):
        super(QtWidgets.QMenuBar,self).__init__(main_window)
        self.main_window = main_window

        file_menu = self.addMenu('File')

        # actions
        open_action = QtWidgets.QAction('&Open File...',main_window)
        exit_action = QtWidgets.QAction('&Exit',main_window)

        # set trigger
        open_action.triggered.connect(self.open)
        exit_action.triggered.connect(QtWidgets.qApp.quit)

        # link
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)


    def open(self):
        graph = self.main_window.workspace.graph
        lat_tree = self.main_window.workspace.lat_tree

        filename = QtWidgets.QFileDialog.getOpenFileName(self.main_window,'Open File')
        filename = filename[0] # previously tuple

        graph.set_model(filename)
        #r,s = graph.model.run(monitor='all') # replace variables with something more descriptive
        #data = graph.model.collect_data(r,'pos','xrms','yrms')
        #graph.plot(data['xrms'],data['xrms'])

        lat_tree.populate(graph.model)
        
        
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # initialize
        main = QtWidgets.QWidget()
        menu_bar = MenuBar(self)
        self.workspace = Workspace(main)

        # set
        self.setWindowTitle('FLAME')
        self.setCentralWidget(main)
        self.setMenuBar(menu_bar)
        layout = QtWidgets.QHBoxLayout(main)
        layout.addWidget(self.workspace)


