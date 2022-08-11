from flame import Machine
from flame_utils import ModelFlame
from collections import OrderedDict
import numpy as np
import os


class Model(ModelFlame):
    def __init__(self, lat_file=None, **kws):
        if lat_file != None or kws:
            super().__init__(lat_file=lat_file, **kws)
        else:
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
            
            super().__init__(machine=Machine(conf))

    def get_value_by_element_attribute(self, attribute, latfile=None, index=None, name=None, type=None, **kws):
        element = self.get_element(latfile=latfile, index=index, name=name, type=type, **kws)
        return element['properties'][attribute]
        
    def get_required_element_attributes(self, latfile=None, index=None, name=None, type=None, **kws):
        required_attributes = {'solenoid': ['L', 'B'],
                               'quadrupole': ['L', 'B2'],
                               'sextupole': ['L', 'B3'],
                               'equad': ['L', 'V', 'radius'],
                               'sbend': ['L', 'phi'],
                               'edipole': ['L', 'phi', 'ver', 'spher'],
                               'rfcavity': ['L', 'f', 'phi', 'scl_fac', 'cavtype']}
        
        element = self.get_element(latfile=latfile, index=index, name=name, type=type, **kws)
        element_type = element['properties']['type']
        
        if element_type in required_attributes.keys():
            return required_attributes[element_type]
        else:
            return None
            
    def get_attribute_unit(self, attribute):
        units = {'L': 'm',
                 'Stripper_IonMass': 'amu', # stripper
                 'Stripper_E1Para': 'MeV/u',
                 'Stripper_upara': 'mrad',
                 'Stripper_E0Para': 'eV/u, None, None',
                 'Stripper_Para': 'um, %, eV/u',
                 'theta_x': 'rad', # orbtrim
                 'theta_y': 'rad',
                 'tm_xkick': 'T*m',
                 'tm_ykick': 'T*m',
                 'xyrotate': 'deg',
                 'B': 'T', # solenoid
                 'dx': 'm',
                 'dy': 'm',
                 'pitch': 'rad',
                 'yaw': 'rad',
                 'roll': 'rad',
                 'B2': 'T/m', # quadrupole
                 'B3': 'T/m^2',  # sextupole
                 'V': 'V', # equad
                 'phi': 'deg', # sbend
                 'phi1': 'deg',
                 'phi2': 'deg',
                 'fringe_x': 'rad/mm', # edipole
                 'fringe_y': 'rad/mm',
                 'f': 'Hz', # rfcavity
                 'Rm': 'mm'}
        
        if attribute in units.keys():
            return units[attribute]
        else:
            return ''
            
    def get_element_default_values(self, latfile=None, index=None, name=None, type=None, **kws):
        default_values = {'sbend': {'phi': 1},
                          'equad': {'radius': 1},
                          'rfcavity': {'L': 0.24, 'f': 80.5e6, 'cavtype': '0.041QWR'}}

        element = self.get_element(latfile=latfile, index=index, name=name, type=type, **kws)
        element_type = element['properties']['type']
        
        if element_type in default_values.keys():
            return default_values[element_type]
        else:
            return dict()

    def get_parameter_unit(self, parameter):
        units = {'ref_IonEk': 'eV/u',
                 'ref_IonEs': 'eV/u',
                 'ref_IonW': 'eV/u',
                 'ref_phis': 'rad',
                 'ref_SampleIonK': 'rad',
                 'ref_Brho': 'Tm',
                 'xcen': 'mm',
                 'ycen': 'mm',
                 'zcen': 'rad',
                 'xpcen': 'rad',
                 'ypcen': 'rad',
                 'zpcen': 'MeV/u',
                 'xrms': 'mm',
                 'yrms': 'mm',
                 'zrms': 'rad',
                 'xprms': 'rad',
                 'yprms': 'rad',
                 'zprms': 'MeV/u',
                 'xemittance': 'mm-mrad',
                 'yemittance': 'mm-mrad',
                 'zemittance': 'rad-MeV/u',
                 'xnemittance': 'mm-mrad',
                 'ynemittance': 'mm-mrad',
                 'znemittance': 'rad-MeV/u',
                 'xtwiss_beta': 'm/rad',
                 'xtwiss_gamma': 'rad/m',
                 'ytwiss_beta': 'm/rad',
                 'ytwiss_gamma': 'rad/m',
                 'ztwiss_beta': 'rad/MeV/u',
                 'ztwiss_gamma': 'MeV/u/rad',
                 'last_caviphi0': 'deg'}
        if parameter in units:
            return units[parameter]
        else:
            return ''
        
    def get_prime_parameters(self):
        return ['xpcen', 'ypcen', 'zpcen',
                'xprms', 'yprms', 'zprms',
                'couple_xpy', 'couple_xyp', 'couple_xpyp']