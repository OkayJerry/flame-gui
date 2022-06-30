from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from flame_utils import ModelFlame, PlotLat
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import numpy as np


class FmMplLine(Line2D):
    # only purpose as for now is to differentiate lines I've added from Line2D
    def __init__(self, xdata, ydata, parent_item):
        super().__init__(xdata, ydata)
        self.parent_item = parent_item


class FmMplCanvas(FigureCanvas):
    def __init__(self, parent=None, filename=None):
        super(FigureCanvas, self).__init__(parent)
        self.model = None
        self.model_history = []
        self.undo_history = []
        self.axes = []
        self.base_ax = None
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        # [   'C0'  ,   'C1'  ,   'C2'  ,   'C3'  ] https://matplotlib.org/3.5.0/users/prev_whats_new/dflt_style_changes.html#colors-in-default-property-cycle

        self.figure.tight_layout()

    def link(self, param_tree, main_window):
        self.param_tree = param_tree
        self.main_window = main_window

    def setModel(self, model):
        self.model = model

    def updateLines(self):
        active_items = self.param_tree.getCheckedItems()
        r, s = self.model.run(monitor='all')
        for item in active_items:
            data = self.model.collect_data(r, 'pos', item.kwrd)
            item.line.set_data(data['pos'], data[item.kwrd])

        self._removeLocation()
        self._plotLocation()

        for ax in self.axes:
            ax.relim()
            ax.autoscale_view()

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def plotItem(self, item):
        self._assignLine(item)

        ax = self._getAxisWithYLabel(item.y_unit)
        if ax is not None:
            ax.add_line(item.line)
        else:
            if self.base_ax is None:  # initial call of plotItem from blank canvas
                ax = self.figure.subplots()
                self.base_ax = ax
                self.base_ax.set_xlabel('pos [m]')
            else:
                ax = self.base_ax.twinx()
                self._setAxisLocation(ax)
                base_xmargin, _ = self.base_ax.margins()
                ax.margins(base_xmargin, 0.425)
            ax.add_line(item.line)
            self.axes.append(ax)
        # if the axis already is that unit, the y-label will just remain the
        # same
        ax.set_ylabel(item.y_unit)

        self._removeLegend()
        self._createLegend()

        self._removeLocation()
        self._plotLocation()

        ax.relim()
        ax.autoscale_view(True, True, True)

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def _setLineColor(self, line):
        taken = []
        for ax in self.axes:
            for ln in ax.lines:
                if isinstance(ln, FmMplLine):  # filters out locational plot
                    taken.append(ln.get_color())
        available = list(set(self.colors) - set(taken))
        n_color = available[0]
        line.set_color(n_color)

    def _getAxisWithYLabel(self, ylabel):
        for ax in self.axes:
            if ylabel == ax.get_ylabel():
                return ax
        return None

    # occurs prior to the appending of current axis
    def _setAxisLocation(self, axis):
        if len(self.axes) == 1:
            axis.yaxis.set_ticks_position('right')
            axis.spines.left.set_position(('outward', 0))
            axis.yaxis.set_label_position('right')
        elif len(self.axes) == 2:
            axis.yaxis.set_ticks_position('left')
            axis.spines.left.set_position(('outward', 60))
            axis.yaxis.set_label_position("left")
        else:
            axis.yaxis.set_ticks_position('right')
            axis.spines.right.set_position(('outward', 60))
            axis.yaxis.set_label_position('right')

    def _updateAxisLocation(self):
        for i in range(len(self.axes)):
            axis = self.axes[i]
            if i == 0:
                axis.yaxis.set_ticks_position('left')
                axis.spines.left.set_position(('outward', 0))
                axis.yaxis.set_label_position('left')
            elif i == 1:
                axis.yaxis.set_ticks_position('right')
                axis.spines.right.set_position(('outward', 0))
                axis.yaxis.set_label_position('right')
            elif i == 2:
                axis.yaxis.set_ticks_position('left')
                axis.spines.left.set_position(('outward', 60))
                axis.yaxis.set_label_position("left")
            else:
                axis.yaxis.set_ticks_position('right')
                axis.spines.right.set_position(('outward', 60))
                axis.yaxis.set_label_position('right')

    def _createLegend(self):
        patches = []
        topmost_ax = self.axes[-1]
        for ax in self.axes:
            for ln in ax.lines:
                if isinstance(ln, FmMplLine):
                    patch = mpatches.Patch(
                        color=ln.get_color(), label=ln.get_label())
                    patches.append(patch)
        topmost_ax.legend(handles=patches, loc='upper left')

    def _removeLegend(self):
        if len(self.axes) > 1:  # new axis just added
            if self.axes[-2].get_legend():  # since new axis was just added, must go back 2
                prev_legend = self.axes[-2].get_legend()
            else:  # sometimes an axis isn't added, so you just need to remove the one in the current axis
                prev_legend = self.axes[-1].get_legend()
            prev_legend.remove()

    def removeItem(self, item):
        item.line.remove()
        self._removeLegend()
        self._removeLocation()

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
                            self._assignLine(ln.parent_item)
                            self.base_ax.add_line(ln.parent_item.line)
                            del ln  # necessary

                        y_unit = above_axis.yaxis.get_label().get_text()
                        self.base_ax.set_ylabel(y_unit)
                        above_axis.remove()
                        self.axes.remove(above_axis)
                else:
                    ax.remove()
                    self.axes.remove(ax)
                    del ax  # necessary

        self._updateAxisLocation()

        for ax in self.axes:
            ax.relim()
            ax.autoscale()

        if len(self.axes) != 0:  # no axes = no legend
            self._createLegend()

        self._plotLocation()

        self.figure.tight_layout()
        self.figure.canvas.draw_idle()

    def _plotLocation(self):
        if self.base_ax:
            ymax, ymin = self._getYMaxMin(self.base_ax)
            yrange = ymax - ymin
            frac_yrange = yrange * 0.1

            if ymax != ymin:  # not a horizonal line
                ycen_eq = ymin - frac_yrange - frac_yrange * 0.5
                yscl_eq = frac_yrange
            else:
                ycen_eq = ymax - 1
                yscl_eq = 1 * 0.09

            lattice = PlotLat(
                self.model.machine,
                auto_scaling=False,
                starting_offset=0)
            lattice.generate(
                ycen=ycen_eq,
                yscl=yscl_eq,
                legend=False,
                option=False,
                axes=self.base_ax)  # locational plot created

            self.base_ax.relim()
            self.base_ax.autoscale_view(True, True, True)

    def _removeLocation(self):
        if self.base_ax:
            for ln in reversed(self.base_ax.lines):  # reversed necessary
                if not isinstance(ln, FmMplLine):
                    ln.remove()
            [p.remove()
             for p in reversed(self.base_ax.patches)]  # reversed necessary

            self.base_ax.relim()
            self.base_ax.autoscale_view(True, True, True)

    def _getYMaxMin(self, axis):
        ymax = -np.inf
        ymin = np.inf
        for ln in axis.lines:
            if isinstance(ln, FmMplLine):
                ydata = ln.get_ydata()
                ln_ymax = max(ydata)
                ln_ymin = min(ydata)
                if ln_ymax > ymax:
                    ymax = ln_ymax
                if ln_ymin < ymin:
                    ymin = ln_ymin
        return ymax, ymin

    def copyModelToHistory(self):
        self.model_history.append(ModelFlame(
            machine=self.model.clone_machine()))
        self.undo_history.clear()
        self.main_window.menu_bar.handleUndoRedoEnabling()

    def _assignLine(self, item):
        r, s = self.model.run(monitor='all')
        data = self.model.collect_data(r, 'pos', item.kwrd)
        item.line = FmMplLine(data['pos'], data[item.kwrd], item)
        item.line.set_label(item.kwrd)
        if item.dashed:
            item.line.set_linestyle('dashed')
        self._setLineColor(item.line)
