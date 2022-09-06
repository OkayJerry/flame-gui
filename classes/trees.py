import globals as glb
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import *


class Tree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        
    def fill(self, item, var):
        if type(var) is dict:
            for key,val in var.items():
                child = QTreeWidgetItem()
                child.setText(0, key)
                item.addChild(child)
                self.fill(child, val)
        elif type(var) is list:
            for element in var:
                self.fill(item, element)
        else:
            child = QTreeWidgetItem()
            child.setText(0, var)
            item.addChild(child)
            
    def getLowLevelItems(self, item):
        L = []
        for i in range(item.childCount()):
            child = item.child(i)
            if child.childCount() == 0:
                L.append(child)
            else:
                L += self.getLowLevelItems(child)
        return L

    def addCheckBoxToLowLevelItems(self):
        low_level_items = self.getLowLevelItems(self.invisibleRootItem())
        for item in low_level_items:
            item.setCheckState(0, Qt.Unchecked)

    def getCheckedItems(self, item):
        L = []
        for i in range(item.childCount()):
            child = item.child(i)
            if child.checkState(0) == Qt.Checked:
                L.append(child)
            L += self.getCheckedItems(child)
        return L 
    
    def getExpandedItems(self, item):
        L = []
        for i in range(item.childCount()):
            child = item.child(i)
            if child.isExpanded():
                L.append(child)
            L += self.getExpandedItems(child)
        return L


