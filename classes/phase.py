import matplotlib as mpl
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import classes.globals as glb


class FmMplPhaseSpaceCanvas(FigureCanvas):
    def __init__(self, parent=None):
        super(FigureCanvas, self).__init__(parent)
        axes = self.figure.subplots(1, 2)
        self.x_axes = axes[0]
        self.y_axes = axes[1]

        for ax in axes:
            ax.margins(0.05, 10)
            ax.set_box_aspect(1)
            ax.grid()

        self.x_axes.set_xlabel('x [mm]')
        self.x_axes.set_ylabel('xp [mrad]')
        self.y_axes.set_xlabel('y [mm]')
        self.y_axes.set_ylabel('yp [mrad]')
        self.figure.tight_layout()

    # Function to convert Twiss parameters to Sigma-matrix (covariance)
    def tws2cov(self, alpha, beta, eps):
        mat = np.zeros([2, 2])
        mat[0, 0] = beta * eps
        mat[0, 1] = mat[1, 0] = -alpha * eps
        mat[1, 1] = (1.0 + alpha * alpha) / beta * eps
        return mat

    # Function to generate phase ellipse from centroid and covariance
    def ellipse(self, cen, cov, facecolor='none', **kws):
        # calculate eigenequation to transform the ellipse
        v, w = np.linalg.eigh(cov)
        u = w[0] / np.linalg.norm(w[0])
        ang = np.arctan2(u[1], u[0]) * 180.0 / np.pi
        v = 2.0 * np.sqrt(v)
        ell = mpl.patches.Ellipse(
            cen,
            v[0],
            v[1],
            180 + ang,
            facecolor=facecolor,
            **kws)
        return ell

    def phaseEllipse(self, d, idx, coor, bmstate, **kws):
        if coor not in ['x', 'y', 'z']:
            return None
        cen = np.array([d[coor + 'cen'][idx], d[coor + 'pcen'][idx]])
        twsa = d[coor + 'twsa'][idx]
        twsb = d[coor + 'twsb'][idx]
        eps = d[coor + 'eps'][idx]
        cov = self.tws2cov(twsa, twsb, eps)
        return self.ellipse(
            cen, cov, **kws), np.array([cen[0], cen[1], twsa, twsb, eps])

    def plotElement(self, element_name):
        [p.remove() for p in reversed(self.x_axes.patches)]
        [p.remove() for p in reversed(self.y_axes.patches)]

        r, s = glb.model.run(monitor='all')
        d = glb.model.collect_data(
            r,
            'xcen',
            'ycen',
            'xpcen',
            'ypcen',
            'xtwsa',
            'ytwsa',
            'xtwsb',
            'ytwsb',
            'xeps',
            'yeps')
        idx = glb.model.find(element_name)[0]

        # 'x' graph
        el, x_res = self.phaseEllipse(d, idx, 'x', r[idx][1], edgecolor='b')
        self.x_axes.add_patch(el)
        self.x_axes.margins(0.05, 0.05)  # necessary for patches?
        self.x_axes.relim()
        self.x_axes.autoscale()

        # 'y' graph
        el, y_res = self.phaseEllipse(d, idx, 'y', r[idx][1], edgecolor='r')
        self.y_axes.add_patch(el)
        self.y_axes.margins(0.05, 0.05)  # necessary for patches?
        self.y_axes.relim()
        self.y_axes.autoscale()

        self.figure.canvas.draw_idle()
        self.figure.tight_layout()
        return x_res, y_res


class PhaseSpaceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Phase Space Plot')
        layout = QVBoxLayout()
        labels = [
            'Centroid Position [mm]',
            'Centroid Momentum [mrad]',
            'Twiss Alpha',
            'Twiss Beta [m/rad]',
            'Geom. Emittance [mm-mrad]']

        search_ws = QWidget()
        search_ws.setLayout(QHBoxLayout())

        self.element_box = QComboBox()
        self.type_box = QComboBox()
        self.graphs = FmMplPhaseSpaceCanvas()
        self.table_view = QTableWidget(5, 3)

        for word in [
            'all',
            'magnetic',
            'quadrupole',
            'drift',
            'orbtrim',
            'marker',
                'sbend']:
            self.type_box.addItem(word)
        self.type_box.currentTextChanged.connect(self.filter)
        self.element_box.currentTextChanged.connect(self.plotCurrentElement)

        self.table_view.setAlternatingRowColors(True)
        self.table_view.setHorizontalHeaderLabels(['', 'x', 'y'])
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_view.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setFocusPolicy(Qt.NoFocus)
        self.table_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_view.verticalHeader().hide()
        for i in range(self.table_view.rowCount()):
            label = labels[i]
            item = QTableWidgetItem()
            item.setText(label)
            self.table_view.setItem(i, 0, item)

        search_ws.layout().addWidget(self.element_box)
        search_ws.layout().addWidget(self.type_box)
        layout.addWidget(search_ws)
        layout.addWidget(self.graphs)
        layout.addWidget(self.table_view)

        self.setLayout(layout)
        self.setMinimumSize(683, 640)

    def link(self, graph):
        self.graphs.root_graph = graph

    def filter(self):
        self.element_box.blockSignals(True)

        self.element_box.clear()
        elements = glb.model.get_element(name=glb.model.get_all_names())
        elements = elements[1:]  # skip header
        for element in elements:
            n = element['properties']['name']
            t = element['properties']['type']
            if t == self.type_box.currentText() or self.type_box.currentText() == 'all':
                self.element_box.addItem(n)
            elif self.type_box.currentText() == 'magnetic':
                if t != 'drift':
                    self.element_box.addItem(n)
        if len(elements) != 0:
            self.plotCurrentElement()

        self.element_box.blockSignals(False)

    def plotCurrentElement(self):
        try:
            x_res, y_res = self.graphs.plotElement(
                self.element_box.currentText())
        except BaseException:
            self.element_box.removeItem(
                self.element_box.findText(
                    self.element_box.currentText()))
            names = glb.model.get_all_names()
            self.element_box.setCurrentText(
                names[1])  # skip header (0th) element
            x_res, y_res = self.graphs.plotElement(
                self.element_box.currentText())

        for i in range(self.table_view.rowCount()):
            x_num = x_res[i]
            y_num = y_res[i]
            x_item = QTableWidgetItem()
            y_item = QTableWidgetItem()
            x_item.setText(str(x_num))
            y_item.setText(str(y_num))

            self.table_view.setItem(i, 1, x_item)
            self.table_view.setItem(i, 2, y_item)

    def open(self):
        self.element_box.blockSignals(True)

        self.setElementBox()
        if len(glb.model.get_all_names()[1:]) != 0:
            self.plotCurrentElement()
            
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.show()

        self.element_box.blockSignals(False)

    def setElementBox(self):
        self.element_box.blockSignals(True)
        self.element_box.clear()
        names = glb.model.get_all_names()
        names = names[1:]
        self.element_box.addItems(names)
        if len(names) != 0:
            self.plotCurrentElement()
        self.element_box.blockSignals(False)
