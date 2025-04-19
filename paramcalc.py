import numpy as np

from module import crystallo as cr
from module import micromech as mm
from module import microstruct as ms

from module import dfetch as fd

'''
Script calculates parameters from mc_data.csv and saves as mc_calc.csv
'''

df, dir = fd.dfread(0)

'''
Micromechanics Calculations
'''
# loads the unit cell parameters
abc_ref, abc_def, angle_ref, angle_def, para = fd.dfload(df, [])

# converts the unit cell parameter to lattice vectors
reflat = cr.unit2vect(abc_ref, angle_ref)
deflat = cr.unit2vect(abc_def, angle_def)

# calculates deformation gradient
F = mm.defgrad(reflat, deflat)

# calculates volume change
detF = mm.defvol(F)

# Calculates lambda2
lam = mm.compat(F, np.eye(3))

'''
Microstructure Calculations
'''
# loads the unit cell parameters and miller indices
abc_ref, abc_def, angle_ref, angle_def, milfrac = fd.dfload(df, ['miller'])

# converts the unit cell parameter to lattice vectors
reflat = cr.unit2vect(abc_ref, angle_ref)
deflat = cr.unit2vect(abc_def, angle_def)

# calculates kinematic compatibility conditions
n, a, s, nu, K, n_n, a_n, s_n, nu_n, K_n = ms.kincomp(F, np.eye(3))

# calculates angle difference
milvec = cr.frac2cart(milfrac, reflat)
theta = cr.minang(n, n_n, milvec)

'''
Geometry Calculations
'''

