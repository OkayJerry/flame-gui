from sys import argv

import numpy as np
from PyQt5.QtWidgets import QApplication

from classes.model import Model

global app
global num_sigfigs
global model
global data
app = QApplication(argv)
num_sigfigs = 4
model = Model()
data = {'element': {},
        'type': {'source': {'attributes': {'required': {},
                                           'optional': {}}},
                 'marker': {'attributes': {'required': {},
                                           'optional': {}}},
                 'stripper': {'attributes': {'required': {'IonChargeStates': {'type': list},
                                                          'charge_model': {'type': float,
                                                                           'default': 'baron'},
                                                          'NCharge': {'type': list}},
                                             'optional': {'Stripper_IonZ': {'type': float,
                                                                            'default': 78.0 / 238.0},
                                                          'Stripper_IonMass': {'type': float,
                                                                               'default': 238.0},
                                                          'Stripper_IonProton': {'type': float,
                                                                                 'default': 92.0},
                                                          'Stripper_E1Para': {'type': float,
                                                                              'default': 2.8874e-3},
                                                          'Stripper_lambda': {'type': float,
                                                                              'default': 5.5740},
                                                          'Stripper_upara': {'type': float,
                                                                             'default': 2.6903},
                                                          'Stripper_E0Para': {'type': list,
                                                                              'default': [16.348e6, 1.00547, -0.10681]},
                                                          'Stripper_Para': {'type': list,
                                                                            'default': [3.0, 20.0, 16.623e6]}}}},
                 'tmatrix': {'attributes': {'required': {'matrix': {'type': np.matrix}},
                                            'optional': {}}},
                 'orbtrim': {'attributes': {'required': {},
                                            'optional': {'realpara': {'type': int,
                                                                      'default': 0},
                                                         'theta_x': {'type': float,
                                                                     'default': 0.0},
                                                         'theta_y': {'type': float,
                                                                     'default': 0.0},
                                                         'tm_xkick': {'type': float,
                                                                      'default': 0.0},
                                                         'tm_ykick': {'type': float,
                                                                      'default': 0.0},
                                                         'xyrotate': {'type': float,
                                                                      'default': 0.0}}}},
                 'drift': {'attributes': {'required': {'L': {'type': float}},
                                          'optional': {}}},
                 'solenoid': {'attributes': {'required': {'L': {'type': float},
                                                          'B': {'type': float}},
                                             'optional': {'dx': {'type': float,
                                                                 'default': 0.0},
                                                          'dy': {'type': float,
                                                                 'default': 0.0},
                                                          'pitch': {'type': float,
                                                                    'default': 0.0},
                                                          'yaw': {'type': float,
                                                                  'default': 0.0},
                                                          'roll': {'type': float,
                                                                   'default': 0.0},
                                                          'ncurve': {'type': int,
                                                                     'default': 0},
                                                          'scl_fac${n}': {'type': float,
                                                                          'default': 0.0},
                                                          'curve${n}': {'type': list,
                                                                        'default': None},
                                                          'CurveFile': {'type': str,
                                                                        'default': None},
                                                          'use_range': {'type': list,
                                                                        'default': None}}}},
                 'quadrupole': {'attributes': {'required': {'L': {'type': float,},
                                                            'B2': {'type': float,}},
                                               'optional': {'dx': {'type': float,
                                                                   'default': 0.0},
                                                            'dy': {'type': float,
                                                                   'default': 0.0},
                                                            'pitch': {'type': float,
                                                                      'default': 0.0},
                                                            'yaw': {'type': float,
                                                                    'default': 0.0},
                                                            'roll': {'type': float,
                                                                     'default': 0.0},
                                                            'ncurve': {'type': int,
                                                                       'default': 0},
                                                            'scl_fac${n}': {'type': float,
                                                                            'default': 0.0},
                                                            'curve${n}': {'type': list,
                                                                          'default': None},
                                                            'CurveFile': {'type': str,
                                                                          'default': None},
                                                            'use_range': {'type': list,
                                                                          'default': None}}}},
                 'sextupole': {'attributes': {'required': {'L': {'type': float},
                                                           'B3': {'type': float}},
                                              'optional': {'dstkick': {'type': int,
                                                                       'default': 1},
                                                           'step': {'type': int,
                                                                    'default': 1},
                                                           'dx': {'type': float,
                                                                  'default': 0.0},
                                                           'dy': {'type': float,
                                                                  'default': 0.0},
                                                           'pitch': {'type': float,
                                                                     'default': 0.0},
                                                           'yaw': {'type': float,
                                                                   'default': 0.0},
                                                           'roll': {'type': float,
                                                                    'default': 0.0}}}},
                 'equad': {'attributes': {'required': {'L': {'type': float},
                                                       'V': {'type': float},
                                                       'radius': {'type': float}},
                                          'optional': {'dx': {'type': float,
                                                              'default': 0.0},
                                                       'dy': {'type': float,
                                                              'default': 0.0},
                                                       'pitch': {'type': float,
                                                                 'default': 0.0},
                                                       'yaw': {'type': float,
                                                               'default': 0.0},
                                                       'roll': {'type': float,
                                                                'default': 0.0},
                                                       'ncurve': {'type': int,
                                                                  'default': 0},
                                                       'scl_fac${n}': {'type': float,
                                                                       'default': 0.0},
                                                       'curve${n}': {'type': list,
                                                                     'default': None},
                                                       'CurveFile': {'type': str,
                                                                     'default': None},
                                                       'use_range': {'type': float,
                                                                     'default': None}}}},
                 'sbend': {'attributes': {'required': {'L': {'type': float},
                                                       'phi': {'type': float},
                                                       'phi1': {'type': float},
                                                       'phi2': {'type': float}},
                                          'optional': {'bg': {'type': float},
                                                       'dx': {'type': float,
                                                              'default': 0.0},
                                                       'dy': {'type': float,
                                                              'default': 0.0},
                                                       'pitch': {'type': float,
                                                                 'default': 0.0},
                                                       'yaw': {'type': float,
                                                               'default': 0.0},
                                                       'roll': {'type': float,
                                                                'default': 0.0}}}},
                 'edipole': {'attributes': {'required': {'L': {'type': float},
                                                         'phi': {'type': float},
                                                         'spher': {'type': int},
                                                         'ver': {'type': int}},
                                            'optional': {'beta': {'type': float},
                                                         'fringe_x': {'type': float,
                                                                      'default': 0.0},
                                                         'fringe_y': {'type': float,
                                                                      'default': 0.0},
                                                         'asymfac': {'type': float,
                                                                     'default': 0.0},
                                                         'dx': {'type': float,
                                                                'default': 0.0},
                                                         'dy': {'type': float,
                                                                'default': 0.0},
                                                         'pitch': {'type': float,
                                                                   'default': 0.0},
                                                         'yaw': {'type': float,
                                                                 'default': 0.0},
                                                         'roll': {'type': float,
                                                                  'default': 0.0}}}},
                 'rfcavity': {'attributes': {'required': {'L': {'type': float},
                                                          'cavtype': {'type': str},
                                                          'f': {'type': float},
                                                          'phi': {'type': float},
                                                          'scl_fac': {'type': float}},
                                             'optional': {'syncflag': {'type': int,
                                                                       'default': 1},
                                                          'datafile': {'type': str},
                                                          'Rm': {'type': float},
                                                          'dx': {'type': float,
                                                                 'default': 0.0},
                                                          'dy': {'type': float,
                                                                 'default': 0.0},
                                                          'pitch': {'type': float,
                                                                    'default': 0.0},
                                                          'yaw': {'type': float,
                                                                  'default': 0.0},
                                                          'roll': {'type': float,
                                                                   'default': 0.0}}}}},
        'parameter': {"ref_beta": {
                        "description": "speed in the unit of light velocity in vacuum of reference charge state, Lorentz beta",
                        "unit": "",
                        "representation": "Beta"
                        },
                      "ref_bg": {
                        "description": "multiplication of beta and gamma of reference charge state",
                        "unit": "",
                        "representation": "BG"
                        },
                      "ref_gamma": {
                        "description": "relativistic energy of reference charge state, Lorentz gamma",
                        "unit": "",
                        "representation": "Gamma"
                        },
                      "ref_IonEk": {
                        "description": "kinetic energy of reference charge state",
                        "unit": "eV/u",
                        "representation": "IonEk"
                        },
                      "ref_IonEs": {
                        "description": "rest energy of reference charge state",
                        "unit": "eV/u",
                        "representation": "IonEs"
                        },
                      "ref_IonQ": {
                        "description": "macro particle number of reference charge state",
                        "unit": "",
                        "representation": "IonQ"
                        },
                      "ref_IonW": {
                        "description": "total energy of reference charge state, i.e. W = E_s + E_k",
                        "unit": "eV/u",
                        "representation": "IonW"
                        },
                      "ref_IonZ": {
                        "description": "reference charge to mass ratio",
                        "unit": "",
                        "representation": "IonZ"
                        },
                      "ref_phis": {
                        "description": "absolute synchrotron phase of reference charge state",
                        "unit": "rad",
                        "representation": "Phis"
                        },
                      "ref_SampleIonK": {
                        "description": "wave-vector in cavities with different beta values of reference charge state",
                        "unit": "rad",
                        "representation": "SampleIonK"
                        },
                      "ref_Brho": {
                        "description": "magnetic rigidity of reference charge state",
                        "unit": "Tm",
                        "representation": "Brho"
                        },
                      "xcen": {
                        "description": "weight average of all charge states for x",
                        "unit": "mm",
                        "representation": "x"
                        },
                      "xrms": {
                        "description": "general rms beam envelope for x",
                        "unit": "mm",
                        "representation": "x"
                        },
                      "ycen": {
                        "description": "weight average of all charge states for y",
                        "unit": "mm",
                        "representation": "y"
                        },
                      "yrms": {
                        "description": "general rms beam envelope for y",
                        "unit": "mm",
                        "representation": "y"
                        },
                      "zcen": {
                        "description": "weight average of all charge states for phi",
                        "unit": "rad",
                        "representation": "z"
                        },  # phi
                      "zrms": {
                        "description": "general rms beam envelope for phi",
                        "unit": "rad",
                        "representation": "z"
                        },  # phi
                      "xpcen": {
                        "description": "weight average of all charge states for x'",
                        "unit": "rad",
                        "representation": "x'"
                        },
                      "xprms": {
                        "description": "general rms beam envelope for x'",
                        "unit": "rad",
                        "representation": "x'"
                        },
                      "ypcen": {
                        "description": "weight average of all charge states for y'",
                        "unit": "rad",
                        "representation": "y'"
                        },
                      "yprms": {
                        "description": "general rms beam envelope for y'",
                        "unit": "rad",
                        "representation": "y'"
                        },
                      "zpcen": {
                        "description": "weight average of all charge states for SE_k",
                        "unit": "MeV/u",
                        "representation": "z'"
                        },
                      "zprms": {
                        "description": "general rms beam envelope for SE_k",
                        "unit": "MeV/u",
                        "representation": "z'"
                        },
                      "xemittance": {
                        "description": "weight average of geometrical x emittance",
                        "unit": "mm-mrad",
                        "representation": "x"
                        },
                      "yemittance": {
                        "description": "weight average of geometrical y emittance",
                        "unit": "mm-mrad",
                        "representation": "y"
                        },
                      "zemittance": {
                        "description": "weight average of geometrical z emittance",
                        "unit": "rad-MeV/u",
                        "representation": "z"
                        },
                      "xnemittance": {
                        "description": "weight average of normalized x emittance",
                        "unit": "mm-mrad",
                        "representation": "norm(x)"
                        },
                      "ynemittance": {
                        "description": "weight average of normalized y emittance",
                        "unit": "mm-mrad",
                        "representation": "norm(y)"
                        },
                      "znemittance": {
                        "description": "weight average of normalized z emittance",
                        "unit": "rad-MeV/u",
                        "representation": "norm(z)"
                        },
                      "xtwiss_beta": {
                        "description": "weight average of twiss beta x",
                        "unit": "m/rad",
                        "representation": "x"
                        },
                      "xtwiss_alpha": {
                        "description": "weight average of twiss alpha x",
                        "unit": "",
                        "representation": "x"
                        },
                      "xtwiss_gamma": {
                        "description": "weight average of twiss gamma x",
                        "unit": "rad/m",
                        "representation": "x"
                        },
                      "ytwiss_beta": {
                        "description": "weight average of twiss beta y",
                        "unit": "m/rad",
                        "representation": "y"
                        },
                      "ytwiss_alpha": {
                        "description": "weight average of twiss alpha y",
                        "unit": "",
                        "representation": "y"
                        },
                      "ytwiss_gamma": {
                        "description": "weight average of twiss gamma y",
                        "unit": "rad/m",
                        "representation": "y"
                        },
                      "ztwiss_beta": {
                        "description": "weight average of twiss beta z",
                        "unit": "rad/MeV/u",
                        "representation": "z"
                        },
                      "ztwiss_alpha": {
                        "description": "weight average of twiss alpha z",
                        "unit": "",
                        "representation": "z"
                        },
                      "ztwiss_gamma": {
                        "description": "weight average of twiss gamma z",
                        "unit": "MeV/u/rad",
                        "representation": "z"
                        },
                      "couple_xy": {
                        "description": "weight average of normalized x-y coupling term",
                        "unit": "",
                        "representation": "x-y"
                        },
                      "couple_xpy": {
                        "description": "weight average of normalized xp-y coupling term",
                        "unit": "",
                        "representation": "x'-y"
                        },
                      "couple_xyp": {
                        "description": "weight average of normalized x-yp coupling term",
                        "unit": "",
                        "representation": "x-y'"
                        },
                      "couple_xpyp": {
                        "description": "weight average of normalized xp-yp coupling term",
                        "unit": "",
                        "representation": "x'-y'"
                        },
                      "last_caviphi0": {
                        "description": "last RF cavity's driven phase",
                        "unit": "deg",
                        "representation": "Last Caviphi"
                        }
        }
}
