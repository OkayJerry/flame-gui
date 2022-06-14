from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from flame_utils import ModelFlame, PlotLat
from matplotlib.lines import Line2D
import numpy as np

class FmMplCanvas(FigureCanvas):
    def __init__(self,parent=None,filename=None):
        super(FigureCanvas,self).__init__(parent)
        self.main_axis = self.figure.subplots()
        self.model = None
        self.filename = None
        self.kwrd_axes = {}
        self.vis_axes_cnt = 0

        self.figure.tight_layout()

 

    def set_model(self,filename):
        self.filename = filename
        self.model = ModelFlame(filename)


    def plot_line(self,x_data,y_data):
        line = Line2D(x_data,y_data)
        self.main_axis.add_line(line)
        self.main_axis.relim(visible_only=True)
        self.main_axis.autoscale_view(True,True,True)
        line.figure.canvas.draw()
        return line

    def plot_loc(self):
        lattice = PlotLat(self.model.machine, auto_scaling=False, starting_offset=0)
        lattice.generate(ycen=-5, yscl=3, legend=False, option=False, axes=self.main_axis)
        # self.main_axis.figure.canvas.draw()

    def plot(self):
        kwrds = [
            "ref_beta",
            "ref_bg",
            "ref_gamma",
            "ref_IonEk",
            "ref_IonEs",
            "ref_IonQ",
            "ref_IonW",
            "ref_IonZ",
            "ref_phis",
            "ref_SampleIonK",
            "ref_Brho",
            "xcen",
            "xpcen",
            "ycen",
            "ypcen",
            "zcen",
            "zpcen",
            "xrms",
            "xprms",
            "yrms",
            "yprms",
            "zrms",
            "zprms",
            "xeps",
            "xepsn",
            "yeps",
            "yepsn",
            "zeps",
            "zepsn",
            "xtwsa", # alpha
            "xtwsb", # beta
            "xtwsg", # gamma
            "ytwsa", # ...
            "ytwsb",
            "ytwsg",
            "ztwsa",
            "ztwsb",
            "ztwsg",
            "cxy",
            "cxpy",
            "cxyp",
            "cxpyp",
            "last_caviphi0",
            # "brho" # cannot use
        ]
        colors = [

        ]

        r,s = self.model.run(monitor='all')
        for i in range(len(kwrds)):
            kwrd = kwrds[i]
            if i == 0:
                axis = self.main_axis
            else:
                axis = self.main_axis.twinx()

            self.model.run(monitor='all')
            data = self.model.collect_data(r,'pos',kwrd)
            line = Line2D(data['pos'],data[kwrd])
            axis.add_line(line)
            # line.set_visible(False)
            axis.set_visible(False)
            axis.relim()
            axis.autoscale_view(True,True,True)
            line.figure.canvas.draw()

            # self.lines[kwrd] = line
            self.kwrd_axes[kwrd] = axis
            

            
