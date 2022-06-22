from PyQt5 import QtWidgets, QtCore
from classes.workspace import * 
from classes.beam import *

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self,main_window):
        super(QtWidgets.QMenuBar,self).__init__(main_window)
        self.main_window = main_window
        self.filename = None
        self.bmstate_window = BeamStateWindow()

        file_menu = self.addMenu('File')
        edit_menu = self.addMenu('Edit')

        # actions
        open_action = QtWidgets.QAction('&Open...',main_window)
        save_action = QtWidgets.QAction('&Save',main_window)
        save_as_action = QtWidgets.QAction('&Save As...',main_window)
        exit_action = QtWidgets.QAction('&Exit',main_window)

        bmstate_action = QtWidgets.QAction('&Beam State',main_window)

        # set trigger
        open_action.triggered.connect(self.open)
        save_action.triggered.connect(self.save)
        save_as_action.triggered.connect(self.save_as)
        exit_action.triggered.connect(QtWidgets.qApp.quit)

        bmstate_action.triggered.connect(lambda: self.bmstate_window.show())

        # link
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(exit_action)

        edit_menu.addAction(bmstate_action)


    def open(self):
        graph = self.main_window.workspace.primary.graph
        lat_tree = self.main_window.workspace.primary.lat_tree

        self.filename = ""
        while self.filename == "" or ".lat" not in self.filename:
            self.filename = QtWidgets.QFileDialog.getOpenFileName(self.main_window,'Open File')
            self.filename = self.filename[0] # previously tuple
            if self.filename == "" or ".lat" not in self.filename:
                warning = QtWidgets.QMessageBox()
                warning.setIcon(QtWidgets.QMessageBox.Critical)
                warning.setText("Please select a .lat file")
                warning.setWindowTitle("ERROR")
                warning.setStandardButtons(QtWidgets.QMessageBox.Ok)

                if warning.exec() == QtWidgets.QMessageBox.Ok:
                    warning.close()

        self.main_window.setWindowTitle("FLAME: " + self.filename)

        graph.set_model(self.filename)

        self.bmstate_window.update(graph)

        lat_tree.model = graph.model
        lat_tree.graph = graph
        lat_tree.config_window.model = graph.model
        lat_tree.populate()
        for i in range(len(lat_tree.header())):
            lat_tree.resizeColumnToContents(i)

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
        self.setMinimumSize(1366,768)

        # components
        main = QtWidgets.QWidget()
        menu_bar = MenuBar(self)
        self.workspace = Workspace(main)
        layout = QtWidgets.QHBoxLayout(main)

        layout.addWidget(self.workspace)

        self.setCentralWidget(main)
        self.setMenuBar(menu_bar)

        # startup
        menu_bar.open()