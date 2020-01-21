#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_file.py                                                      #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Monday, January 20th 2020, 9:25:05 pm                       #
# Last Modified : Monday, January 20th 2020, 9:27:07 pm                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Tests FileObject and FileFactory classes."""
import os
import shutil

import numpy as np
import pandas as pd
import pytest
from pytest import mark


from datastudio.base.file import *

class FileIOTests:

    @mark.fileio
    def test_file_io_numpy_array_write(self, get_numpy_arrays):     
        # Clean up data
        shutil.rmtree("./tests/test_data/test_file/")  
        # Test with correct extension
        a,b,c,d,e = get_numpy_arrays
        path = "./tests/test_data/test_file/numpy_array_a.npy"
        f = FileIONumpy()
        f.write(path, content=a)
        assert os.path.exists(path), "Numpy file not created"
        # Test without correct extension
        path = "./tests/test_data/test_file/numpy_array_b.txt"
        newpath = path + '.npy'
        f.write(path, content=b)
        assert not os.path.exists(path), "File with incorrect extension saved"
        assert os.path.exists(newpath), "File with correct extension not saved"
        
    @mark.fileio
    def test_file_io_numpy_array_read(self, get_numpy_arrays):        
        # Test .npy
        a,b,c,d,e = get_numpy_arrays
        path = "./tests/test_data/test_file/numpy_array_a.npy"
        f = FileIONumpy()
        a_test = f.read(path)
        assert np.array_equal(a,a_test), "Numpy array read failed. Not equal to original"


    @mark.fileio
    def test_file_io_csv(self):             
        pathin = "./tests/test_data/san_francisco.csv"
        pathout = "./tests/test_data/test_file/san_francisco.csv"
        if os.path.exists(pathout):
            os.remove(pathout)
        f = FileIOCSV()        
        df = f.read(pathin)
        assert isinstance(df, pd.DataFrame), "FileIOCSV didn't return a dataframe"        
        f.write(pathout, content=df)
        assert os.path.exists(pathout), "FileIOCSV didn't write file."
        
    @mark.fileio
    def test_file_io_csv_gsv(self):             
        pathin = "./tests/test_data/san_francisco.csv.gz"
        pathout = "./tests/test_data/test_file/san_francisco.csv.gz"
        if os.path.exists(pathout):
            os.remove(pathout)
        f = FileIOCSVgz()        
        df = f.read(pathin)
        assert isinstance(df, pd.DataFrame), "FileIOCSVgz didn't return a dataframe"        
        f.write(pathout, content=df)
        assert os.path.exists(pathout), "FileIOCSVgz didn't write file."        

