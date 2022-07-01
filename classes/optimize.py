from PyQt5 import QtWidgets, QtCore


class OptimizationWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Optimization')
        self.setMinimumSize(1100, 500)

        layout = QtWidgets.QHBoxLayout()
        ws1 = QtWidgets.QWidget()
        ws2 = QtWidgets.QWidget()
        ws1.setLayout(QtWidgets.QVBoxLayout())
        ws2.setLayout(QtWidgets.QVBoxLayout())

        self.element_table = QtWidgets.QTableWidget(0, 3)
        self.select_button = QtWidgets.QPushButton()
        self.target_label = QtWidgets.QLabel()
        self.param_tree = QtWidgets.QTreeWidget()
        self.opt_button = QtWidgets.QPushButton()
        self.select_window = SelectWindow(self)

        self.element_table.setHorizontalHeaderLabels(
            ['Name', 'Attribute', 'x0'])
        self.element_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.element_table.verticalHeader().hide()

        self.select_button.setText('Select Elements')
        self.select_button.clicked.connect(lambda: self.select_window.show())

        self.target_label.setText('Target: --')

        self.param_tree.setHeaderHidden(True)
        self.fillParamTree()

        self.opt_button.setText('Optimize')

        ws1.layout().addWidget(self.target_label)
        ws1.layout().addWidget(self.element_table)
        ws1.layout().addWidget(self.select_button)
        ws2.layout().addWidget(self.param_tree)
        ws2.layout().addWidget(self.opt_button)

        layout.addWidget(ws1, 2)
        layout.addWidget(ws2)
        self.setLayout(layout)

    def link(self, graph):
        self.graph = graph

    def open(self):
        self.select_window.fill(self.graph.model)
        
        self.show()

    def updateElementTable(self):
        while self.element_table.rowCount() > 1:
            self.element_table.removeRow(0)

        select_table = self.select_window.table
        for i in range(select_table.rowCount()):
            knob_check = select_table.cellWidget(i, 0).children()[1]
            target_check = select_table.cellWidget(i, 1).children()[1]
            item = select_table.item(i, 2)
            if knob_check.checkState() == QtCore.Qt.Checked:
                n_item = QtWidgets.QTableWidgetItem()
                n_item.setText(item.text())

                combo = QtWidgets.QComboBox()
                element = self.graph.model.get_element(name=item.text())[0]
                for key, val in element['properties'].items():
                    if key != 'name' and key != 'type':
                        combo.addItem(key)

                self.element_table.insertRow(self.element_table.rowCount())
                self.element_table.setItem(i, 0, n_item)
                self.element_table.setCellWidget(i, 1, combo)

            if target_check.checkState() == QtCore.Qt.Checked:
                self.target_label.setText('Target: ' + item.text())

        if select_table.rowCount() != 0:
            self.element_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            self.element_table.horizontalHeader().setStretchLastSection(True)
        self.select_window.close()

    def fillParamTree(self):
        # top-level
        reference = QtWidgets.QTreeWidgetItem()
        actual = QtWidgets.QTreeWidgetItem()
        reference.setText(0, "Reference")
        actual.setText(0, "Actual")

        # secondary_level
        ion_ek = QtWidgets.QTreeWidgetItem()
        phis = QtWidgets.QTreeWidgetItem()
        cen = QtWidgets.QTreeWidgetItem()
        rms = QtWidgets.QTreeWidgetItem()
        tws = QtWidgets.QTreeWidgetItem()
        tws_a = QtWidgets.QTreeWidgetItem()
        tws_b = QtWidgets.QTreeWidgetItem()
        tws_g = QtWidgets.QTreeWidgetItem()
        cpl = QtWidgets.QTreeWidgetItem()
        cen.setText(0, "cen")
        rms.setText(0, "rms")
        tws.setText(0, "twiss")
        tws_a.setText(0, "alpha")
        tws_b.setText(0, "beta")
        tws_g.setText(0, "gamma")
        cpl.setText(0, "couple")

        reference.addChild(ion_ek)
        reference.addChild(phis)

        actual.addChild(cen)
        actual.addChild(rms)
        actual.addChild(tws)
        actual.addChild(cpl)

        for param in [cen, rms]:
            for var in ["x", "y", "z", "x'", "y'", "z'"]:
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, var)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(0, QtCore.Qt.Unchecked)

                param.addChild(item)

        for radiation_type in [tws_a, tws_b, tws_g]:
            tws.addChild(radiation_type)
            for var in ["x", "y", "z"]:
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, var)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(0, QtCore.Qt.Unchecked)

                radiation_type.addChild(item)

        for var in ["x-y", "x'-y", "x-y'", "x'-y'"]:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, var)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(0, QtCore.Qt.Unchecked)

            cpl.addChild(item)

        self.param_tree.addTopLevelItem(reference)
        self.param_tree.addTopLevelItem(actual)


class SelectWindow(QtWidgets.QWidget):
    def __init__(self, opt_window):
        super().__init__()
        self.setWindowTitle('Select Elements')
        self.opt_window = opt_window
        layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget(0, 3)
        self.button = QtWidgets.QPushButton()

        self.table.verticalHeader().hide()
        self.table.setHorizontalHeaderLabels(['Knob', 'Target', 'Name'])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.button.setText('Confirm')
        self.button.clicked.connect(self.opt_window.updateElementTable)

        layout.addWidget(self.table)
        layout.addWidget(self.button)

        self.setLayout(layout)
        
    def fill(self, model):
        while self.table.rowCount() > 1:
            self.table.removeRow(0)

        names = model.get_all_names()
        names = names[1:]
        for i in range(len(names)):
            name = names[i]

            knob_widget = QtWidgets.QWidget()
            knob_check = QtWidgets.QCheckBox()
            target_widget = QtWidgets.QWidget()
            target_check = QtWidgets.QCheckBox()

            knob_layout = QtWidgets.QHBoxLayout()
            knob_layout.addWidget(knob_check)
            knob_layout.setAlignment(QtCore.Qt.AlignCenter)
            knob_layout.setContentsMargins(0,0,0,0)
            knob_widget.setLayout(knob_layout)

            target_layout = QtWidgets.QHBoxLayout()
            target_layout.addWidget(target_check)
            target_layout.setAlignment(QtCore.Qt.AlignCenter)
            target_layout.setContentsMargins(0,0,0,0)
            target_widget.setLayout(target_layout)

            item = QtWidgets.QTableWidgetItem()
            item.setText(name)

            self.table.insertRow(self.table.rowCount())
            self.table.setCellWidget(i, 0, knob_widget)
            self.table.setCellWidget(i, 1, target_widget)
            self.table.setItem(i, 2, item)