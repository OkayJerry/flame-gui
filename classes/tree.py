from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from sigfig import round

import classes.globals as glb


class DoubleDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        line_edit = QLineEdit(parent)
        if index.sibling(index.row(), 5).data(
        ) is None:  # if corresponding unit is none
            return line_edit
        validator = QtGui.QDoubleValidator(line_edit)
        line_edit.setValidator(validator)
        return line_edit


class Item(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        
        self.actual_val = None
        self.sigfig_val = None
        self.sci_val = None
        
    def setValue(self, column, value, num_sigfigs):
        self.actual_val = float(value)
        self.sigfig_val = float(round(value, sigfigs=num_sigfigs))

        if num_sigfigs == 1:
            self.sci_val = "{:.0e}".format(self.sigfig_val)
        elif num_sigfigs == 2:
            self.sci_val = "{:.1e}".format(self.sigfig_val)
        elif num_sigfigs == 3:
            self.sci_val = "{:.2e}".format(self.sigfig_val)
        elif num_sigfigs == 4:
            self.sci_val = "{:.3e}".format(self.sigfig_val)
        elif num_sigfigs == 5:
            self.sci_val = "{:.4e}".format(self.sigfig_val)
        elif num_sigfigs == 6:
            self.sci_val = "{:.5e}".format(self.sigfig_val)
        elif num_sigfigs == 7:
            self.sci_val = "{:.6e}".format(self.sigfig_val)
        elif num_sigfigs == 8:
            self.sci_val = "{:.7e}".format(self.sigfig_val)
            
        self.setText(column, self.sci_val)


class LatTree(QTreeWidget):
    def __init__(self, parent=None):
        super(QTreeWidget, self).__init__(parent)
        self.headers = ['Index', 'Name', 'Type', 'Attribute', 'Value', 'Unit']
        self.workspace = parent

        # format
        self.setAlternatingRowColors(True)
        self.setColumnCount(len(self.headers))
        self.setHeaderLabels(self.headers)

        # edit
        self.setItemDelegateForColumn(
            self.headers.index('Value'),
            DoubleDelegate(self))
        self.itemDoubleClicked.connect(self._handle_edits)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.itemChanged.connect(self.updateModel)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def link(self, graph, lat_config):
        self.graph = graph
        self.config_window = lat_config

    def populate(self):
        index_i = self.headers.index('Index')
        name_i = self.headers.index('Name')
        type_i = self.headers.index('Type')
        attr_i = self.headers.index('Attribute')
        val_i = self.headers.index('Value')
        unit_i = self.headers.index('Unit')

        elements = glb.model.get_element(
            name=glb.model.get_all_names())
        elements = elements[1:]

        for element in elements:
            item = Item()
            item.setText(index_i, str(element['index']))
            for key, val in element['properties'].items():
                val = str(val)
                if key == 'name':
                    item.setText(name_i, val)
                elif key == 'type':
                    item.setText(type_i, val)
                else:
                    if item.text(
                            attr_i) == '' and 'L' not in element['properties'].keys():
                        item.setText(attr_i, key)
                        item.setValue(val_i, val, glb.num_sigfigs)
                    elif item.text(attr_i) == '' and key == 'L':
                        item.setText(attr_i, key)
                        item.setValue(val_i, val, glb.num_sigfigs)
                    else:  # children are just attribute-value-unit tuples
                        child = Item()
                        item.addChild(child)
                        child.setText(attr_i, key)
                        child.setValue(val_i, val, glb.num_sigfigs)
                        self._setUnit(child)
                self._setUnit(item)
            self.addTopLevelItem(item)

    def _setUnit(self, item):
        attr_i = self.headers.index('Attribute')
        unit_i = self.headers.index('Unit')

        unit_info = {
            'theta_x': 'rad',
            'theta_y': 'rad',
            'tm_xkick': 'T*m',
            'tm_ykick': 'T*m',
            'xyrotate': 'deg',
            'L': 'm',
            'B': 'T',
            'dx': 'm',
            'dy': 'm',
            'pitch': 'rad',
            'yaw': 'rad',
            'roll': 'rad',
            'B2': 'T/m',
            'B3': 'T/m^2',
            'V': 'V',
            'radius': 'm',
            'phi': 'deg',
            'phi1': 'deg',
            'phi2': 'deg',
            'fringe_x': 'rad/mm',
            'fringe_y': 'rad/mm',
            'f': 'Hz',
            'Rm': 'mm'
        }

        if item.text(attr_i) in unit_info:
            item.setText(unit_i, unit_info[item.text(attr_i)])

    def updateModel(self, item):
        name_i = self.headers.index('Name')
        attr_i = self.headers.index('Attribute')
        val_i = self.headers.index('Value')
        unit_i = self.headers.index('Unit')

        selected = self.currentItem()
        attribute = selected.text(attr_i)
        unit = selected.text(unit_i)

        if not selected.parent():
            element = selected.text(name_i)
        else:
            element = selected.parent().text(name_i)

        if unit != "":
            val = float(selected.text(val_i))
        else:
            val = selected.text(val_i)

        glb.model.reconfigure(element, {attribute: val})
        self.workspace.refresh()

    def _handle_edits(self, item, col):
        index_i = self.headers.index('Index')
        name_i = self.headers.index('Name')
        type_i = self.headers.index('Type')

        if col == index_i or col == name_i or col == type_i:  # odd logic, but others didn't work?
            return
        self.editItem(item, col)
        self.graph.copyModelToHistory()

    def typeFilter(self, filter_text):
        type_i = self.headers.index('Type')

        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if filter_text == 'all':
                item.setHidden(False)
                continue
            elif filter_text == 'magnetic':
                if item.text(type_i) == 'drift':
                    item.setHidden(True)
                else:
                    item.setHidden(False)
                continue

            if item.text(type_i) != filter_text:
                item.setHidden(True)
            else:
                item.setHidden(False)

    def setConfig(self, window):
        self.config_window = window

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)

        ins_elem = QAction('Insert Element', self)
        edit_elem = QAction('Edit Selected Element', self)
        rem_elem = QAction('Remove Element', self)

        ins_elem.triggered.connect(self.insElement)
        edit_elem.triggered.connect(self.editElement)
        rem_elem.triggered.connect(self.removeElement)

        self.menu.addAction(ins_elem)
        self.menu.addAction(edit_elem)
        self.menu.addAction(rem_elem)

        self.menu.popup(QtGui.QCursor.pos())

    def insElement(self):
        if self.currentItem() is not None:
            index_i = self.headers.index('Index')
            item = self.currentItem()
            if item.parent():
                item = item.parent()
            self.config_window.insertItem(item.text(index_i))
        else:
            if self.topLevelItemCount() == 0:
                self.config_window.insertItem('1')
            else:
                i = self.topLevelItemCount() + 1
                self.config_window.insertItem(str(i))

        self.config_window.show()

    def editElement(self):
        item = self.currentItem()
        if item.parent():
            item = item.parent()
        self.config_window.editItem(item)
        self.config_window.show()

    def removeElement(self):
        index_i = self.headers.index('Index')
        item = self.currentItem()
        glb.model.pop_element(int(item.text(index_i)))
        self.workspace.refresh()


