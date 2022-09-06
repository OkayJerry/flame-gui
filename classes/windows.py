from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser

import globals as glb
import matplotlib as mpl
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from scipy.optimize import differential_evolution, minimize


class MainWindow(QMainWindow):
    def __init__(self):
        from classes.canvases import MainCanvas
        from classes.trees import ModelElementView, ParameterSelect
        from classes.utility import (MenuBar, ModelElementFilters,
                                     NavigationToolbar)
        
        self.active_param_cnt = 0
        
        super().__init__()
        self.setWindowTitle('FLAME-GUI')
        self.setWindowIcon(QIcon('images/frib.jpg'))
        self.setMenuBar(MenuBar(self))
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QHBoxLayout())

        # dividing workspace into parts
        ws_left = QWidget()
        ws_right = QWidget()
        ws_left.setLayout(QVBoxLayout())
        ws_right.setLayout(QVBoxLayout())

        # ws_left
        self.canvas = MainCanvas()
        self.nav_toolbar = NavigationToolbar(self.canvas, ws_left)
        self.element_view = ModelElementView(self)
        self.filters = ModelElementFilters(self.element_view)
        
        ws_left.layout().addWidget(self.nav_toolbar)
        ws_left.layout().addWidget(self.canvas, 3)
        ws_left.layout().addWidget(self.filters)
        ws_left.layout().addWidget(self.element_view, 2)
        
        # ws_right
        self.param_select = ParameterSelect()
        
        self.param_select.itemChanged.connect(self.paramSelectToCanvas)

        ws_right.layout().addWidget(self.param_select)
        
        # making adjustable
        splitter = QSplitter()
        splitter.addWidget(ws_left)
        splitter.addWidget(ws_right)
        
        # finalizing
        self.centralWidget().layout().addWidget(splitter)

    def refresh(self, new_file=False):
        if new_file:
            self.handleFileName(filename=self.menuBar().filename)

        self.element_view.refresh(new_file=new_file)
        self.canvas.refresh()
        self.menuBar().bmstate_window.refresh()
        self.menuBar().phase_window.refresh()
        self.menuBar().opt_window.refresh(new_file=new_file)
        
    def handleFileName(self, filename=''):
        if filename:
            self.setWindowTitle("FLAME-GUI: " + filename)
        else:
            self.setWindowTitle("FLAME-GUI")
        
    def paramSelectToCanvas(self, item, col):
        param = self.param_select.convertItemIntoParam(item)
        if self.active_param_cnt <= 4 and item.checkState(col) == Qt.Unchecked:
            self.canvas.removeParameter(param)
            self.active_param_cnt -= 1
        elif self.active_param_cnt < 4:
            self.canvas.plotParameter(param)
            self.active_param_cnt += 1
        else:
            self.param_select.blockSignals(True)
            item.setCheckState(0, Qt.Unchecked)
            self.param_select.blockSignals(False)

            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("You can only select four parameters at a time!")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)

            if warning.exec() == QMessageBox.Ok:
                warning.close()
        
        
