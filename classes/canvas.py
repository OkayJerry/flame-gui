from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from flame_utils import ModelFlame, PlotLat
from matplotlib.lines import Line2D
import numpy as np

class FmMplCanvas(FigureCanvas):
    def __init__(self,parent=None,filename=None,width=5,height=3):
        super(FigureCanvas,self).__init__(parent)
        self.fig = Figure(figsize=(width,height))
        self.ax = self.figure.subplots()
        self.model = None
        self.filename = None

        self.fig.tight_layout()

 

    def set_model(self,filename):
        self.filename = filename
        self.model = ModelFlame(filename)


    def plot_line(self,x_data,y_data):
        line = Line2D(x_data,y_data)
        self.ax.add_line(line)
        self.ax.relim()
        self.ax.autoscale_view(True,True,True)
        line.figure.canvas.draw()
        return line

    def plot_loc(self):
        lattice = PlotLat(self.model.machine, auto_scaling=False, starting_offset=0)
        lattice.generate(ycen=-5, yscl=3, legend=False, option=False, axes=self.ax)
        # self.ax.figure.canvas.draw()
