from PyQt5 import QtWidgets, QtGui
from classes.tree import *
from classes.canvas import *
from classes.legend import *
from classes.utility import WorkspaceOneItem

workspace_one_items = {
    "ref_beta": {
        "description": "speed in the unit of light velocity in vacuum of reference charge state, Lorentz beta",
        "unit": "",
        "representation": "Beta"
    },
    "ref_bg": {
        "description": "multiplication of beta and gamma of reference charge state",
        "unit": "",
        "representation": "BG"
    },
    "ref_gamma": {
        "description": "relativistic energy of reference charge state, Lorentz gamma",
        "unit": "",
        "representation": "Gamma"
    },
    "ref_IonEk": {
        "description": "kinetic energy of reference charge state",
        "unit": "eV/u",
        "representation": "IonEk"
    },
    "ref_IonEs": {
        "description": "rest energy of reference charge state",
        "unit": "eV/u",
        "representation": "IonEs"
    },
    "ref_IonQ": {
        "description": "macro particle number of reference charge state",
        "unit": "",
        "representation": "IonQ"
    },
    "ref_IonW": {
        "description": "total energy of reference charge state, i.e. W = E_s + E_k",
        "unit": "eV/u",
        "representation": "IonW"
    },
    "ref_IonZ": {
        "description": "reference charge to mass ratio",
        "unit": "",
        "representation": "IonZ"
    },
    "ref_phis": {
        "description": "absolute synchrotron phase of reference charge state",
        "unit": "rad",
        "representation": "Phis"
    },
    "ref_SampleIonK": {
        "description": "wave-vector in cavities with different beta values of reference charge state",
        "unit": "rad",
        "representation": "SampleIonK"
    },
    "ref_Brho": {
        "description": "magnetic rigidity of reference charge state",
        "unit": "Tm",
        "representation": "Brho"
    },
    # "Brho": {
    #     "description": "magnetic rigidity of reference charge state",
    #     "unit": "Tm",
    #     "representation": "Brho"
    # },
    "xcen": {
        "description": "weight average of all charge states for x",
        "unit": "mm",
        "representation": "x"
    },
    "xrms": {
        "description": "general rms beam envelope for x]",
        "unit": "mm",
        "representation": "x"
    },
    "xpcen": {
        "description": "weight average of all charge states for x'",
        "unit": "rad",
        "representation": "x'"
    },
    "xprms": {
        "description": "general rms beam envelope for x'",
        "unit": "rad",
        "representation": "x'"
    },
    "ycen": {
        "description": "weight average of all charge states for y",
        "unit": "mm",
        "representation": "y"
    },
    "yrms": {
        "description": "general rms beam envelope for y",
        "unit": "mm",
        "representation": "y"
    },
    "ypcen": {
        "description": "weight average of all charge states for y'",
        "unit": "rad",
        "representation": "y'"
    },
    "yprms": {
        "description": "general rms beam envelope for y'",
        "unit": "rad",
        "representation": "y'"
    },
    "zcen": {
        "description": "weight average of all charge states for phi",
        "unit": "rad",
        "representation": "z"
    }, # phi
    "zrms": {
        "description": "general rms beam envelope for phi",
        "unit": "rad",
        "representation": "z"
    }, # phi
    "zpcen": {
        "description": "weight average of all charge states for SE_k",
        "unit": "MeV/u",
        "representation": "z'"
    }, # SE_k
    "zprms": {
        "description": "general rms beam envelope for SE_k",
        "unit": "MeV/u",
        "representation": "z'"
    }, # SE_k
    "xemittance": {
        "description": "weight average of geometrical x emittance",
        "unit": "mm-mrad",
        "representation": "x"
    },
    "xnemittance": {
        "description": "weight average of normalized x emittance",
        "unit": "mm-mrad",
        "representation": "norm(x)"
    },
    "yemittance": {
        "description": "weight average of geometrical y emittance",
        "unit": "mm-mrad",
        "representation": "y"
    },
    "ynemittance": {
        "description": "weight average of normalized y emittance",
        "unit": "mm-mrad",
        "representation": "norm(y)"
    },
    "zemittance": {
        "description": "weight average of geometrical z emittance",
        "unit": "rad-MeV/u",
        "representation": "z"
    },
    "znemittance": {
        "description": "weight average of normalized z emittance",
        "unit": "rad-MeV/u",
        "representation": "norm(z)"
    },
    "xtwiss_beta": {
        "description": "weight average of twiss beta x",
        "unit": "m/rad",
        "representation": "x"
    },
    "xtwiss_alpha": {
        "description": "weight average of twiss alpha x",
        "unit": "",
        "representation": "x"
    },
    "xtwiss_gamma": {
        "description": "weight average of twiss gamma x",
        "unit": "rad/m",
        "representation": "x"
    },
    "ytwiss_beta": {
        "description": "weight average of twiss beta y",
        "unit": "m/rad",
        "representation": "y"
    },
    "ytwiss_alpha": {
        "description": "weight average of twiss alpha y",
        "unit": "",
        "representation": "y"
    },
    "ytwiss_gamma": {
        "description": "weight average of twiss gamma y",
        "unit": "rad/m",
        "representation": "y"
    },
    "ztwiss_beta": {
        "description": "weight average of twiss beta z",
        "unit": "rad/MeV/u",
        "representation": "z"
    },
    "ztwiss_alpha": {
        "description": "weight average of twiss alpha z",
        "unit": "",
        "representation": "z"
    },
    "ztwiss_gamma": {
        "description": "weight average of twiss gamma z",
        "unit": "MeV/u/rad",
        "representation": "z"
    },
    "couple_xy": {
        "description": "weight average of normalized x-y coupling term",
        "unit": "",
        "representation": "x-y"
    },
    "couple_xpy": {
        "description": "weight average of normalized xp-y coupling term",
        "unit": "",
        "representation": "x'-y"
    },
    "couple_xyp": {
        "description": "weight average of normalized x-yp coupling term",
        "unit": "",
        "representation": "x-y'"
    },
    "couple_xpyp": {
        "description": "weight average of normalized xp-yp coupling term",
        "unit": "",
        "representation": "x'-y'"
    },
    "last_caviphi0": {
        "description": "last RF cavity's driven phase",
        "unit": "deg",  
        "representation": "Last Caviphi"
    }
}

