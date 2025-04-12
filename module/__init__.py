'''
shamemlib

A library for microstructure and micromechanics calculations.
Focused on shape-memory and shape-memory-like materials.

Author: Yunsu Park
Version: 0.1.0
'''

__author__ = 'Yunsu Park'
__version__ = '0.1.0'

# --- Crystallography tools ---
from .crystallo import unit2vect, frac2cart, cart2frac

# --- Micromechanics tools ---
from .micromech import defgrad, streten, defvol, defare, defstr

# --- Microstructure compatibility tools ---
from .microstruct import kincomp, supcomp

__all__ = ['unit2vect', 'frac2cart', 'cart2frac',
           'defgrad', 'streten', 'defvol', 'defare', 'defstr',
           'kincomp', 'supcomp']
