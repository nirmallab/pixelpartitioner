#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:56:57 2024
@author: Ajit Johnson Nirmal
"""

# package functions
from pixelpartitioner.getImages import getImages
from pixelpartitioner.PixelPartitioner import PixelPartitioner
from pixelpartitioner.plotPixel import plotPixel

# other packages
import os
import pytest

@pytest.fixture
def dirPath ():
    # set up dir
    folderPath = str(os. getcwd()) + '/pixelpartitioner/tests/data'
    return folderPath


def test_getImages (folderPath):
    # run function
    imagePaths = getImages(folderPath=folderPath, extension='tif' )
    # test
    assert len(imagePaths) == 2