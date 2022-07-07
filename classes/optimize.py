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
        self.original_vals = {}

    def _setx0Nelder(self, text):
        item = QtWidgets.QTableWidgetItem()
        val = self.graph.model.get_element(
            name=self.element)[0]['properties'][text]
        item.setText(str(val))
        if text not in self.original_vals:
            self.original_vals[text] = str(val)
        item.setToolTip('Original Value: ' + self.original_vals[text])
        self.table.setItem(self.row_num, 2, item)

    def _setx0Evo(self, text):
        low_item = QtWidgets.QTableWidgetItem()
        high_item = QtWidgets.QTableWidgetItem()
        val = self.graph.model.get_element(
            name=self.element)[0]['properties'][text]

        if val > 0:
            val = np.floor(val * 10)
            low_item.setText('0')
            high_item.setText(str(val))
            if text not in self.original_vals:
                self.original_vals[text] = ['0', str(val)]
        elif val < 0:
            val = np.ceil(val * 10)
            low_item.setText(str(val))
            high_item.setText('0')
            if text not in self.original_vals:
                self.original_vals[text] = [str(val), '0']
        else:
            low_item.setText('0')
            high_item.setText('10')
            if text not in self.original_vals:
                self.original_vals[text] = ['0', '10']

        low_item.setToolTip('Original Value: ' + self.original_vals[text][0])
        high_item.setToolTip('Original Value: ' + self.original_vals[text][1])

        self.table.setItem(self.row_num, 2, low_item)
        self.table.setItem(self.row_num, 3, high_item)


class OptimizationWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Optimization')
        self.setMinimumSize(1200, 500)

        self.target_params = {}

        layout = QtWidgets.QHBoxLayout()
        self.tabs = QtWidgets.QTabWidget()
        tab1 = QtWidgets.QWidget()
        tab2 = QtWidgets.QWidget()
        tab1.setLayout(QtWidgets.QVBoxLayout())
        tab2.setLayout(QtWidgets.QVBoxLayout())
        ws1 = QtWidgets.QWidget()
        ws2 = QtWidgets.QWidget()
        ws1.setLayout(QtWidgets.QVBoxLayout())
        ws2.setLayout(QtWidgets.QVBoxLayout())

        self.nelder_table = QtWidgets.QTableWidget(0, 3)
        self.evo_table = QtWidgets.QTableWidget(0, 4)
        self.select_button = QtWidgets.QPushButton()
        self.target_label = QtWidgets.QLabel()
        self.param_tree = QtWidgets.QTreeWidget()
        self.opt_button = QtWidgets.QPushButton()
        self.select_window = SelectWindow(self)

        self.nelder_table.setAlternatingRowColors(True)
        self.nelder_table.setHorizontalHeaderLabels(
            ['Name', 'Attribute', 'x0'])
        self.nelder_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.nelder_table.verticalHeader().hide()
        self.nelder_table.cellChanged.connect(self.updateModel)

        self.evo_table.setAlternatingRowColors(True)
        self.evo_table.setHorizontalHeaderLabels(
            ['Name', 'Attribute', 'x0-Low', 'x0-High'])
        self.evo_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.evo_table.verticalHeader().hide()
        # self.evo_table.cellChanged.connect(self.updateModel)

        self.select_button.setText('Select Elements')
        self.select_button.clicked.connect(lambda: self.select_window.show())

        self.target_label.setText('Target: --')

        self.param_tree.setAlternatingRowColors(True)
        self.param_tree.setHeaderLabels(
            ['Parameter', 'Target Value', 'Weight'])
        self.param_tree.setColumnCount(3)
        self.param_tree.setItemDelegateForColumn(1, DoubleDelegate(self))
        self.param_tree.setItemDelegateForColumn(2, DoubleDelegate(self))
        self.param_tree.itemDoubleClicked.connect(self._handle_edits)
        self.param_tree.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.param_tree.itemChanged.connect(self._handleTargetParam)
        self.fillParamTree()
        self.param_tree.header().resizeSection(1, 165)
        self.param_tree.header().resizeSection(2, 90)
        self.param_tree.header().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.opt_button.setText('Optimize')
        self.opt_button.clicked.connect(self.optimize)

        tab1.layout().addWidget(self.nelder_table)
        tab2.layout().addWidget(self.evo_table)
        self.tabs.addTab(tab1, 'Nelder-Mead')
        self.tabs.addTab(tab2, 'Differential Evolution')

        ws1.layout().addWidget(self.target_label)
        ws1.layout().addWidget(self.tabs)
        ws1.layout().addWidget(self.select_button)
        ws2.layout().addWidget(self.param_tree)
        ws2.layout().addWidget(self.opt_button)

        layout.addWidget(ws1)  # , 7)
        layout.addWidget(ws2)  # , 5)
        self.setLayout(layout)

    def link(self, workspace):
        self.graph = workspace.graph
        self.workspace = workspace
        self.select_window.graph = workspace.graph

    def _handle_edits(self, item, col):
        if col == 0:  # odd logic, but others didn't work?
            return
        self.param_tree.editItem(item, col)

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
                self.target_params[param] = [
                    float(
                        item.text(1)), float(
                        item.text(2))]
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

        global _costGeneric  # for pickle

        def _costGeneric(x, k, o):
            for i, n in enumerate(k.keys()):
                model.reconfigure(n, {k[n]: x[i]})
            r, s = model.run(to_element=o['location'])
            dif = []
            t = o['target']
            for n, v in zip(t.keys(), t.values()):
                if isinstance(v, (list, tuple)):
                    val = getattr(s, n) * v[1] - v[0]
                elif isinstance(v, (int, float)):
                    val = getattr(s, n) - v
                else:
                    val = 0.0
                dif.append(val)
            dif = np.asarray(dif)
            return sum(dif * dif)

        for i in range(self.nelder_table.rowCount()):
            name = self.nelder_table.item(i, 0).text()
            attr = self.nelder_table.cellWidget(i, 1).currentText()
            knob[name] = attr

        if self.tabs.tabText(self.tabs.currentIndex()) == 'Nelder-Mead':
            x0 = np.array([model.get_element(name=n)[0]
                           ['properties'][knob[n]] for n in knob])
            ans = minimize(
                _costGeneric, x0, args=(
                    knob, obj), method='Nelder-Mead')
        else:
            x0 = []
            for i in range(self.evo_table.rowCount()):
                low = float(self.evo_table.item(i, 2).text())
                high = float(self.evo_table.item(i, 3).text())
                x0.append((low, high))

            ans = differential_evolution(
                _costGeneric, x0, args=(
                    knob, obj), workers=-1)

        self.nelder_table.cellWidget(i, 1).original_vals = {}
        self.evo_table.cellWidget(i, 1).original_vals = {}
        self.workspace.refresh()
        self.select_window.checkPrevCheckedItems()

        popup = QtWidgets.QMessageBox()
        popup.setIcon(QtWidgets.QMessageBox.Information)
        popup.setText("Model has been optimized.")
        popup.setDetailedText(str(ans))
        popup.setWindowTitle("SUCCESS")
        popup.setStandardButtons(QtWidgets.QMessageBox.Ok)

        te = popup.findChild(QtWidgets.QTextEdit)
        te.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        width = te.document().idealWidth() + te.document().documentMargin() + \
            te.verticalScrollBar().width()
        te.parent().setFixedWidth(width)

        if popup.exec() == QtWidgets.QMessageBox.Ok:
            popup.close()

    def open(self):
        self.select_window.fill(self.graph.model)
        self.show()

    def updateElementTable(self):
        self.nelder_table.blockSignals(True)
        self.evo_table.blockSignals(True)

        while self.nelder_table.rowCount() > 0:
            self.nelder_table.removeRow(0)
        while self.evo_table.rowCount() > 0:
            self.evo_table.removeRow(0)

        select_table = self.select_window.table
        present_knobs = self.getKnobs()
        self.target_label.setText('Target: --')

        for i in range(select_table.rowCount()):
            try:
                knob_check = select_table.cellWidget(i, 0).children()[1]
            except BaseException:
                knob_check = QtWidgets.QCheckBox()
                knob_check.setCheckState(QtCore.Qt.Unchecked)
            target_check = select_table.cellWidget(i, 1).children()[1]
            item = select_table.item(i, 2)
            if knob_check.checkState() == QtCore.Qt.Checked and item.text() not in present_knobs:
                nelder_item = QtWidgets.QTableWidgetItem()
                evo_item = QtWidgets.QTableWidgetItem()
                nelder_item.setText(item.text())
                evo_item.setText(item.text())

                element = self.graph.model.get_element(name=item.text())[0]
                nelder_combo = ComboBox(
                    element['properties']['name'],
                    self.nelder_table.rowCount(),
                    self.nelder_table,
                    self.graph)
                evo_combo = ComboBox(
                    element['properties']['name'],
                    self.evo_table.rowCount(),
                    self.evo_table,
                    self.graph)
                for key, val in element['properties'].items():
                    if key != 'name' and key != 'type':
                        nelder_combo.addItem(key)
                        evo_combo.addItem(key)

                nelder_combo.currentTextChanged.connect(
                    nelder_combo._setx0Nelder)
                self.nelder_table.insertRow(self.nelder_table.rowCount())
                self.nelder_table.setItem(
                    self.nelder_table.rowCount() - 1, 0, nelder_item)
                self.nelder_table.setCellWidget(
                    self.nelder_table.rowCount() - 1, 1, nelder_combo)
                nelder_combo._setx0Nelder(nelder_combo.currentText())

                evo_combo.currentTextChanged.connect(evo_combo._setx0Evo)
                self.evo_table.insertRow(self.evo_table.rowCount())
                self.evo_table.setItem(
                    self.evo_table.rowCount() - 1, 0, evo_item)
                self.evo_table.setCellWidget(
                    self.evo_table.rowCount() - 1, 1, evo_combo)
                evo_combo._setx0Evo(evo_combo.currentText())

                if len(element['properties']) == 3:
                    nelder_combo.setEnabled(False)
                    evo_combo.setEnabled(False)

            if target_check.checkState() == QtCore.Qt.Checked:
                self.target_label.setText('Target: ' + item.text())

        if select_table.rowCount() != 0:
            self.nelder_table.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            self.nelder_table.horizontalHeader().setStretchLastSection(True)

            self.evo_table.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            self.evo_table.horizontalHeader().setStretchLastSection(True)

        self.select_window.close()
        self.nelder_table.blockSignals(False)
        self.evo_table.blockSignals(False)

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
            param.setTextAlignment(1, QtCore.Qt.AlignCenter)
            param.setTextAlignment(2, QtCore.Qt.AlignCenter)
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
                item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                item.setFlags(
                    item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
                item.setCheckState(0, QtCore.Qt.Unchecked)

                param.addChild(item)

        for radiation_type in [tws_a, tws_b, tws_g]:
            tws.addChild(radiation_type)
            for var in ["x", "y", "z"]:
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, var)
                item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                item.setFlags(
                    item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
                item.setCheckState(0, QtCore.Qt.Unchecked)

                radiation_type.addChild(item)

        for var in ["x-y", "x'-y", "x-y'", "x'-y'"]:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, var)
            item.setTextAlignment(1, QtCore.Qt.AlignCenter)
            item.setTextAlignment(2, QtCore.Qt.AlignCenter)
            item.setFlags(
                item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
            item.setCheckState(0, QtCore.Qt.Unchecked)

            cpl.addChild(item)

        self.param_tree.addTopLevelItem(reference)
        self.param_tree.addTopLevelItem(actual)

    def updateElements(self):
        self.nelder_table.blockSignals(True)
        self.evo_table.blockSignals(True)

        # target
        target = self.target_label.text()
        target = target[target.find(' ') + 1:]
        if target not in self.graph.model.get_all_names()[
                1:] or self.select_window.checked['target'][1] is None:
            self.target_label.setText('Target: --')

        # nelder-mead table
        for i in range(self.nelder_table.rowCount()):
            item = self.nelder_table.item(i, 0)
            try:
                element = item.text()
            except BaseException:
                continue
            if element not in self.graph.model.get_all_names()[1:]:
                self.nelder_table.removeRow(self.nelder_table.row(item))
            else:
                nelder_combo = self.nelder_table.cellWidget(i, 1)
                nelder_combo._setx0Nelder(nelder_combo.currentText())

        # differential evolution table
        for i in range(self.evo_table.rowCount()):
            item = self.evo_table.item(i, 0)
            try:
                element = item.text()
            except BaseException:
                continue
            if element not in self.graph.model.get_all_names()[1:]:
                self.evo_table.removeRow(self.evo_table.row(item))
            else:
                evo_combo = self.evo_table.cellWidget(i, 1)
                evo_combo._setx0Evo(evo_combo.currentText())

        # select window table
        for i in range(self.select_window.table.rowCount()):
            item = self.select_window.table.item(i, 2)
            try:
                element = item.text()
            except BaseException:
                continue
            if element not in self.graph.model.get_all_names()[1:]:
                self.select_window.table.removeRow(
                    self.select_window.table.row(item))  # remove from checked items
                try:
                    element_i = self.select_window.checked['knobs'][0].index(
                        element)
                    self.select_window.checked['knobs'][0].pop(element_i)
                    self.select_window.checked['knobs'][1].pop(element_i)
                except ValueError:
                    pass
                if element == self.select_window.checked['target'][1]:
                    self.select_window.checked['target'][0] = None
                    self.select_window.checked['target'][1] = None

        self.nelder_table.blockSignals(False)
        self.evo_table.blockSignals(False)

    def updateModel(self, row):
        model = self.graph.model
        element = self.nelder_table.item(row, 0).text()
        attr = self.nelder_table.cellWidget(row, 1).currentText()
        val = float(self.nelder_table.item(row, 2).text())

        model.reconfigure(element, {attr: val})
        self.workspace.refresh()

    def getKnobs(self):
        knobs = []
        for i in range(self.nelder_table.rowCount()):
            element = self.nelder_table.item(i, 0).text()
            knobs.append(element)
        return knobs


class SelectWindow(QtWidgets.QWidget):
    def __init__(self, opt_window):
        super().__init__()
        self.checked = {
            'knobs': [[], []],
            'target': [None, None]
        }
        self.setWindowTitle('Select Elements')
        self.setMinimumSize(550, 375)
        self.opt_window = opt_window
        self.graph = None
        layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget(0, 3)
        self.button = QtWidgets.QPushButton()

        self.table.setAlternatingRowColors(True)
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
        while self.table.rowCount() > 0:
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
            if self.checked['target'][0]:
                target_index = self.checked['target'][0]
                if element_index > target_index:
                    warning = QtWidgets.QMessageBox()
                    warning.setIcon(QtWidgets.QMessageBox.Critical)
                    warning.setText("Cannot use knob beyond target location.")
                    warning.setWindowTitle("ERROR")
                    warning.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    if warning.exec() == QtWidgets.QMessageBox.Ok:
                        warning.close()
                        checkbox.setCheckState(QtCore.Qt.Unchecked)
                elif element_index in self.checked['knobs'][0]:
                    self.checked['knobs'][0].remove(element_index)
                    self.checked['knobs'][1].remove(element_name)
                else:
                    self.checked['knobs'][0].append(element_index)
                    self.checked['knobs'][1].append(element_name)
            elif element_index in self.checked['knobs'][0]:
                self.checked['knobs'][0].remove(element_index)
                self.checked['knobs'][1].remove(element_name)
            else:
                self.checked['knobs'][0].append(element_index)
                self.checked['knobs'][1].append(element_name)
        elif index.column() == 1:
            if self.checked['target'][0]:
                if self.checked['target'][0] == element_index:
                    self.checked['target'][0] = None
                    self.checked['target'][1] = None
                else:
                    target_checkbox = self.table.cellWidget(
                        self.checked['target'][0] - 1, 1).children()[1]
                    target_checkbox.blockSignals(True)
                    target_checkbox.setCheckState(QtCore.Qt.Unchecked)
                    self.checked['target'][0] = element_index
                    self.checked['target'][1] = element_name
                    target_checkbox.blockSignals(False)
            else:
                self.checked['target'][0] = element_index
                self.checked['target'][1] = element_name

            for knob_index in self.checked['knobs'][0]:
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
                        if element_index == self.checked['target'][0]:
                            self.checked['target'][0] = None
                            self.checked['target'][1] = None
                    break
        checkbox.blockSignals(False)

    def checkPrevCheckedItems(self):
        for i in range(self.table.rowCount()):
            element = self.table.item(i, 2).text()
            if element in self.checked['knobs'][1]:
                checkbox = self.table.cellWidget(i, 0).children()[1]
                checkbox.setCheckState(QtCore.Qt.Checked)
            elif element in self.checked['target'][1]:
                checkbox = self.table.cellWidget(i, 1).children()[1]
                checkbox.setCheckState(QtCore.Qt.Checked)
