#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:56:57 2024
@author: Ajit Johnson Nirmal
"""

from pixelpartitioner.getImages import getImages
from pixelpartitioner.pixelpartitioner import pixelpartitioner
from pixelpartitioner.plotPixel import plotPixel
import os


def test_getImages (directory):
    # set up dir
    directory = os. getcwd() + '/pixelpartitioner/tests/data'
    # run function
    imagePaths = getImages(directory, extension='tif' )
    # test
    assert len(imagePaths) == 2

