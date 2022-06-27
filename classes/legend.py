from PyQt5.QtWidgets import QTreeWidget, QHeaderView, QTreeWidgetItem, QAbstractItemView, QComboBox, QMessageBox
from PyQt5 import QtCore
from PyQt5 import QtGui


class Legend(QTreeWidget):
    def __init__(self, parent=None):  # ,graph,items,parent=None):
        super(QTreeWidget, self).__init__(parent)

        # self.graph = graph
        # self.items = items
        self.checked_box_cnt = 0
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.ignore_next_item_change = False

    def link(self, items, graph):
        self.items = items
        self.graph = graph

        self.fill()

    def fill(self):

        # Parameter            Visible
        # ├─ Reference beam
        # │   ├─ ref_beta        [ ]
        # │   ├─ ref_bg          [ ]
        # │   ├─ ref_gamma       [ ]
        # │   └─ ...
        # └─ Actual beam
        #     ├─ beta            [ ]
        #     ├─ bg              [ ]
        #     ├─ gamma           [ ]
        #     ├─ ...
        #     ├─ cen
        #     │   ├─ x           [ ]
        #     │   ├─ y           [ ]
        #     │   └─ z           [ ]
        #     ├─ rms
        #     │   ├─ x           [x]
        #     │   ├─ y           [x]
        #     │   └─ z           [ ]
        #     ├─ ...
        #     └─ couple
        #         ├─ xy          [ ]
        #         ├─ xpy         [ ]
        #         ├─ xyp         [ ]
        #         └─ xpyp        [ ]

        for lst in self.items.values():
            for item in lst:
                item.setText(0, item.text_repr)
                item.setToolTip(0, item.description)

        # top-level
        reference = QTreeWidgetItem()
        actual = QTreeWidgetItem()
        reference.setText(0, "Reference")
        actual.setText(0, "Actual")

        # secondary_level
        cen = QTreeWidgetItem()
        rms = QTreeWidgetItem()
        emt = QTreeWidgetItem()
        tws = QTreeWidgetItem()
        tws_x = QTreeWidgetItem()
        tws_y = QTreeWidgetItem()
        tws_z = QTreeWidgetItem()
        cpl = QTreeWidgetItem()
        others = QTreeWidgetItem()
        cen.setText(0, "cen")
        rms.setText(0, "rms")
        emt.setText(0, "emittance")
        tws.setText(0, "twiss")
        tws_x.setText(0, "alpha")
        tws_y.setText(0, "beta")
        tws_z.setText(0, "gamma")
        cpl.setText(0, "couple")
        others.setText(0, "others")

        # creating view
        self.addTopLevelItem(reference)
        for item in self.items["ref"]:
            reference.addChild(item)

        self.addTopLevelItem(actual)
        actual.addChild(cen)
        for item in self.items["cen"]:
            cen.addChild(item)

        actual.addChild(rms)
        for item in self.items["rms"]:
            rms.addChild(item)

        actual.addChild(emt)
        for item in self.items["emittance"]:
            emt.addChild(item)

        actual.addChild(tws)
        tws.addChild(tws_x)
        for item in self.items["twiss_alpha"]:
            tws_x.addChild(item)
        tws.addChild(tws_y)
        for item in self.items["twiss_beta"]:
            tws_y.addChild(item)
        tws.addChild(tws_z)
        for item in self.items["twiss_gamma"]:
            tws_z.addChild(item)

        actual.addChild(cpl)
        for item in self.items["couple"]:
            cpl.addChild(item)

        actual.addChild(others)
        for item in self.items["others"]:
            others.addChild(item)

        # enabling checkbox
        for lst in self.items.values():
            for item in lst:
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(0, QtCore.Qt.Unchecked)

        self.itemChanged.connect(self.handle_checkboxes)

    def handle_checkboxes(self, item, col):
        if item.checkState(col) == 0:
            self.graph.remove_item(item)
            self.checked_box_cnt -= 1
        elif self.checked_box_cnt < 4:
            self.graph.plot_item(item)
            self.checked_box_cnt += 1
        else:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Critical)
            warning.setText("You can only select four parameters at a time")
            warning.setWindowTitle("ERROR")
            warning.setStandardButtons(QMessageBox.Ok)

            if warning.exec() == QMessageBox.Ok:
                warning.close()

            self.blockSignals(True)
            item.setCheckState(0, QtCore.Qt.Unchecked)
            self.blockSignals(False)

    def getCheckedItems(self):
        checked_items = []
        for lst in self.items.values():
            for item in lst:
                if item.checkState(0) == QtCore.Qt.Checked:
                    checked_items.append(item)
        return checked_items
