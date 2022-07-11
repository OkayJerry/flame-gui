from PyQt5 import QtWidgets, QtGui, QtCore


class PreferenceWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()

        self.app_fsize_scroll = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.plt_fsize_scroll = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.tree_dec_spin = QtWidgets.QSpinBox()

        app_fsize_label = QtWidgets.QLabel('Application Font Size:')
        plt_fsize_label = QtWidgets.QLabel('Plot Font Size:')
        tree_dec_label = QtWidgets.QLabel('Element Tree View Significant Figures:')

        layout.addWidget(app_fsize_label, 0, 0)
        layout.addWidget(plt_fsize_label, 1, 0)
        layout.addWidget(tree_dec_label, 2, 0)
        layout.addWidget(self.app_fsize_scroll, 0, 1)
        layout.addWidget(self.plt_fsize_scroll, 1, 1)
        layout.addWidget(self.tree_dec_spin, 2, 1)

        self.setLayout(layout)