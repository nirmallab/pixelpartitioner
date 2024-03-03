#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:56:57 2024
@author: Ajit Johnson Nirmal
"""

from pixelpartitioner.getImages import getImages
from pixelpartitioner.PixelPartitioner import PixelPartitioner
from pixelpartitioner.plotPixel import plotPixel
import os


def test_getImages (directory):
    # set up dir
    dirPath = os. getcwd() + '/pixelpartitioner/tests/data'
    print(str(directory))
    # run function
    imagePaths = getImages(directory=dirPath, extension='tif' )
    # test
    assert len(imagePaths) == 2

