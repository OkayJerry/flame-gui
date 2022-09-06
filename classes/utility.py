import flame
import globals as glb
import numpy as np
from flame_utils import ModelFlame
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.lines import Line2D
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QKeySequence
from PyQt5.QtWidgets import *

from classes.model import Model


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        from classes.windows import (BeamStateWindow, OptimizationWindow,
                                     PhaseSpaceWindow, PreferenceWindow)

        super().__init__(parent=parent)
        self.filename = ''

        # objects
        self.bmstate_window = BeamStateWindow()
        self.opt_window = OptimizationWindow()
        self.phase_window = PhaseSpaceWindow()
        self.pref_window = PreferenceWindow()
        self.model_history = []
        self.undo_history = []
        
        # menus
        file_menu = self.addMenu('File')
        edit_menu = self.addMenu('Edit')
        view_menu = self.addMenu('View')

        # 'file' menu
        new_action = QAction('&New', self.parent())
        open_action = QAction('&Open...', self.parent())
        save_action = QAction('&Save', self.parent())
        save_as_action = QAction('&Save As...', self.parent())
        exit_action = QAction('&Exit', self.parent())
        
        new_action.setShortcut(QKeySequence.New)
        open_action.setShortcut(QKeySequence.Open)
        save_action.setShortcut(QKeySequence.Save)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        exit_action.setShortcut(QKeySequence.Quit)

        new_action.triggered.connect(self.newFile)
        open_action.triggered.connect(self.openFile)
        save_action.triggered.connect(self.saveFile)
        save_as_action.triggered.connect(self.saveFileAs)
        exit_action.triggered.connect(qApp.quit)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(exit_action)

        # 'edit' menu
        self.undo_action = QAction('&Undo', self.parent())
        self.redo_action = QAction('&Redo', self.parent())
        bmstate_action = QAction('&Beam State', self.parent())
        opt_action = QAction('&Optimization', self.parent())
        
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.redo_action.setShortcut(QKeySequence.Redo)
        
        self.undo_action.triggered.connect(self.undoModels)
        self.redo_action.triggered.connect(self.redoModels)
        bmstate_action.triggered.connect(self.bmstate_window.open)
        opt_action.triggered.connect(self.opt_window.open)
        
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addAction(bmstate_action)
        edit_menu.addAction(opt_action)

        # 'view' menu
        phase_action = QAction('&Phase Space', self.parent())
        pref_action = QAction('&Preferences', self.parent())
        
        phase_action.triggered.connect(self.phase_window.open)
        pref_action.triggered.connect(self.pref_window.open)
        
        view_menu.addAction(phase_action)
        view_menu.addAction(pref_action)

        # finalizing
        self.handleUndoRedoEnabling()
        
    def newFile(self):
        from classes.model import Model

        glb.model = Model()

        self.filename = ''
        glb.main_window.refresh(new_file=True)
        self.clearHistory()
        
        
    def openFile(self):
        while True:
            filename = QFileDialog.getOpenFileName(self.parent(), 'Open File', filter="Lattice File (*.lat)")[0]  # previously tuple)
            if filename:
                if ".lat" not in filename:
                    warning = QMessageBox()
                    warning.setIcon(QMessageBox.Critical)
                    warning.setText("Didn't select a .lat file")
                    warning.setWindowTitle("ERROR")
                    warning.setStandardButtons(QMessageBox.Ok)

                    if warning.exec() == QMessageBox.Ok:
                        warning.close()
                        continue

                self.parent().setWindowTitle("FLAME: " + filename)

                glb.model = Model(filename)
                if 'Eng_Data_Dir' not in glb.model.machine.conf().keys():
                    n_conf = glb.model.machine.conf()
                    n_conf['Eng_Data_Dir'] = flame.__file__.replace('__init__.py', 'test/data')
                    glb.model = Model(machine=flame.Machine(n_conf))

                self.filename = filename
                glb.main_window.refresh(new_file=True)
                self.clearHistory()
            break
        
    def saveFile(self):
        glb.model.generate_latfile(latfile=self.filename)

    def saveFileAs(self):
        filename = QFileDialog.getSaveFileName(self, "Save File", "model.lat", "Lattice File (*.lat)")[0]  # previously tuple
        if filename:
            glb.model.generate_latfile(latfile=filename)
            
            self.filename = filename
            self.parent().handleFileName(filename=self.filename)

            
    def copyModelToHistory(self):
        from classes.model import Model

        self.model_history.append(Model(machine=glb.model.clone_machine()))
        self.undo_history.clear()
        self.handleUndoRedoEnabling()

    def undoModels(self):
        self.undo_history.append(glb.model)
        glb.model = self.model_history.pop(-1)
        self.parent().refresh()
        self.handleUndoRedoEnabling()

    def redoModels(self):
        self.model_history.append(glb.model)
        glb.model = self.undo_history.pop(-1)
        self.parent().refresh()
        self.handleUndoRedoEnabling()
        
    def clearHistory(self):
        self.undo_history.clear()
        self.model_history.clear()
        self.handleUndoRedoEnabling()

    def handleUndoRedoEnabling(self):
        if self.model_history:
            self.undo_action.setEnabled(True)
        else:
            self.undo_action.setEnabled(False)

        if self.undo_history:
            self.redo_action.setEnabled(True)
        else:
            self.redo_action.setEnabled(False)
        
        
