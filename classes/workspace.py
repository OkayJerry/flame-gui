from PyQt5 import QtWidgets
from classes.tree import *
from classes.canvas import *
from classes.legend import *
from classes.utility import ItemWrapper

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
    "zcen": {
        "description": "weight average of all charge states for phi",
        "unit": "rad",
        "representation": "z"
    },  # phi
    "zrms": {
        "description": "general rms beam envelope for phi",
        "unit": "rad",
        "representation": "z"
    },  # phi
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
    "zpcen": {
        "description": "weight average of all charge states for SE_k",
        "unit": "MeV/u",
        "representation": "z'"
    },  # SE_k
    "zprms": {
        "description": "general rms beam envelope for SE_k",
        "unit": "MeV/u",
        "representation": "z'"
    },  # SE_k
    "xemittance": {
        "description": "weight average of geometrical x emittance",
        "unit": "mm-mrad",
        "representation": "x"
    },
    "yemittance": {
        "description": "weight average of geometrical y emittance",
        "unit": "mm-mrad",
        "representation": "y"
    },
    "zemittance": {
        "description": "weight average of geometrical z emittance",
        "unit": "rad-MeV/u",
        "representation": "z"
    },
    "xnemittance": {
        "description": "weight average of normalized x emittance",
        "unit": "mm-mrad",
        "representation": "norm(x)"
    },
    "ynemittance": {
        "description": "weight average of normalized y emittance",
        "unit": "mm-mrad",
        "representation": "norm(y)"
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


class Workspace(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)

        self.main_window = parent
        self.items = self._createItems()

        # setting up sub-workspaces
        ws1 = QtWidgets.QWidget(self)
        ws2 = QtWidgets.QWidget(self)

        ws1.setLayout(QtWidgets.QVBoxLayout())
        ws2.setLayout(QtWidgets.QVBoxLayout())

        # objects
        self.graph = FmMplCanvas()
        self.toolbar = NavigationToolbar(self.graph, ws1)
        self.filters = LatTreeFilters()
        self.lat_editor = LatTree(self)
        self.config_window = LatElementConfig(self)

        actions = self.toolbar.findChildren(QtWidgets.QAction)
        for a in actions:
            if a.text() == 'Customize':
                print(a.icon())
                self.toolbar.removeAction(a)
                break

        self.param_tree = Legend()

        # linking objects
        self.graph.link(self.param_tree, self.main_window)
        self.toolbar.actions()[0].triggered.connect(
            lambda: self.graph.figure.tight_layout())  # home button pressed
        self.filters.link(self.lat_editor)
        self.lat_editor.link(self.graph, self.config_window)
        self.config_window.link(self.graph, self.lat_editor)

        self.param_tree.link(self.items, self.graph)

        # handling layouts
        ws1.layout().addWidget(self.toolbar)
        ws1.layout().addWidget(self.graph, 3)
        ws1.layout().addWidget(self.filters)
        ws1.layout().addWidget(self.lat_editor, 2)

        ws2.layout().addWidget(self.param_tree)

        # components
        layout = QtWidgets.QHBoxLayout()
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(ws1)
        splitter.addWidget(ws2)
        layout.addWidget(splitter)
        self.setLayout(layout)

    def link(self, phase_window, opt_window, bmstate_window):
        self.phase_window = phase_window
        self.opt_window = opt_window
        self.bmstate_window = bmstate_window

    def refresh(self):
        # .lat editor
        name_i = self.lat_editor.headers.index('Name')
        expanded_elements = []
        for i in range(self.lat_editor.topLevelItemCount()):
            element = self.lat_editor.topLevelItem(i)
            if element.isExpanded():
                expanded_elements.append(element.text(name_i))

        self.lat_editor.clear()
        self.lat_editor.populate()
        self.lat_editor.typeFilter(self.filters.combo_box.currentText())

        for element in expanded_elements:
            item = self.lat_editor.findItems(
                element, QtCore.Qt.MatchExactly, name_i)[0]
            item.setExpanded(True)

        # graph
        self.graph.updateLines()

        # phase space window
        element = self.phase_window.element_box.currentText()
        self.phase_window.setElementBox()
        self.phase_window.filter()
        self.phase_window.element_box.setCurrentText(element)

        # optimization window
        self.opt_window.select_window.refresh()
        self.opt_window.fillTables()

        # beamstate window
        self.bmstate_window.update()

    def _createItems(self):
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

        for kwrd, attr in workspace_one_items.items():
            item = ItemWrapper()
            item.kwrd = kwrd
            item.x_unit = "pos"
            item.y_unit = attr["unit"]
            item.description = attr["description"]
            item.text_repr = attr["representation"]

            if "'" in attr["representation"]:  # x', y', z' (prime)
                item.dashed = True

            for k, v in object_dict.items():
                if k in kwrd:
                    v.append(item)
                    break
                elif k == "others":  # if item made it to "others", it belongs there
                    object_dict["others"].append(item)

        return object_dict