class ModelElementView(Tree):
    def __init__(self):
        from classes.windows import ModelElementConfigWindow
        from classes.utility import ElementTreeDelegate
        
        super().__init__()
        self._delegate = ElementTreeDelegate()  # prevents python garbage collection
        self.config_window = ModelElementConfigWindow()
        
        headers = ['Index', 'Name', 'Type', 'Attribute', 'Value', 'Unit']
        self.setHeaderLabels(headers)
        self.setColumnCount(len(headers))
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setItemDelegateForColumn(4, self._delegate)
        
        self.itemDoubleClicked.connect(self.handleEdits)

    def refresh(self, new_file=False):
        from classes.utility import EditMatrixButton
        
        if not new_file:
            expanded_elements = self.getExpandedElements()
            
        self.clear()

        elements = glb.model.get_element(name=glb.model.get_all_names())[1:]
        items_with_matrix = []
        
        for element in elements:
            item = QTreeWidgetItem()
            item.setText(0, str(element['index']))
            if 'tmatrix' == element['properties']['type'] and item not in items_with_matrix:
                items_with_matrix.append(item)
            for key, val in element['properties'].items():
                if key == 'name':
                    item.setText(1, val)
                elif key == 'type':
                    if val == 'tmatrix':
                        items_with_matrix.append(item)
                    item.setText(2, str(val))
                else:
                    if item.text(3) == '' and 'L' not in element['properties'].keys():
                        try:
                            f_string = "{:." + str(glb.num_sigfigs - 1) + "e}"
                            val = f_string.format(val)
                        except:
                            pass
                        item.setText(3, key)
                        if item not in items_with_matrix:
                            item.setText(4, str(val))
                    elif item.text(3) == '' and key == 'L':
                        f_string = "{:." + str(glb.num_sigfigs - 1) + "e}"
                        val = f_string.format(val)
                        item.setText(3, key)
                        if item not in items_with_matrix:
                            item.setText(4, str(val))
                    else:  # children are just attribute-value-unit tuples
                        f_string = "{:." + str(glb.num_sigfigs - 1) + "e}"
                        val = f_string.format(val)
                        child = QTreeWidgetItem()
                        item.addChild(child)
                        child.setText(3, key)
                        if child not in items_with_matrix:
                            child.setText(3, str(val))
                        child.setText(5, glb.model.get_attribute_unit(key))
            item.setText(5, glb.model.get_attribute_unit(item.text(3)))
            self.addTopLevelItem(item)
            
            for item in items_with_matrix:
                self.setItemWidget(item, 4, EditMatrixButton(element_name=item.text(1), parent=self))
            
        if not new_file:
            for element in expanded_elements:
                try:
                    item = self.findItems(element, Qt.MatchExactly, 1)[0]
                    item.setExpanded(True)
                except:
                    print(item.text(1) + " could not be found...")

    def handlePostEdit(self, item):
        menu_bar = self.main_window.menuBar()
        menu_bar.copyModelToHistory()
        
        attribute = item.text(3)
        unit = item.text(5)

        if not item.parent():
            element = item.text(1)
        else:
            element = item.parent().text(1)

        try:
            val = float(item.text(4))
            f_string = "{:." + str(glb.num_sigfigs - 1) + "e}"
            item.setText(4, f_string.format(val))
        except:
            val = item.text(4)

        glb.model.reconfigure(element, {attribute: val})
        glb.main_window.refresh()
        
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        ins_elem = QAction('Insert Element', self)
        edit_elem = QAction('Edit Selected Element', self)
        rem_elem = QAction('Remove Element', self)

        ins_elem.triggered.connect(self.insertElement)
        edit_elem.triggered.connect(self.editElement)
        rem_elem.triggered.connect(self.removeElement)

        menu.addAction(ins_elem)
        menu.addAction(edit_elem)
        menu.addAction(rem_elem)

        menu.popup(QCursor.pos())
        
    def insertElement(self):
        if self.currentItem():
            item = self.currentItem()
            if item.parent():
                item = item.parent()
            self.config_window.insertElement(item.text(0))
        else:
            if self.topLevelItemCount() == 0:
                self.config_window.insertElement('1')
            else:
                i = self.topLevelItemCount() + 1
                self.config_window.insertElement(str(i))

        self.config_window.open()
    
    def editElement(self):
        item = self.currentItem()
        
        if not item:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("No element selected.")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)
            if warning.exec() == QMessageBox.Ok:
                warning.close()
                return
        elif item.parent():
            item = item.parent()

        element_index = int(item.text(0))
        self.config_window.openElement(element_index)

        self.config_window.open()

    def removeElement(self):
        item = self.currentItem()

        if not item:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("No element selected.")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)
            if warning.exec() == QMessageBox.Ok:
                warning.close()
                return
        elif item.parent():
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("Must select element, not element attribute.")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)
            if warning.exec() == QMessageBox.Ok:
                warning.close()
                return

        glb.model.pop_element(int(item.text(0)))
        glb.main_window.refresh()

    def handleEdits(self, item, column):
        if column != 4:
            return
        elif item.text(3) == '':
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            return

        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable) 
        self.editItem(item, column)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def getExpandedElements(self):
        L = []
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item.isExpanded():
                L.append(item.text(1))
        return L


class ParameterSelect(Tree):
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.data = {'Reference': ['Beta', 'BG', 'Gamma', 'IonEk', 'IonEs', 'IonQ', 'IonW', 'IonZ', 'Phis', 'SampleIonK', 'Brho'],
                     'Actual': {'cen': ["x", "y", "z", "x'", "y'", "z'"],
                                'rms': ["x", "y", "z", "x'", "y'", "z'"],
                                'emittance': ["x", "y", "z", "norm(x)", "norm(y)", "norm(z)"],
                                'twiss': {'alpha': ["x", "y", "z"],
                                    'beta': ["x", "y", "z"],
                                    'gamma': ["x", "y", "z"]},
                                'couple': ["x-y", "x'-y", "x-y'", "x'-y'"],
                                'others': 'Last Caviphi'}}
        
        # populating
        self.fill(self.invisibleRootItem(), self.data)
        self.addCheckBoxToLowLevelItems()
        
        # adding description
        ll_items = self.getLowLevelItems(self.invisibleRootItem())
        for item in ll_items:
            parameter = self.convertItemIntoParam(item)
            item.setToolTip(0, glb.data['parameter'][parameter]['description'])

    def convertItemIntoParam(self, item):
        text = item.text(0)
        if text in self.data['Reference']:
            if text == 'Beta' or text == 'BG' or text =='Gamma' or text == 'Phis':
                text = text.lower()
            return 'ref_' + text
        else:
            parent_text = item.parent().text(0)
            if "'" in text:
                text = text.replace("'", 'p')
            if '-' in text:
                text = text.replace('-', '')
                
            if parent_text == 'cen':
                return text + 'cen'
            elif parent_text == 'rms':
                return text + 'rms'
            elif parent_text == 'emittance':
                if 'norm' in text:
                    text = text.replace('norm(', '')
                    text = text.replace(')', 'n')
                return text + 'emittance'
            elif parent_text == 'alpha':
                return text + 'twiss_alpha'
            elif parent_text == 'beta':
                return text + 'twiss_beta'
            elif parent_text == 'gamma':
                return text + 'twiss_gamma'
            elif parent_text == 'couple':
                return 'couple_' + text
            elif parent_text == 'others':
                return 'last_caviphi0'
        
        raise NotImplementedError(text + ' is not in ' + str(self) + ' data!')
                
                    

        

