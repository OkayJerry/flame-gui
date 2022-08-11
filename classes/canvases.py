import globals as glb
import matplotlib.patches as mpatches
import numpy as np
from flame_utils import PlotLat
from matplotlib.backends.backend_qtagg import FigureCanvas
import matplotlib.pyplot as plt

from classes.utility import Line


class MainCanvas(FigureCanvas):
    def __init__(self):
        super().__init__()
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        self.base_ax = None
        self.axes = []
        self.lines = {}
        self.custom_colors = {}

    def plotParameter(self, param):
        param_unit = glb.model.get_parameter_unit(param)
        ax = self.getAxisWithYLabel(param_unit)
        ln = self.createLine(param)
        
        if ax:
            ax.add_line(ln)
        else:
            if self.base_ax is None:
                ax = self.figure.subplots()
                self.base_ax = ax
                self.base_ax.set_xlabel('pos [m]')
            else:
                ax = self.base_ax.twinx()
                self.setAxisLocation(ax)
                base_xmargin, _ = self.base_ax.margins()
                ax.margins(base_xmargin, 0.425)
            ax.add_line(ln)
            self.axes.append(ax)
            
        self.lines[param] = ln
        ax.set_ylabel(param_unit)

        self.removeLegend()
        self.createLegend()

        self.removeLocation()
        self.plotLocation()

        ax.relim()
        ax.autoscale()
        
        self.figure.tight_layout()
        self.draw_idle()
        
    def removeParameter(self, param):
        self.lines[param].remove()
        self.lines.pop(param)
        self.removeLegend()
        self.removeLocation()
        
        for ax in self.axes:
            if len(ax.lines) == 0:
                if ax == self.base_ax:
                    if len(self.axes) == 1:
                        self.base_ax = None
                        ax.remove()
                        self.axes.remove(ax)
                        del ax  # because any left over reference will remain on the canvas: https://stackoverflow.com/questions/4981815/how-to-remove-lines-in-a-matplotlib-plot
                    else:
                        above_axis = self.axes[1]
                        for ln in above_axis.get_lines():
                            above_axis.lines.remove(ln)
                            n_ln = self.createLine(list(self.lines.keys())[list(self.lines.values()).index(ln)]) # getting 'dict' key from value
                            self.base_ax.add_line(n_ln)
                            self.lines[n_ln.param] = n_ln
                            del ln  # necessary

                        y_unit = above_axis.yaxis.get_label().get_text()
                        self.base_ax.set_ylabel(y_unit)
                        above_axis.remove()
                        self.axes.remove(above_axis)
                        del above_axis
                else:
                    ax.remove()
                    self.axes.remove(ax)
                    del ax  # necessary

        self.updateAxisLocation()

        for ax in self.axes:
            ax.relim()
            ax.autoscale()

        if len(self.axes) != 0:  # no axes = no legend
            self.createLegend()

        self.plotLocation()

        self.figure.tight_layout()
        self.draw_idle()
            
    def getAxisWithYLabel(self, y_label):
        for ax in self.axes:
            if y_label == ax.get_ylabel():
                return ax
        return None
    
    def setAxisLocation(self, axis):
        if len(self.axes) == 1:
            axis.yaxis.set_ticks_position('right')
            axis.spines.left.set_position(('outward', 0))
            axis.spines.right.set_position(('outward', 0))
            axis.yaxis.set_label_position('right')
        elif len(self.axes) == 2:
            axis.yaxis.set_ticks_position('left')
            axis.spines.left.set_position(('outward', 70))
            axis.spines.right.set_position(('outward', 0))
            axis.yaxis.set_label_position("left")
        else:
            axis.yaxis.set_ticks_position('right')
            axis.spines.left.set_position(('outward', 0))
            axis.spines.right.set_position(('outward', 70))
            axis.yaxis.set_label_position('right')
    
    def createLine(self, param):
        r, _ = glb.model.run(monitor='all')
        data = glb.model.collect_data(r, 'pos', param)
        ln = Line(data['pos'], data[param], param)
        ln.set_label(param)
        if param in glb.model.get_prime_parameters():
            ln.set_linestyle('dashed')
        self.setLineColor(param, ln)
        return ln

    def createLegend(self):
        patches = []
        topmost_ax = self.axes[-1]
        for ax in self.axes:
            for ln in ax.lines:
                if isinstance(ln, Line):
                    patch = mpatches.Patch(color=ln.get_color(), label=ln.get_label())
                    patches.append(patch)
        legend = topmost_ax.legend(handles=patches, loc='upper left')
        legend.set_draggable(True)

    def removeLegend(self):
        if len(self.axes) > 1:  # new axis just added
            if self.axes[-2].get_legend():  # since new axis was just added, must go back 2
                prev_legend = self.axes[-2].get_legend()
            else:  # sometimes an axis isn't added, so you just need to remove the one in the current axis
                prev_legend = self.axes[-1].get_legend()
            prev_legend.remove()
        
    def setLineColor(self, param, line):
        taken = []
        for ln in self.lines.values():
            taken.append(ln.get_color())
        available = list(set(self.colors) - set(taken))
        n_color = available[0]

        if param not in self.custom_colors:
            line.set_color(n_color)
        else:
            line.set_color(self.custom_colors[param])

    def updateAxisLocation(self):
        for i in range(len(self.axes)):
            axis = self.axes[i]
            if i == 0:
                axis.yaxis.set_ticks_position('left')
                axis.spines.left.set_position(('outward', 0))
                axis.spines.right.set_position(('outward', 0))
                axis.yaxis.set_label_position('left')
            elif i == 1:
                axis.yaxis.set_ticks_position('right')
                axis.spines.left.set_position(('outward', 0))
                axis.spines.right.set_position(('outward', 0))
                axis.yaxis.set_label_position('right')
            elif i == 2:
                axis.yaxis.set_ticks_position('left')
                axis.spines.left.set_position(('outward', 70))
                axis.spines.right.set_position(('outward', 0))
                axis.yaxis.set_label_position("left")
            else:
                axis.yaxis.set_ticks_position('right')
                axis.spines.left.set_position(('outward', 0))
                axis.spines.right.set_position(('outward', 70))
                axis.yaxis.set_label_position('right')

    def plotLocation(self):
        if self.base_ax:
            ymax, ymin = self.getYMaxMin(self.base_ax)
            yrange = ymax - ymin
            frac_yrange = yrange * 0.1

            if ymax != ymin:  # not a horizonal line
                ycen_eq = ymin - frac_yrange - frac_yrange * 0.5
                yscl_eq = frac_yrange
            else:
                ycen_eq = ymax - 1
                yscl_eq = 1 * 0.09

            lattice = PlotLat(glb.model.machine, auto_scaling=False, starting_offset=0)
            lattice.generate(ycen=ycen_eq, yscl=yscl_eq, legend=False, option=False, axes=self.base_ax)  # locational plot created

            self.base_ax.relim()
            self.base_ax.autoscale_view(True, True, True)

    def removeLocation(self):
        if self.base_ax:
            for ln in reversed(self.base_ax.lines):  # reversed necessary
                if not isinstance(ln, Line):
                    ln.remove()
            [p.remove() for p in reversed(self.base_ax.patches)]  # reversed necessary

            self.base_ax.relim()
            self.base_ax.autoscale_view(True, True, True)

    def getYMaxMin(self, axis):
        ymax = -np.inf
        ymin = np.inf
        for ln in axis.lines:
            if isinstance(ln, Line):
                ydata = ln.get_ydata()
                ln_ymax = max(ydata)
                ln_ymin = min(ydata)
                if ln_ymax > ymax:
                    ymax = ln_ymax
                if ln_ymin < ymin:
                    ymin = ln_ymin
        return ymax, ymin

    def refresh(self):
        self.figure.clear()
        self.axes.clear()
        self.lines.clear()
        self.base_ax = None
        
        param_select = self.parent().parent().parent().parent().param_select
        active_items = param_select.getCheckedItems(param_select.invisibleRootItem())
        for item in active_items:
            param = param_select.convertItemIntoParam(item)
            self.plotParameter(param)

        for ax in self.axes:
            ax.relim()
            ax.autoscale()

        self.figure.tight_layout()
        self.draw_idle()


