from PyQt5 import QtWidgets, QtGui, QtCore
import classes.globals as glb
import matplotlib
from configparser import ConfigParser

class PreferenceWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('Preferences')
        layout = QtWidgets.QGridLayout()
        self.menubar = parent
        
        self.config = ConfigParser()
        settings = self._getSettings()

        apply_button = QtWidgets.QPushButton()
        self.app_fsize_spin = QtWidgets.QSpinBox()
        self.plt_fsize_spin = QtWidgets.QSpinBox()
        self.tree_dec_spin = QtWidgets.QSpinBox()
        
        self.app_fsize_spin.setValue(settings['AppFontSize'])
        self.plt_fsize_spin.setValue(settings['PlotFontSize'])
        self.tree_dec_spin.setValue(settings['LatTreeSigFigs'])
        self.app_fsize_spin.setRange(1, 20)
        self.plt_fsize_spin.setRange(1, 15)
        self.tree_dec_spin.setRange(1, 8)

        app_fsize_label = QtWidgets.QLabel('Application Font Size:')
        plt_fsize_label = QtWidgets.QLabel('Plot Font Size:')
        tree_dec_label = QtWidgets.QLabel('Lattice Tree Significant Figures:')

        apply_button.setText('Apply')
        apply_button.clicked.connect(self._apply)

        layout.addWidget(app_fsize_label, 0, 0)
        layout.addWidget(plt_fsize_label, 1, 0)
        layout.addWidget(tree_dec_label, 2, 0)
        layout.addWidget(self.app_fsize_spin, 0, 1)
        layout.addWidget(self.plt_fsize_spin, 1, 1)
        layout.addWidget(self.tree_dec_spin, 2, 1)
        layout.addWidget(apply_button, 3, 1)

        self.setLayout(layout)
        self._apply()
            
    def _getSettings(self):
        self.config.read('settings.ini')
        app_fsize = self.config.getint('main', 'AppFontSize')
        plt_fsize = self.config.getint('main', 'PlotFontSize')
        lattree_sigfigs = self.config.getint('main', 'LatTreeSigFigs')
        return {'AppFontSize': app_fsize,
                'PlotFontSize': plt_fsize,
                'LatTreeSigFigs': lattree_sigfigs} 

    def _setSettings(self):
        self.config.read('settings.ini')
        self.config.set('main', 'AppFontSize', str(self.app_fsize_spin.value()))
        self.config.set('main', 'PlotFontSize', str(self.plt_fsize_spin.value()))
        self.config.set('main', 'LatTreeSigFigs', str(self.tree_dec_spin.value()))
        with open("settings.ini","w") as f:
            self.config.write(f)

    def _apply(self):
        # application font size
        glb.app.setStyleSheet("QWidget {font-size: " + str(self.app_fsize_spin.value()) + "pt;}")
        
        # graph font size
        graph = self.menubar.main_window.workspace.graph
        matplotlib.rc('font', size=self.plt_fsize_spin.value())
        graph.refresh()

        # (LatTree) Sig Figs
        glb.num_sigfigs = self.tree_dec_spin.value()
        lat_editor = self.menubar.main_window.workspace.lat_editor
        filters = self.menubar.main_window.workspace.filters
        lat_editor.clear()
        lat_editor.populate()
        lat_editor.typeFilter(filters.combo_box.currentText())

        self._setSettings()