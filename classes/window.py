from PyQt5 import QtWidgets
from classes.workspace import *
from classes.beam import *
from classes.phase import PhaseSpaceWindow
from classes.optimize import OptimizationWindow
from classes.pref import PreferenceWindow
from flame_utils import ModelFlame
from flame import Machine
import flame
from collections import OrderedDict
import numpy as np
import os
import classes.globals as glb


class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, main_window):
        super(QtWidgets.QMenuBar, self).__init__(main_window)
        self.main_window = main_window
        self.model_history = []
        self.undo_history = []
        self.filename = None
        self.bmstate_window = BeamStateWindow()
        self.phase_window = PhaseSpaceWindow()
        self.opt_window = OptimizationWindow()
        self.pref_window = PreferenceWindow(self)

        # menus
        file_menu = self.addMenu('File')
        edit_menu = self.addMenu('Edit')
        view_menu = self.addMenu('View')

        # actions
        new_action = QtWidgets.QAction('&New', main_window)
        open_action = QtWidgets.QAction('&Open...', main_window)
        save_action = QtWidgets.QAction('&Save', main_window)
        save_as_action = QtWidgets.QAction('&Save As...', main_window)
        exit_action = QtWidgets.QAction('&Exit', main_window)

        self.undo_action = QtWidgets.QAction('&Undo', main_window)
        self.redo_action = QtWidgets.QAction('&Redo', main_window)
        self.bmstate_action = QtWidgets.QAction('&Beam State', main_window)
        self.opt_action = QtWidgets.QAction('&Optimization', main_window)

        phase_action = QtWidgets.QAction('&Phase Space', main_window)
        pref_action = QtWidgets.QAction('&Preferences', main_window)

        # set shortcuts
        new_action.setShortcut(QtGui.QKeySequence.New)
        open_action.setShortcut(QtGui.QKeySequence.Open)
        save_action.setShortcut(QtGui.QKeySequence.Save)
        save_as_action.setShortcut(QtGui.QKeySequence.SaveAs)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)

        self.undo_action.setShortcut(QtGui.QKeySequence.Undo)
        self.redo_action.setShortcut(QtGui.QKeySequence.Redo)

        # set trigger
        new_action.triggered.connect(self.new)
        open_action.triggered.connect(self.open)
        save_action.triggered.connect(self.save)
        save_as_action.triggered.connect(self.saveAs)
        exit_action.triggered.connect(QtWidgets.qApp.quit)

        self.undo_action.triggered.connect(self.undoModels)
        self.redo_action.triggered.connect(self.redoModels)
        self.bmstate_action.triggered.connect(
            lambda: self.bmstate_window.show())
        self.opt_action.triggered.connect(lambda: self.opt_window.show())

        phase_action.triggered.connect(self.phase_window.open)
        pref_action.triggered.connect(
            lambda: self.pref_window.show())

        # link
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(exit_action)

        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addAction(self.bmstate_action)
        edit_menu.addAction(self.opt_action)

        view_menu.addAction(phase_action)
        view_menu.addAction(pref_action)

        self.handleUndoRedoEnabling()

    def new(self):
        glb.model = glb.createModel()
        # self.main_window.menu_bar.opt_window.clear()
        self.main_window.workspace.refresh()
        
    def open(self):
        graph = self.main_window.workspace.graph
        lat_editor = self.main_window.workspace.lat_editor
        opt_window = self.main_window.menu_bar.opt_window

        while True:
            self.filename = QtWidgets.QFileDialog.getOpenFileName(
                self.main_window, 'Open File', filter="Lattice File (*.lat)")[0]  # previously tuple
            if self.filename: 
                if ".lat" not in self.filename:
                    warning = QtWidgets.QMessageBox()
                    warning.setIcon(QtWidgets.QMessageBox.Critical)
                    warning.setText("Didn't select a .lat file")
                    warning.setWindowTitle("ERROR")
                    warning.setStandardButtons(QtWidgets.QMessageBox.Ok)

                    if warning.exec() == QtWidgets.QMessageBox.Ok:
                        warning.close()
                        continue

                self.main_window.setWindowTitle("FLAME: " + self.filename)

                glb.model = ModelFlame(self.filename)
                if 'Eng_Data_Dir' not in glb.model.machine.conf().keys():
                    n_conf = glb.model.machine.conf()
                    n_conf['Eng_Data_Dir'] = flame.__file__.replace(
                        '__init__.py', 'test/data')
                    glb.model = ModelFlame(machine=Machine(n_conf))
                graph.updateLines()
                self.bmstate_window.update()
                lat_editor.populate()
                opt_window.clear()
                opt_window.select_window.setKnobs()
                # opt_window.select_window.fill()

                for i in range(len(lat_editor.header())):
                    lat_editor.resizeColumnToContents(i)

                self.phase_window.setElementBox()
            break

    def save(self):
        glb.model.generate_latfile(latfile=self.filename)

    def saveAs(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "model.lat", "Lattice File (*.lat)")[0]  # previously tuple
        if filename:
            glb.model.generate_latfile(latfile=filename)

    def undoModels(self):
        model_history = self.main_window.workspace.graph.model_history
        undo_history = self.main_window.workspace.graph.undo_history

        undo_history.append(glb.model)
        prev = model_history.pop(-1)
        glb.model = prev
        self.main_window.workspace.refresh()

        self.handleUndoRedoEnabling()

    def redoModels(self):
        model_history = self.main_window.workspace.graph.model_history
        undo_history = self.main_window.workspace.graph.undo_history

        model_history.append(glb.model)
        subsequent = undo_history.pop(-1)
        glb.model = subsequent
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

        # properties
        self.setWindowTitle('FLAME')
        self.setMinimumSize(1366, 768)

        # components
        main = QtWidgets.QWidget()
        self.workspace = Workspace(self)
        self.menu_bar = MenuBar(self)
        layout = QtWidgets.QHBoxLayout(main)

        layout.addWidget(self.workspace)

        self.setCentralWidget(main)
        self.setMenuBar(self.menu_bar)

        # startup
        self.menu_bar.bmstate_window.link(self.workspace.graph, self.workspace)
        self.menu_bar.phase_window.link(self.workspace.graph)
        self.menu_bar.opt_window.link(self.workspace)
        self.workspace.link(
            self.menu_bar.phase_window,
            self.menu_bar.opt_window,
            self.menu_bar.bmstate_window)

        self._createModel()

    def _createModel(self):
        vec = np.zeros(7)
        vec[6] = 1.0
        mat = np.zeros([7, 7])
        mat[0, 0] = mat[2, 2] = 1.0
        mat[1, 1] = mat[3, 3] = 1.0e-6

        source = OrderedDict([
            ('name', 'S'),
            ('type', 'source'),
            ('vector_variable', 'BC'),
            ('matrix_variable', 'S')
        ])

        conf = OrderedDict([
            ('sim_type', 'MomentMatrix'),
            ('IonEk', 1e6),
            ('IonEs', 931494320.0),
            ('IonChargeStates', np.array([0.5])),
            ('NCharge', np.array([1.0])),
            ('BC0', vec),
            ('S0', mat),
            ('elements', [source]),
            ('Eng_Data_Dir', os.getcwd() + '/FLAME/python/flame/test/data')
        ])

        glb.model = ModelFlame(machine=Machine(conf))
        # self.menu_bar.opt_window.link(self.workspace)
        self.menu_bar.bmstate_window.update()
