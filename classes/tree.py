from PyQt5.QtWidgets import QTreeWidget, QHeaderView, QTreeWidgetItem, QAbstractItemView, QStyledItemDelegate, QLineEdit, QMenu, QAction
from PyQt5 import QtCore, QtGui



class DoubleDelegate(QStyledItemDelegate):
    def __init__(self,parent=None):
        super().__init__(parent)

    def createEditor(self,parent,option,index):
        lineEdit = QLineEdit(parent)
        if index.sibling(index.row(),4).data() == None: # if corresponding unit is none
            return lineEdit
        # print(parent.currentItem.text(4))
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
        self.setColumnCount(6)
        self.setHeaderLabels(self.headers)
        # self.header().setSectionResizeMode(QHeaderView.Stretch)

        # edit
        self.setItemDelegateForColumn(4,DoubleDelegate(self))
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

    def filter(self,filter_text):
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

        addElem = QAction('Add Element',self)
        editElem = QAction('Edit Selected Element',self)
        remElem = QAction('Remove Element',self)
        remAttr = QAction('Remoce Attribue',self)

        addElem.triggered.connect(self.addElement)
        editElem.triggered.connect(self.editElement)
        remElem.triggered.connect(self.removeElement)
        remAttr.triggered.connect(self.removeAttribute)

        self.menu.addAction(addElem)
        self.menu.addAction(editElem)
        self.menu.addAction(remElem)

        self.menu.popup(QtGui.QCursor.pos())

    def addElement(self):
        item = self.currentItem()
        self.config_window.show()

    def editElement(self):
        item = self.currentItem()
        self.config_window.editItem(item)
        self.config_window.show()
        

    def removeElement(self):
        item = self.currentItem()
        self.config_window.show()

    def removeAttribute(self):
        item = self.currentItem()