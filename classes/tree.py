from PyQt5.QtWidgets import QTreeWidget, QHeaderView, QTreeWidgetItem, QAbstractItemView, QStyledItemDelegate, QLineEdit
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

        # format
        self.setColumnCount(5)
        self.setHeaderLabels(['Name','Type','Attribute','Value','Unit'])
        # self.header().setSectionResizeMode(QHeaderView.Stretch)

        # edit
        self.setItemDelegateForColumn(3,DoubleDelegate(self))
        self.itemDoubleClicked.connect(self._handle_edits)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.itemChanged.connect(self.update_model)


    def populate(self):
        self.elements = self.model.get_element(name=self.model.get_all_names())
        self.elements = self.elements[1:]
        
        for element in self.elements:
            item = Item()
            for key,val in element['properties'].items():
                val = str(val)
                if key == 'name':
                    item.setText(0,val)
                elif key == 'type':
                    item.setText(1,val)
                else:
                    if item.text(2) == '' and 'L' not in element['properties'].keys():
                        item.setText(2,key)
                        item.setText(3,val)
                    elif item.text(2) == '' and key == 'L':
                        item.setText(2,key)
                        item.setText(3,val)
                    else: # children are just attribute-value-unit tuples
                        child = Item()
                        item.addChild(child)
                        child.setText(2,key)
                        child.setText(3,val)
                        self._set_unit(child)
                self._set_unit(item)
            self.addTopLevelItem(item)

    def _set_unit(self,item):
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

        if item.text(2) in unit_info:
            item.setText(4,unit_info[item.text(2)])



    def update_model(self):
        selected = self.currentItem()
        attribute = selected.text(2)
        unit = selected.text(4)

        if not selected.parent():
            element = selected.text(0)
        else:
            element = selected.parent().text(0)

        if unit != "":
            val = float(selected.text(3))
        else:
            val = selected.text(3)

        self.model.reconfigure(element, {attribute: val})


    def _handle_edits(self,item,col):
        if col == 0 or col == 1: # odd logic, but others didn't work?
            return
        self.editItem(item,col)

    def filter(self,filter_text):
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if filter_text == 'all':
                item.setHidden(False)
                continue
            elif filter_text == 'magnetic':
                if item.text(1) == 'drift':
                    item.setHidden(True)
                else:
                    item.setHidden(False)
                continue

            if item.text(1) != filter_text:
                item.setHidden(True)
            else:
                item.setHidden(False)