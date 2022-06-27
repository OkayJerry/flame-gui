from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from flame_utils import ModelFlame, hplot
import matplotlib as mpl
import numpy as np

class FmMplPhaseSpaceCanvas(FigureCanvas):
    def __init__(self,parent=None):
        super(FigureCanvas,self).__init__(parent)
        axes = self.figure.subplots(1,2)
        self.x_axes = axes[0]
        self.y_axes = axes[1]
        
        for ax in axes:
            ax.margins(0.05,10)
            ax.set_box_aspect(1)
            ax.grid()
            
        self.x_axes.set_xlabel('x [mm]')
        self.x_axes.set_ylabel('xp [mrad]')
        self.y_axes.set_xlabel('y [mm]')
        self.y_axes.set_ylabel('yp [mrad]')

    def tws2cov(self,alpha,beta,eps): # Function to convert Twiss parameters to Sigma-matrix (covariance)
        mat = np.zeros([2,2])
        mat[0,0] = beta*eps
        mat[0,1] = mat[1,0] = -alpha*eps
        mat[1,1] = (1.0 + alpha*alpha)/beta*eps
        return mat

    def ellipse(self,cen,cov,facecolor='none',**kws): # Function to generate phase ellipse from centroid and covariance
        # calculate eigenequation to transform the ellipse
        v, w = np.linalg.eigh(cov)
        u = w[0]/np.linalg.norm(w[0])
        ang = np.arctan2(u[1], u[0])*180.0/np.pi
        v = 2.0*np.sqrt(v)
        ell = mpl.patches.Ellipse(cen, v[0], v[1], 180+ang, facecolor=facecolor, **kws)
        return ell

    def phase_ellipse(self,d,idx,coor,bmstate,**kws):
        if not coor in ['x', 'y', 'z']:
            return None
        cen   = np.array([d[coor+'cen'][idx], d[coor+'pcen'][idx]])
        twsa = d[coor+'twsa'][idx]
        twsb = d[coor+'twsb'][idx]
        eps  = d[coor+'eps'][idx]
        cov = self.tws2cov(twsa, twsb, eps)
        return self.ellipse(cen, cov, **kws), np.array([cen[0], cen[1], twsa, twsb, eps])

    def plot_element(self,element_name):
        model = self.root_graph.model

        [p.remove() for p in reversed(self.x_axes.patches)]
        [p.remove() for p in reversed(self.y_axes.patches)]

        r, s = model.run(monitor='all')
        d = model.collect_data(r, 'xcen', 'ycen', 'xpcen', 'ypcen', 'xtwsa', 'ytwsa', 'xtwsb', 'ytwsb', 'xeps', 'yeps')    
        idx = model.find(element_name)[0]

        # 'x' graph
        el, x_res = self.phase_ellipse(d,idx,'x',r[idx][1],edgecolor='b')
        self.x_axes.add_patch(el)
        self.x_axes.relim()
        self.x_axes.autoscale_view()

        # 'y' graph
        el, y_res = self.phase_ellipse(d,idx,'y',r[idx][1],edgecolor='r')
        self.y_axes.add_patch(el)
        self.y_axes.relim()
        self.y_axes.autoscale_view()

        self.figure.canvas.draw_idle()
        self.figure.tight_layout()
        return x_res, y_res





class PhaseSpaceWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Phase Space Plot')
        layout = QtWidgets.QVBoxLayout()
        labels = ['Centroid Position [mm]','Centroid Momentum [mrad]','Twiss Alpha','Twiss Beta [m/rad]','Geom. Emittance [mm-mrad]']

        self.elementBox = QtWidgets.QComboBox()
        self.graphs = FmMplPhaseSpaceCanvas()
        self.tableView = QtWidgets.QTableWidget(5,3)

        self.elementBox.currentTextChanged.connect(self.plot_current_element)

        self.tableView.setHorizontalHeaderLabels(['','x','y'])
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.verticalHeader().hide()
        for i in range(self.tableView.rowCount()):
            label = labels[i]
            item = QtWidgets.QTableWidgetItem()
            item.setText(label)
            self.tableView.setItem(i,0,item)

        layout.addWidget(self.elementBox)
        layout.addWidget(self.graphs)
        layout.addWidget(self.tableView)

        self.setLayout(layout)

    def link(self,graph):
        self.graphs.root_graph = graph

    def plot_current_element(self):
        x_res, y_res = self.graphs.plot_element(self.elementBox.currentText())

        for i in range(self.tableView.rowCount()):
            x_num = x_res[i]
            y_num = y_res[i]
            x_item = QtWidgets.QTableWidgetItem()
            y_item = QtWidgets.QTableWidgetItem()
            x_item.setText(str(x_num))
            y_item.setText(str(y_num))

            self.tableView.setItem(i,1,x_item)
            self.tableView.setItem(i,2,y_item)
        



    def open(self):
        self.elementBox.blockSignals(True)
        model = self.graphs.root_graph.model

        self.elementBox.clear()
        names = model.get_all_names()
        names = names[1:]

        self.elementBox.addItems(names)

        self.plot_current_element()

        self.show()
        self.elementBox.blockSignals(False)
        