class FileTests:

    @mark.file
    def test_file_init(self):     
        path = "./tests/test_data/san_francisco.csv"
        f = File(path=path)
        name = f.name
        path2 = f.path
        directory = f.directory
        locked = f.is_locked
        exists = f.exists
        filename = f.filename
        file_ext = f.file_ext
        assert name == 'san_francisco', "File Test: Invalid name"  
        assert path2 == path, "File Test: Invalid path"  
        assert directory == './tests/test_data', "File Test: Invalid directory"  
        assert locked is False, "File Test: Invalid locked value"  
        assert exists is True, "File Test: Invalid exists"  
        assert filename == 'san_francisco.csv', "File Test: Invalid filename"  
        assert file_ext == '.csv', "File Test: Invalid file extension"  

    @mark.file
    def test_file_copy(self):
        pathfrom =  "./tests/test_data/san_francisco.csv"
        pathto = "./tests/test_data/test_file/san_francisco.csv"
        if os.path.exists(pathto):
            os.remove(pathto)
        f = File(pathfrom)
        f.copy(pathto)
        assert os.path.exists(pathto), "File Test: Copy - File didn't copy"

    @mark.file
    def test_file_move(self):
        pathfrom =  "./tests/test_data/san_francisco.csv"
        pathto = "./tests/test_data/test_file/san_francisco.csv"
        if os.path.exists(pathto):
            os.remove(pathto)
        f = File(pathfrom)
        f.move(pathto)
        path = f.path
        directory = f.directory        
        assert not os.path.exists(pathfrom), "File Test: move - File didn't move"
        assert os.path.exists(pathto), "File Test: move - File didn't move"
        assert path == pathto, "File Test: Move - File path not updated"
        assert directory == os.path.dirname(pathto), "File Test: Move File directory not updated"
        # Test locked file
        f.lock()
        f.move(pathfrom)
        assert not os.path.exists(pathfrom), "File Test: move - Locked file moved."
        # Put the file back
        f.unlock()
        f.move(pathfrom)
        assert os.path.exists(pathfrom), "File Test: move - Unlocked file not moved."

  
    @mark.file
    def test_file_rename(self):
        path =  "./tests/test_data/san_francisco.csv"
        name = "bay_area.txt"
        newpath = "./tests/test_data/bay_area.csv"
        # Attempt to rename locked file.
        f = File(path)
        f.lock()
        f.rename(name)
        assert f.path == path, "Renamed locked file."
        f.unlock()
        locked = f.is_locked
        assert locked is False, "Unlock didn't work"
        f.rename(name)
        assert f.filename == "bay_area.csv", "File not renamed"
        assert f.path == newpath, "File not renamed"
        f.rename("san_francisco")

    @mark.file
    def test_file_csv(self):
        path =  "./tests/test_data/san_francisco.csv"
        f = File(path)
        # Read entire file
        df1 = f.read()
        assert isinstance(df1, pd.DataFrame), "Dataframe not returned."
        assert df1.shape[1] > 60, "Not all columns returned"
        # Read two columns
        df2 = f.read(columns=['id', 'bathrooms'])
        assert isinstance(df2, pd.DataFrame), "Dataframe not returned."
        assert df2.shape[1] == 2, "Number of columns not correct."
        # Write csv
        f.write(df1)
        df1 = f.read()
        assert isinstance(df1, pd.DataFrame), "Dataframe not returned."
        assert df1.shape[1] > 60, "Not all columns returned"
        # Write csv
        f.write(df2)
        df2 = f.read()
        assert isinstance(df2, pd.DataFrame), "Dataframe not returned."
        assert df2.shape[1] == 2, "Number of columns not correct."

    @mark.file
    def test_file_csv_gz(self):
        path =  "./tests/test_data/san_francisco.csv.gz"
        f = File(path)
        # Read entire file
        df1 = f.read()
        assert isinstance(df1, pd.DataFrame), "Dataframe not returned."
        assert df1.shape[1] > 60, "Not all columns returned"
        # Read two columns
        df2 = f.read(columns=['id', 'bathrooms'])
        assert isinstance(df2, pd.DataFrame), "Dataframe not returned."
        assert df2.shape[1] == 2, "Number of columns not correct."
        # Write csv
        f.write(df1)
        df1 = f.read()
        assert isinstance(df1, pd.DataFrame), "Dataframe not returned."
        assert df1.shape[1] > 60, "Not all columns returned"
        # Write csv
        f.write(df2)
        df2 = f.read()
        assert isinstance(df2, pd.DataFrame), "Dataframe not returned."
        assert df2.shape[1] == 2, "Number of columns not correct."

    @mark.file
    def test_file_numpy(self, get_numpy_arrays):
        path =  "./tests/test_data/test_file/numpy_array_a.npy"
        a,b,c,d,e = get_numpy_arrays
        f = File(path)
        # Read numpy array
        a_read = f.read()
        assert isinstance(a_read, (np.generic, np.ndarray)), "Numpy array not returned."
        assert np.array_equal(a,a_read), "Array read does not equal array written" 
        f.write(b)
        b_read = f.read()
        assert isinstance(b_read, (np.generic, np.ndarray)), "Numpy array not returned."
        assert np.array_equal(b,b_read), "Array read does not equal array written" 