class PhaseSpaceCanvas(FigureCanvas):
    def __init__(self):
        super().__init__()
        plt.subplots_adjust(left=2.0, right=2.1, top=2.1, bottom=2.0)
        subplots = self.figure.subplots(1, 2)
        self.left_subplot = subplots[0]
        self.right_subplot = subplots[1]
        
        for subplot in subplots:
            subplot.margins(0.05, 10)
            subplot.set_box_aspect(1)
            subplot.grid()

        self.left_subplot.set_xlabel('x [mm]')
        self.left_subplot.set_ylabel('xp [mrad]')
        self.right_subplot.set_xlabel('y [mm]')
        self.right_subplot.set_ylabel('yp [mrad]')
        self.figure.tight_layout()
        
    def plotElement(self, element_name):
        r, _ = glb.model.run(monitor='all')
        data = glb.model.collect_data(r, 'xcen', 'ycen', 'xpcen', 'ypcen', 'xtwsa', 'ytwsa', 'xtwsb', 'ytwsb', 'xeps', 'yeps')
        idx = glb.model.find(element_name)[0]
        
        # 'x' graph
        el, x_res = self.phaseEllipse(data, idx, 'x', edgecolor='b')
        self.left_subplot.add_patch(el)
        self.left_subplot.margins(0.05, 0.05)  # necessary for patches?
        self.left_subplot.relim()
        self.left_subplot.autoscale()

        # 'y' graph
        el, y_res = self.phaseEllipse(data, idx, 'y', edgecolor='r')
        self.right_subplot.add_patch(el)
        self.right_subplot.margins(0.05, 0.05)  # necessary for patches?
        self.right_subplot.relim()
        self.right_subplot.autoscale()

        self.draw_idle()
        self.figure.tight_layout()
        return x_res, y_res

    def clearSubplots(self):
        [p.remove() for p in reversed(self.left_subplot.patches)]
        [p.remove() for p in reversed(self.right_subplot.patches)]

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
        ell = mpatches.Ellipse(cen, v[0], v[1], 180 + ang, facecolor=facecolor, **kws)
        return ell

    def phaseEllipse(self, d, idx, coor, **kws):
        if coor not in ['x', 'y', 'z']:
            return None
        cen = np.array([d[coor + 'cen'][idx], d[coor + 'pcen'][idx]])
        twsa = d[coor + 'twsa'][idx]
        twsb = d[coor + 'twsb'][idx]
        eps = d[coor + 'eps'][idx]
        cov = self.tws2cov(twsa, twsb, eps)
        return self.ellipse(cen, cov, **kws), np.array([cen[0], cen[1], twsa, twsb, eps])