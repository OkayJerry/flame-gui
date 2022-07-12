import os
from sys import argv
from collections import OrderedDict

import numpy as np
from PyQt5.QtWidgets import QApplication
from flame_utils import ModelFlame
from flame import Machine
from PyQt5.QtGui import QFont


def createModel():
    vec = np.zeros(7)
    vec[6] = 1.0
    mat = np.zeros([7, 7])
    mat[0, 0] = mat[2, 2] = 1.0
    mat[1, 1] = mat[3, 3] = 1.0e-6

    source = OrderedDict([
        ('name', 'S'),
        ('type', 'source'),
        ('vector_variable', 'BC'),
        ('matrix_variable', 'S')
    ])

    conf = OrderedDict([
        ('sim_type', 'MomentMatrix'),
        ('IonEk', 1e6),
        ('IonEs', 931494320.0),
        ('IonChargeStates', np.array([0.5])),
        ('NCharge', np.array([1.0])),
        ('BC0', vec),
        ('S0', mat),
        ('elements', [source]),
        ('Eng_Data_Dir', os.getcwd() + '/FLAME/python/flame/test/data')
    ])
    
    return ModelFlame(machine=Machine(conf))

global app
global model
global num_sigfigs

app = QApplication(argv)
model = createModel()
num_sigfigs = 3