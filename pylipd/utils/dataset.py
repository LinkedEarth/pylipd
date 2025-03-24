#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 17:56:50 2023

@author: deborahkhider

Makes it easy to import some specific lpd files for testing and documentation purpose
"""

from pathlib import Path
import glob
from pylipd.lipd import LiPD

DATA_DIR = Path(__file__).parents[1].joinpath("data").resolve()
FOLDER_DIR = DATA_DIR.joinpath('Pages2k/')
TEMP12_DIR = DATA_DIR.joinpath('Temp12k')

def available_dataset_names():
    '''Helper function to easily see what datasets are available to load

    Returns
    -------
    names : list
        List of datasets available via the `load_dataset` method. 

    '''
    path_name = str(DATA_DIR)+'/*.lpd'
    files_unique = glob.glob(path_name)
    
    dir_name = str(FOLDER_DIR)+'/*.lpd'
    files_dir = (glob.glob(dir_name))
    
    temp12_dir = str(TEMP12_DIR)+'/*.lpd'
    temp12_files = (glob.glob(temp12_dir)) 
    
    files = files_unique + files_dir + temp12_files
    
    names = []
    for item in files:
        names.append(item.split('/')[-1].rsplit('.', 1)[0])
    
    return names


def load_datasets(names):
    
    if type(names) is not list:
        names = [names]
    
    path_name = str(DATA_DIR)+'/*.lpd'
    files_unique = glob.glob(path_name)
    dir_name = str(FOLDER_DIR)+'/*.lpd'
    files_dir = (glob.glob(dir_name)) 
    temp12_dir = str(TEMP12_DIR)+'/*.lpd'
    temp12_files = (glob.glob(temp12_dir)) 
    
       
    files = files_unique + files_dir + temp12_files
    
    full_paths = []
    for name in names:
       try:
           full_paths.append(list(filter(lambda a: name in a,files))[0])
       except:
           pass
    
    L = LiPD()
    print(full_paths)
    L.load(full_paths)
   
    return L

def load_dir(name = 'Pages2k'):
    
        
    L = LiPD()
    if name == 'Pages2k':
        L.load_from_dir(str(FOLDER_DIR))
    elif name == 'Temp12k':
        L.load_from_dir(str(TEMP12_DIR))
    else:
        raise ValueError('Directory should be either Pages2k or Temp12k')
    
    return L
