from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt5 import QtCore
from PyQt5 import QtGui

parameters = {
    "pos": "longitudinally propagating position, [m]",
    "ref_beta": "speed in the unit of light velocity in vacuum of reference charge state, Lorentz beta, [1]",
    "ref_bg": "multiplication of beta and gamma of reference charge state, [1]",
    "ref_gamma": "relativistic energy of reference charge state, Lorentz gamma, [1]",
    "ref_IonEk": "kinetic energy of reference charge state, [eV/u]",
    "ref_IonEs": "rest energy of reference charge state, [eV/u]",
    "ref_IonQ": "macro particle number of reference charge state, [1]",
    "ref_IonW": "total energy of reference charge state, [eV/u], i.e. W = E_s + E_k",
    "ref_IonZ": "reference charge to mass ratio, e.g.",
    "ref_phis": "absolute synchrotron phase of reference charge state, [rad]",
    "ref_SampleIonK": "wave-vector in cavities with different beta values of reference charge state, [rad]",
    "ref_Brho": "magnetic rigidity of reference charge state, [Tm]",
    "Brho": "magnetic rigidity of reference charge state, [Tm]",
    "xcen": "weight average of all charge states for x, [mm]",
    "xrms": "general rms beam envelope for x, [mm]",
    "xpcen": "weight average of all charge states for x', [rad]",
    "xprms": "general rms beam envelope for x', [rad]",
    "ycen": "weight average of all charge states for y, [mm]",
    "yrms": "general rms beam envelope for y, [mm]",
    "ypcen": "weight average of all charge states for y', [rad]",
    "yprms": "general rms beam envelope for y', [rad]",
    "zcen": "weight average of all charge states for phi, [rad]", # phi
    "zrms": "general rms beam envelope for phi, [rad]", # phi
    "zpcen": "weight average of all charge states for SE_k, [MeV/u]", # SE_k
    "zprms": "general rms beam envelope for SE_k, [MeV/u]", # SE_k
    "xemittance": "weight average of geometrical x emittance, [mm-mrad]",
    "xnemittance": "weight average of normalized x emittance, [mm-mrad]",
    "yemittance": "weight average of geometrical y emittance, [mm-mrad]",
    "ynemittance": "weight average of normalized y emittance, [mm-mrad]",
    "zemittance": "weight average of geometrical z emittance, [rad-MeV/u]",
    "znemittance": "weight average of normalized z emittance, [rad-MeV/u]",
    "xtwiss_beta": "weight average of twiss beta x, [m/rad]",
    "xtwiss_alpha": "weight average of twiss alpha x, [1]",
    "xtwiss_gamma": "weight average of twiss gamma x, [rad/m]",
    "ytwiss_beta": "weight average of twiss beta y, [m/rad]",
    "ytwiss_alpha": "weight average of twiss alpha y, [1]",
    "ytwiss_gamma": "weight average of twiss gamma y, [rad/m]",
    "ztwiss_beta": "weight average of twiss beta z, [rad/MeV/u]",
    "ztwiss_alpha": "weight average of twiss alpha z, [1]",
    "ztwiss_gamma": "weight average of twiss gamma z, [MeV/u/rad]",
    "couple_xy": "weight average of normalized x-y coupling term, [1]",
    "couple_xpy": "weight average of normalized xp-y coupling term, [1]",
    "couple_xyp": "weight average of normalized x-yp coupling term, [1]",
    "couple_xpyp": "weight average of normalized xp-yp coupling term, [1]",
    "last_caviphi0": "last RF cavity's driven phase, [deg]"
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
