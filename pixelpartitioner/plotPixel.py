#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on Sun Mar  3 14:13:43 2024
# @author: Ajit Johnson Nirmal
"""

The `plotPixel` function visualizes the effect of multi-class OTSU thresholding on an image, 
highlighting the positive regions determined by the threshold. he result is a side-by-side plot 
of the original and highlighted images, with a quantitative display of the positive pixels' 
percentage.

"""

#import
import matplotlib.pyplot as plt
import numpy as np
import tifffile
from skimage import exposure, filters
from skimage.color import rgb2gray, gray2rgb

# function
def plotPixel(imagePath, 
              num_classes=2):

    """
Parameters:
        image_path (str): 
            The path to the image file to be processed. Supports formats readable by tifffile, such as TIFF.
        num_classes (int, optional): 
            The number of classes to divide the pixel intensity range into using OTSU thresholding. Default is 2.
    
Returns:
        Plot (matplotlib): 
            Returns a plot comparing original image with the regions identified to be positive for signal.
    
    
Example:
    ```python
    
    # Plot the results for image.tif
    
    pp.plotPixel(image_path='/path/to/image.tif', num_classes=3)
    
    ```
    
    """

    
    # Load the image using tifffile
    image = tifffile.imread(imagePath)
    
    # Check if the image is RGB and convert to grayscale if necessary
    if image.ndim == 3 and image.shape[2] == 3:
        greyImage = rgb2gray(image)
    
    # Normalize the image intensity to the range [0, 1]
    normalized_image = exposure.rescale_intensity(greyImage.astype(np.float32), out_range=(0, 1))
    
    # Apply multi-class Otsu thresholding with user-defined number of classes
    thresholds = filters.threshold_multiotsu(normalized_image, classes=num_classes)
    regions = np.digitize(normalized_image, bins=thresholds)
    
    # Calculate the percentage of pixels in the brightest class
    brightest_pixels = np.sum(regions == num_classes - 1)
    total_pixels = np.prod(regions.shape)
    percentage_brightest = (brightest_pixels / total_pixels) * 100
    
    # Highlight regions in the brightest class
    highlighted_image = gray2rgb(normalized_image) if normalized_image.ndim == 2 else normalized_image.copy()
    highlighted_image[regions == num_classes - 1] = [1, 0, 0]  # Red for the brightest class
    
    # Plotting
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].imshow(image, cmap='gray')
    ax[0].set_title('Original Image')
    ax[0].axis('off')
    
    ax[1].imshow(highlighted_image)
    ax[1].set_title('Highlighted Positive Regions')
    ax[1].axis('off')
    
    plt.figtext(0.5, 0.01, f'Percentage of Positive Pixels: {percentage_brightest:.2f}%', ha="center", fontsize=12)
    plt.tight_layout()
    
    #plt.show()