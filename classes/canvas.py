from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from flame_utils import ModelFlame, PlotLat
from matplotlib.lines import Line2D
from classes.utility import WorkspaceOneItem
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
        self.colors = ['C0','C1','C2','C3'] # See: https://matplotlib.org/3.5.0/users/prev_whats_new/dflt_style_changes.html#colors-in-default-property-cycle

        # axes
        base_ax = self.figure.subplots()
        base_ax.set_visible(False)
        self.axes.append(base_ax)
        for _ in range(4):
            ax = base_ax.twinx()
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
        if item.dashed == True:
            item.line.set_linestyle('dashed') # ------------------------ linestyle
        self._plot_line(item.line,item.y_unit)
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

    def remove_item(self,item):
        self._remove_line(item.line)
        self.update_axis()
        self.figure.tight_layout()
        self.figure.canvas.draw()

    def _remove_line(self,line):
        for ax in self.axes:
            if line in ax.lines and len(ax.lines) == 1:
        #         ax.lines.pop(0)
                ax.set_visible(False)
                break
        line.remove()

    def choose_color(self,line):
        taken = []
        for ax in self.axes:
            for ln in ax.lines:
                taken.append(ln.get_color())
        available = list(set(self.colors) - set(taken))
        line.set_color(available[0])
        print(available[0])

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