class NavigationToolbar(NavigationToolbar2QT):
    def __init__(self, canvas, parent):
        self.toolitems = (('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan', 'Left button pans, Right button zooms\nx/y fixes axis, CTRL fixes aspect', 'move', 'pan'),
        ('Zoom', 'Zoom to rectangle\nx/y fixes axis', 'zoom_to_rect', 'zoom'),
        ('Subplots', 'Configure plot', 'subplots', 'configure_subplots'),
        ('Color', 'Select line color', "qt4_editor_options", 'select_line_color'), # new
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
        )
        super().__init__(canvas, parent)
        self.update()

        self.line_combo = QComboBox()
        select_button = QPushButton()

        select_button.setText('Select Current Line')
        select_button.clicked.connect(self.choose_color)

        self.select_window = QWidget()
        self.select_window.setWindowTitle('Line Select')
        self.select_window.setMinimumWidth(200)
        self.select_window.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.select_window.setLayout(QVBoxLayout())
        self.select_window.layout().addWidget(self.line_combo)
        self.select_window.layout().addWidget(select_button)

    def select_line_color(self):
        canvas = self.parent().parent().parent().canvas
        
        self.line_combo.clear()
        for param in canvas.lines.keys():
            self.line_combo.addItem(param)

        if self.line_combo.count() == 0:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("No lines visible")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)

            if warning.exec() == QMessageBox.Ok:
                warning.close()
                return

        self.select_window.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.select_window.activateWindow()
        self.select_window.show()

    def choose_color(self):
        canvas = self.parent().parent().parent().canvas
        
        self.select_window.close()
        for ln in canvas.lines.values():
            if self.line_combo.currentText() == ln.get_label():
                color = QColorDialog.getColor(title=ln.get_label())
                if color.isValid():
                    canvas.custom_colors[ln.get_label()] = color.name()
                    ln.set_color(color.name())
                    canvas.refresh()
                break
            
        
class SigFigLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setValidator(QDoubleValidator())
        self.editingFinished.connect(self.convertToSciNotation)

    def convertToSciNotation(self):
        if not self.text():
            return

        self.blockSignals(True)
        num = float(self.text())
        f_string = "{:." + str(glb.num_sigfigs - 1) + "e}"
        f_string = f_string.format(num)
        self.setText(f_string)
        self.blockSignals(False)

        
class SigFigTableLineEdit(SigFigLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }")


class InvisibleTableLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }")

