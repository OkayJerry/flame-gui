from PyQt5.QtWidgets import QTreeWidget, QHeaderView, QTreeWidgetItem, QAbstractItemView, QComboBox
from PyQt5 import QtCore
from PyQt5 import QtGui

class LegendItem(QTreeWidgetItem):
    def __init__(self,unit=None,pseudo=None):
        super().__init__()
        self.unit = unit
        self.pseudo = pseudo
        self.line = None


class Legend(QTreeWidget):
    def __init__(self,graph,parent=None):
        super(QTreeWidget,self).__init__(parent)

        self.graph = graph
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.fill()
        
    def fill(self):

        # Parameter            Visible
        # ├─ Reference beam
        # │   ├─ ref_beta        [ ]
        # │   ├─ ref_bg          [ ]
        # │   ├─ ref_gamma       [ ]
        # │   └─ ...
        # └─ Actual beam
        #     ├─ beta            [ ]
        #     ├─ bg              [ ]
        #     ├─ gamma           [ ]
        #     ├─ ...
        #     ├─ cen
        #     │   ├─ x           [ ]
        #     │   ├─ y           [ ]
        #     │   └─ z           [ ]
        #     ├─ rms
        #     │   ├─ x           [x]
        #     │   ├─ y           [x]
        #     │   └─ z           [ ]
        #     ├─ ...
        #     └─ couple
        #         ├─ xy          [ ]
        #         ├─ xpy         [ ]
        #         ├─ xyp         [ ]
        #         └─ xpyp        [ ]


        # reference
        reference = QTreeWidgetItem()
        reference.setText(0,"Reference")
        #   parameters
        ref_beta = LegendItem(None,"ref_beta")
        ref_bg = LegendItem(None,"ref_bg")
        ref_gamma = LegendItem(None,"ref_gamma")
        ref_IonEk = LegendItem("eV/u","ref_IonEk")
        ref_IonEs = LegendItem("eV/u","ref_IonEs")
        ref_IonQ = LegendItem(None,"ref_IonQ")
        ref_IonW = LegendItem("eV/u","ref_IonW")
        ref_IonZ = LegendItem(None,"ref_IonZ")
        ref_phis = LegendItem("rad","ref_phis")
        ref_SampleIonK = LegendItem("rad","ref_SampleIonK")
        ref_Brho = LegendItem("Tm","ref_Brho")

        ref_beta.setText(0,"Beta")
        ref_bg.setText(0,"BG")
        ref_gamma.setText(0,"Gamma")
        ref_IonEk.setText(0,"IonEk")
        ref_IonEs.setText(0,"IonEs")
        ref_IonQ.setText(0,"IonQ")
        ref_IonW.setText(0,"IonW")
        ref_IonZ.setText(0,"IonZ")
        ref_phis.setText(0,"Phis")
        ref_SampleIonK.setText(0,"SampleIonK")
        ref_Brho.setText(0,"Brho")

        ref_beta.setToolTip(0,"speed in the unit of light velocity in vacuum of reference charge state, Lorentz beta")
        ref_bg.setToolTip(0,"multiplication of beta and gamma of reference charge state")
        ref_gamma.setToolTip(0,"relativistic energy of reference charge state, Lorentz gamma")
        ref_IonEk.setToolTip(0,"kinetic energy of reference charge state")
        ref_IonEs.setToolTip(0,"rest energy of reference charge state")
        ref_IonQ.setToolTip(0,"macro particle number of reference charge state")
        ref_IonW.setToolTip(0,"total energy of reference charge state, i.e. W = E_s + E_k")
        ref_IonZ.setToolTip(0,"reference charge to mass ratio")
        ref_phis.setToolTip(0,"absolute synchrotron phase of reference charge state")
        ref_SampleIonK.setToolTip(0,"wave-vector in cavities with different beta values of reference charge state")
        ref_Brho.setToolTip(0,"magnetic rigidity of reference charge state")

        # actual
        actual = QTreeWidgetItem()
        actual.setText(0,"Actual")
        #   sub categories
        cen = QTreeWidgetItem()
        rms = QTreeWidgetItem()
        emt = QTreeWidgetItem()
        tws = QTreeWidgetItem()
        tws_x = QTreeWidgetItem()
        tws_y = QTreeWidgetItem()
        tws_z = QTreeWidgetItem()
        cpl = QTreeWidgetItem()
        others = QTreeWidgetItem()

        cen.setText(0,"cen")
        rms.setText(0,"rms")
        emt.setText(0,"emittance")
        tws.setText(0,"twiss")
        tws_x.setText(0,"alpha")
        tws_y.setText(0,"beta")
        tws_z.setText(0,"gamma")
        cpl.setText(0,"couple")
        others.setText(0,"others")

        #   parameters
        cen_x = LegendItem("mm","xcen")
        cen_xp = LegendItem("rad","xpcen")
        cen_y = LegendItem("mm","ycen")
        cen_yp = LegendItem("rad","ypcen")
        cen_z = LegendItem("rad","zcen")
        cen_zp = LegendItem("MeV/u","zpcen")
        rms_x = LegendItem("mm","xrms")
        rms_xp = LegendItem("rad","xprms")
        rms_y = LegendItem("mm","yrms")
        rms_yp = LegendItem("rad","yprms")
        rms_z = LegendItem("rad","zrms")
        rms_zp = LegendItem("MeV/u","zprms")
        emt_x = LegendItem("mm-mrad","xeps")
        emt_xn = LegendItem("mm-mrad","xepsn")
        emt_y = LegendItem("mm-mrad","yeps")
        emt_yn = LegendItem("mm-mrad","yepsn")
        emt_z = LegendItem("rad-MeV/u","zeps")
        emt_zn = LegendItem("rad-MeV/u","zepsn")
        tws_x_a = LegendItem(None,"xtwsa") # alpha
        tws_x_b = LegendItem("m/rad","xtwsb") # beta
        tws_x_g = LegendItem("rad/m","xtwsg") # gamma
        tws_y_a = LegendItem(None,"ytwsa") # ...
        tws_y_b = LegendItem("m/rad","ytwsb")
        tws_y_g = LegendItem("rad/m","ytwsg")
        tws_z_a = LegendItem(None,"ztwsa")
        tws_z_b = LegendItem("rad/MeV/u","ztwsb")
        tws_z_g = LegendItem("MeV/u/rad","ztwsg")
        cpl_xy = LegendItem(None,"cxy")
        cpl_xpy = LegendItem(None,"cxpy")
        cpl_xyp = LegendItem(None,"cxyp")
        cpl_xpyp = LegendItem(None,"cxpyp")
        last_caviphi0 = LegendItem("deg","last_caviphi0")
        brho = LegendItem("Tm","brho")

        cen_x.setText(0,"x")
        cen_xp.setText(0,"x'")
        cen_y.setText(0,"y")
        cen_yp.setText(0,"y'")
        cen_z.setText(0,"z")
        cen_zp.setText(0,"z'")
        rms_x.setText(0,"x")
        rms_xp.setText(0,"x'")
        rms_y.setText(0,"y")
        rms_yp.setText(0,"y'")
        rms_z.setText(0,"z")
        rms_zp.setText(0,"z'")
        emt_x.setText(0,"x")
        emt_xn.setText(0,"norm(x)")
        emt_y.setText(0,"y")
        emt_yn.setText(0,"norm(y)")
        emt_z.setText(0,"z")
        emt_zn.setText(0,"norm(z)")
        tws_x_a.setText(0,"x")
        tws_x_b.setText(0,"x")
        tws_x_g.setText(0,"x")
        tws_y_a.setText(0,"y")
        tws_y_b.setText(0,"y")
        tws_y_g.setText(0,"y")
        tws_z_a.setText(0,"z")
        tws_z_b.setText(0,"z")
        tws_z_g.setText(0,"z")
        cpl_xy.setText(0,"x-y")
        cpl_xpy.setText(0,"x'-y")
        cpl_xyp.setText(0,"x-y'")
        cpl_xpyp.setText(0,"x'-y'")
        last_caviphi0.setText(0,"Last Caviphi")
        brho.setText(0,"Brho")

        cen_x.setToolTip(0,"weight average of all charge states for x")
        cen_xp.setToolTip(0,"weight average of all charge states for x'")
        cen_y.setToolTip(0,"weight average of all charge states for y")
        cen_yp.setToolTip(0,"weight average of all charge states for y'")
        cen_z.setToolTip(0,"weight average of all charge states for phi")
        cen_zp.setToolTip(0,"weight average of all charge states for SE_k")
        rms_x.setToolTip(0,"general rms beam envelope for x")
        rms_xp.setToolTip(0,"general rms beam envelope for x'")
        rms_y.setToolTip(0,"general rms beam envelope for y")
        rms_yp.setToolTip(0,"general rms beam envelope for y'")
        rms_z.setToolTip(0,"general rms beam envelope for phi")
        rms_zp.setToolTip(0,"general rms beam envelope for SE_k")
        emt_x.setToolTip(0,"weight average of geometrical x emittance")
        emt_xn.setToolTip(0,"weight average of normalized x emittance")
        emt_y.setToolTip(0,"weight average of geometrical y emittance")
        emt_yn.setToolTip(0,"weight average of normalized y emittance")
        emt_z.setToolTip(0,"weight average of geometrical z emittance")
        emt_zn.setToolTip(0,"weight average of normalized z emittance")
        tws_x_a.setToolTip(0,"weight average of twiss alpha x")
        tws_x_b.setToolTip(0,"weight average of twiss beta x")
        tws_x_g.setToolTip(0,"weight average of twiss gamma x")
        tws_y_a.setToolTip(0,"weight average of twiss alpha y")
        tws_y_b.setToolTip(0,"weight average of twiss beta y")
        tws_y_g.setToolTip(0,"weight average of twiss gamma y")
        tws_z_a.setToolTip(0,"weight average of twiss alpha z")
        tws_z_b.setToolTip(0,"weight average of twiss beta z")
        tws_z_g.setToolTip(0,"weight average of twiss gamma z")
        cpl_xy.setToolTip(0,"weight average of normalized x-y coupling term")
        cpl_xpy.setToolTip(0,"weight average of normalized xp-y coupling term")
        cpl_xyp.setToolTip(0,"weight average of normalized x-yp coupling term")
        cpl_xpyp.setToolTip(0,"weight average of normalized xp-yp coupling term")
        last_caviphi0.setToolTip(0,"last RF cavity's driven phase")
        brho.setToolTip(0,"magnetic rigidity of reference charge state")

        ref_list = [ref_beta,ref_bg,ref_gamma,ref_IonEk,ref_IonEs,ref_IonQ,ref_IonW,ref_IonZ,ref_phis,ref_SampleIonK,ref_Brho]
        cen_list = [cen_x,cen_y,cen_z,cen_xp,cen_yp,cen_zp]
        rms_list = [rms_x,rms_y,rms_z,rms_xp,rms_yp,rms_zp]
        emt_list = [emt_x,emt_y,emt_z,emt_xn,emt_yn,emt_zn]
        tws_a_list = [tws_x_a,tws_y_a,tws_z_a]
        tws_b_list = [tws_x_b,tws_y_b,tws_z_b]
        tws_g_list = [tws_x_g,tws_y_g,tws_z_g]
        tws_list = tws_a_list + tws_b_list + tws_g_list
        cpl_list = [cpl_xy,cpl_xpy,cpl_xyp,cpl_xpyp]
        others_list = [last_caviphi0,brho]
        params_list = ref_list + cen_list + rms_list + emt_list + tws_list + cpl_list + others_list

        self.addTopLevelItem(reference)
        for param in ref_list:
            reference.addChild(param)

        self.addTopLevelItem(actual)
        actual.addChild(cen)
        for param in cen_list:
            cen.addChild(param)

        actual.addChild(rms)
        for param in rms_list:
            rms.addChild(param)

        actual.addChild(emt)
        for param in emt_list:
            emt.addChild(param)

        actual.addChild(tws)
        tws.addChild(tws_x)
        for param in tws_a_list:
            tws_x.addChild(param)
        tws.addChild(tws_y)
        for param in tws_b_list:
            tws_y.addChild(param)
        tws.addChild(tws_z)
        for param in tws_g_list:
            tws_z.addChild(param)

        actual.addChild(cpl)
        for param in cpl_list:
            cpl.addChild(param)

        actual.addChild(others)
        for param in others_list:
            others.addChild(param)

        for param in params_list:
            param.setFlags(param.flags() | QtCore.Qt.ItemIsUserCheckable)
            param.setCheckState(0, QtCore.Qt.Unchecked)


        self.itemChanged.connect(self.handle_checkboxes)

    def handle_checkboxes(self,item,col):
        if item.checkState(col) == 0 and item.line:
            item.line.set_visible(False)
        elif item.checkState(col) != 0 and item.line:
            item.line.set_visible(True)
        else:
            r,s = self.graph.model.run(monitor='all') # replace variables with something more descriptive
            data = self.graph.model.collect_data(r,'pos',item.pseudo)
            self.graph.plot_loc()
            item.line = self.graph.plot_line(data['pos'],data[item.pseudo])


        self.graph.ax.relim(visible_only=True)
        self.graph.ax.autoscale_view(True,True,True)
        item.line.figure.canvas.draw()



