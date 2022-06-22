from PyQt5.QtWidgets import QTreeWidget, QHeaderView, QTreeWidgetItem, QAbstractItemView, QStyledItemDelegate, QLineEdit, QMenu, QAction, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets



class DoubleDelegate(QStyledItemDelegate):
    def __init__(self,parent=None):
        super().__init__(parent)

    def createEditor(self,parent,option,index):
        lineEdit = QLineEdit(parent)
        if index.sibling(index.row(),5).data() == None: # if corresponding unit is none
            return lineEdit
        validator = QtGui.QDoubleValidator(lineEdit)
        lineEdit.setValidator(validator)
        return lineEdit;


class Item(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)


class LatTree(QTreeWidget):
    def __init__(self,parent,model=None):
        super(QTreeWidget,self).__init__(parent)
        self.model = model
        self.config_window = None

        self.headers = ['Index','Name','Type','Attribute','Value','Unit']

        # format
        self.setColumnCount(len(self.headers))
        self.setHeaderLabels(self.headers)
        # self.header().setSectionResizeMode(QHeaderView.Stretch)

        # edit
        self.setItemDelegateForColumn(self.headers.index('Value'),DoubleDelegate(self))
        self.itemDoubleClicked.connect(self._handle_edits)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.itemChanged.connect(self.update_model)


    def populate(self):
        index_i = self.headers.index('Index')
        name_i = self.headers.index('Name')
        type_i = self.headers.index('Type')
        attr_i = self.headers.index('Attribute')
        val_i = self.headers.index('Value')
        unit_i = self.headers.index('Unit')

        self.elements = self.model.get_element(name=self.model.get_all_names())
        self.elements = self.elements[1:]
        
        for element in self.elements:
            item = Item()
            item.setText(index_i,str(element['index']))
            for key,val in element['properties'].items():
                val = str(val)
                if key == 'name':
                    item.setText(name_i,val)
                elif key == 'type':
                    item.setText(type_i,val)
                else:
                    if item.text(attr_i) == '' and 'L' not in element['properties'].keys():
                        item.setText(attr_i,key)
                        item.setText(val_i,val)
                    elif item.text(attr_i) == '' and key == 'L':
                        item.setText(attr_i,key)
                        item.setText(val_i,val)
                    else: # children are just attribute-value-unit tuples
                        child = Item()
                        item.addChild(child)
                        child.setText(attr_i,key)
                        child.setText(val_i,val)
                        self._set_unit(child)
                self._set_unit(item)
            self.addTopLevelItem(item)

    def _set_unit(self,item):
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
            item.setText(unit_i,unit_info[item.text(attr_i)])



    def update_model(self):
        name_i = self.headers.index('Name')
        type_i = self.headers.index('Type')
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

        self.model.reconfigure(element, {attribute: val})


    def _handle_edits(self,item,col):
        index_i = self.headers.index('Index')
        name_i = self.headers.index('Name')
        type_i = self.headers.index('Type')

        if col == index_i or col == name_i or col == type_i: # odd logic, but others didn't work?
            return
        self.editItem(item,col)

    def type_filter(self,filter_text):
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





    def set_config(self,window):
        self.config_window = window

    def contextMenuEvent(self,event):
        self.menu = QMenu(self)

        insElem = QAction('Insert Element',self)
        editElem = QAction('Edit Selected Element',self)
        remElem = QAction('Remove Element',self)
        # remAttr = QAction('Remoce Attribue',self)

        insElem.triggered.connect(self.insElement)
        editElem.triggered.connect(self.editElement)
        remElem.triggered.connect(self.removeElement)
        # remAttr.triggered.connect(self.removeAttribute)

        self.menu.addAction(insElem)
        self.menu.addAction(editElem)
        self.menu.addAction(remElem)

        self.menu.popup(QtGui.QCursor.pos())

    def insElement(self):
        index_i = self.headers.index('Index')
        item = self.currentItem()
        if item.parent():
            item = item.parent()
        self.config_window.insertItem(item.text(index_i))
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
        self.model.pop_element(int(item.text(index_i)))
        self.clear()
        self.populate()

    # def removeAttribute(self):



class LatTreeFilters(QWidget):
    def __init__(self,parent=None):
        super(QWidget,self).__init__(parent)

        # componenets
        self.parent = parent
        self.layout = QHBoxLayout()
        self.combo_box = QComboBox()
        self.search_bar = QLineEdit()
    
        for word in ['all','magnetic','quadrupole','drift','orbtrim','marker','sbend']:
            self.combo_box.addItem(word)
        self.combo_box.currentTextChanged.connect(self.parent.lat_tree.type_filter)
        self.combo_box.setFixedWidth(300)

        self.search_bar.setPlaceholderText('Search Element Name')
        self.search_bar.textChanged.connect(self.name_filter)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(self.search_bar)

        self.setLayout(self.layout)

    def name_filter(self,filter_text):
        tree = self.parent.lat_tree
        name_i = tree.headers.index('Name')
        tree.type_filter(self.combo_box.currentText())

        for i in range(tree.topLevelItemCount()):
            item = tree.topLevelItem(i)
            if item.isHidden() == False:
                if filter_text not in item.text(name_i):
                    item.setHidden(True)