class TargetSelect(Tree):
    def __init__(self):
        from classes.utility import SigFigDelegate
        
        super().__init__()

        # objects
        self._delegates = [SigFigDelegate(), SigFigDelegate()] # prevents python garbage collection
        self.data = {'Reference': ['IonEk', 'Phis'],
                     'Actual': {'cen': ["x", "y", "z", "x'", "y'", "z'"],
                                'rms': ["x", "y", "z", "x'", "y'", "z'"],
                                'emittance': ["x", "y", "z", "norm(x)", "norm(y)", "norm(z)"],
                                'twiss': {'alpha': ["x", "y", "z"],
                                          'beta': ["x", "y", "z"],
                                          'gamma': ["x", "y", "z"]},
                                'couple': ["x-y", "x'-y", "x-y'", "x'-y'"]}}

        self.setColumnCount(3)
        self.setHeaderLabels(['Parameter', 'Target Value', 'Weight'])
        self.header().setDefaultAlignment(Qt.AlignCenter)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.setItemDelegateForColumn(1, self._delegates[0])
        self.setItemDelegateForColumn(2, self._delegates[1])

        self.itemDoubleClicked.connect(self.handleEdits)

        self.fill(self.invisibleRootItem(), self.data)
        self.addCheckBoxToLowLevelItems()
        for item in self.getLowLevelItems(self.invisibleRootItem()):
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            
        # adding description
        ll_items = self.getLowLevelItems(self.invisibleRootItem())
        for item in ll_items:
            parameter = self.convertItemIntoParam(item)
            item.setToolTip(0, glb.data['parameter'][parameter]['description'])

    def handleEdits(self, item, column):
        if column == 0 or item not in self.getLowLevelItems(self.invisibleRootItem()):
            return
        self.editItem(item, column)

    def convertItemIntoParam(self, item):
        text = item.text(0)
        if text in self.data['Reference']:
            if text == 'Beta' or text == 'BG' or text =='Gamma' or text == 'Phis':
                text = text.lower()
            return 'ref_' + text
        else:
            parent_text = item.parent().text(0)
            if "'" in text:
                text = text.replace("'", 'p')
            if '-' in text:
                text = text.replace('-', '')
                
            if parent_text == 'cen':
                return text + 'cen'
            elif parent_text == 'rms':
                return text + 'rms'
            elif parent_text == 'emittance':
                if 'norm' in text:
                    text = text.replace('norm(', '')
                    text = text.replace(')', 'n')
                return text + 'emittance'
            elif parent_text == 'alpha':
                return text + 'twiss_alpha'
            elif parent_text == 'beta':
                return text + 'twiss_beta'
            elif parent_text == 'gamma':
                return text + 'twiss_gamma'
            elif parent_text == 'couple':
                return 'couple_' + text
            elif parent_text == 'others':
                return 'last_caviphi0'
        
        raise NotImplementedError(text + ' is not in ' + str(self) + ' data!')