class LatTreeFilterWorkspace(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(QtWidgets.QWidget,self).__init__(parent)

        # componenets
        self.parent = parent
        self.layout = QtWidgets.QHBoxLayout()
        self.combo_box = QtWidgets.QComboBox()
    
        self.set_combo_box()
        self.layout.setContentsMargins(0, 0, 0, 0)


        self.layout.addWidget(self.combo_box)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def set_combo_box(self):
        for word in ['all','magnetic','quadrupole','drift','orbtrim','marker','sbend']:
            self.combo_box.addItem(word)

        self.combo_box.currentTextChanged.connect(self.parent.lat_tree.filter)
        self.combo_box.setFixedWidth(300)
        



class PrimaryWorkspace(QtWidgets.QWidget):
    def __init__(self,graph,items,parent=None):

        super(QtWidgets.QWidget,self).__init__(parent)

        # components
        self.layout = QtWidgets.QVBoxLayout()
        self.graph = graph
        self.lat_tree = LatTree(self)
        self.filter_workspace = LatTreeFilterWorkspace(self)
        self.config_window = LatElementConfig(self.lat_tree,self.filter_workspace.combo_box)

        self.lat_tree.set_config(self.config_window)

        self.layout.addWidget(self.graph,3)
        self.layout.addWidget(self.filter_workspace)
        self.layout.addWidget(self.lat_tree,2)

        self.setLayout(self.layout)

class SecondaryWorkspace(QtWidgets.QWidget):
    def __init__(self,graph,items,parent=None):
        super(QtWidgets.QWidget,self).__init__(parent)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.legend = Legend(graph,items,self)
        
        self.layout.addWidget(self.legend)
        
        self.setLayout(self.layout)


class Workspace(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(QtWidgets.QWidget,self).__init__(parent)

        self.objects = self._create_objects()
        self.graph = FmMplCanvas(self.objects)
        self.primary = PrimaryWorkspace(self.graph,self.objects,self)
        self.secondary = SecondaryWorkspace(self.graph,self.objects,self)

        # components
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.primary,3)
        self.layout.addWidget(self.secondary,1)
        self.setLayout(self.layout)

    def _create_objects(self):
        object_dict = {
            "ref": [],
            "cen": [],
            "rms": [],
            "emittance": [],
            "twiss_alpha": [],
            "twiss_beta": [],
            "twiss_gamma": [],
            "couple": [],
            "others": []
        }

        for kwrd,attr in workspace_one_items.items():
            item = WorkspaceOneItem()
            item.kwrd = kwrd
            item.x_unit = "pos"
            item.y_unit = attr["unit"]
            item.description = attr["description"]
            item.text_repr = attr["representation"]

            if "'" in attr["representation"]: # x', y', z' (prime)
                item.dashed = True

            for k,v in object_dict.items():
                if k in kwrd:
                    v.append(item)
                    break
                elif k == "others": # if item made it to "others", it belongs there
                    object_dict["others"].append(item)

        return object_dict

class LatElementConfig(QtWidgets.QWidget):
    def __init__(self,lat_tree,tree_filter):
        super().__init__()
        self.tree = lat_tree
        self.tree_filter = tree_filter
        self.model = None
        self.editing = False

        top_row = QtWidgets.QWidget()
        bottom_row = QtWidgets.QWidget()

        self.layout = QtWidgets.QVBoxLayout()
        top_row_layout = QtWidgets.QHBoxLayout()
        bottom_row_layout = QtWidgets.QHBoxLayout()

        self.setMinimumSize(800,600)
        self.setWindowTitle('.lat Config')

        index_label = QtWidgets.QLabel()
        name_label = QtWidgets.QLabel()
        type_label = QtWidgets.QLabel()
        self.index_line = QtWidgets.QLineEdit()
        self.name_line = QtWidgets.QLineEdit()
        self.type_box = QtWidgets.QComboBox()

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

        self.attr_table = QtWidgets.QTableWidget(1, 2)
        self.attr_table.setHorizontalHeaderLabels(['Attribute','Value','Unit'])
        self.attr_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.add_attr_button = QtWidgets.QPushButton()
        self.commit_button = QtWidgets.QPushButton()
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
        attr = QtWidgets.QTableWidgetItem()
        val = QtWidgets.QTableWidgetItem()

        attr.setText(topLevelItem.text(attr_i))
        val.setText(topLevelItem.text(val_i))

        self.attr_table.setItem(0,0,attr)
        self.attr_table.setItem(0,1,val)
        
        # rest of the attributes
        for i in range(topLevelItem.childCount()):
            self.attr_table.insertRow(self.attr_table.rowCount())
            child = topLevelItem.child(i)

            attr = QtWidgets.QTableWidgetItem()
            val = QtWidgets.QTableWidgetItem()

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
        self.tree.filter(self.tree_filter.currentText())

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