from PyQt5.QtWidgets import QTreeWidgetItem


class ItemWrapper(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        # objects
        # self.graph = None # MatPlotLib FigureCanvas
        self.line = None  # MatPlotLib Line
        self.axis = None  # MatPlotLib Axis

        # attributes
        self.kwrd = None  # FLAME functions
        self.x_unit = None  # MatPlotLib Label
        self.y_unit = None  # MatPlotLib Label
        self.description = None  # PyQt Tool Tip
        self.text_repr = None  # within QTreeWidget
        self.dashed = False
