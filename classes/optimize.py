from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import *
from scipy.optimize import differential_evolution, minimize

import classes.globals as glb


def _differential_evolution(func, x0, args, workers): # wrapper
    return differential_evolution(_costGeneric, x0, args=args, workers=workers)

class DoubleDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        line_edit = QLineEdit(parent)
        validator = QDoubleValidator(line_edit)
        line_edit.setValidator(validator)
        return line_edit
    

class OptComboBox(QComboBox):
    def __init__(self, element, nelder_table, row_num):
        super().__init__()
        self.element = element
        self.table = nelder_table
        self.row_num = row_num
        
        self.original_vals = {}
        self.bmstate_components = {'Q/A': glb.model.bmstate.ref_IonZ,
                                   'energy': glb.model.bmstate.ref_IonEk,
                                   'magnetic rigidity': glb.model.bmstate.ref_Brho,
                                   'x-position': glb.model.bmstate.xcen,
                                   'y-position': glb.model.bmstate.ycen,
                                   'z-position': glb.model.bmstate.zcen,
                                   'x-momentum': glb.model.bmstate.xpcen,
                                   'y-momentum': glb.model.bmstate.ypcen,
                                   'z-momentum': glb.model.bmstate.zpcen}
        
        if type(self.element) is str: # is a bmstate element
            self.setEnabled(False)
        else: # is a model element
            if len(self.element['properties']) == 3: # 'name' and 'type' with an attribute
                self.setEnabled(False)

            for key in self.element['properties'].keys():
                if key != 'name' and key != 'type':
                    self.addItem(key)
        
            

    def setx0Nelder(self, attr=''):
        if type(self.element) == dict: # is a model element
            val = self.element['properties'][attr]
        else: # is a bmstate element
            attr = self.element
            val = self.bmstate_components[attr]

        item = QTableWidgetItem()
        item.setText(str(val))
        if attr not in self.original_vals:
            self.original_vals[attr] = str(val)
        item.setToolTip('Original Value: ' + self.original_vals[attr])
        self.table.setItem(self.row_num, 2, item)

    def setx0Evo(self, attr=''):
        if type(self.element) == dict: # is a model element
            val = self.element['properties'][attr]
        else: # is a bmstate element
            attr = self.element
            val = self.bmstate_components[attr]
            
        low_item = QTableWidgetItem()
        high_item = QTableWidgetItem()
        
        if val > 0:
            val = np.floor(val * 10)
            low_item.setText('0')
            high_item.setText(str(val))
            if attr not in self.original_vals:
                self.original_vals[attr] = ['0', str(val)]
        elif val < 0:
            val = np.ceil(val * 10)
            low_item.setText(str(val))
            high_item.setText('0')
            if attr not in self.original_vals:
                self.original_vals[attr] = [str(val), '0']
        else:
            low_item.setText('0')
            high_item.setText('10')
            if attr not in self.original_vals:
                self.original_vals[attr] = ['0', '10']

        low_item.setToolTip('Original Value: ' + self.original_vals[attr][0])
        high_item.setToolTip('Original Value: ' + self.original_vals[attr][1])

        self.table.setItem(self.row_num, 2, low_item)
        self.table.setItem(self.row_num, 3, high_item)
        
        

class OptimizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Optimization')
        self.setMinimumSize(1200, 500)
        self.setLayout(QHBoxLayout())
        self.select_window = SelectWindow(self)
        self.target_params = {}

        # layout components
        ws1 = QWidget()
        ws2 = QWidget()
        nelder_tab = QWidget()
        evo_tab = QWidget()
        self.tabs = QTabWidget()
        ws1.setLayout(QVBoxLayout())
        ws2.setLayout(QVBoxLayout())
        nelder_tab.setLayout(QVBoxLayout())
        evo_tab.setLayout(QVBoxLayout())

        # workspace 1 : top-bottom
        self.target_label = QLabel('Target: --')
        self.nelder_table = QTableWidget(0, 3)
        self.evo_table = QTableWidget(0, 4)
        select_button = QPushButton('Select Elements')

        self.nelder_table.setAlternatingRowColors(True)
        self.nelder_table.setHorizontalHeaderLabels(['Name', 'Attribute', 'x0'])
        self.nelder_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.nelder_table.verticalHeader().hide()

        self.evo_table.setAlternatingRowColors(True)
        self.evo_table.setHorizontalHeaderLabels(['Name', 'Attribute', 'x0-Low', 'x0-High'])
        self.evo_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.evo_table.verticalHeader().hide()

        select_button.clicked.connect(lambda: self.select_window.show())

        nelder_tab.layout().addWidget(self.nelder_table)
        evo_tab.layout().addWidget(self.evo_table)
        self.tabs.addTab(nelder_tab, 'Nelder-Mead')
        self.tabs.addTab(evo_tab, 'Differential Evolution')
        ws1.layout().addWidget(self.target_label)
        ws1.layout().addWidget(self.tabs)
        ws1.layout().addWidget(select_button)

        # workspace 2 : top-bottom
        self.param_tree = QTreeWidget()
        opt_button = QPushButton('Optimize')

        self.param_tree.setAlternatingRowColors(True)
        self.param_tree.setItemDelegateForColumn(1, DoubleDelegate(self))
        self.param_tree.setItemDelegateForColumn(2, DoubleDelegate(self))
        self.param_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.param_tree.itemDoubleClicked.connect(self._handleEdits)
        # self.param_tree.itemChanged.connect(self._handleTargetParam)
        self.param_tree.setHeaderLabels(['Parameter', 'Target Value', 'Weight'])
        self.param_tree.setColumnCount(3)
        self.param_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.param_tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.param_tree.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.param_tree.header().setDefaultAlignment(Qt.AlignCenter)
        self.param_tree.header().setStretchLastSection(False)
        self.fillParamTree()
        
        opt_button.clicked.connect(self.optimize)

        ws2.layout().addWidget(self.param_tree)
        ws2.layout().addWidget(opt_button)

        # finalizing
        splitter = QSplitter()
        splitter.addWidget(ws1)
        splitter.addWidget(ws2)
        self.layout().addWidget(splitter)

    def clear(self):
        self.nelder_table.setRowCount(0)
        self.evo_table.setRowCount(0)

    def link(self, workspace):
        self.workspace = workspace
        self.graph = workspace.graph

    def optimize(self):
        self.fillTargetParams(self.param_tree.invisibleRootItem())
        
        if len(self.target_params) == 0:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("No checked parameters.")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)
            if warning.exec() == QMessageBox.Ok:
                warning.close()
                return
            
        for val in self.target_params.values(): 
            if val == None:
                warning = QMessageBox()
                warning.setIcon(QMessageBox.Critical)
                warning.setText("All checked parameters must have a target value and weight.")
                warning.setWindowTitle("ERROR")
                warning.setStandardButtons(QMessageBox.Ok)
                if warning.exec() == QMessageBox.Ok:
                    warning.close()
                    return
                
        knobs = {}
        bmstate = {'Q/A': 'ref_IonZ',
                   'energy': 'ref_IonEk',
                   'magnetic rigidity': 'ref_Brho',
                   'x-position': 'xcen',
                   'y-position': 'ycen',
                   'z-position': 'zcen',
                   'x-momentum': 'xpcen',
                   'y-momentum': 'ypcen',
                   'z-momentum': 'zpcen'}
        obj = {'location': self.select_window.data['target'],
               'target': self.target_params}
        
        if self.tabs.tabText(self.tabs.currentIndex()) == 'Nelder-Mead':
            current_table = self.nelder_table
        else: # tab is 'Differential Evolution'
            current_table = self.evo_table
            
        for i in range(current_table.rowCount()):
            name = current_table.item(i, 0).text()
            if name not in bmstate.keys():
                attr = current_table.cellWidget(i, 1).currentText()
            else:
                attr = bmstate[name]
            knobs[name] = attr
            
        if len(knobs) == 0 or obj['location'] == None:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("Must select knobs and a target.")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)
            if warning.exec() == QMessageBox.Ok:
                warning.close()
                return
            
        global _costGeneric  # for pickle
        def _costGeneric(x, k, o):
            
            for i, n in enumerate(k.keys()):
                if n in bmstate.keys():
                    setattr(glb.model.bmstate, k[n], x[i]) 
                else:
                    glb.model.reconfigure(n, {k[n]: x[i]})
            r, s = glb.model.run(to_element=o['location'])
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
        
        self.graph.copyModelToHistory()
        executor = ThreadPoolExecutor(max_workers=3)
        
        if current_table is self.nelder_table:
            array = []
            for n in knobs.keys():
                if n not in bmstate.keys():
                    array.append(glb.model.get_element(name=n)[0]['properties'][knobs[n]])
                else:
                    array.append(getattr(glb.model.bmstate, knobs[n]))
                    
            x0 = np.array(array)
            ans = executor.submit(minimize, fun=_costGeneric, x0=x0, args=(knobs, obj), method='Nelder-Mead')
            ans = ans.result()
        else:
            x0 = []
            for i in range(self.evo_table.rowCount()):
                low = float(self.evo_table.item(i, 2).text())
                high = float(self.evo_table.item(i, 3).text())
                x0.append((low, high))

            # currently executing on the same thread
            ans = executor.submit(_differential_evolution, func=_costGeneric, x0=x0, args=(knobs, obj), workers=-1)
            ans = ans.result()
            
        self.workspace.refresh()

        popup = QMessageBox()
        popup.setIcon(QMessageBox.Information)
        popup.setText("Model has been optimized.")
        popup.setDetailedText(str(ans))
        popup.setWindowTitle("SUCCESS")
        popup.setStandardButtons(QMessageBox.Ok)

        te = popup.findChild(QTextEdit)
        te.setLineWrapMode(QTextEdit.NoWrap)
        width = te.document().idealWidth() + te.document().documentMargin() + \
            te.verticalScrollBar().width()
        te.parent().setFixedWidth(width)

        if popup.exec() == QMessageBox.Ok:
            popup.close()

        
    def fillTables(self):
        self.select_window.close()
        self.clear()
        target_index = self.select_window.data['target']
        bmstate = self.select_window.data['knobs']['bmstate']
        element_indexes = sorted(self.select_window.data['knobs']['elements'])
        if target_index:
            target = glb.model.get_element(index=target_index)[0]['properties']['name']

        knobs = []
        for component in bmstate:
            knobs.append(component)
        for i in element_indexes:
            element = glb.model.get_element(index=i)[0] # ['properties']['name']
            knobs.append(element)

        if target_index:
            self.target_label.setText('Target: ' + target)
        else:
            self.target_label.setText('Target: --')
        
        for knob in knobs:
            final_row_index = self.nelder_table.rowCount()
            nelder_combo = OptComboBox(knob, self.nelder_table, final_row_index)
            evo_combo = OptComboBox(knob, self.evo_table, final_row_index)

            nelder_item = QTableWidgetItem()
            evo_item = QTableWidgetItem()

            if knob in bmstate:
                nelder_item.setText(knob)
                evo_item.setText(knob)
            else:
                nelder_item.setText(knob['properties']['name'])
                evo_item.setText(knob['properties']['name'])
            
            self.nelder_table.insertRow(final_row_index)
            self.nelder_table.setItem(final_row_index, 0, nelder_item)
            self.nelder_table.setCellWidget(final_row_index, 1, nelder_combo)

            self.evo_table.insertRow(final_row_index)
            self.evo_table.setItem(final_row_index, 0, evo_item)
            self.evo_table.setCellWidget(final_row_index, 1, evo_combo)

            nelder_combo.setx0Nelder(nelder_combo.currentText())
            evo_combo.setx0Evo(evo_combo.currentText())
            nelder_combo.currentTextChanged.connect(nelder_combo.setx0Nelder)
            evo_combo.currentTextChanged.connect(evo_combo.setx0Evo)

    def fillParamTree(self):
        # top-level
        reference = QTreeWidgetItem()
        actual = QTreeWidgetItem()
        reference.setText(0, "Reference")
        actual.setText(0, "Actual")

        # secondary_level
        ion_ek = QTreeWidgetItem()
        phis = QTreeWidgetItem()
        cen = QTreeWidgetItem()
        rms = QTreeWidgetItem()
        tws = QTreeWidgetItem()
        tws_a = QTreeWidgetItem()
        tws_b = QTreeWidgetItem()
        tws_g = QTreeWidgetItem()
        cpl = QTreeWidgetItem()
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
            param.setText(2, '1')
            param.setTextAlignment(1, Qt.AlignCenter)
            param.setTextAlignment(2, Qt.AlignCenter)
            param.setFlags(
                param.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            param.setCheckState(0, Qt.Unchecked)
            reference.addChild(param)

        actual.addChild(cen)
        actual.addChild(rms)
        actual.addChild(tws)
        actual.addChild(cpl)

        for param in [cen, rms]:
            for var in ["x", "y", "z", "x'", "y'", "z'"]:
                item = QTreeWidgetItem()
                item.setText(0, var)
                item.setText(2, '1')
                item.setTextAlignment(1, Qt.AlignCenter)
                item.setTextAlignment(2, Qt.AlignCenter)
                item.setFlags(
                    item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
                item.setCheckState(0, Qt.Unchecked)

                param.addChild(item)

        for radiation_type in [tws_a, tws_b, tws_g]:
            tws.addChild(radiation_type)
            for var in ["x", "y", "z"]:
                item = QTreeWidgetItem()
                item.setText(0, var)
                item.setText(2, '1')
                item.setTextAlignment(1, Qt.AlignCenter)
                item.setTextAlignment(2, Qt.AlignCenter)
                item.setFlags(
                    item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
                item.setCheckState(0, Qt.Unchecked)

                radiation_type.addChild(item)

        for var in ["x-y", "x'-y", "x-y'", "x'-y'"]:
            item = QTreeWidgetItem()
            item.setText(0, var)
            item.setText(2, '1')
            item.setTextAlignment(1, Qt.AlignCenter)
            item.setTextAlignment(2, Qt.AlignCenter)
            item.setFlags(
                item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            item.setCheckState(0, Qt.Unchecked)

            cpl.addChild(item)

        self.param_tree.addTopLevelItem(reference)
        self.param_tree.addTopLevelItem(actual)
        
    def _handleEdits(self, item, col):
        if col == 0:  # odd logic, but others didn't work?
            return
        self.param_tree.editItem(item, col)
        
    def fillTargetParams(self, item):
        if item.childCount() == 0:
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

            if item.checkState(0) == Qt.Checked:
                target_val = item.text(1)
                weight = item.text(2)
                try:
                    self.target_params[param] = [float(target_val), float(weight)]
                except ValueError:
                    self.target_params[param] = None
            elif param in self.target_params.keys():
                self.target_params.pop(param)
        else:
            for i in range(item.childCount()):
                self.fillTargetParams(item.child(i))

        
class SelectWindow(QWidget):
    def __init__(self, opt_window):
        super().__init__()
        self.setWindowTitle('Select Elements')
        self.setMinimumSize(550, 375)
        self.setLayout(QVBoxLayout())
        self.opt_window = opt_window

        self.data = {'knobs': {'bmstate': [],
                               'elements': []},
                     'target': None}
        
        # workspace : top-bottom
        self.bmstate_table = QTableWidget(0, 2)
        self.element_table = QTableWidget(0, 3)
        confirm_button = QPushButton('Confirm')

        self.bmstate_table.setAlternatingRowColors(True)
        self.bmstate_table.setHorizontalHeaderLabels(['Knob', 'Name'])
        self.bmstate_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.bmstate_table.horizontalHeader().setStretchLastSection(True)
        self.bmstate_table.verticalHeader().hide()
        self.bmstate_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.bmstate_table.setFocusPolicy(Qt.NoFocus)
        self.bmstate_table.setSelectionMode(QAbstractItemView.NoSelection)

        self.element_table.setAlternatingRowColors(True)
        self.element_table.setHorizontalHeaderLabels(['Knob', 'Target', 'Name'])
        self.element_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.element_table.horizontalHeader().setStretchLastSection(True)
        self.element_table.verticalHeader().hide()
        self.element_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.element_table.setFocusPolicy(Qt.NoFocus)
        self.element_table.setSelectionMode(QAbstractItemView.NoSelection)

        confirm_button.clicked.connect(self.opt_window.fillTables)

        # finalizing
        self.setKnobs()
        self.layout().addWidget(self.bmstate_table)
        self.layout().addWidget(self.element_table)
        self.layout().addWidget(confirm_button)

    def clear(self):
        self.bmstate_table.setRowCount(0)
        self.element_table.setRowCount(0)

    def refresh(self):
        # element removal
        rows_to_remove = []
        names = glb.model.get_all_names()[1:]
        self.data['knobs']['elements'].clear()
        for i in range(self.element_table.rowCount()):
            item = self.element_table.item(i, 2)
            name = item.text()
            if name not in names:
                rows_to_remove.append(i)
                if item.element_index == self.data['target']:
                    self.data['target'] = None
                self.adjustDataIndexesBeyond(i + 1)
        
        for row_num in sorted(rows_to_remove, reverse=True): # reverse so rows numbers don't shift backward
            self.element_table.removeRow(row_num)
            
        # element addition
        current_elements = []
        for i in range(self.element_table.rowCount()):
            item = self.element_table.item(i, 2)
            current_elements.append(item.text())

        for name in names:
            if name not in current_elements:
                element = glb.model.get_element(name=name)[0]
                element_index = element['index']
            
                knob_widget = QWidget()
                target_widget = QWidget()
                knob_checkbox = QCheckBox()
                target_checkbox = QCheckBox()
                item = ItemWrapper(name, element_index)

                knob_checkbox.stateChanged.connect(self.handleCheckBox)

                knob_widget.setLayout(QHBoxLayout())
                knob_widget.layout().setAlignment(Qt.AlignCenter)
                knob_widget.layout().setContentsMargins(0, 0, 0, 0)
                knob_widget.layout().addWidget(knob_checkbox)

                target_checkbox.stateChanged.connect(self.handleCheckBox)

                target_widget.setLayout(QHBoxLayout())
                target_widget.layout().setAlignment(Qt.AlignCenter)
                target_widget.layout().setContentsMargins(0, 0, 0, 0)
                target_widget.layout().addWidget(target_checkbox)

                self.element_table.insertRow(element_index - 1)
                if len(element['properties']) > 2: # always contains 'name' and 'type'
                    self.element_table.setCellWidget(element_index - 1, 0, knob_widget)
                self.element_table.setCellWidget(element_index - 1, 1, target_widget)
                self.element_table.setItem(element_index - 1, 2, item)

                self.adjustDataIndexesBeyond(element_index, removal=True)

                
        print(self.data)

    def adjustDataIndexesBeyond(self, index, removal=False):
        if len(glb.model.get_all_names()[1:]) == 0:
            return

        # In element removal, allows us to adjust data['target'] += 1, without
        # having to update the item.element_index beforehand. This is necessary
        # because the next item.element_index would also be equal to data['target].
        # Note: this is not the case for element addition, hence the boolean.
        for i in sorted(range(self.element_table.rowCount())[index:], reverse=removal):
            item = self.element_table.item(i, 2)
            n_index = glb.model.get_element(name=item.text())[0]['index']
            try:
                knob_checkbox = self.element_table.cellWidget(i, 0).children()[1]
            except: # for items without knobs
                knob_checkbox = QCheckBox()
                knob_checkbox.setCheckState(Qt.Unchecked)
            if item.element_index == self.data['target']:
                print(item.element_index, self.data['target'])
                self.data['target'] = n_index
            if knob_checkbox.checkState() == Qt.Checked:
                self.data['knobs']['elements'].append(n_index)
            item.element_index = n_index

    def handleCheckBox(self, state):
        checkbox = QApplication.focusWidget()
        center_qwidget = checkbox.parent()
        row_qwidget = center_qwidget.parent()
        table = row_qwidget.parent()
        
        if table is self.bmstate_table:
            name_column = 1
        else:
            name_column = 2
            
        i = table.indexAt(center_qwidget.pos())
        element_name = table.item(i.row(), name_column).text()

        if table is self.element_table:
            element_index = glb.model.get_index_by_name(name=element_name)[element_name][0]
        
        checkbox.blockSignals(True)
        if state == Qt.Unchecked:
            if i.column() == 0:
                if table is self.element_table:
                    self.data['knobs']['elements'].remove(element_index)
                else:
                    self.data['knobs']['bmstate'].remove(element_name)
            else:
                self.data['target'] = None
        else:
            if i.column() == 0:
                if table is self.element_table:
                    if self.data['target']:
                        if element_index > self.data['target']:
                            checkbox.setCheckState(Qt.Unchecked)
                            warning = QMessageBox()
                            warning.setIcon(QMessageBox.Critical)
                            warning.setText("Cannot use knob beyond target location.")
                            warning.setWindowTitle("ERROR")
                            warning.setStandardButtons(QMessageBox.Ok)
                            if warning.exec() == QMessageBox.Ok:
                                warning.close()
                                checkbox.blockSignals(False)
                                return
                    self.data['knobs']['elements'].append(element_index)
                else:
                    self.data['knobs']['bmstate'].append(element_name)
            else:
                for knob_index in self.data['knobs']['elements']:
                    if element_index < knob_index:
                        checkbox.setCheckState(Qt.Unchecked)
                        warning = QMessageBox()
                        warning.setIcon(QMessageBox.Critical)
                        warning.setText("Target must be at or beyond final knob.")
                        warning.setWindowTitle("ERROR")
                        warning.setStandardButtons(QMessageBox.Ok)
                        if warning.exec() == QMessageBox.Ok:
                            warning.close()
                            checkbox.blockSignals(False)
                            return
                if self.data['target']:
                    target_name = glb.model.get_element(index=self.data['target'])[0]['properties']['name']
                    for i in range(self.element_table.rowCount()):
                        name = self.element_table.item(i, name_column).text()
                        if name == target_name:
                            target_checkbox = self.element_table.cellWidget(i, 1).children()[1]
                            target_checkbox.blockSignals(True)
                            target_checkbox.setCheckState(Qt.Unchecked)
                            target_checkbox.blockSignals(False)
                        
                self.data['target'] = element_index
                    
        print(self.data)
        checkbox.blockSignals(False)
        

    def setKnobs(self):
        names = glb.model.get_all_names()[1:]
        bmstate_components = ['Q/A', 'energy', 'magnetic rigidity', 
                              'x-position', 'y-position', 'z-position',
                              'x-momentum', 'y-momentum', 'z-momentum']
        
        # beamstate table
        for i in range(len(bmstate_components)):
            component = bmstate_components[i]

            qwidget = QWidget()
            checkbox = QCheckBox(parent=self.bmstate_table)
            item = QTableWidgetItem()

            qwidget.setLayout(QHBoxLayout())
            qwidget.layout().setAlignment(Qt.AlignCenter)
            qwidget.layout().setContentsMargins(0, 0, 0, 0)
            qwidget.layout().addWidget(checkbox)

            checkbox.stateChanged.connect(self.handleCheckBox)

            item.setText(component)

            final_row_index = self.bmstate_table.rowCount()
            self.bmstate_table.insertRow(final_row_index)
            self.bmstate_table.setCellWidget(final_row_index, 0, qwidget)
            self.bmstate_table.setItem(final_row_index, 1, item)
            
        # element table
        for name in names:
            element = glb.model.get_element(name=name)[0]
            
            knob_widget = QWidget()
            target_widget = QWidget()
            knob_checkbox = QCheckBox()
            target_checkbox = QCheckBox()
            item = ItemWrapper(name, element['index'])

            knob_checkbox.stateChanged.connect(self.handleCheckBox)

            knob_widget.setLayout(QHBoxLayout())
            knob_widget.layout().setAlignment(Qt.AlignCenter)
            knob_widget.layout().setContentsMargins(0, 0, 0, 0)
            knob_widget.layout().addWidget(knob_checkbox)

            target_checkbox.stateChanged.connect(self.handleCheckBox)

            target_widget.setLayout(QHBoxLayout())
            target_widget.layout().setAlignment(Qt.AlignCenter)
            target_widget.layout().setContentsMargins(0, 0, 0, 0)
            target_widget.layout().addWidget(target_checkbox)

            final_row_index = self.element_table.rowCount()
            self.element_table.insertRow(final_row_index)
            if len(element['properties']) > 2: # always contains 'name' and 'type'
                self.element_table.setCellWidget(final_row_index, 0, knob_widget)
            self.element_table.setCellWidget(final_row_index, 1, target_widget)
            self.element_table.setItem(final_row_index, 2, item)
            
class ItemWrapper(QTableWidgetItem):
    def __init__(self, element_name, element_index):
        super().__init__()
        self.setText(element_name)
        self.element_index = element_index
