from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from flame_utils import ModelFlame, hplot

class FmMplCanvas(FigureCanvas):
    def __init__(self,parent=None,filename=None,width=5,height=3):
        super(FigureCanvas,self).__init__(parent)
        self.fig = Figure(figsize=(width,height))
        self.ax = self.figure.subplots()
        self.lines = []
        self.model = None

        self.fig.tight_layout()
 

    def set_model(self,filename):
        self.model = ModelFlame(filename)

 
    def plot(self,x_data,y_data):
        line = self.ax.plot(x_data,y_data)

