from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QLineEdit, QTreeWidgetItem

import classes.globals as glb


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
        self.given_color = None


class SigFigLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setValidator(QDoubleValidator())
        self.editingFinished.connect(self.convertToSciNotation)
        # self.textChanged.connect(self.convertToSciNotation)
        # self.textEdited.connect(self.convertToSciNotation)

    def convertToSciNotation(self):
        if not self.text():
            return

        self.blockSignals(True)
        num = float(self.text())
        f_string = "{:." + str(glb.num_sigfigs - 1) + "e}"
        f_string = f_string.format(num)
        self.setText(f_string)
        self.blockSignals(False)
        

class SigFigTableLineEdit(SigFigLineEdit):
    def __init__(self):
        super().__init__()
        self.setFrame(False)
        self.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }")
