"""
used with parser2.py, the new file format (aff)
"""
import numpy as np

parameters = {
    'mode': 'fd',
    'xc': 'LDA',
    'occupations': None,
    'poissonsolver': None,
    'h': None,  # Angstrom
    'gpts': None,
    'kpts': [(0.0, 0.0, 0.0)],
    'nbands': None,
    'charge': 0,
    'setups': {},
    'basis': {},
    'spinpol': None,
    'fixdensity': False,
    'filter': None,
    'mixer': None,
    'eigensolver': None,
    'background_charge': None,
    'external': None,
    'random': False,
    'hund': False,
    'maxiter': 333,
    'idiotproof': True,
    'symmetry': {'point_group': True,
                 'time_reversal': True,
                 'symmorphic': True,
                 'tolerance': 1e-7},
    'convergence': {'energy': 0.0005,  # eV / electron
                    'density': 1.0e-4,
                    'eigenstates': 4.0e-8,  # eV^2
                    'bands': 'occupied',
                    'forces': np.inf},  # eV / Ang
    'dtype': None,  # Deprecated
    'width': None,  # Deprecated
    'verbose': 0}


