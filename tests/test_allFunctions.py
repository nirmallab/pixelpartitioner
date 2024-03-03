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
def dirPath():
    # Returns the folder path for use in tests
    folderPath = os.path.join(os.getcwd(), 'tests', 'data')
    return folderPath

@pytest.fixture
def imagePaths(dirPath):
    # Uses dirPath fixture to get image paths
    return getImages(folderPath=dirPath, extension='tif')


def test_getImages(dirPath):  # Parameter name matches the fixture name
    # Run function with the path provided by the fixture
    imagePaths = getImages(folderPath=dirPath, extension='tif')
    # Test: expecting 2 .tif images in the specified directory
    assert len(imagePaths) == 2
    
def test_PixelPartitioner(imagePaths,dirPath):
    # run function
    results = PixelPartitioner (imagePaths=imagePaths, outputFolder=dirPath)
    # test    
    assert results.loc['image_1.tif'].tolist()[0] == pytest.approx(0.208126)

def test_plotPixel():
    import matplotlib.pyplot as plt
    imagePath = os.path.join(os.getcwd(), 'tests', 'data', 'image_1.tif')
    plotPixel(imagePath)
    fig = plt.gcf()
    # test
    assert fig.axes[0].get_title() == "Original Image"
    
    