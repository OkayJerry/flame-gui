from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from flame_utils import ModelFlame, PlotLat
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
from classes.utility import WorkspaceOneItem
from PyQt5 import QtGui
import numpy as np

class FmMplLine(Line2D): # only purpose as for now is to differentiate lines I've added from Line2D
    def __init__(self, xdata, ydata):
        super().__init__(xdata, ydata)

class FmMplCanvas(FigureCanvas):
    def __init__(self,items,parent=None,filename=None):
        super(FigureCanvas,self).__init__(parent)
        self.model = None
        self.legend = None
        self.filename = None
        self.axes = []
        self.base_ax = None
        self.colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728']
                    # [   'C0'  ,   'C1'  ,   'C2'  ,   'C3'  ] https://matplotlib.org/3.5.0/users/prev_whats_new/dflt_style_changes.html#colors-in-default-property-cycle

        self.figure.tight_layout()

    def set_model(self,filename):
        self.filename = filename
        self.model = ModelFlame(filename)

    def update_lines(self):
        active_items = self.legend.getCheckedItems()
        r,s = self.model.run(monitor='all')
        for item in active_items:
            data = self.model.collect_data(r,'pos',item.kwrd)
            item.line.set_data(data['pos'],data[item.kwrd])

        self._remove_lat()
        self._plot_lat()

        for ax in self.axes:
            ax.relim()
            ax.autoscale_view()

        self.figure.tight_layout()
        self.figure.canvas.draw()
            

        


    def plot_item(self,item):
        r,s = self.model.run(monitor='all')
        data = self.model.collect_data(r,'pos',item.kwrd)
        item.line = FmMplLine(data['pos'],data[item.kwrd])
        item.line.set_label(item.kwrd)
        if item.dashed == True:
            item.line.set_linestyle('dashed')
        self._set_line_color(item.line)

        ax = self._get_axis_with_ylabel(item.y_unit)
        if ax != None:
            ax.add_line(item.line)
        else:
            if self.base_ax == None: # initial call of plot_item from blank canvas
                ax = self.figure.subplots()
                self.base_ax = ax
            else:
                ax = self.base_ax.twinx()
                self._set_axis_location(ax)
                base_xmargin,_ = self.base_ax.margins()
                ax.margins(base_xmargin,0.425)
            ax.add_line(item.line)
            self.axes.append(ax)
        ax.set_ylabel(item.y_unit) # if the axis already is that unit, the y-label will just remain the same
        
        self._remove_legend()
        self._create_legend()

        self._remove_lat()
        self._plot_lat()

        ax.relim()
        ax.autoscale_view(True,True,True)

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def _set_line_color(self,line):
        taken = []
        for ax in self.axes:
            for ln in ax.lines:
                if type(ln) == FmMplLine: # filters out locational plot
                    taken.append(ln.get_color())
        available = list(set(self.colors) - set(taken))
        n_color = available[0]
        line.set_color(n_color)

    def _get_axis_with_ylabel(self,ylabel):
        for ax in self.axes:
            if ylabel == ax.get_ylabel():
                return ax
        return None

    def _set_axis_location(self,axis): # occurs prior to the appending of current axis
        if len(self.axes) == 1:
            axis.yaxis.set_ticks_position('right')
            axis.spines.left.set_position(('outward',0))
            axis.yaxis.set_label_position('right')
        elif len(self.axes) == 2:
            axis.yaxis.set_ticks_position('left')
            axis.spines.left.set_position(('outward',60))
            axis.yaxis.set_label_position("left")
        else:
            axis.yaxis.set_ticks_position('right')
            axis.spines.right.set_position(('outward',60))
            axis.yaxis.set_label_position('right')

    def _create_legend(self):
        patches = []
        topmost_ax = self.axes[-1]
        for ax in self.axes:
            for ln in ax.lines:
                if type(ln) == FmMplLine:
                    patch = mpatches.Patch(color=ln.get_color(),label=ln.get_label())
                    patches.append(patch)
        topmost_ax.legend(handles=patches,loc='upper left')

    def _remove_legend(self):
        if len(self.axes) > 1: # new axis just added
            if self.axes[-2].get_legend(): # since new axis was just added, must go back 2
                prev_legend = self.axes[-2].get_legend()
            else: # sometimes an axis isn't added, so you just need to remove the one in the current axis
                prev_legend = self.axes[-1].get_legend()
            prev_legend.remove()


    def remove_item(self,item):
        item.line.remove()
        self._remove_legend()
        self._remove_lat()

        for ax in self.axes:
            if len(ax.lines) == 0:
                if ax == self.base_ax:
                    self.base_ax = None
                ax.remove()
                self.axes.remove(ax)
                if len(self.axes) != 0 and self.base_ax == None: # must reassign base_ax for PlotLat()
                    self.base_ax = self.axes[0]
                    # setting to defaults
                    self.base_ax.margins(0.05,0.05)
                    self.base_ax.yaxis.set_ticks_position('left')
                    self.base_ax.spines.left.set_position(('outward',0))
                    self.base_ax.yaxis.set_label_position('left')

        if len(self.axes) != 0: # no axes = no legend
            self._create_legend()

        if self.base_ax:
            self._plot_lat()

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def _plot_lat(self):
        ymax,ymin = self._get_ymaxmin(self.base_ax)
        yrange = ymax - ymin
        frac_yrange = yrange * 0.1

        if ymax != ymin: # not a horizonal line
            ycen_eq = ymin - frac_yrange - frac_yrange * 0.5
            yscl_eq = frac_yrange
        else:
            ycen_eq = ymax - 1
            yscl_eq = 1 * 0.09

        lattice = PlotLat(self.model.machine, auto_scaling=False, starting_offset=0)
        lattice.generate(ycen=ycen_eq, yscl=yscl_eq, legend=False, option=False, axes=self.base_ax) # locational plot created

        self.base_ax.relim()
        self.base_ax.autoscale_view(True,True,True)

    def _remove_lat(self):
        for ln in reversed(self.base_ax.lines): # reversed necessary
            if type(ln) != FmMplLine:
                ln.remove()
        [p.remove() for p in reversed(self.base_ax.patches)] # reversed necessary

        if self.base_ax:
            self.base_ax.relim()
            self.base_ax.autoscale_view(True,True,True)

    def _get_ymaxmin(self,axis):
        ymax = -np.inf
        ymin = np.inf
        for ln in axis.lines:
            if type(ln) == FmMplLine:
                ydata = ln.get_ydata()
                ln_ymax = max(ydata)
                ln_ymin = min(ydata)
                if ln_ymax > ymax:
                    ymax = ln_ymax
                if ln_ymin < ymin:
                    ymin = ln_ymin
        return ymax,ymin