#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : conftest.py                                                       #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Monday, January 20th 2020, 9:26:05 pm                       #
# Last Modified : Monday, January 20th 2020, 9:26:52 pm                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
# %%
import os

import numpy as np
from pytest import fixture

@fixture(scope="session")
def get_numpy_arrays():
    a = np.arange(0,100)
    b = np.reshape(a, (25,4))
    c = np.logspace(0,100)
    d = np.reshape(c, (5,-1))
    e = np.array([a,b,c,d])
    return a, b, c, d, e




    