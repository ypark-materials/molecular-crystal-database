'''
microstruct.py

Microstruct module contains functions for shape-memory alloy microstructure calculations

Author: Yunsu Park
Created: Jan 7 2025
Affiliation: University of California, Santa Barbara
Contact: yunsu@ucsb.edu
''' 

import numpy as np

def kincomp(F, G):
    G_inv = np.linalg.inv(G)
    C = G_inv.T @ F.T @ F @ G_inv
    
    if np.all(np.equal(C , np.eye(3))):
        return 0
    
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
    
    #calculates twinning for type I
    kap = 1

    n = (np.sqrt(lam[2]) - np.sqrt(lam[0]))/np.sqrt(lam[2]-lam[0]) * (-np.sqrt(1-lam[0]) * (G.T @ e[:,0]) + kap*np.sqrt(lam[2]-1)* (G.T @ e[:,2]))
    rho = np.linalg.norm(n)
    n = n/rho

    a = rho * (np.sqrt(lam[2]*(1-lam[0])/(lam[2]-lam[0]))*e[:,0] + 
               kap*np.sqrt(lam[0]*(lam[2]-1)/(lam[2]-lam[0]))*e[:,2])

    s = np.linalg.norm(a) * np.linalg.norm( (G_inv @ n) )
    nu = a/np.linalg.norm(a)
    K = (G_inv @ n)/ np.linalg.norm( (G_inv @ n) )
    
    #calculates twinning for type II
    kap = -1

    n_n = (np.sqrt(lam[2]) - np.sqrt(lam[0]))/np.sqrt(lam[2]-lam[0]) * (-np.sqrt(1-lam[0]) * (G.T @ e[:,0]) + kap*np.sqrt(lam[2]-1)* (G.T @ e[:,2]))
    rho_n = np.linalg.norm(n_n)
    n_n = n_n/rho_n

    a_n = rho_n * (np.sqrt(lam[2]*(1-lam[0])/(lam[2]-lam[0]))*e[:,0] + 
               kap*np.sqrt(lam[0]*(lam[2]-1)/(lam[2]-lam[0]))*e[:,2])

    s_n = np.linalg.norm(a_n) * np.linalg.norm( (G_inv @ n_n) )
    nu_n = a_n/np.linalg.norm(a_n)
    K_n = (G_inv @ n_n)/ np.linalg.norm( (G_inv @ n_n) )

    return n, a, s, nu, K, n_n, a_n, s_n, nu_n, K_n

def supcomp(F): 
    pass