class BeamStateWindow(QWidget):
    def __init__(self, main_window, parent=None):
        from classes.utility import SigFigLineEdit
        
        super().__init__(parent=parent)
        self.setWindowTitle('Initial Beam State Editor')
        self.setLayout(QGridLayout())
        self.main_window = main_window

        # beam centroid/envelope
        qa_label = QLabel('Q / A:')
        self.qa_line = SigFigLineEdit()
        self.kwrdB_box = QComboBox()
        self.kwrdB_line = SigFigLineEdit()

        self.kwrdB_box.addItems(['Energy', 'Magnetic Rigidity'])
        self.kwrdB_box.currentTextChanged.connect(self.updateBmstateKwrd)

        self.layout().addWidget(qa_label, 0, 1)
        self.layout().addWidget(self.kwrdB_box, 1, 1)
        self.layout().addWidget(self.qa_line, 0, 2)
        self.layout().addWidget(self.kwrdB_line, 1, 2)
        
        # separator
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(h_line, 2, 0, 1, 3)
        
        # variable/twiss section
        self.var_box = QComboBox()
        pos_label = QLabel('Position:')
        mom_label = QLabel('Momentum:')
        self.kwrd1_box = QComboBox()
        self.kwrd2_box = QComboBox()
        alpha_label = QLabel('Alpha:')
        self.pos_line = SigFigLineEdit()
        self.mom_line = SigFigLineEdit()
        self.kwrd1_line = SigFigLineEdit()
        self.alpha_line = SigFigLineEdit()
        self.kwrd2_line = SigFigLineEdit()
        self.reset_button = QPushButton('Reset')
        self.apply_button = QPushButton('Apply')
        
        self.var_box.addItems(['x', 'y', 'z'])
        self.kwrd1_box.addItems(['beam size [mm]', 'twiss beta [m/rad]'])
        self.kwrd2_box.addItems(['geom. emittance [mm-mrad]', 'norm. emittance [mm-mrad]'])
        
        self.var_box.currentTextChanged.connect(self.updateVariableDependant)
        self.kwrd1_box.currentTextChanged.connect(self.updateKwrd1)
        self.kwrd2_box.currentTextChanged.connect(self.updateKwrd2)
        self.reset_button.clicked.connect(self.refresh)
        self.apply_button.clicked.connect(self.apply)
        
        self.layout().addWidget(self.var_box, 3, 0)
        self.layout().addWidget(pos_label, 4, 1)
        self.layout().addWidget(self.pos_line, 4, 2)
        self.layout().addWidget(mom_label, 5, 1)
        self.layout().addWidget(self.mom_line, 5, 2)
        self.layout().addWidget(self.kwrd1_box, 6, 1)
        self.layout().addWidget(self.kwrd1_line, 6, 2)
        self.layout().addWidget(alpha_label, 7, 1)
        self.layout().addWidget(self.alpha_line, 7, 2)
        self.layout().addWidget(self.kwrd2_box, 8, 1)
        self.layout().addWidget(self.kwrd2_line, 8, 2)
        self.layout().addWidget(self.reset_button, 9, 1)
        self.layout().addWidget(self.apply_button, 9, 2)

        self.refresh()

    def open(self):
        self.refresh()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.show()
        
    def refresh(self):
        # universal section
        qa_val = glb.model.bmstate.ref_IonZ

        self.qa_line.setText(str(qa_val))
        self.qa_line.convertToSciNotation()

        kwrdB = self.kwrdB_box.currentText()
        self.updateBmstateKwrd(kwrdB)

        # variable section
        alpha_val = glb.model.bmstate.xtwsa
        self.updateVariableDependant()
        
        kwrd1 = self.kwrd1_box.currentText()
        kwrd2 = self.kwrd2_box.currentText()
        self.updateKwrd1(kwrd1)
        self.updateKwrd2(kwrd2)

        self.alpha_line.setText(str(alpha_val))
        self.alpha_line.convertToSciNotation()
        
    def apply(self):
        self.main_window.menuBar().copyModelToHistory()

        var = self.var_box.currentText()
        qa_val = self.qa_line.text()
        b_val = self.kwrdB_line.text()
        pos_val = self.pos_line.text()
        mom_val = self.mom_line.text()
        alpha_val = self.alpha_line.text()
        kwrd1_val = self.kwrd1_line.text()
        kwrd2_val = self.kwrd2_line.text()

        values = [qa_val, b_val, pos_val, mom_val, alpha_val, kwrd1_val, kwrd2_val]
        for val in values:
            try:
                val = float(val)
            except:
                warning = QMessageBox()
                warning.setIcon(QMessageBox.Critical)
                warning.setText("Not all values formatted correctly.")
                warning.setWindowTitle("ERROR")
                warning.setStandardButtons(QMessageBox.Ok)
                if warning.exec() == QMessageBox.Ok:
                    warning.close()
                    return

        qa_val = float(qa_val)
        b_val = float(b_val)
        pos_val = float(pos_val)
        mom_val = float(mom_val)
        alpha_val = float(alpha_val)
        kwrd1_val = float(kwrd1_val)
        kwrd2_val = float(kwrd2_val)
        
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

        
    def updateVariableDependant(self):
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

        self.pos_line.convertToSciNotation()
        self.mom_line.convertToSciNotation()
        
    def updateKwrd1(self, text):
        if text == 'beam size [mm]':
            val = glb.model.bmstate.xrms
        else:
            val = glb.model.bmstate.xtwsb
        self.kwrd1_line.setText(str(val))
        self.kwrd1_line.convertToSciNotation()      

    def updateKwrd2(self, text):
        if text == 'geom. emittance [mm-mrad]':
            val = glb.model.bmstate.xeps
        else:
            val = glb.model.bmstate.xepsn
        self.kwrd2_line.setText(str(val))
        self.kwrd2_line.convertToSciNotation()

    def updateBmstateKwrd(self, text):
        if text == 'Energy':
            val = glb.model.bmstate.ref_IonEk
        else:
            val = glb.model.bmstate.ref_Brho
        self.kwrdB_line.setText(str(val))
        self.kwrdB_line.convertToSciNotation()

        