class LatTreeFilters(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        # componenets
        self.parent = parent
        self.layout = QHBoxLayout()
        self.combo_box = QComboBox()
        self.search_bar = QLineEdit()

        for word in [
            'all',
            'magnetic',
            'quadrupole',
            'drift',
            'orbtrim',
            'marker',
                'sbend']:
            self.combo_box.addItem(word)
        self.combo_box.setFixedWidth(300)

        self.search_bar.setPlaceholderText('Search Element Name')
        self.search_bar.textChanged.connect(self.nameFilter)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(self.search_bar)

        self.setLayout(self.layout)

    def link(self, lat_editor):
        self.lat_editor = lat_editor
        self.combo_box.currentTextChanged.connect(self.lat_editor.typeFilter)

    def nameFilter(self, filter_text):
        name_i = self.lat_editor.headers.index('Name')
        self.lat_editor.typeFilter(self.combo_box.currentText())

        for i in range(self.lat_editor.topLevelItemCount()):
            item = self.lat_editor.topLevelItem(i)
            if item.isHidden() == False:
                if filter_text not in item.text(name_i):
                    item.setHidden(True)


class LatElementConfig(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.edit_mode = False
        self.workspace = parent

        top_row = QWidget()
        bottom_row = QWidget()

        self.layout = QVBoxLayout()
        top_row_layout = QHBoxLayout()
        bottom_row_layout = QHBoxLayout()

        bottom_row_layout.setContentsMargins(0, 0, 0, 0)

        self.setMinimumSize(800, 600)
        self.setWindowTitle('.lat Config')

        index_label = QLabel()
        name_label = QLabel()
        type_label = QLabel()
        self.index_spin = QSpinBox()
        self.name_line = QLineEdit()
        self.type_box = QComboBox()

        index_label.setText('Index:')
        name_label.setText('Name:')
        type_label.setText('Type:')
        self.index_spin.setRange(1, 1)
        self.name_line.setPlaceholderText('Element Name')
        top_row_layout.addWidget(index_label)
        top_row_layout.addWidget(self.index_spin)
        top_row_layout.addWidget(name_label)
        top_row_layout.addWidget(self.name_line)
        top_row_layout.addWidget(type_label)

        types = ['marker', 'stripper', 'tmatrix', 'orbtrim', 'drift',
                 'solenoid', 'quadrupole', 'sextupole', 'equad', 'sbend',
                 'edipole', 'rfcavity']
        for t in types:
            self.type_box.addItem(t)
        top_row_layout.addWidget(self.type_box)
        self.type_box.currentTextChanged.connect(self._setRequiredProperties)

        self.attr_table = QTableWidget(1, 2)
        self.attr_table.setAlternatingRowColors(True)
        self.attr_table.setHorizontalHeaderLabels(
            ['Attribute', 'Value', 'Unit'])
        self.attr_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attr_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.attr_table.itemChanged.connect(self.handleBlankRow)

        self.rem_attr_button = QPushButton()
        self.commit_button = QPushButton()
        self.rem_attr_button.setText('Remove Selected Attribute')
        self.commit_button.setText('Apply')
        self.rem_attr_button.clicked.connect(self.removeAttribute)
        self.commit_button.clicked.connect(self.apply)

        bottom_row_layout.addWidget(self.rem_attr_button)
        bottom_row_layout.addWidget(self.commit_button)

        top_row.setLayout(top_row_layout)
        bottom_row.setLayout(bottom_row_layout)
        self.layout.addWidget(top_row)
        self.layout.addWidget(self.attr_table)
        self.layout.addWidget(bottom_row)
        self.setLayout(self.layout)

    def link(self, graph, lat_editor):
        self.graph = graph
        self.lat_editor = lat_editor

    def removeAttribute(self):
        indices = self.attr_table.selectionModel().selectedRows()
        for index in sorted(indices):
            self.attr_table.removeRow(index.row())

    def insertItem(self, index):
        self.index_spin.setRange(1, len(glb.model.get_all_names()))
        self.index_spin.setValue(int(index))
        self._setRequiredProperties()

    def editItem(self, top_level_item):
        self.index_spin.setRange(1, len(glb.model.get_all_names()))
        self.attr_table.blockSignals(True)
        self.edit_mode = True

        index_i = self.lat_editor.headers.index('Index')
        name_i = self.lat_editor.headers.index('Name')
        type_i = self.lat_editor.headers.index('Type')
        attr_i = self.lat_editor.headers.index('Attribute')
        val_i = self.lat_editor.headers.index('Value')

        elem_index = top_level_item.text(index_i)
        elem_name = top_level_item.text(name_i)
        elem_type = top_level_item.text(type_i)

        self.index_spin.setValue(int(elem_index))
        self.name_line.setText(elem_name)
        self.type_box.setCurrentText(elem_type)

        # disabling changes
        self.index_spin.setEnabled(False)
        self.name_line.setEnabled(False)
        self.type_box.setEnabled(False)

        # top level attribute only
        attr = QTableWidgetItem()
        val = QTableWidgetItem()

        attr_text = top_level_item.text(attr_i)
        attr.setText(attr_text)
        val.setText(str(glb.model.get_element(name=elem_name)[0]['properties'][attr_text]))
        self.attr_table.setRowCount(0)
        self.attr_table.insertRow(0)

        self.attr_table.setItem(0, 0, attr)
        self.attr_table.setItem(0, 1, val)

        # rest of the attributes
        for i in range(top_level_item.childCount()):
            self.attr_table.insertRow(self.attr_table.rowCount())
            child = top_level_item.child(i)

            attr = QTableWidgetItem()
            val = QTableWidgetItem()

            attr_text = child.text(attr_i)
            attr.setText(attr_text)
            val.setText(str(glb.model.get_element(name=elem_name)[0]['properties'][attr_text]))

            self.attr_table.setItem(i + 1, 0, attr)
            self.attr_table.setItem(i + 1, 1, val)

        # adding blank row at bottom
        self.attr_table.insertRow(self.attr_table.rowCount())

        self.attr_table.blockSignals(False)

    def _setRequiredProperties(self):
        while self.attr_table.rowCount() > 1:
            self.attr_table.removeRow(0)

        t = self.type_box.currentText()
        attributes = []
        defaults = {}
        if t == 'solenoid':
            attr1 = QTableWidgetItem()
            attr2 = QTableWidgetItem()
            attr1.setText('L')
            attr2.setText('B')
            attributes.append(attr1)
            attributes.append(attr2)
        elif t == 'quadrupole':
            attr1 = QTableWidgetItem()
            attr2 = QTableWidgetItem()
            attr1.setText('L')
            attr2.setText('B2')
            attributes.append(attr1)
            attributes.append(attr2)
        elif t == 'sextupole':
            attr1 = QTableWidgetItem()
            attr2 = QTableWidgetItem()
            attr1.setText('L')
            attr2.setText('B3')
            attributes.append(attr1)
            attributes.append(attr2)
        elif t == 'sbend':
            attr1 = QTableWidgetItem()
            attr2 = QTableWidgetItem()
            attr1.setText('L')
            attr2.setText('phi')
            attributes.append(attr1)
            attributes.append(attr2)
            defaults['phi'] = 1
        elif t == 'equad':
            attr1 = QTableWidgetItem()
            attr2 = QTableWidgetItem()
            attr3 = QTableWidgetItem()
            attr1.setText('L')
            attr2.setText('V')
            attr3.setText('radius')
            attributes.append(attr1)
            attributes.append(attr2)
            attributes.append(attr3)
            defaults['radius'] = 1
        elif t == 'edipole':
            attr1 = QTableWidgetItem()
            attr2 = QTableWidgetItem()
            attr3 = QTableWidgetItem()
            attr4 = QTableWidgetItem()
            attr1.setText('L')
            attr2.setText('phi')
            attr3.setText('ver')
            attr4.setText('spher')
            attributes.append(attr1)
            attributes.append(attr2)
            attributes.append(attr3)
            attributes.append(attr4)
            defaults['phi'] = 1
        elif t == 'rfcavity':
            attr1 = QTableWidgetItem()
            attr2 = QTableWidgetItem()
            attr3 = QTableWidgetItem()
            attr4 = QTableWidgetItem()
            attr5 = QTableWidgetItem()
            attr1.setText('L')
            attr2.setText('f')
            attr3.setText('phi')
            attr4.setText('scl_fac')
            attr5.setText('cavtype')
            attributes.append(attr1)
            attributes.append(attr2)
            attributes.append(attr3)
            attributes.append(attr4)
            attributes.append(attr5)
            defaults['L'] = 0.24
            defaults['f'] = 80.5e6
            defaults['cavtype'] = '0.041QWR'

        for i in range(len(attributes)):
            attribute = attributes[i]
            self.attr_table.insertRow(self.attr_table.rowCount())
            self.attr_table.setItem(i, 0, attribute)
            if attribute.text() in defaults.keys():
                val = QTableWidgetItem()
                val.setText(str(defaults[attribute.text()]))
                self.attr_table.setItem(i, 1, val)

    def apply(self):
        self.graph.copyModelToHistory()

        units = [
            'theta_x', 'theta_y', 'tm_xkick', 'tm_ykick', 'xyrotate',
            'L', 'B', 'dx', 'dy', 'pitch', 'yaw', 'roll', 'B2', 'B3',
            'V', 'radius', 'phi', 'phi1', 'phi2', 'fringe_x',
            'fringe_y', 'f', 'Rm', 'scl_fac'
        ]

        d = {}
        for i in range(self.attr_table.rowCount()):
            for j in range(self.attr_table.columnCount()):
                cell = self.attr_table.item(i, j)
                if cell:
                    text = cell.text()

                    if j == 0:  # index of attribute name
                        attr_name = text
                    elif j == 1:  # index of attribute value
                        if attr_name in units:
                            attr_val = float(text)
                        else:
                            attr_val = text
            d[attr_name] = attr_val

        d['name'] = self.name_line.text()
        d['type'] = self.type_box.currentText()
        i = self.index_spin.value()

        if self.edit_mode:
            glb.model.pop_element(index=i)

        glb.model.insert_element(index=i, element=d)

        self.workspace.refresh()
        self.lat_editor.setCurrentItem(None)
        self.edit_mode = False
        self.index_spin.setMaximum(self.lat_editor.topLevelItemCount() + 1)

    def clear(self):
        self.index_spin.setEnabled(True)
        self.name_line.setEnabled(True)
        self.type_box.setEnabled(True)
        self.index_spin.clear()
        self.name_line.clear()
        while self.attr_table.rowCount() > 1:
            self.attr_table.removeRow(0)

    def closeEvent(self, event):  # overriding window close
        self.clear()
        event.accept()

    def handleBlankRow(self):
        row = self.attr_table.rowCount() - 1
        col = self.attr_table.columnCount() - 1
        bottom_item_col1 = self.attr_table.item(row, col - 1)
        bottom_item_col2 = self.attr_table.item(row, col)
        if bottom_item_col1 is not None and bottom_item_col2 is not None:
            if bottom_item_col1.text() != "" and bottom_item_col2.text() != "":
                self.attr_table.insertRow(row + 1)
