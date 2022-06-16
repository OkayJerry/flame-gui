from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from flame_utils import ModelFlame, PlotLat
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
from classes.utility import WorkspaceOneItem
from PyQt5 import QtGui
import numpy as np

class FmMplCanvas(FigureCanvas):
    def __init__(self,items,parent=None,filename=None):
        super(FigureCanvas,self).__init__(parent)
        self.model = None
        self.filename = None
        self.kwrd_axes = {}
        self.vis_axes_cnt = 0
        self.items = items
        self.axes = []
        self.colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728']
                    # [   'C0'  ,   'C1'  ,   'C2'  ,   'C3'  ] https://matplotlib.org/3.5.0/users/prev_whats_new/dflt_style_changes.html#colors-in-default-property-cycle

        # axes
        self.base_ax = self.figure.subplots()
        self.base_ax.set_xlabel('pos [m]')
        self.base_ax.set_visible(False)
        self.axes.append(self.base_ax)
        for _ in range(3):
            ax = self.base_ax.twinx()
            ax.set_visible(False)
            self.axes.append(ax)

        self.figure.tight_layout()

 

    def set_model(self,filename):
        self.filename = filename
        self.model = ModelFlame(filename)

    def plot_loc(self):
        y_min,y_max = self.get_ylim()
        # print(y_min,y_max)


        lattice = PlotLat(self.model.machine, auto_scaling=False, starting_offset=0)
        lattice.generate(ycen=-5, yscl=3, legend=False, option=False, axes=self.main_axis)

    def plot_item(self,item):
        r,s = self.model.run(monitor='all')
        data = self.model.collect_data(r,'pos',item.kwrd)
        item.line = Line2D(data['pos'],data[item.kwrd])
        item.line.set_label(item.kwrd)
        if item.dashed == True:
            item.line.set_linestyle('dashed')
        self._plot_line(item.line,item.y_unit)
        self.handle_legend()
        self.update_axis()
        self.figure.tight_layout()
        self.figure.canvas.draw()

    def _plot_line(self,line,unit):
        self.choose_color(line)
        for ax in self.axes:
            if not ax.get_visible():
                ax.set_ylabel(unit)
                ax.add_line(line)
                ax.set_visible(True)
                ax.relim()
                ax.autoscale_view(True,True,True)
                line.figure.canvas.draw()
                break
            elif unit == ax.get_ylabel():
                ax.add_line(line)
                ax.relim()
                ax.autoscale_view(True,True,True)
                break
        
        line.figure.canvas.draw()

    def handle_legend(self):
        patches = []
        topmost_ax = self.axes[0]
        for ax in self.axes:
            if ax.get_legend():
                ax.get_legend().remove()
            for line in ax.lines:
                patch = mpatches.Patch(color=line.get_color(),label=line.get_label())
                patches.append(patch)
            if ax.get_visible():
                topmost_ax = ax
        topmost_ax.legend(handles=patches,loc="upper left")

    def remove_item(self,item):
        self._remove_line(item.line)
        self.update_axis()
        self.handle_legend()
        self.figure.tight_layout()
        self.figure.canvas.draw()

    def _remove_line(self,line):
        for ax in self.axes:                   
            if line in ax.lines and len(ax.lines) == 1:
                # self.axes.append(self.axes.pop(self.axes.index(ax)))
                ax.set_visible(False)
                break
        line.remove()

    def choose_color(self,line):
        taken = []
        for ax in self.axes:
            for ln in ax.lines:
                taken.append(ln.get_color())
        available = list(set(self.colors) - set(taken))
        n_color = available[0]
        line.set_color(n_color)


    def get_visible_axes_cnt(self):
        cnt = 0
        for ax in self.axes:
            if ax.get_visible():
                cnt += 1
        return cnt

    def get_visible_line_cnt(self):
        cnt = 0
        for ax in self.axes:
            for line in ax.lines:
                if line.get_visible():
                    cnt += 1
        return cnt

    def update_axis(self):
        vis_so_far = 0 
        for ax in self.axes:
            if ax != self.base_ax and len(self.base_ax.lines) == 0 and len(ax.lines) != 0:
                self.base_ax.set_visible(True)
                ax.set_visible(False)
                for line in ax.lines:
                    line.remove()
                    self.base_ax.add_line(line)

        for ax in self.axes:
            if ax.get_visible():
                vis_so_far += 1

                if vis_so_far == 1:
                    ax.yaxis.set_ticks_position('left')
                    ax.spines.left.set_position(('outward',0))
                    ax.yaxis.set_label_position("left")
                elif vis_so_far == 2:
                    ax.yaxis.set_ticks_position('right')
                    ax.spines.left.set_position(('outward',0))
                    ax.yaxis.set_label_position('right')
                elif vis_so_far == 3:
                    ax.yaxis.set_ticks_position('left')
                    ax.spines.left.set_position(('outward',60))
                    ax.yaxis.set_label_position("left")
                else:
                    ax.yaxis.set_ticks_position('right')
                    ax.spines.right.set_position(('outward',60))
                    ax.yaxis.set_label_position('right')

            ax.relim()
            ax.autoscale_view(True,True,True)