class PhaseSpaceWindow(QWidget):
    def __init__(self, parent=None):
        from classes.canvases import PhaseSpaceCanvas
        from classes.tables import Table
        
        super().__init__(parent=parent)
        self.setWindowTitle('Phase Space Plot')
        self.setLayout(QVBoxLayout())
        filter_widget = QWidget()
        filter_widget.setLayout(QHBoxLayout())

        # objects
        self.element_box = QComboBox()
        self.type_box = QComboBox()
        self.canvas = PhaseSpaceCanvas()
        self.table = Table(5, 3)

        self.type_box.addItems(['all', 'magnetic', 'quadrupole', 'drift', 'orbtrim', 'marker', 'sbend'])
        self.table.setHorizontalHeaderLabels(['', 'x', 'y'])
        labels = ['Centroid Position [mm]', 'Centroid Momentum [mrad]', 'Twiss Alpha', 'Twiss Beta [m/rad]', 'Geom. Emittance [mm-mrad]']
        for i in range(len(labels)):
            label = labels[i]
            item = QTableWidgetItem()
            item.setText(label)
            self.table.setItem(i, 0, item)

        self.type_box.currentTextChanged.connect(self.filterElementBox)
        self.element_box.currentTextChanged.connect(self.plotCurrentElement)

        # finalizing
        filter_widget.layout().addWidget(self.element_box)
        filter_widget.layout().addWidget(self.type_box)
        self.layout().addWidget(filter_widget)
        self.layout().addWidget(self.canvas, 3)
        self.layout().addWidget(self.table, 2)

    def open(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.show()
        
    def refresh(self, new_file=False):
        element = self.element_box.currentText()
        self.setElementBox()
        self.filterElementBox()
        if len(glb.model.get_all_names()[1:]) != 0:
            self.element_box.setCurrentText(element)
            self.plotCurrentElement()
        else:
            self.canvas.clearSubplots()
            self.canvas.figure.tight_layout()
            self.canvas.draw_idle()
            for i in range(self.table.rowCount()):
                for j in range(2):
                    item = self.table.item(i, j + 1)
                    item.setText('')

    def plotCurrentElement(self):
        self.canvas.clearSubplots()

        try:
            x_res, y_res = self.canvas.plotElement(self.element_box.currentText())
        except BaseException: # current element was removed
            self.element_box.removeItem(self.element_box.findText(self.element_box.currentText()))
            names = glb.model.get_all_names()
            self.element_box.setCurrentText(names[1])  # skip header (0th) element
            x_res, y_res = self.canvas.plotElement(self.element_box.currentText())

        for i in range(self.table.rowCount()):
            x_num = x_res[i]
            y_num = y_res[i]
            
            f_string = "{:." + str(glb.num_sigfigs - 1) + "e}"
            x_num = f_string.format(x_num)
            y_num = f_string.format(y_num)
    
            x_item = QTableWidgetItem()
            y_item = QTableWidgetItem()
            x_item.setText(x_num)
            y_item.setText(y_num)

            self.table.setItem(i, 1, x_item)
            self.table.setItem(i, 2, y_item)
    
    def setElementBox(self):
        self.element_box.blockSignals(True)
        self.element_box.clear()
        names = glb.model.get_all_names()[1:]
        self.element_box.addItems(names)
        self.element_box.blockSignals(False)
        
    def filterElementBox(self):
        self.element_box.blockSignals(True)

        self.element_box.clear()
        elements = glb.model.get_element(name=glb.model.get_all_names())[1:]
        for element in elements:
            n = element['properties']['name']
            t = element['properties']['type']
            if t == self.type_box.currentText() or self.type_box.currentText() == 'all':
                self.element_box.addItem(n)
            elif self.type_box.currentText() == 'magnetic':
                if t != 'drift':
                    self.element_box.addItem(n)
        if len(elements) != 0:
            self.plotCurrentElement()

        self.element_box.blockSignals(False)
        
        
class OptimizationWindow(QWidget):
    def __init__(self, main_window, parent=None):
        from classes.tables import NelderEvoTables
        from classes.trees import TargetSelect

        super().__init__(parent=parent)
        self.setWindowTitle('Optimization')
        self.setLayout(QHBoxLayout())
        
        self.main_window = main_window
        self.select_window = OptimizationSelectElementWindow(self)
        
        # dividing workspace into parts
        ws_left = QWidget()
        ws_right = QWidget()
        nelder_tab = QWidget()
        evo_tab = QWidget()
        ws_left.setLayout(QVBoxLayout())
        ws_right.setLayout(QVBoxLayout())
        nelder_tab.setLayout(QHBoxLayout())
        evo_tab.setLayout(QHBoxLayout())
        
        # ws_left
        self.target_label = QLabel('Target: --')
        self.tables = NelderEvoTables()
        select_button = QPushButton('Select Elements')

        select_button.clicked.connect(self.select_window.open)

        ws_left.layout().addWidget(self.target_label)
        ws_left.layout().addWidget(self.tables)
        ws_left.layout().addWidget(select_button)
        
        # ws_right
        self.target_select = TargetSelect()
        opt_button = QPushButton('Optimize')

        opt_button.clicked.connect(self.optimize)

        ws_right.layout().addWidget(self.target_select)
        ws_right.layout().addWidget(opt_button)

        # making adjustable
        splitter = QSplitter()
        splitter.addWidget(ws_left)
        splitter.addWidget(ws_right)
        
        # finalizing
        self.layout().addWidget(splitter)

    def open(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.show()

    def clear(self):
        self.tables.clear()
        self.select_window.clear()
        self.target_label.setText('Target: --')

    def refresh(self, new_file=False):
        if new_file:
            self.clear()
        
        self.select_window.refresh()

    def optimize(self):
        target_params = self.getTargetParams()
        
        if len(target_params) == 0:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("No checked parameters.")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)
            if warning.exec() == QMessageBox.Ok:
                warning.close()
                return
            
        for val in target_params.values(): 
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
                   'z-momentum': 'zpcen',
                   'beam size [mm]': 'xrms',
                   'twiss beta [m/rad]': 'xtwsb',
                   'alpha': 'xtwsa',
                   'geom. emittance [mm-mrad]': 'xeps',
                   'norm. emittance [mm-mrad]': 'xepsn'}
        obj = {'location': self.select_window.data['target'],
               'target': target_params}
        
        if self.tables.tabText(self.tables.currentIndex()) == 'Nelder-Mead':
            current_table = self.tables.nelder
        else: # tab is 'Differential Evolution'
            current_table = self.tables.evo
            
        for i in range(current_table.rowCount()):
            name = current_table.item(i, 0).text()
            if name not in glb.data['element']['beam state'].keys():
                attr = current_table.cellWidget(i, 1).currentText()
            else:
                attr = glb.data['element']['beam state'][name]
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
            
            for i, name in enumerate(k.keys()):
                if name in glb.data['element']['beam state'].keys():
                    print(k[name], x[i])
                    for_set_twiss = ['beam size', 'twiss beta', 'alpha', 'geom. emittance', 'norm. emittance']
                    if any(ext in name for ext in for_set_twiss):
                            if 'beam size' in name:
                                kwargs = {'rmssize': x[i]}
                            elif 'twiss beta' in name:
                                kwargs = {'beta': x[i]}
                            elif 'alpha' in name:
                                kwargs = {'alpha': x[i]}
                            elif 'geom. emittance' in name:
                                kwargs = {'emittance': x[i]}
                            else:
                                kwargs = {'nemittance': x[i]}
                                
                            glb.model.bmstate.set_twiss(name[:1], **kwargs)   
                            continue         
                            
                    setattr(glb.model.bmstate, k[name]['abbreviation'], x[i]) 
                else:
                    glb.model.reconfigure(n, {k[name]: x[i]})
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
        
        self.main_window.menuBar().copyModelToHistory()
        executor = ThreadPoolExecutor(max_workers=None)
        
        if current_table is self.tables.nelder:
            array = []
            for n in knobs.keys():
                if n not in glb.data['element']['beam state'].keys():
                    print('no beam state:', knobs[n])
                    array.append(glb.model.get_element(name=n)[0]['properties'][knobs[n]])
                else:
                    print('yes beam state:', knobs[n])
                    array.append(getattr(glb.model.bmstate, knobs[n]['abbreviation']))
                    
            x0 = np.array(array)
            ans = executor.submit(minimize, fun=_costGeneric, x0=x0, args=(knobs, obj), method='Nelder-Mead')
            ans = ans.result()
        else:
            x0 = []
            for i in range(self.tables.evo.rowCount()):
                low = float(self.tables.evo.cellWidget(i, 2).text())
                high = float(self.tables.evo.cellWidget(i, 3).text())
                x0.append((low, high))

            # currently executing on the same thread
            #ans = executor.submit(_differential_evolution, func=_costGeneric, x0=x0, args=(knobs, obj), workers=1)
            ans = executor.submit(differential_evolution, func=_costGeneric, bounds=x0, args=(knobs, obj), workers=-1)
            ans = ans.result()
            
        self.main_window.refresh()

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
            
    def getTargetParams(self):
        target_params = {}
        for item in self.target_select.getLowLevelItems(self.target_select.invisibleRootItem()):
            parent = item.parent()

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
                    target_params[param] = [float(target_val), float(weight)]
                except ValueError:
                    target_params[param] = None
                
        return target_params

        
