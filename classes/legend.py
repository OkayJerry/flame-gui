from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt5 import QtCore
from PyQt5 import QtGui

parameters = {
    "pos": {
        description: "longitudinally propagating position",
        unit: "m"
        },
    "ref_beta":
        {
        description: "speed in the unit of light velocity in vacuum of reference charge state, Lorentz beta",
        unit: None
        },
    "ref_bg":
        {
        description: "multiplication of beta and gamma of reference charge state",
        unit: None
        },
    "ref_gamma": {
        description: "relativistic energy of reference charge state, Lorentz gamma",
        unit: None
        },
    "ref_IonEk": {
        description: "kinetic energy of reference charge state",
        unit: "eV/u"
        },
    "ref_IonEs": {
        description: "rest energy of reference charge state",
        unit: "eV/u"
        },
    "ref_IonQ": {
        description: "macro particle number of reference charge state",
        unit: None
        },
    "ref_IonW": {
        description: "total energy of reference charge state, i.e. W = E_s + E_k",
        unit: "eV/u"
        },
    "ref_IonZ": {
        description: "reference charge to mass ratio",
        unit: None
        },
    "ref_phis": {
        description: "absolute synchrotron phase of reference charge state",
        unit: "rad"
        },
    "ref_SampleIonK": {
        description: "wave-vector in cavities with different beta values of reference charge state",
        unit: "rad"
        },
    "ref_Brho": {
        description: "magnetic rigidity of reference charge state",
        unit: "Tm"
        },
    "Brho": {
        description: "magnetic rigidity of reference charge state",
        unit: "Tm"
        },
    "xcen": {
        description: "weight average of all charge states for x",
        unit: "mm"
        },
    "xrms": {
        description: "general rms beam envelope for x]",
        unit: "mm"
        },
    "xpcen": {
        description: "weight average of all charge states for x'",
        unit: "rad"
        },
    "xprms": {
        description: "general rms beam envelope for x'",
        unit: "rad"
        },
    "ycen": {
        description: "weight average of all charge states for y",
        unit: "mm"
        },
    "yrms": {
        description: "general rms beam envelope for y",
        unit: "mm"
        },
    "ypcen": {
        description: "weight average of all charge states for y'",
        unit: "rad"
        },
    "yprms": {
        description: "general rms beam envelope for y'",
        unit: "rad"
        },
    "zcen": {
        description: "weight average of all charge states for phi",
        unit: "rad"
        }, # phi
    "zrms": {
        description: "general rms beam envelope for phi",
        unit: "rad"
        }, # phi
    "zpcen": {
        description: "weight average of all charge states for SE_k",
        unit: "MeV/u"
        }, # SE_k
    "zprms": {
        description: "general rms beam envelope for SE_k",
        unit: "MeV/u"
        }, # SE_k
    "xemittance": {
        description: "weight average of geometrical x emittance",
        unit: "mm-mrad"
        },
    "xnemittance": {
        description: "weight average of normalized x emittance",
        unit: "mm-mrad"
        },
    "yemittance": {
        description: "weight average of geometrical y emittance",
        unit: "mm-mrad"
        },
    "ynemittance": {
        description: "weight average of normalized y emittance",
        unit: "mm-mrad"
        },
    "zemittance": {
        description: "weight average of geometrical z emittance",
        unit: "rad-MeV/u"
        },
    "znemittance": {
        description: "weight average of normalized z emittance",
        unit: "rad-MeV/u"
        },
    "xtwiss_beta": {
        description: "weight average of twiss beta x",
        unit: "m/rad"
        },
    "xtwiss_alpha": {
        description: "weight average of twiss alpha x",
        unit: None
        },
    "xtwiss_gamma": {
        description: "weight average of twiss gamma x",
        unit: "rad/m"
        },
    "ytwiss_beta": {
        description: "weight average of twiss beta y",
        unit: "m/rad"
        },
    "ytwiss_alpha": {
        description: "weight average of twiss alpha y",
        unit: None
        },
    "ytwiss_gamma": {
        description: "weight average of twiss gamma y",
        unit: "rad/m"
        },
    "ztwiss_beta": {
        description: "weight average of twiss beta z",
        unit: "rad/MeV/u"
        },
    "ztwiss_alpha": {
        description: "weight average of twiss alpha z",
        unit: None
        },
    "ztwiss_gamma": {
        description: "weight average of twiss gamma z",
        unit: "MeV/u/rad"
        },
    "couple_xy": {
        description: "weight average of normalized x-y coupling term",
        unit: None
        },
    "couple_xpy": {
        description: "weight average of normalized xp-y coupling term",
        unit: None
        },
    "couple_xyp": {
        description: "weight average of normalized x-yp coupling term",
        unit: None
        },
    "couple_xpyp": {
        description: "weight average of normalized xp-yp coupling term",
        unit: None
        },
    "last_caviphi0": {
        description: "last RF cavity's driven phase",
        unit: "deg"
        }
}


            

class Legend(QTableWidget):
    def __init__(self, parent=None):
        super(QTableWidget,self).__init__(parent)

        self.setColumnCount(2)
        self.setRowCount(len(parameters))
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFont(QtGui.QFont('Arial',5))

        self.setHorizontalHeaderItem(0,QTableWidgetItem('Visible'))
        self.setHorizontalHeaderItem(1,QTableWidgetItem('Parameter'))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fill()

    def fill(self):
        i = 0
        for key,val in parameters.items():
            item = QTableWidgetItem(key)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.setItem(i,1,item)
            i += 1

        self.resizeRowsToContents()
        self.resizeColumnsToContents()
