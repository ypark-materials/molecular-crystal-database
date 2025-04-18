'''
dfetch.py

dfetch module contains functions for molecular crystal database data wrangling

Author: Yunsu Park
Created: Feb 14 2025
Affiliation: University of California, Santa Barbara
Contact: yunsu@ucsb.edu
'''

import pandas as pd
import numpy as np
import os

def dfread(print_info):
    '''
    Fetches and reads the mc_data.csv and converts it to a pandas dataframe
    Deletes data not containing unit cell parameters

    Parameters:
        print_info (integer): 
            if 1 prints the dataframe directory and its info

    Returns:
        df_na (dataframe): 
            dataframe containing molecular crystal crystallography
        df_dir (string):
            dataframe directory
    '''
    # Fetches and reads the df
    df_dir = os.path.join(os.getcwd(), 'data', 'mc_data.csv') 
    df = pd.read_csv(df_dir)

    # Delets data not containing unit cell parameters
    necessary_header = ['a_ref', 'b_ref', 'c_ref', 'a_def', 'b_def', 'c_def', 'alpha_ref', 'beta_ref', 'gamma_ref', 'alpha_def', 'beta_def', 'gamma_def']
    df_na = df[df[necessary_header].notna().all(axis=1)]

    # prints df info
    if print_info == 1:
        print(df_dir)
        print(df.info()) 
    
    return df_na, df_dir

def dfload(df, header):
    '''
    Loads the unit cell parameters and user defined header parameters

    Parameters:
        df (dataframe): 
            molecular crystal dataframe
        header (list):
            dataframe header that will load list

    Returns:
        abc_ref (ndarray [shape (1, 3)]): 
            a b c unit cell parameter for the reference configuration
        abc_def (ndarray [shape (1, 3)]): 
            a b c unit cell parameter for the deformed configuration
        angle_ref (ndarray [shape (1, 3)]): 
            alpha beta gamma unit cell parameter for the reference configuration
        angle_def (ndarray [shape (1, 3)]): 
            alpha beta gamma unit cell parameter for the deformed configuration
        para (ndarray [shape (1, *)]):
            user defined parameter
    '''
    
    # Checks if header exists
    if header != [] and header not in df.columns:
        print(f'ERROR: "{header}" is not a header in the df')
        return 1

    # Defines the headers to load
    header = ['a_ref', 'b_ref', 'c_ref', 'a_def', 'b_def', 'c_def', 'alpha_ref', 'beta_ref', 'gamma_ref', 'alpha_def', 'beta_def', 'gamma_def'] + header
    
    # Deletes all the rows where header is NaN
    df = df[df[header].notna().all(axis=1)]

    # Loads the unit cell parameters
    abc_ref = df[['a_ref', 'b_ref', 'c_ref']].values #reference state
    abc_def = df[['a_def', 'b_def', 'c_def']].values #deformed state

    angle_ref = np.radians(df[['alpha_ref', 'beta_ref', 'gamma_ref']].values) #reference state
    angle_def = np.radians(df[['alpha_def', 'beta_def', 'gamma_def']].values) #reference state

    # Loads the header parameters
    para = df[header]

    return abc_ref, abc_def, angle_ref, angle_def, para

def dim_to_array(dim_array):
    '''
    Converts geometric data string data of crystal geometry to variables

    Parameters:
        df (dataframe): 
            molecular crystal dataframe
        header (list):
            dataframe header that will load list

    Returns:
        abc_ref (ndarray [shape (1, 3)]): 
            a b c unit cell parameter for the reference configuration
        abc_def (ndarray [shape (1, 3)]): 
            a b c unit cell parameter for the deformed configuration
        angle_ref (ndarray [shape (1, 3)]): 
            alpha beta gamma unit cell parameter for the reference configuration
        angle_def (ndarray [shape (1, 3)]): 
            alpha beta gamma unit cell parameter for the deformed configuration
        para (ndarray [shape (1, *)]):
            user defined parameter
    '''
    dim_float = np.zeros([dim_array.size, 3])

    for n_array in range(dim_array.size):
        #dim_string =" ".join(map(str, dim_array.iloc[n_array]))
        dim_string = dim_array.iloc[n_array]
        # Split the string by 'x'
        dims = dim_string.split('x')
        # Process each dimension
        processed_dims = []
        
        for dim in dims:
            if 'um' in dim:  # Check if 'um' is in the dimension
                processed_dims.append(float(dim.replace('um', '')) * 10**-6)  # Convert to m
            elif 'mm' in dim:  # Check if 'mm' is in the dimension
                processed_dims.append(float(dim.replace('mm', '')) * 10**-3)  # Convert to m
            elif 'nm' in dim:  # Check if 'nm' is in the dimension
                processed_dims.append(float(dim.replace('nm', '')) * 10**-9)  # Convert to m
            elif 'cm' in dim:  # Check if 'nm' is in the dimension
                processed_dims.append(float(dim.replace('cm', '')) * 10**-2)  # Convert to m
            else:
                processed_dims.append(float(dim))  # Convert to integer as-is

        dim_float[n_array, :] = np.array(processed_dims)

    return dim_float