class LatElementConfig(QWidget):
    def __init__(self,lat_tree,tree_filter):
        super().__init__()
        self.tree = lat_tree
        self.tree_filter = tree_filter
        self.model = None
        self.editing = False

        top_row = QWidget()
        bottom_row = QWidget()

        self.layout = QVBoxLayout()
        top_row_layout = QHBoxLayout()
        bottom_row_layout = QHBoxLayout()

        self.setMinimumSize(800,600)
        self.setWindowTitle('.lat Config')

        index_label = QLabel()
        name_label = QLabel()
        type_label = QLabel()
        self.index_line = QLineEdit()
        self.name_line = QLineEdit()
        self.type_box = QComboBox()

        index_label.setText('Index:')
        name_label.setText('Name:')
        type_label.setText('Type:')
        self.index_line.setPlaceholderText('Element Index')
        self.name_line.setPlaceholderText('Element Name')
        self.index_line.setValidator(QtGui.QIntValidator(self.index_line))
        top_row_layout.addWidget(index_label)
        top_row_layout.addWidget(self.index_line)
        top_row_layout.addWidget(name_label)
        top_row_layout.addWidget(self.name_line)
        top_row_layout.addWidget(type_label)

        for t in ['quadrupole','drift','orbtrim','marker','sbend']:
            self.type_box.addItem(t)
        top_row_layout.addWidget(self.type_box)

        self.attr_table = QTableWidget(1, 2)
        self.attr_table.setHorizontalHeaderLabels(['Attribute','Value','Unit'])
        self.attr_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.add_attr_button = QPushButton()
        self.commit_button = QPushButton()
        self.add_attr_button.setText('Add Blank Attribute')
        self.commit_button.setText('Finish and Save')
        self.add_attr_button.clicked.connect(lambda: self.attr_table.insertRow(self.attr_table.rowCount()))
        self.commit_button.clicked.connect(self.finishAndSave)

        bottom_row_layout.addWidget(self.add_attr_button)
        bottom_row_layout.addWidget(self.commit_button)

        top_row.setLayout(top_row_layout)
        bottom_row.setLayout(bottom_row_layout)
        self.layout.addWidget(top_row)
        self.layout.addWidget(self.attr_table)
        self.layout.addWidget(bottom_row)
        self.setLayout(self.layout)


    def insertItem(self,index):
        self.index_line.setText(index)


    def editItem(self,topLevelItem):
        self.editing = True

        index_i = self.tree.headers.index('Index')
        name_i = self.tree.headers.index('Name')
        type_i = self.tree.headers.index('Type')
        attr_i = self.tree.headers.index('Attribute')
        val_i = self.tree.headers.index('Value')

        elem_index = topLevelItem.text(index_i)
        elem_name = topLevelItem.text(name_i)
        elem_type = topLevelItem.text(type_i)

        self.index_line.setText(elem_index)
        self.name_line.setText(elem_name)
        self.type_box.setCurrentText(elem_type)

        # disabling changes
        self.index_line.setEnabled(False)
        self.name_line.setEnabled(False)
        self.type_box.setEnabled(False)

        # top level attribute only
        attr = QTableWidgetItem()
        val = QTableWidgetItem()

        attr.setText(topLevelItem.text(attr_i))
        val.setText(topLevelItem.text(val_i))

        self.attr_table.setItem(0,0,attr)
        self.attr_table.setItem(0,1,val)
        
        # rest of the attributes
        for i in range(topLevelItem.childCount()):
            self.attr_table.insertRow(self.attr_table.rowCount())
            child = topLevelItem.child(i)

            attr = QTableWidgetItem()
            val = QTableWidgetItem()

            attr.setText(child.text(attr_i))
            val.setText(child.text(val_i))

            self.attr_table.setItem(i+1,0,attr)
            self.attr_table.setItem(i+1,1,val)


    def finishAndSave(self):
        d = {}
        for i in range(self.attr_table.rowCount()):
            for j in range(self.attr_table.columnCount()):
                cell = self.attr_table.item(i,j)
                if cell:
                    text = cell.text()

                    if j == 0: # index of attribute name
                        attr_name = text
                    elif j == 1: # index of attribute value
                        attr_val = text
            d[attr_name] = attr_val

        if self.editing:
            self.model.reconfigure(self.name_line.text(),d)
        else:
            d['name'] = self.name_line.text()
            d['type'] = self.type_box.currentText()
            self.model.insert_element(index=int(self.index_line.text()),element=d)

        self.tree.clear()
        self.tree.populate()
        self.tree.type_filter(self.tree_filter.currentText())

        self.editing = False
        self.close()
        self.clear()


    def clear(self):
        self.index_line.setEnabled(True)
        self.name_line.setEnabled(True)
        self.type_box.setEnabled(True)
        self.index_line.clear()
        self.name_line.clear()
        self.attr_table.clear()

    
    def closeEvent(self,event): # overriding window close
        self.clear()
        event.accept()