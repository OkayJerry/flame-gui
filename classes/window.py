from PyQt5 import QtWidgets, QtCore
from classes.workspace import * 
from classes.beam import *
from classes.phase import PhaseSpaceWindow

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self,main_window):
        super(QtWidgets.QMenuBar,self).__init__(main_window)
        self.main_window = main_window
        self.model_history = []
        self.undo_history = []
        self.filename = None

        self.bmstate_window = BeamStateWindow()
        self.phase_window = PhaseSpaceWindow()

        self.bmstate_window.link(main_window.workspace.graph)
        self.phase_window.link(main_window.workspace.graph)

        # menus
        file_menu = self.addMenu('File')
        edit_menu = self.addMenu('Edit')
        view_menu = self.addMenu('View')

        # actions
        open_action = QtWidgets.QAction('&Open...',main_window)
        save_action = QtWidgets.QAction('&Save',main_window)
        save_as_action = QtWidgets.QAction('&Save As...',main_window)
        exit_action = QtWidgets.QAction('&Exit',main_window)

        self.undo_action = QtWidgets.QAction('&Undo',main_window)
        self.redo_action = QtWidgets.QAction('&Redo',main_window)
        self.bmstate_action = QtWidgets.QAction('&Beam State',main_window)

        phase_action = QtWidgets.QAction('&Phase Space',main_window)

        # set shortcuts
        open_action.setShortcut(QtGui.QKeySequence.Open)
        save_action.setShortcut(QtGui.QKeySequence.Save)
        save_as_action.setShortcut(QtGui.QKeySequence.SaveAs)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)

        self.undo_action.setShortcut(QtGui.QKeySequence.Undo)
        self.redo_action.setShortcut(QtGui.QKeySequence.Redo)

        # set trigger
        open_action.triggered.connect(self.open)
        save_action.triggered.connect(self.save)
        save_as_action.triggered.connect(self.save_as)
        exit_action.triggered.connect(QtWidgets.qApp.quit)

        self.undo_action.triggered.connect(self.undo_models)
        self.redo_action.triggered.connect(self.redo_models)
        self.bmstate_action.triggered.connect(lambda: self.bmstate_window.show())

        phase_action.triggered.connect(self.phase_window.open)

        # link
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(exit_action)

        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addAction(self.bmstate_action)

        view_menu.addAction(phase_action)


        self.handleUndoRedoEnabling()
        self.bmstate_action.setEnabled(False)


    def open(self):
        graph = self.main_window.workspace.graph
        latEditor = self.main_window.workspace.latEditor


        self.filename = QtWidgets.QFileDialog.getOpenFileName(self.main_window,'Open File')
        self.filename = self.filename[0] # previously tuple
        if ".lat" not in self.filename:
            warning = QtWidgets.QMessageBox()
            warning.setIcon(QtWidgets.QMessageBox.Critical)
            warning.setText("Didn't select a .lat file")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QtWidgets.QMessageBox.Ok)

            if warning.exec() == QtWidgets.QMessageBox.Ok:
                warning.close()
                return

        self.main_window.setWindowTitle("FLAME: " + self.filename)

        graph.set_model(self.filename)
        self.bmstate_window.update(graph)
        latEditor.populate()

        for i in range(len(latEditor.header())):
            latEditor.resizeColumnToContents(i)

        self.main_window.fileIsOpen = True
        self.main_window.handleFileOpen()

    def save(self):
        model = self.main_window.workspace.graph.model
        model.generate_latfile(latfile=self.filename)


    def save_as(self):
        model = self.main_window.workspace.graph.model
        name = QtWidgets.QFileDialog.getSaveFileName(self,'Save File')
        name = name[0] # previously tuple
        model.generate_latfile(latfile=name)

    def undo_models(self):
        crnt = self.main_window.workspace.graph.model
        model_history = self.main_window.workspace.graph.model_history
        undo_history = self.main_window.workspace.graph.undo_history

        undo_history.append(crnt)
        prev = model_history.pop(-1)
        self.main_window.workspace.graph.model = prev
        self.main_window.workspace.refresh()

        self.handleUndoRedoEnabling()

    def redo_models(self):
        crnt = self.main_window.workspace.graph.model
        model_history = self.main_window.workspace.graph.model_history
        undo_history = self.main_window.workspace.graph.undo_history

        model_history.append(crnt)
        subsequent = undo_history.pop(-1)
        self.main_window.workspace.graph.model = subsequent
        self.main_window.workspace.refresh()

        self.handleUndoRedoEnabling()

    def handleUndoRedoEnabling(self):
        model_history = self.main_window.workspace.graph.model_history
        undo_history = self.main_window.workspace.graph.undo_history

        if model_history:
            self.undo_action.setEnabled(True) 
        else:
            self.undo_action.setEnabled(False)

        if undo_history:
            self.redo_action.setEnabled(True)
        else:
            self.redo_action.setEnabled(False)
        
        
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.fileIsOpen = False

        # properties
        self.setWindowTitle('FLAME')
        self.setMinimumSize(1366,768)

        # components
        main = QtWidgets.QWidget()
        self.workspace = Workspace(self)
        self.menu_bar = MenuBar(self)
        layout = QtWidgets.QHBoxLayout(main)

        layout.addWidget(self.workspace)

        self.setCentralWidget(main)
        self.setMenuBar(self.menu_bar)

        # startup
        self.menu_bar.open()

    def handleFileOpen(self):
        if self.fileIsOpen:
            self.menu_bar.bmstate_action.setEnabled(True)