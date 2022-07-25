from configparser import ConfigParser

import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import classes.globals as glb


class PreferenceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('Preferences')
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        layout = QGridLayout()
        self.menubar = parent
        
        self.config = ConfigParser()
        settings = self._getSettings()

        apply_button = QPushButton()
        default_button = QPushButton()
        self.app_fsize_spin = QSpinBox()
        self.plt_fsize_spin = QSpinBox()
        self.sigfig_spin = QSpinBox()
        
        self.app_fsize_spin.setValue(settings['AppFontSize'])
        self.plt_fsize_spin.setValue(settings['PlotFontSize'])
        self.sigfig_spin.setValue(settings['NumSigFigs'])
        self.app_fsize_spin.setRange(1, 20)
        self.plt_fsize_spin.setRange(1, 15)
        self.sigfig_spin.setRange(1, 2147483647)

        app_fsize_label = QLabel('Application Font Size:')
        plt_fsize_label = QLabel('Plot Font Size:')
        sigfig_label = QLabel('Significant Figures:')

        apply_button.setText('Apply')
        apply_button.clicked.connect(self._apply)
        default_button.setText('Default')
        default_button.clicked.connect(self._default)

        layout.addWidget(app_fsize_label, 0, 0)
        layout.addWidget(plt_fsize_label, 1, 0)
        layout.addWidget(sigfig_label, 2, 0)
        layout.addWidget(default_button, 3, 0)
        layout.addWidget(self.app_fsize_spin, 0, 1)
        layout.addWidget(self.plt_fsize_spin, 1, 1)
        layout.addWidget(self.sigfig_spin, 2, 1)
        layout.addWidget(apply_button, 3, 1)

        self.setLayout(layout)
        self._apply()
            
    def open(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive) # restoring to maximized/normal state
        self.activateWindow()
        self.show()

    def _default(self):
        self.app_fsize_spin.setValue(9)
        self.plt_fsize_spin.setValue(10)
        self.sigfig_spin.setValue(4)
        
    def _getSettings(self):
        self.config.read('settings.ini')
        app_fsize = self.config.getint('main', 'AppFontSize')
        plt_fsize = self.config.getint('main', 'PlotFontSize')
        num_sigfigs = self.config.getint('main', 'NumSigFigs')
        return {'AppFontSize': app_fsize,
                'PlotFontSize': plt_fsize,
                'NumSigFigs': num_sigfigs} 

    def _setSettings(self):
        self.config.read('settings.ini')
        self.config.set('main', 'AppFontSize', str(self.app_fsize_spin.value()))
        self.config.set('main', 'PlotFontSize', str(self.plt_fsize_spin.value()))
        self.config.set('main', 'NumSigFigs', str(self.sigfig_spin.value()))
        with open("settings.ini","w") as f:
            self.config.write(f)

    def _apply(self):
        # application font size
        glb.app.setStyleSheet("QWidget {font-size: " + str(self.app_fsize_spin.value()) + "pt;}")
        
        # graph font size
        graph = self.menubar.main_window.workspace.graph
        matplotlib.rc('font', size=self.plt_fsize_spin.value())
        graph.refresh()

        # Sig Figs
        glb.num_sigfigs = self.sigfig_spin.value()
        lat_editor = self.menubar.main_window.workspace.lat_editor
        filters = self.menubar.main_window.workspace.filters
        name_i = lat_editor.headers.index('Name')
        
        expanded_elements = []
        for i in range(lat_editor.topLevelItemCount()):
            element = lat_editor.topLevelItem(i)
            if element.isExpanded():
                expanded_elements.append(element.text(name_i))
        
        lat_editor.clear()
        lat_editor.populate()
        lat_editor.typeFilter(filters.combo_box.currentText())
        
        for element in expanded_elements:
            item = lat_editor.findItems(
                element, Qt.MatchExactly, name_i)[0]
            item.setExpanded(True)
            
        self.menubar.opt_window.fillTables()

        try: # for when there are no elements
            self.menubar.phase_window.plotCurrentElement()
        except:
            pass

        self._setSettings()
