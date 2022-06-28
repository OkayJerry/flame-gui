from PyQt5 import QtWidgets, QtCore, QtGui


class BeamStateWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Beam State Editor')
        layout = QtWidgets.QGridLayout()

        # universal section
        self.qa_label = QtWidgets.QLabel()
        self.energy_label = QtWidgets.QLabel()
        self.mr_label = QtWidgets.QLabel()
        self.qa_spin = QtWidgets.QSpinBox()
        self.energy_spin = QtWidgets.QSpinBox()
        self.mr_spin = QtWidgets.QSpinBox()

        self.qa_label.setText('Q / A:')
        self.energy_label.setText('Energy:')
        self.mr_label.setText('Magnetic Rigidity:')
        self.qa_spin.setRange(-2147483648, 2147483648)
        self.energy_spin.setRange(-2147483648, 2147483648)
        self.mr_spin.setRange(-2147483648, 2147483648)
        
        layout.addWidget(self.qa_label, 0, 1)
        layout.addWidget(self.energy_label, 1, 1)
        layout.addWidget(self.mr_label, 2, 1)
        layout.addWidget(self.qa_spin, 0, 2)
        layout.addWidget(self.energy_spin, 1, 2)
        layout.addWidget(self.mr_spin, 2, 2)

        # separator
        h_line = QtWidgets.QFrame()
        h_line.setFrameShape(QtWidgets.QFrame.HLine)
        h_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(h_line, 3, 0, 1, 3)

        # variable section
        self.var_box = QtWidgets.QComboBox()
        self.kwrd1_box = QtWidgets.QComboBox()
        self.kwrd2_box = QtWidgets.QComboBox()
        self.alpha_label = QtWidgets.QLabel()
        self.alpha_spin = QtWidgets.QDoubleSpinBox()
        self.kwrd1_spin = QtWidgets.QDoubleSpinBox()
        self.kwrd2_spin = QtWidgets.QDoubleSpinBox()
        self.commit_button = QtWidgets.QPushButton()

        self.alpha_label.setText('Alpha:')
        self.commit_button.setText('Apply')
        self.commit_button.clicked.connect(self.apply)

        for var in ['x', 'y', 'z']:
            self.var_box.addItem(var)
        for kwrd in ['beam size [mm]', 'twiss beta [m/rad]']:
            self.kwrd1_box.addItem(kwrd)
        for kwrd in ['geom. emittance [mm-mrad]', 'norm. emittance [mm-mrad]']:
            self.kwrd2_box.addItem(kwrd)

        self.alpha_spin.setRange(-2147483648, 2147483648)
        self.kwrd1_spin.setRange(0, 2147483648)
        self.kwrd2_spin.setRange(0, 2147483648)

        self.alpha_spin.setValue(0)

        layout.addWidget(self.var_box, 4, 0)
        layout.addWidget(self.kwrd1_box, 5, 1)
        layout.addWidget(self.kwrd1_spin, 5, 2)
        layout.addWidget(self.alpha_label, 6, 1)
        layout.addWidget(self.alpha_spin, 6, 2)
        layout.addWidget(self.kwrd2_box, 7, 1)
        layout.addWidget(self.kwrd2_spin, 7, 2)
        layout.addWidget(self.commit_button, 8, 2)

        self.setLayout(layout)

    def link(self, graph, workspace):
        self.graph = graph
        self.workspace = workspace

    def update(self, graph):
        kwrd1 = self.kwrd1_box.currentText()
        kwrd2 = self.kwrd2_box.currentText()

        if kwrd1 == 'beam size [mm]':
            kwrd1_val = self.graph.model.bmstate.xrms
        else:
            kwrd1_val = self.graph.model.bmstate.xtwsb

        if kwrd2 == 'geom. emittance [mm-mrad]':
            kwrd2_val = self.graph.model.bmstate.xeps
        else:
            kwrd2_val = self.graph.model.bmstate.xepsn

        self.alpha_spin.setValue(self.graph.model.bmstate.xtwsa)
        self.kwrd1_spin.setValue(kwrd1_val)
        self.kwrd2_spin.setValue(kwrd2_val)

    def apply(self):
        var = self.var_box.currentText()
        alpha_val = self.alpha_spin.value()
        kwrd1_val = self.kwrd1_spin.value()
        kwrd2_val = self.kwrd2_spin.value()

        if self.kwrd1_box.currentText() == 'beam size [mm]':
            if self.kwrd2_box.currentText() == 'geom. emittance [mm-mrad]':
                self.graph.model.bmstate.set_twiss(
                    var, rmssize=kwrd1_val, alpha=alpha_val, emittance=kwrd2_val)
            else:
                self.graph.model.bmstate.set_twiss(
                    var, rmssize=kwrd1_val, alpha=alpha_val, nemittance=kwrd2_val)
        else:
            if self.kwrd2_box.currentText() == 'geom. emittance [mm-mrad]':
                self.graph.model.bmstate.set_twiss(
                    var, beta=kwrd1_val, alpha=alpha_val, emittance=kwrd2_val)
            else:
                self.graph.model.bmstate.set_twiss(
                    var, beta=kwrd1_val, alpha=alpha_val, nemittance=kwrd2_val)

        self.workspace.refresh()
        self.graph.copyModelToHistory()
