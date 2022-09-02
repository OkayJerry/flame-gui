from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import globals as glb
import numpy as np


class Table(QTableWidget):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns, parent=parent)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setStyleSheet('''
    QTableWidget::item::selected, QTableWidget QLineEdit { 
        background-color: rgba(0, 0, 0, 0);
    }
''')
        self.verticalHeader().hide()


class NelderEvoTables(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        nelder_tab = QWidget()
        evo_tab = QWidget()
        nelder_tab.setLayout(QHBoxLayout())
        evo_tab.setLayout(QHBoxLayout())

        self.nelder = Table(0, 3)
        self.evo = Table(0, 4)
        self.nelder.setHorizontalHeaderLabels(['Name', 'Attribute', 'x0'])
        self.evo.setHorizontalHeaderLabels(['Name', 'Attribute', 'x0-Low', 'x0-High'])

        nelder_tab.layout().addWidget(self.nelder)
        evo_tab.layout().addWidget(self.evo)
        self.addTab(nelder_tab, 'Nelder-Mead')
        self.addTab(evo_tab, 'Differential Evolution')

    def clear(self):
        self.nelder.setRowCount(0)
        self.evo.setRowCount(0)

    def fill(self):
        from classes.utility import OptComboBox

        select_window = self.parent().parent().parent().select_window
        self.clear()
        bmstate = select_window.data['knobs']['bmstate']
        element_indexes = sorted(select_window.data['knobs']['elements'])

        knobs = []
        for component in bmstate:
            knobs.append(component)
        for i in element_indexes:
            element = glb.model.get_element(index=i)[0] # ['properties']['name']
            knobs.append(element)

        for knob in knobs:
            final_row_index = self.nelder.rowCount()
            nelder_combo = OptComboBox(knob, self.nelder, final_row_index)
            evo_combo = OptComboBox(knob, self.evo, final_row_index)

            nelder_item = QTableWidgetItem()
            evo_item = QTableWidgetItem()

            if knob in bmstate:
                nelder_item.setText(knob)
                evo_item.setText(knob)
            else:
                nelder_item.setText(knob['properties']['name'])
                evo_item.setText(knob['properties']['name'])
            
            self.nelder.insertRow(final_row_index)
            self.nelder.setItem(final_row_index, 0, nelder_item)
            self.nelder.setCellWidget(final_row_index, 1, nelder_combo)

            self.evo.insertRow(final_row_index)
            self.evo.setItem(final_row_index, 0, evo_item)
            self.evo.setCellWidget(final_row_index, 1, evo_combo)

            nelder_combo.setx0Nelder(nelder_combo.currentText())
            evo_combo.setx0Evo(evo_combo.currentText())
            nelder_combo.currentTextChanged.connect(nelder_combo.setx0Nelder)
            evo_combo.currentTextChanged.connect(evo_combo.setx0Evo)

            
class ModelElementAttributeTable(Table):
    def __init__(self, parent=None):
        super().__init__(0, 2, parent=parent)
        self.setHorizontalHeaderLabels(['Attribute', 'Value', 'Unit'])
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.default()

        self.cellChanged.connect(self.handleBlankRow)

    def default(self):
        from classes.utility import ElementConfigTableLineEdit, ElementConfigTableLineEdit
        self.blockSignals(True)

        self.setRowCount(1)
        attribute = ElementConfigTableLineEdit()
        value = ElementConfigTableLineEdit()
        attribute.editingFinished.connect(self.handleBlankRow)
        value.editingFinished.connect(self.handleBlankRow)
        self.setCellWidget(0, 0, attribute)
        self.setCellWidget(0, 1, value)
        
        self.blockSignals(False)
        
    def handleSigFigItemEnabling(self):
        config_window = self.parent()
        for i in range(self.rowCount()):
            attribute = self.cellWidget(i, 0)
            value = self.cellWidget(i, 1)
            typename = config_window.type_box.currentText()
            attribute_data = glb.data['type'][typename]['attributes']
            attribute_data = attribute_data['required'] | attribute_data['optional']
            if attribute.text() in attribute_data.keys() and attribute_data[attribute.text()]['type'] == float:
                value.enableSigFig()
                

    def setAttributes(self, element):
        self.blockSignals(True)

        for k,v in element['properties'].items():
            if k != 'name' and k != 'type':
                # getting items because handleBlankRow()
                attribute = self.cellWidget(self.rowCount() - 1, 0) 
                value = self.cellWidget(self.rowCount() - 1, 1)
                attribute.setText(str(k))

                typename = element['properties']['type']
                if k in glb.data['type'][typename]['attributes']['required']:
                    attribute.setEnabled(False)

                value.setText(str(v))
                value.convertToSciNotation()
                self.newRow()

        self.handleSigFigItemEnabling()
        self.blockSignals(False)

    def setRequiredAttributes(self, typename):
        self.blockSignals(True)
        self.default()

        required = glb.data['type'][typename]['attributes']['required']
        for k,v in required.items():
            # getting items because handleBlankRow()
            attribute = self.cellWidget(self.rowCount() - 1, 0) 
            value = self.cellWidget(self.rowCount() - 1, 1)
            attribute.setText(str(k))
            attribute.setEnabled(False)
            
            if 'default' in v.keys():
                value.setText(str(v['default']))
                value.convertToSciNotation()
                
            self.newRow()

        self.handleSigFigItemEnabling()
        self.blockSignals(False)

    def handleBlankRow(self):
        bottom_attribute = self.cellWidget(self.rowCount() - 1, 0)
        bottom_value = self.cellWidget(self.rowCount() - 1, 1)
        
        if bottom_attribute.text() and bottom_value.text():
            self.newRow()

    def newRow(self):
        from classes.utility import ElementConfigTableLineEdit
        
        self.insertRow(self.rowCount())

        attribute = ElementConfigTableLineEdit()
        value = ElementConfigTableLineEdit()

        attribute.editingFinished.connect(self.handleBlankRow)
        value.editingFinished.connect(self.handleBlankRow)
        
        self.setCellWidget(self.rowCount() - 1, 0, attribute)
        self.setCellWidget(self.rowCount() - 1, 1, value)

    def removeRowByCellWidget(self, cell_widget):         
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if cell_widget == self.cellWidget(i, j):
                    if i == self.rowCount() - 1:
                        # clear row
                        self.cellWidget(i, 0).setText('')
                        self.cellWidget(i, 1).setText('')
                    elif self.cellWidget(i, 0).isEnabled():
                        self.removeRow(i)
                    else:
                        warning = QMessageBox()
                        warning.setIcon(QMessageBox.Critical)
                        warning.setText("Attribute is required for type.")
                        warning.setWindowTitle("ERROR")
                        warning.setStandardButtons(QMessageBox.Ok)
                        if warning.exec() == QMessageBox.Ok:
                            warning.close()
                        
                    return

class MatrixTable(Table):
    def __init__(self, rows, columns, parent=None):
        from classes.utility import SigFigTableLineEdit

        super().__init__(rows, columns, parent=parent)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().show()
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setCellWidget(i, j, SigFigTableLineEdit())

    def fill(self, element_name):
        matrix = glb.model.get_element(name=element_name)[0]['properties']['matrix']
        
        row, column = 0, 0
        for i in range(len(matrix)):
            if i % self.columnCount() == 0 and i != 0:
                row += 1
                column = 0
            cell = self.cellWidget(row, column)
            cell.setText(str(matrix[i]))
            cell.convertToSciNotation()
            column += 1
        
    def getMatrix(self):
        matrix = []
        for i in range(self.rowCount()):
            matrix.append([])
            for j in range(self.columnCount()):
                matrix[i].append(np.float64(self.cellWidget(i, j).text()))
        return np.array(matrix).flatten()