from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
from scipy.optimize import minimize, differential_evolution


class DoubleDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        line_edit = QtWidgets.QLineEdit(parent)
        validator = QtGui.QDoubleValidator(line_edit)
        line_edit.setValidator(validator)
        return line_edit


class ComboBox(QtWidgets.QComboBox):
    def __init__(self, element_name, row_num, table, graph):
        super().__init__()
        self.element = element_name
        self.graph = graph
        self.row_num = row_num
        self.table = table

    def _setx0(self, text):
        item = QtWidgets.QTableWidgetItem()
        item.setText(str(self.graph.model.get_element(
            name=self.element)[0]['properties'][text]))
        self.table.setItem(self.row_num, 2, item)


class OptimizationWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Optimization')
        self.setMinimumSize(1200, 500)

        self.target_params = {}

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
        self.element_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.element_table.verticalHeader().hide()
        self.element_table.cellChanged.connect(self.updateModel)

        self.select_button.setText('Select Elements')
        self.select_button.clicked.connect(lambda: self.select_window.show())

        self.target_label.setText('Target: --')

        self.param_tree.setHeaderLabels(['Parameter', 'Target Value'])
        self.param_tree.setColumnCount(2)
        self.param_tree.setItemDelegateForColumn(1, DoubleDelegate(self))
        self.param_tree.itemDoubleClicked.connect(self._handle_edits)
        self.param_tree.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.param_tree.itemChanged.connect(self._handleTargetParam)
        self.fillParamTree()
        self.param_tree.header().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.param_tree.header().setStretchLastSection(True)

        self.opt_button.setText('Optimize')
        self.opt_button.clicked.connect(self.optimize)

        ws1.layout().addWidget(self.target_label)
        ws1.layout().addWidget(self.element_table)
        ws1.layout().addWidget(self.select_button)
        ws2.layout().addWidget(self.param_tree)
        ws2.layout().addWidget(self.opt_button)

        layout.addWidget(ws1, 5)
        layout.addWidget(ws2, 3)
        self.setLayout(layout)

    def link(self, workspace):
        self.graph = workspace.graph
        self.workspace = workspace
        self.select_window.graph = workspace.graph

    def _handle_edits(self, item, col):
        if col == 0:  # odd logic, but others didn't work?
            return
        self.param_tree.editItem(item, col)

    def _costGeneric(self, x, knob, obj):
        model = self.graph.model
        for i, n in enumerate(knob.keys()):
            model.reconfigure(n, {knob[n]: x[i]})
        r, s = model.run(to_element=obj['location'])
        t = obj['target']
        dif = np.array(
            [getattr(s, n) - v for n, v in zip(t.keys(), t.values())])
        return sum(dif * dif)

    def _handleTargetParam(self, item):
        parent = item.parent()
        val = item.text(1)

        if parent.text(0) == "Reference":
            if item.text(0) == "IonEk":
                param = "ref_IonEk"
            elif item.text(0) == "Phis":
                param = "ref_phis"
        else:
            if item.text(0) == "x":
                param = "x"
            elif item.text(0) == "y":
                param = "y"
            elif item.text(0) == "z":
                param = "z"
            elif item.text(0) == "x'":
                param = "xp"
            elif item.text(0) == "y'":
                param = "yp"
            elif item.text(0) == "z'":
                param = "zp"

            if parent.text(0) == "cen":
                param += "cen"
            elif parent.text(0) == "rms":
                param += "rms"
            elif parent.text(0) == "alpha":
                param += "twiss_alpha"
            elif parent.text(0) == "beta":
                param += "twiss_beta"
            elif parent.text(0) == "gamma":
                param += "twiss_gamma"
            elif parent.text(0) == "couple":
                param = "couple_"
                if item.text(0) == "x-y":
                    param += "xy"
                elif item.text(0) == "x'-y":
                    param += "xpy"
                elif item.text(0) == "x-y'":
                    param += "xyp"
                elif item.text(0) == "x'-y'":
                    param += "xpyp"

        if item.checkState(0) == QtCore.Qt.Checked:
            try:
                self.target_params[param] = float(item.text(1))
            except BaseException:
                self.target_params[param] = None
        else:
            try:
                self.target_params.pop(param)
            except BaseException:
                return

    def optimize(self):
        self.graph.copyModelToHistory()
        knob = {}
        model = self.graph.model
        target = self.target_label.text()
        obj = {
            'location': target[target.find(' ') + 1:],
            'target': self.target_params
        }

        for i in range(self.element_table.rowCount()):
            name = self.element_table.item(i, 0).text()
            attr = self.element_table.cellWidget(i, 1).currentText()
            knob[name] = attr

        x0 = np.array([model.get_element(name=n)[0]
                      ['properties'][knob[n]] for n in knob])
        ans = minimize(
            self._costGeneric, x0, args=(
                knob, obj), method='Nelder-Mead')

        self.workspace.refresh()

    def open(self):
        self.select_window.fill(self.graph.model)
        self.show()

    def updateElementTable(self):
        self.element_table.blockSignals(True)
        while self.element_table.rowCount() > 1:
            self.element_table.removeRow(0)

        select_table = self.select_window.table
        for i in range(select_table.rowCount()):
            try:
                knob_check = select_table.cellWidget(i, 0).children()[1]
            except BaseException:
                knob_check = QtWidgets.QCheckBox()
                knob_check.setCheckState(QtCore.Qt.Unchecked)
            target_check = select_table.cellWidget(i, 1).children()[1]
            item = select_table.item(i, 2)
            if knob_check.checkState() == QtCore.Qt.Checked:
                n_item = QtWidgets.QTableWidgetItem()
                n_item.setText(item.text())

                element = self.graph.model.get_element(name=item.text())[0]
                combo = ComboBox(
                    element['properties']['name'],
                    self.element_table.rowCount(),
                    self.element_table,
                    self.graph)
                for key, val in element['properties'].items():
                    if key != 'name' and key != 'type':
                        combo.addItem(key)

                combo.currentTextChanged.connect(combo._setx0)
                self.element_table.insertRow(self.element_table.rowCount())
                self.element_table.setItem(
                    self.element_table.rowCount() - 1, 0, n_item)
                self.element_table.setCellWidget(
                    self.element_table.rowCount() - 1, 1, combo)
                combo._setx0(combo.currentText())
                if len(element['properties']) == 3:
                    combo.setEnabled(False)

            if target_check.checkState() == QtCore.Qt.Checked:
                self.target_label.setText('Target: ' + item.text())

        if select_table.rowCount() != 0:
            self.element_table.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            self.element_table.horizontalHeader().setStretchLastSection(True)
        self.select_window.close()

        self.element_table.blockSignals(False)

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
        ion_ek.setText(0, "IonEk")
        phis.setText(0, "Phis")
        cen.setText(0, "cen")
        rms.setText(0, "rms")
        tws.setText(0, "twiss")
        tws_a.setText(0, "alpha")
        tws_b.setText(0, "beta")
        tws_g.setText(0, "gamma")
        cpl.setText(0, "couple")

        for param in [ion_ek, phis]:
            param.setFlags(
                param.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
            param.setCheckState(0, QtCore.Qt.Unchecked)
            reference.addChild(param)

        actual.addChild(cen)
        actual.addChild(rms)
        actual.addChild(tws)
        actual.addChild(cpl)

        for param in [cen, rms]:
            for var in ["x", "y", "z", "x'", "y'", "z'"]:
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, var)
                item.setFlags(
                    item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
                item.setCheckState(0, QtCore.Qt.Unchecked)

                param.addChild(item)

        for radiation_type in [tws_a, tws_b, tws_g]:
            tws.addChild(radiation_type)
            for var in ["x", "y", "z"]:
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, var)
                item.setFlags(
                    item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
                item.setCheckState(0, QtCore.Qt.Unchecked)

                radiation_type.addChild(item)

        for var in ["x-y", "x'-y", "x-y'", "x'-y'"]:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, var)
            item.setFlags(
                item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
            item.setCheckState(0, QtCore.Qt.Unchecked)

            cpl.addChild(item)

        self.param_tree.addTopLevelItem(reference)
        self.param_tree.addTopLevelItem(actual)

    def updateElements(self):
        self.element_table.blockSignals(True)

        # target
        target = self.target_label.text()
        target = target[target.find(' ') + 1:]
        if target not in self.graph.model.get_all_names()[1:]:
            self.target_label.setText('Target: --')

        # element table
        for i in range(self.element_table.rowCount()):
            item = self.element_table.item(i, 0)
            try:
                element = item.text()
            except BaseException:
                continue
            if element not in self.graph.model.get_all_names()[1:]:
                self.element_table.removeRow(self.element_table.row(item))
            else:
                attr = self.element_table.cellWidget(i, 1).currentText()
                x0 = QtWidgets.QTableWidgetItem()
                x0.setText(str(self.graph.model.get_element(
                    name=element)[0]['properties'][attr]))
                self.element_table.setItem(i, 2, x0)

        # select window table
        for i in range(self.select_window.table.rowCount()):
            item = self.select_window.table.item(i, 2)
            try:
                element = item.text()
            except BaseException:
                continue
            if element not in self.graph.model.get_all_names()[1:]:
                self.select_window.table.removeRow(
                    self.select_window.table.row(item))

        self.element_table.blockSignals(False)

    def updateModel(self, row):
        model = self.graph.model
        element = self.element_table.item(row, 0).text()
        attr = self.element_table.cellWidget(row, 1).currentText()
        val = float(self.element_table.item(row, 2).text())
        model.reconfigure(element, {attr: val})
        self.workspace.refresh()


class SelectWindow(QtWidgets.QWidget):
    def __init__(self, opt_window):
        super().__init__()
        self.checked = {
            'knobs': [],
            'target': None
        }
        self.setWindowTitle('Select Elements')
        self.setMinimumSize(550, 375)
        self.opt_window = opt_window
        self.graph = None
        layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget(0, 3)
        self.button = QtWidgets.QPushButton()

        self.table.verticalHeader().hide()
        self.table.setHorizontalHeaderLabels(['Knob', 'Target', 'Name'])
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.button.setText('Confirm')
        self.button.clicked.connect(self.opt_window.updateElementTable)

        layout.addWidget(self.table)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def fill(self, model):
        model = self.graph.model
        while self.table.rowCount() > 1:
            self.table.removeRow(0)

        names = model.get_all_names()
        names = names[1:]
        for i in range(len(names)):
            name = names[i]
            element = model.get_element(name=name)[0]

            knob_widget = QtWidgets.QWidget()
            knob_check = QtWidgets.QCheckBox()
            target_widget = QtWidgets.QWidget()
            target_check = QtWidgets.QCheckBox()

            knob_layout = QtWidgets.QHBoxLayout()
            knob_layout.addWidget(knob_check)
            knob_layout.setAlignment(QtCore.Qt.AlignCenter)
            knob_layout.setContentsMargins(0, 0, 0, 0)
            knob_widget.setLayout(knob_layout)

            target_layout = QtWidgets.QHBoxLayout()
            target_layout.addWidget(target_check)
            target_layout.setAlignment(QtCore.Qt.AlignCenter)
            target_layout.setContentsMargins(0, 0, 0, 0)
            target_widget.setLayout(target_layout)

            knob_check.stateChanged.connect(self.handleTargetKnobs)
            target_check.stateChanged.connect(self.handleTargetKnobs)

            item = QtWidgets.QTableWidgetItem()
            item.setText(name)

            self.table.insertRow(self.table.rowCount())
            if len(element['properties']) > 2:
                self.table.setCellWidget(
                    self.table.rowCount() - 1, 0, knob_widget)
            self.table.setCellWidget(
                self.table.rowCount() - 1, 1, target_widget)
            self.table.setItem(self.table.rowCount() - 1, 2, item)

    def handleTargetKnobs(self):
        model = self.graph.model
        checkbox = QtWidgets.QApplication.focusWidget()
        checkbox.blockSignals(True)
        index = self.table.indexAt(checkbox.parent().pos())
        element_name = self.table.item(index.row(), 2).text()
        element_index = model.get_index_by_name(
            name=element_name)[element_name][0]
        if index.column() == 0:
            if self.checked['target']:
                target_index = self.checked['target']
                if element_index > target_index:
                    warning = QtWidgets.QMessageBox()
                    warning.setIcon(QtWidgets.QMessageBox.Critical)
                    warning.setText("Cannot use knob beyond target location.")
                    warning.setWindowTitle("ERROR")
                    warning.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    if warning.exec() == QtWidgets.QMessageBox.Ok:
                        warning.close()
                        checkbox.setCheckState(QtCore.Qt.Unchecked)
                elif element_index in self.checked['knobs']:
                    self.checked['knobs'].remove(element_index)
                else:
                    self.checked['knobs'].append(element_index)
            elif element_index in self.checked['knobs']:
                self.checked['knobs'].remove(element_index)
            else:
                self.checked['knobs'].append(element_index)
        elif index.column() == 1:
            if self.checked['target']:
                if self.checked['target'] == element_index:
                    self.checked['target'] = None
                else:
                    warning = QtWidgets.QMessageBox()
                    warning.setIcon(QtWidgets.QMessageBox.Critical)
                    warning.setText("You can only select one target location.")
                    warning.setWindowTitle("ERROR")
                    warning.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    if warning.exec() == QtWidgets.QMessageBox.Ok:
                        warning.close()
                        checkbox.setCheckState(QtCore.Qt.Unchecked)
            else:
                self.checked['target'] = element_index

            for knob_index in self.checked['knobs']:
                if element_index < knob_index:
                    warning = QtWidgets.QMessageBox()
                    warning.setIcon(QtWidgets.QMessageBox.Critical)
                    warning.setText(
                        "Target must be beyond all knobs or at then final knob.")
                    warning.setWindowTitle("ERROR")
                    warning.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    if warning.exec() == QtWidgets.QMessageBox.Ok:
                        warning.close()
                        checkbox.setCheckState(QtCore.Qt.Unchecked)
                    break
        checkbox.blockSignals(False)
