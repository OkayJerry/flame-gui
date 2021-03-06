import numpy as np
from PyQt5.QtCore import QLocale, Qt
from PyQt5.QtWidgets import *

import classes.globals as glb


class BeamStateSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setDecimals(10)
        self.valueChanged.connect(self.setStep)

    def setStep(self):
        step_size = self.value() * 0.1
        if step_size < 0:
            step_size *= -1
        elif step_size == 0:
            step_size = 1
        self.setSingleStep(step_size)

    def textFromValue(self, value):
        return QLocale().toString(value, 'g', QLocale.FloatingPointShortest)


class BeamStateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Initial Beam State Editor')
        layout = QGridLayout()

        # universal section
        self.qa_label = QLabel()
        self.energy_label = QLabel()
        self.mr_label = QLabel()
        self.qa_spin = BeamStateSpinBox()
        self.energy_spin = BeamStateSpinBox()
        self.mr_spin = BeamStateSpinBox()

        self.qa_label.setText('Q / A:')
        self.energy_label.setText('Energy:')
        self.mr_label.setText('Magnetic Rigidity:')
        self.qa_spin.setRange(-2147483648, 2147483648)
        self.energy_spin.setRange(-2147483648, 2147483648)
        self.mr_spin.setRange(-2147483648, 2147483648)

        self.mr_spin.valueChanged.connect(
            lambda: self._updateTwin(self.energy_spin))
        self.energy_spin.valueChanged.connect(
            lambda: self._updateTwin(self.mr_spin))

        layout.addWidget(self.qa_label, 0, 1)
        layout.addWidget(self.energy_label, 1, 1)
        layout.addWidget(self.mr_label, 2, 1)
        layout.addWidget(self.qa_spin, 0, 2)
        layout.addWidget(self.energy_spin, 1, 2)
        layout.addWidget(self.mr_spin, 2, 2)

        # separator
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(h_line, 3, 0, 1, 3)

        # variable section
        self.pos_label = QLabel()
        self.mom_label = QLabel()
        self.var_box = QComboBox()
        self.kwrd1_box = QComboBox()
        self.kwrd2_box = QComboBox()
        self.alpha_label = QLabel()
        self.pos_spin = BeamStateSpinBox()
        self.mom_spin = BeamStateSpinBox()
        self.kwrd1_spin = BeamStateSpinBox()
        self.alpha_spin = BeamStateSpinBox()
        self.kwrd2_spin = BeamStateSpinBox()
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

        self.pos_spin.setRange(-2147483648, 2147483648)
        self.mom_spin.setRange(-2147483648, 2147483648)
        self.alpha_spin.setRange(-2147483648, 2147483648)
        self.kwrd1_spin.setRange(0, 2147483648)
        self.kwrd2_spin.setRange(0, 2147483648)

        layout.addWidget(self.var_box, 4, 0)
        layout.addWidget(self.pos_label, 5, 1)
        layout.addWidget(self.pos_spin, 5, 2)
        layout.addWidget(self.mom_label, 6, 1)
        layout.addWidget(self.mom_spin, 6, 2)
        layout.addWidget(self.kwrd1_box, 7, 1)
        layout.addWidget(self.kwrd1_spin, 7, 2)
        layout.addWidget(self.alpha_label, 8, 1)
        layout.addWidget(self.alpha_spin, 8, 2)
        layout.addWidget(self.kwrd2_box, 9, 1)
        layout.addWidget(self.kwrd2_spin, 9, 2)
        layout.addWidget(self.reset_button, 10, 1)
        layout.addWidget(self.commit_button, 10, 2)

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
        energy_val = glb.model.bmstate.ref_IonEk
        mr_val = glb.model.bmstate.ref_Brho

        self.qa_spin.setValue(qa_val)
        self.energy_spin.setValue(energy_val)
        self.mr_spin.setValue(mr_val)

        # variable section
        alpha_val = glb.model.bmstate.xtwsa
        self._updateVariableDependant()
        
        kwrd1 = self.kwrd1_box.currentText()
        kwrd2 = self.kwrd2_box.currentText()
        self._updateKwrd1(kwrd1)
        self._updateKwrd2(kwrd2)

        self.alpha_spin.setValue(alpha_val)

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

        self.pos_spin.setValue(pos_val)
        self.mom_spin.setValue(mom_val)

    def _updateTwin(self, twin):
        bmstate = glb.model.bmstate.clone()
        if twin is self.energy_spin:
            self.energy_spin.blockSignals(True)
            bmstate.ref_Brho = self.mr_spin.value()
            self.energy_spin.setValue(bmstate.ref_IonEk)
            self.energy_spin.blockSignals(False)
        elif twin is self.mr_spin:
            self.mr_spin.blockSignals(True)
            bmstate.ref_IonEk = self.energy_spin.value()
            self.mr_spin.setValue(bmstate.ref_Brho)
            self.mr_spin.blockSignals(False)

    def apply(self):
        var = self.var_box.currentText()
        qa_val = self.qa_spin.value()
        energy_val = self.energy_spin.value()
        mr_val = self.mr_spin.value()
        pos_val = self.pos_spin.value()
        mom_val = self.mom_spin.value()
        alpha_val = self.alpha_spin.value()
        kwrd1_val = self.kwrd1_spin.value()
        kwrd2_val = self.kwrd2_spin.value()

        glb.model.bmstate.ref_IonZ = qa_val
        glb.model.bmstate.ref_IonEk = energy_val
        glb.model.bmstate.ref_Brho = mr_val

        glb.model.bmstate.IonZ = np.array(
            [qa_val for _ in range(len(glb.model.bmstate.IonZ))])
        glb.model.bmstate.IonEk = np.array(
            [energy_val for _ in range(len(glb.model.bmstate.IonEk))])
        glb.model.bmstate.Brho = np.array(
            [mr_val for _ in range(len(glb.model.bmstate.Brho))])
        
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
        self.kwrd1_spin.setValue(val)
            

    def _updateKwrd2(self, text):
        if text == 'geom. emittance [mm-mrad]':
            val = glb.model.bmstate.xeps
        else:
            val = glb.model.bmstate.xepsn
        self.kwrd2_spin.setValue(val)
