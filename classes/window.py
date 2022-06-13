from PyQt5 import QtWidgets
from classes.workspace import * 

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self,main_window):
        super(QtWidgets.QMenuBar,self).__init__(main_window)
        self.main_window = main_window
        self.filename = None

        file_menu = self.addMenu('File')

        # actions
        open_action = QtWidgets.QAction('&Open...',main_window)
        save_action = QtWidgets.QAction('&Save',main_window)
        save_as_action = QtWidgets.QAction('&Save As...',main_window)
        exit_action = QtWidgets.QAction('&Exit',main_window)

        # set trigger
        open_action.triggered.connect(self.open)
        save_action.triggered.connect(self.save)
        save_as_action.triggered.connect(self.save_as)
        exit_action.triggered.connect(QtWidgets.qApp.quit)

        # link
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(exit_action)


    def open(self):
        graph = self.main_window.workspace.primary.graph
        lat_tree = self.main_window.workspace.primary.lat_tree

        self.filename = QtWidgets.QFileDialog.getOpenFileName(self.main_window,'Open File')
        self.filename = self.filename[0] # previously tuple

        graph.set_model(self.filename)

        lat_tree.model = graph.model
        lat_tree.populate()

    def save(self):
        model = self.main_window.workspace.graph.model
        model.generate_latfile(latfile=self.filename)


    def save_as(self):
        model = self.main_window.workspace.graph.model
        name = QtWidgets.QFileDialog.getSaveFileName(self,'Save File')
        name = name[0] # previously tuple
        model.generate_latfile(latfile=name)


        
        
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # properties
        self.setWindowTitle('FLAME')
        self.setMinimumSize(1280,720)

        # components
        main = QtWidgets.QWidget()
        menu_bar = MenuBar(self)
        self.workspace = Workspace(main)
        layout = QtWidgets.QHBoxLayout(main)

        layout.addWidget(self.workspace)

        self.setCentralWidget(main)
        self.setMenuBar(menu_bar)


