'''
micromech.py

Micromech module contains functions for mechanics calculations in the microscale

Author: Yunsu Park
Created: Feb 13 2025
Affiliation: University of California, Santa Barbara
Contact: yunsu@ucsb.edu
'''

import numpy as np

def defgrad(reflat, deflat):
    '''
    Calculates the deformation gradient from the lattice vectors of the reference and deformed configuration

    Parameters:
        reflat (ndarray [shape (3, 3)]):
            reference lattice matrix with a as the parallel vector
            [[a1, b1, c1], 
             [0,  b2, c2], 
             [0,  0,  c3]]
        deflat (ndarray [shape (1, 3)]): 
            deformed lattice matrix with a as the parallel vector
            [[a1, b1, c1], 
             [0,  b2, c2], 
             [0,  0,  c3]]

    Returns:
        F (ndarray [shape (3, 3)]):
            deformation gradient for the material 
            going from the reference configuration (reflat) to the deformed configuration (deflat)
    '''

    F = deflat @ np.linalg.inv(reflat)

    return F


def streten(F):
    '''
    Polar decomposes the deformation gradient to the stretch tensor (U) and rotation matrix (Q) [F=QU]

    Parameters:
        F (ndarray [shape (3, 3)]):
            deformation gradient for the material 

    Returns:
        U (ndarray [shape (3, 3)]):
            stretch tensor from the deforamtion gradient (F)
        Q (ndarray [shape (3, 3)]):
            rotation matrix from the deformation gradient (F)
    '''

    C = F.T @ F

    # Compute Eigenvalues and Eigenvectors
    eig_val, eig_vec = np.linalg.eig(C)

    # Ensure eigenvalues are positive (they should be, but check to avoid numerical issues)
    lam = np.sqrt(np.abs(eig_val))  # Take sqrt of eigenvalues to get singular values

    # Construct U correctly using outer products
    U = sum(lam[i] * np.outer(eig_vec[:, i], eig_vec[:, i]) for i in range(3))

    # Compute Q = F * U^(-1)
    U_inv = np.linalg.inv(U) 
    Q = F @ U_inv

    return U, Q

def defvol(F):
    pass
def defare(F): 
    pass
def defstr(F):
    pass

def compat(F, G):
    '''
    Checks the compatibility condition (lam1 <= 1, lam2 = 1, lam3 >= 1)

    Parameters:
        F (ndarray [shape (3, 3)]):
            deformation gradient for martensite variant I
        G (ndarray [shape (3, 3)]):
            deformation gradient for martensite variant J or austenite
    Returns:
        lam (ndarray [shape (1, 3)]):
            eigenvalue for matrix C in ascending order
        e (ndarray [shape (3, 3)]):
            eigenvector for matrix C as column vectors associated with the eigenvalue
    '''
    #calculates C matrix
    G_inv = np.linalg.inv(G)
    C = G_inv.T @ F.T @ F @ G_inv
    
    #checks if C is not identity
    if np.all(np.equal(C , np.eye(3))):
        print('ERROR: C is tensor is an identity matrix')
        return 0
    
    #calculates the eigenvale lam and vector e
    lam, e = np.linalg.eig(C)
    
    #sorting eigenvector and values from low to high (ascending order)
    idx = lam.argsort()
    lam = lam[idx]
    e = e[:,idx]

    #checks if kinematic compatibility is met
    if not (lam[0] <= 1 and lam[1] == 1 and lam[2] >= 1):
        print('WARNING: eigenvalues does not satisfy kinematic compatibility')
        print(' lam1 = ', lam[0])
        print(' lam2 = ', lam[1])
        print(' lam3 = ', lam[2] , '\n')

    return lam, e