class OptimizationSelectElementWindow(QWidget):
    def __init__(self, parent=None):
        from classes.tables import Table
        from classes.utility import ModelElementFilters
        
        super().__init__(parent=parent)
        self.data = {'knobs': {'bmstate': [],
                               'elements': []},
                     'target': None}
        self.setWindowTitle('Select Elements For Optimization')
        self.setLayout(QVBoxLayout())
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        
        # objects
        self.bmstate_table = Table(0, 2)
        self.element_table = Table(0, 3, parent=self)
        self.element_filters = ModelElementFilters(self.element_table)
        confirm_button = QPushButton('Confirm')

        self.bmstate_table.setHorizontalHeaderLabels(['Knob', 'Beamstate Element'])
        self.bmstate_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.bmstate_table.horizontalHeader().setStretchLastSection(True)
        self.element_table.setHorizontalHeaderLabels(['Knob', 'Target', 'Model Element'])
        self.element_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.element_table.horizontalHeader().setStretchLastSection(True)

        confirm_button.clicked.connect(self.confirmAction)
        
        # finalizing
        self.setKnobs()
        self.layout().addWidget(self.bmstate_table)
        self.layout().addWidget(self.element_filters)
        self.layout().addWidget(self.element_table)
        self.layout().addWidget(confirm_button)
        

    def open(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.show()
        
    def confirmAction(self):
        self.parent().tables.fill()
        target_index = self.data['target']
        if target_index:
            target = glb.model.get_element(index=target_index)[0]['properties']['name']
            self.parent().target_label.setText('Target: ' + target)
        else:
            self.parent().target_label.setText('Target: --')
        
        self.close()

    def clear(self):
        self.element_table.setRowCount(0)
        self.data = {'knobs': {'bmstate': [],
                               'elements': []},
                     'target': None}
        
        for i in range(self.bmstate_table.rowCount()):
            knob_checkbox = self.bmstate_table.cellWidget(i, 0).children()[1]
            knob_checkbox.blockSignals(True)
            knob_checkbox.setCheckState(Qt.Unchecked)
            knob_checkbox.blockSignals(False)

        

    def refresh(self):
        from classes.utility import ElementIndexTableItemWrapper

        # element removal
        rows_to_remove = []
        names = glb.model.get_all_names()[1:]
        for i in range(self.element_table.rowCount()):
            item = self.element_table.item(i, 2)
            name = item.text()
            if name not in names:
                rows_to_remove.append(i)
                if item.element_index in self.data['knobs']['elements']:
                    self.data['knobs']['elements'].remove(item.element_index)
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
                item = ElementIndexTableItemWrapper(name, element_index)

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
                self.data['target'] = n_index
            if knob_checkbox.checkState() == Qt.Checked:
                self.data['knobs']['elements'].remove(item.element_index)
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
                    
        checkbox.blockSignals(False)
        

    def setKnobs(self):
        from classes.utility import ElementIndexTableItemWrapper

        names = glb.model.get_all_names()[1:]
        
        # beamstate table
        for component in glb.data['element']['beam state'].keys():

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
            item = ElementIndexTableItemWrapper(name, element['index'])

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


        
class PreferenceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle('Preferences')
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setLayout(QGridLayout())
        settings = self.getSettings()
        
        # objects
        app_fsize_label = QLabel('Application Font Size:')
        plt_fsize_label = QLabel('Plot Font Size:')
        sigfig_label = QLabel('Significant Figures:')
        self.app_fsize_spin = QSpinBox()
        self.plt_fsize_spin = QSpinBox()
        self.sigfig_spin = QSpinBox()
        default_button = QPushButton('Default')
        apply_button = QPushButton('Apply')
        
        self.app_fsize_spin.setValue(settings['AppFontSize'])
        self.plt_fsize_spin.setValue(settings['PlotFontSize'])
        self.sigfig_spin.setValue(settings['NumSigFigs'])

        default_button.clicked.connect(self.setDefault)
        apply_button.clicked.connect(self.apply)

        # finalizing
        self.layout().addWidget(app_fsize_label, 0, 0)
        self.layout().addWidget(plt_fsize_label, 1, 0)
        self.layout().addWidget(sigfig_label, 2, 0)
        self.layout().addWidget(default_button, 3, 0)
        self.layout().addWidget(self.app_fsize_spin, 0, 1)
        self.layout().addWidget(self.plt_fsize_spin, 1, 1)
        self.layout().addWidget(self.sigfig_spin, 2, 1)
        self.layout().addWidget(apply_button, 3, 1)

    def open(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.show()
    
    def apply(self):
        # application font size
        glb.app.setStyleSheet("QWidget {font-size: " + str(self.app_fsize_spin.value()) + "pt;}")
        
        # graph font size
        mpl.rc('font', size=self.plt_fsize_spin.value())

        # significant figures
        glb.num_sigfigs = self.sigfig_spin.value()
        
        self.parent().refresh()

    def setDefault(self):
        self.app_fsize_spin.setValue(9)
        self.plt_fsize_spin.setValue(10)
        self.sigfig_spin.setValue(4)
        
    def setSettings(self):
        config = ConfigParser()
        config.read('settings.ini')
        config.set('main', 'AppFontSize', str(self.app_fsize_spin.value()))
        config.set('main', 'PlotFontSize', str(self.plt_fsize_spin.value()))
        config.set('main', 'NumSigFigs', str(self.sigfig_spin.value()))
        with open('settings.ini','w') as f:
            config.write(f)
        
    def getSettings(self):
        config = ConfigParser()
        config.read('settings.ini')
        app_fsize = config.getint('main', 'AppFontSize')
        plt_fsize = config.getint('main', 'PlotFontSize')
        num_sigfigs = config.getint('main', 'NumSigFigs')
        return {'AppFontSize': app_fsize,
                'PlotFontSize': plt_fsize,
                'NumSigFigs': num_sigfigs}


class ModelElementConfigWindow(QWidget):
    def __init__(self, main_window, parent=None):
        from classes.tables import ModelElementAttributeTable

        super().__init__(parent=parent)
        self.setWindowTitle('Model Element Config')
        self.setLayout(QVBoxLayout())
        self.main_window = main_window

        top_row = QWidget()
        top_row.setLayout(QHBoxLayout())

        # objects
        index_label = QLabel()
        name_label = QLabel()
        type_label = QLabel()
        self.index_spin = QSpinBox()
        self.name_line = QLineEdit()
        self.type_box = QComboBox()
        self.attr_table = ModelElementAttributeTable(parent=self)
        self.apply_button = QPushButton('Apply')

        index_label.setText('Index:')
        self.index_spin.setRange(1, 1)
        name_label.setText('Name:')
        type_label.setText('Type:')
        self.name_line.setPlaceholderText('Element Name')
        self.type_box.addItems(['marker', 'orbtrim', 'drift', # 'stripper', 'tmatrix',
                'solenoid', 'quadrupole', 'sextupole', 'equad', 'sbend',
                'edipole', 'rfcavity'])

        self.type_box.currentTextChanged.connect(self.attr_table.setRequiredAttributes)
        self.apply_button.clicked.connect(self.apply)

        # finalizing
        top_row.layout().addWidget(index_label)
        top_row.layout().addWidget(self.index_spin)
        top_row.layout().addWidget(name_label)
        top_row.layout().addWidget(self.name_line)
        top_row.layout().addWidget(type_label)
        top_row.layout().addWidget(self.type_box)

        self.layout().addWidget(top_row)
        self.layout().addWidget(self.attr_table)
        self.layout().addWidget(self.apply_button)
        
    def open(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.show()
        
    def refresh(self):
        self.updateIndexSpinBox()

    def openElement(self, element_index):
        self.updateIndexSpinBox()
        self.index_spin.setEnabled(False)
        self.type_box.setEnabled(False)

        element = glb.model.get_element(index=element_index)[0]

        self.index_spin.setValue(element_index)
        self.name_line.setText(element['properties']['name'])
        self.type_box.setCurrentText(element['properties']['type'])
        
        self.attr_table.default()
        self.attr_table.setAttributes(element)
        
    def insertElement(self, index):
        self.updateIndexSpinBox()
        self.index_spin.setEnabled(True)
        self.type_box.setEnabled(True)

        self.index_spin.setValue(int(index))

        self.attr_table.default()
        self.attr_table.setRequiredAttributes(self.type_box.currentText())
        
    def updateIndexSpinBox(self):
        num_elements = len(glb.model.get_all_names()[1:])
        self.index_spin.setRange(1, num_elements + 1)

    def apply(self):
        if not self.name_line.text():
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("Element must have a name.")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)
            if warning.exec() == QMessageBox.Ok:
                warning.close()
                return
            
        d = {}
        for i in range(self.attr_table.rowCount() - 1):
            attribute = self.attr_table.cellWidget(i, 0)
            value = self.attr_table.cellWidget(i, 1)
            try:
                d[attribute.text()] = float(value.text())
            except:
                warning = QMessageBox()
                warning.setIcon(QMessageBox.Critical)
                warning.setText("Each attribute must have a value.")
                warning.setWindowTitle("ERROR")
                warning.setStandardButtons(QMessageBox.Ok)
                if warning.exec() == QMessageBox.Ok:
                    warning.close()
                    return

        d['name'] = self.name_line.text()
        d['type'] = self.type_box.currentText()
        i = self.index_spin.value()

        self.main_window.menuBar().copyModelToHistory()

        if self.type_box.isEnabled() == False:
            glb.model.pop_element(index=i)

        glb.model.insert_element(index=i, element=d)

        self.main_window.refresh()
        self.updateIndexSpinBox()

class EditMatrixWindow(QWidget):
    def __init__(self, parent=None):
        from classes.tables import MatrixTable
        
        super().__init__(parent=parent)
        self.setWindowTitle('Edit Matrix')
        self.setLayout(QVBoxLayout())
        
        self.table = MatrixTable(7, 7)
        self.button = QPushButton('Confirm')
        self.button.clicked.connect(self.setMatrix)
        self.layout().addWidget(self.table)
        self.layout().addWidget(self.button)
        
    def open(self, element_name):
        self.element_name = element_name
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.table.fill(element_name)
        self.show()
        
    def setMatrix(self):
        glb.main_window.menuBar().copyModelToHistory()
        glb.model.reconfigure(self.element_name, {'matrix': self.table.getMatrix()})
        glb.main_window.refresh()
        self.close()