class ElementConfigTableLineEdit(InvisibleTableLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.editingFinished.connect(self.convertToSciNotation)
    
    def contextMenuEvent(self, event):
        table = self.parent().parent()
        menu = QMenu()

        remove_row = QAction('Remove Row', self)
        remove_row.triggered.connect(lambda: table.removeRowByCellWidget(self))
        menu.addAction(remove_row)

        menu.exec(event.globalPos())
        del menu
        
    def enableSigFig(self):
        self.setValidator(QDoubleValidator())
    
    def convertToSciNotation(self):
        if not self.text():
            return

        self.blockSignals(True)
        try:
            num = float(self.text())
            f_string = "{:." + str(glb.num_sigfigs - 1) + "e}"
            f_string = f_string.format(num)
            self.setText(f_string)
        except:
            pass
        self.blockSignals(False)


class SigFigDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        return SigFigLineEdit(parent)


class ElementTreeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        element_tree = parent.parent()
        item = element_tree.itemFromIndex(index)
        attribute = item.text(3)
        if item.parent():
            item = item.parent()
        typename = item.text(2)

        line_edit = QLineEdit(parent)
        for category in glb.data['type'][typename]['attributes'].values():
            if attribute in category.keys():
                type = category[attribute]['type']
                if type == float or attribute == 'aper':
                    line_edit = SigFigLineEdit(parent)
                    break
        line_edit.editingFinished.connect(lambda: element_tree.handlePostEdit(item))
        return line_edit

        
class ModelElementFilters(QWidget):
    def __init__(self, to_filter):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.to_filter = to_filter

        # objects
        self.type_box = QComboBox()
        self.search_bar = QLineEdit()

        self.type_box.addItems(['all', 'magnetic', 'quadrupole', 'drift', 'orbtrim', 'marker', 'sbend'])
        self.type_box.setFixedWidth(150)
        self.search_bar.setPlaceholderText('Search Model Element Name')

        self.type_box.currentTextChanged.connect(self.typeFilter)
        self.search_bar.textChanged.connect(self.nameFilter)

        # finalizing
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.type_box)
        self.layout().addWidget(self.search_bar)

    def typeFilter(self, filter_text):
        from classes.tables import Table
        
        if type(self.to_filter) is Table:
            self.to_filter.parent().refresh()
            if filter_text == 'all':
                return
            
            rows_to_remove = []
            for i in range(self.to_filter.rowCount()):
                name = self.to_filter.item(i, 2).text()  # only works for select element table for optimization
                element_type = glb.model.get_element(name=name)[0]['properties']['type']
                if filter_text == 'magnetic':
                    if element_type == 'drift':
                        print(name, element_type)
                        rows_to_remove.append(i)
                elif element_type != filter_text:
                    rows_to_remove.append(i)

            for i, row in enumerate(rows_to_remove):  # enumerate makes it so you have the number of previously removed rows (row indexes change after removal)
                self.to_filter.removeRow(row - i)
        
        else:
            for i in range(self.to_filter.topLevelItemCount()):
                item = self.to_filter.topLevelItem(i)
                if filter_text == 'all':
                    item.setHidden(False)
                    continue
                elif filter_text == 'magnetic':
                    if item.text(2) == 'drift':
                        item.setHidden(True)
                    else:
                        item.setHidden(False)
                    continue

                if item.text(2) != filter_text:
                    item.setHidden(True)
                else:
                    item.setHidden(False)

    def nameFilter(self, filter_text):
        from classes.tables import Table
        
        if type(self.to_filter) is Table:
            self.typeFilter(self.type_box.currentText())
            
            rows_to_remove = []
            for i in range(self.to_filter.rowCount()):
                name = self.to_filter.item(i, 2).text()  # only works for select element table for optimization
                if filter_text not in name:
                    rows_to_remove.append(i)
                    
            for i, row in enumerate(rows_to_remove):  # enumerate makes it so you have the number of previously removed rows (row indexes change after removal)
                self.to_filter.removeRow(row - i)
                
        else:
            self.typeFilter(self.type_box.currentText())
            for i in range(self.to_filter.topLevelItemCount()):
                item = self.to_filter.topLevelItem(i)
                if item.isHidden() == False:
                    if filter_text not in item.text(1):
                        item.setHidden(True)
    
