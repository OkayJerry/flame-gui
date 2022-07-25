import numpy as np
from PyQt5.QtCore import QLocale, Qt
from PyQt5.QtWidgets import *

import classes.globals as glb
from classes.utility import SigFigLineEdit


class BeamStateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Initial Beam State Editor')
        layout = QGridLayout()

        # universal section
        self.qa_label = QLabel()
        self.kwrdB_box = QComboBox()
        self.qa_line = SigFigLineEdit()
        self.kwrdB_line = SigFigLineEdit()

        self.qa_label.setText('Q / A:')
        
        for kwrd in ['Energy', 'Magnetic Rigidity']:
            self.kwrdB_box.addItem(kwrd)
            
        self.kwrdB_box.currentTextChanged.connect(self._updateBmstateKwrd)

        layout.addWidget(self.qa_label, 0, 1)
        layout.addWidget(self.kwrdB_box, 1, 1)
        layout.addWidget(self.qa_line, 0, 2)
        layout.addWidget(self.kwrdB_line, 1, 2)

        # separator
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(h_line, 2, 0, 1, 3)

        # variable section
        self.pos_label = QLabel()
        self.mom_label = QLabel()
        self.var_box = QComboBox()
        self.kwrd1_box = QComboBox()
        self.kwrd2_box = QComboBox()
        self.alpha_label = QLabel()
        self.pos_line = SigFigLineEdit()
        self.mom_line = SigFigLineEdit()
        self.kwrd1_line = SigFigLineEdit()
        self.alpha_line = SigFigLineEdit()
        self.kwrd2_line = SigFigLineEdit()
        self.reset_button = QPushButton('Reset')
        self.commit_button = QPushButton('Apply')

        self.pos_label.setText('Position:')
        self.mom_label.setText('Momentum:')
        self.alpha_label.setText('Alpha:')

        for var in ['x', 'y', 'z']:
            self.var_box.addItem(var)
        for kwrd in ['beam size [mm]', 'twiss beta [m/rad]']:
            self.kwrd1_box.addItem(kwrd)
        for kwrd in ['geom. emittance [mm-mrad]', 'norm. emittance [mm-mrad]']:
            self.kwrd2_box.addItem(kwrd)

        self.var_box.currentTextChanged.connect(self._updateVariableDependant)
        self.kwrd1_box.currentTextChanged.connect(self._updateKwrd1)
        self.kwrd2_box.currentTextChanged.connect(self._updateKwrd2)
        self.reset_button.clicked.connect(self.update)
        self.commit_button.clicked.connect(self.apply)

        layout.addWidget(self.var_box, 3, 0)
        layout.addWidget(self.pos_label, 4, 1)
        layout.addWidget(self.pos_line, 4, 2)
        layout.addWidget(self.mom_label, 5, 1)
        layout.addWidget(self.mom_line, 5, 2)
        layout.addWidget(self.kwrd1_box, 6, 1)
        layout.addWidget(self.kwrd1_line, 6, 2)
        layout.addWidget(self.alpha_label, 7, 1)
        layout.addWidget(self.alpha_line, 7, 2)
        layout.addWidget(self.kwrd2_box, 8, 1)
        layout.addWidget(self.kwrd2_line, 8, 2)
        layout.addWidget(self.reset_button, 9, 1)
        layout.addWidget(self.commit_button, 9, 2)

        self.setLayout(layout)
        self.update()

    def open(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.update()
        self.show()

    def link(self, graph, workspace):
        self.graph = graph
        self.workspace = workspace

    def update(self):
        # universal section
        qa_val = glb.model.bmstate.ref_IonZ

        self.qa_line.setText(str(qa_val))

        kwrdB = self.kwrdB_box.currentText()
        self._updateBmstateKwrd(kwrdB)

        # variable section
        alpha_val = glb.model.bmstate.xtwsa
        self._updateVariableDependant()
        
        kwrd1 = self.kwrd1_box.currentText()
        kwrd2 = self.kwrd2_box.currentText()
        self._updateKwrd1(kwrd1)
        self._updateKwrd2(kwrd2)

        self.alpha_line.setText(str(alpha_val))

    def _updateVariableDependant(self):
        var = self.var_box.currentText()

        if var == 'x':
            pos_val = glb.model.bmstate.xcen
            mom_val = glb.model.bmstate.xpcen
        elif var == 'y':
            pos_val = glb.model.bmstate.ycen
            mom_val = glb.model.bmstate.ypcen
        elif var == 'z':
            pos_val = glb.model.bmstate.zcen
            mom_val = glb.model.bmstate.zpcen

        self.pos_line.setText(str(pos_val))
        self.mom_line.setText(str(mom_val))

    def apply(self):
        var = self.var_box.currentText()
        qa_val = float(self.qa_line.text())
        b_val = float(self.kwrdB_line.text())
        pos_val = float(self.pos_line.text())
        mom_val = float(self.mom_line.text())
        alpha_val = float(self.alpha_line.text())
        kwrd1_val = float(self.kwrd1_line.text())
        kwrd2_val = float(self.kwrd2_line.text())

        glb.model.bmstate.ref_IonZ = qa_val
        glb.model.bmstate.IonZ = np.array([qa_val for _ in range(len(glb.model.bmstate.IonZ))])
        
        if self.kwrdB_box.currentText() == 'Energy':
            glb.model.bmstate.ref_IonEk = b_val
            glb.model.bmstate.IonEk = np.array([b_val for _ in range(len(glb.model.bmstate.IonEk))])
        else:
            glb.model.bmstate.ref_Brho = b_val
            glb.model.bmstate.Brho = np.array([b_val for _ in range(len(glb.model.bmstate.Brho))])

        if var == 'x':
            glb.model.bmstate.xcen = pos_val
            glb.model.bmstate.xpcen = mom_val
        elif var == 'y':
            glb.model.bmstate.ycen = pos_val
            glb.model.bmstate.ypcen = mom_val
        elif var == 'z':
            glb.model.bmstate.zcen = pos_val
            glb.model.bmstate.zpcen = mom_val
            
        if self.kwrd1_box.currentText() == 'beam size [mm]':
            if self.kwrd2_box.currentText() == 'geom. emittance [mm-mrad]':
                glb.model.bmstate.set_twiss(
                    var, rmssize=kwrd1_val, alpha=alpha_val, emittance=kwrd2_val)
            else:
                glb.model.bmstate.set_twiss(
                    var, rmssize=kwrd1_val, alpha=alpha_val, nemittance=kwrd2_val)
        else:
            if self.kwrd2_box.currentText() == 'geom. emittance [mm-mrad]':
                glb.model.bmstate.set_twiss(
                    var, beta=kwrd1_val, alpha=alpha_val, emittance=kwrd2_val)
            else:
                glb.model.bmstate.set_twiss(
                    var, beta=kwrd1_val, alpha=alpha_val, nemittance=kwrd2_val)

        self.workspace.refresh()
        self.graph.copyModelToHistory()
        
    def _updateKwrd1(self, text):
        if text == 'beam size [mm]':
            val = glb.model.bmstate.xrms
        else:
            val = glb.model.bmstate.xtwsb
        self.kwrd1_line.setText(str(val))
            

    def _updateKwrd2(self, text):
        if text == 'geom. emittance [mm-mrad]':
            val = glb.model.bmstate.xeps
        else:
            val = glb.model.bmstate.xepsn
        self.kwrd2_line.setText(str(val))

    def _updateBmstateKwrd(self, text):
        if text == 'Energy':
            val = glb.model.bmstate.ref_IonEk
        else:
            val = glb.model.bmstate.ref_Brho
        self.kwrdB_line.setText(str(val))