class Line(Line2D):
    def __init__(self, xdata, ydata, param):
        super().__init__(xdata, ydata)
        self.param = param


class ElementIndexTableItemWrapper(QTableWidgetItem):
    def __init__(self, element_name, element_index):
        super().__init__()
        self.setText(element_name)
        self.element_index = element_index


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
                                   'z-momentum': glb.model.bmstate.zpcen,
                                   
                                   'x beam size [mm]': glb.model.bmstate.xrms,
                                   'x twiss beta [m/rad]': glb.model.bmstate.xtwsb,
                                   'x alpha': glb.model.bmstate.xtwsa,
                                   'x geom. emittance [mm-mrad]': glb.model.bmstate.xeps,
                                   'x norm. emittance [mm-mrad]': glb.model.bmstate.xepsn,
                                   'y beam size [mm]': glb.model.bmstate.yrms,
                                   'y twiss beta [m/rad]': glb.model.bmstate.ytwsb,
                                   'y alpha': glb.model.bmstate.ytwsa,
                                   'y geom. emittance [mm-mrad]': glb.model.bmstate.yeps,
                                   'y norm. emittance [mm-mrad]': glb.model.bmstate.yepsn,
                                   'z beam size [mm]': glb.model.bmstate.zrms,
                                   'z twiss beta [m/rad]': glb.model.bmstate.ztwsb,
                                   'z alpha': glb.model.bmstate.ztwsa,
                                   'z geom. emittance [mm-mrad]': glb.model.bmstate.zeps,
                                   'z norm. emittance [mm-mrad]': glb.model.bmstate.zepsn}
        
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

        line_edit = SigFigTableLineEdit()
        line_edit.setText(str(val))
        line_edit.convertToSciNotation()
        if attr not in self.original_vals:
            self.original_vals[attr] = str(val)
        line_edit.setToolTip('Original Value: ' + self.original_vals[attr])
        self.table.setCellWidget(self.row_num, 2, line_edit)

    def setx0Evo(self, attr=''):
        if type(self.element) == dict: # is a model element
            val = self.element['properties'][attr]
        else: # is a bmstate element
            attr = self.element
            val = self.bmstate_components[attr]
            
        low_edit = SigFigTableLineEdit()
        high_edit = SigFigTableLineEdit()

        if val > 0:
            val = np.floor(val * 10)
            low_edit.setText('0')
            high_edit.setText(str(val))
            if attr not in self.original_vals:
                self.original_vals[attr] = ['0', str(val)]
        elif val < 0:
            val = np.ceil(val * 10)
            low_edit.setText(str(val))
            high_edit.setText('0')
            if attr not in self.original_vals:
                self.original_vals[attr] = [str(val), '0']
        else:
            low_edit.setText('0')
            high_edit.setText('10')
            if attr not in self.original_vals:
                self.original_vals[attr] = ['0', '10']


        low_edit.convertToSciNotation()
        high_edit.convertToSciNotation()

        low_edit.setToolTip('Original Value: ' + self.original_vals[attr][0])
        high_edit.setToolTip('Original Value: ' + self.original_vals[attr][1])

        self.table.setCellWidget(self.row_num, 2, low_edit)
        self.table.setCellWidget(self.row_num, 3, high_edit)

class EditMatrixButton(QPushButton):
    def __init__(self, element_name, parent=None):
        from classes.windows import EditMatrixWindow
        
        super().__init__(parent=parent)
        self.window = EditMatrixWindow()
        self.setText('Edit Matrix')
        self.clicked.connect(lambda: self.window.open(element_name))

        self.setMaximumSize(100, 50)
                