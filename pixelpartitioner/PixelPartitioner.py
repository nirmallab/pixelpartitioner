#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on Tue Feb 13 22:02:40 2024
# @author: Ajit Johnson Nirmal
"""

The `PixelPartitioner` function applies multi-class OTSU thresholding to a set of images 
to partition pixels based on intensity. It iteratively increases the number of classes for 
images with a high percentage of pixels exceeding a specified threshold, accumulating 
results in a DataFrame. The final results are saved in a CSV file within the specified output folder.

"""


import os
import shutil
import numpy as np
import tifffile
import pandas as pd
from skimage import filters, exposure, color
from skimage.color import rgb2gray


def process_images(image_paths, outputFolder, num_classes):
    results = []  # To store results for each image
    
    # Automatically generate the outputFolderName based on num_classes
    outputFolderName = f"{num_classes}_class_OTSU"
    
    # Construct the final output folder path by combining outputFolder and outputFolderName
    final_output_folder = os.path.join(outputFolder, outputFolderName)
    
    # Clear the final output folder if it exists, then recreate it
    if os.path.exists(final_output_folder):
        shutil.rmtree(final_output_folder)
    os.makedirs(final_output_folder)
    
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    for image_path in image_paths:
        # Load the image using tifffile
        image = tifffile.imread(image_path)
        
        # Check if the image is RGB and convert to grayscale if necessary
        if image.ndim == 3 and image.shape[2] == 3:
            image = rgb2gray(image)
        
        # Normalize the image intensity to the range [0, 1]
        normalized_image = exposure.rescale_intensity(image.astype(np.float32), out_range=(0, 1))
        
        # Apply multi-class Otsu thresholding with user-defined number of classes
        thresholds = filters.threshold_multiotsu(normalized_image, classes=num_classes)
        regions = np.digitize(normalized_image, bins=thresholds)
        
        # Calculate the percentage of pixels in the brightest class
        brightest_pixels = np.sum(regions == num_classes - 1)
        total_pixels = np.prod(regions.shape)
        percentage_brightest = (brightest_pixels / total_pixels) * 100
        
        # Highlight regions in the brightest class
        if normalized_image.ndim == 2:
            highlighted_image = color.gray2rgb(normalized_image)
        highlighted_image[regions == num_classes - 1] = [1, 0, 0]
        
        # Ensure the final output folder exists
        if not os.path.exists(final_output_folder):
            os.makedirs(final_output_folder)
        
        # Construct the output image path using the final output folder path
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)
        output_image_path = os.path.join(final_output_folder, f"{name}_overlay{ext}")
        
        # Save the highlighted image using tifffile
        tifffile.imwrite(output_image_path, (highlighted_image * 255).astype(np.uint8))
        
        # Append results
        results.append({'FileName': name + ext, f"{num_classes}_class_OTSU": percentage_brightest})

    # Convert results to DataFrame
    df = pd.DataFrame(results)
    return df



def PixelPartitioner (imagePaths, 
                      outputFolder, 
                      num_classes=2,
                      percentPositiveThreshold=5,
                      verbose=True):
    
    """
    
Parameters:
        imagePaths (list of str): 
            A list of paths to images that will undergo pixel partitioning.
        outputFolder (str): 
            The directory where the output results, including a master DataFrame as a CSV file, will be saved. The function will create a 'results' subfolder in this directory for the CSV file.
        num_classes (int, optional): 
            The initial number of classes to use for OTSU thresholding. Default is 2.
        percentPositiveThreshold (int or float, optional): 
            The percentage threshold used to determine if an image has a greater percentage of pixels in the highest class than specified. Images exceeding this threshold will be re-processed in subsequent iterations with an increased number of classes. Default is 5.
        verbose (bool, optional): 
            If True, the function will print verbose messages about its progress. Default is True.
    
Returns:
        DataFrame (pandas.DataFrame): 
            A DataFrame containing the cumulative results of the pixel partitioning process, with columns representing the results of different num_classes iterations.
    
Example:
        ```python
            
        imagePaths = ['/path/to/images/img1.tif', '/path/to/images/img2.tif']
        outputFolder = '/path/to/output'
        num_classes = 2
        percentPositiveThreshold = 5
    
        # Execute pixel partitioning
        results_df = pp.PixelPartitioner(imagePaths=imagePaths, 
                                      outputFolder=outputFolder, 
                                      num_classes=num_classes, 
                                      percentPositiveThreshold=percentPositiveThreshold)
    
    """

    
    # loop through all TSU thresholds
    paths_to_remaining_files = imagePaths[:]  # Copy of the initial list of image paths
    master_df = pd.DataFrame()  # Initialize an empty DataFrame for accumulating results
    first_num_classes = num_classes  # Store the initial num_classes value
    
    # Loop until there are no remaining files to process
    while len(paths_to_remaining_files) > 0:
        
        # Print statements for verbose output
        if verbose: 
            print(f'Performing OTSU Thresholding with {num_classes} classes')
        
        # Perform multi-class OTSU thresholding
        df = process_images(image_paths=paths_to_remaining_files, outputFolder=outputFolder, num_classes=num_classes)
        
        # Identify images that have a greater percentage of pixels than the user-specified threshold
        column_name = f"{num_classes}_class_OTSU"  # Dynamic column name based on num_classes
        failedSample = df[df[column_name] > percentPositiveThreshold]['FileName'].tolist()
        
        # Prepare the DataFrame for merging
        df.set_index('FileName', inplace=True)
        
        # Merge with the master DataFrame
        if master_df.empty:
            master_df = df[[column_name]].copy()
        else:
            # Ensuring all previous iterations are carried forward even if they're missing in the current df
            master_df = master_df.join(df[[column_name]], how='outer')
    
        # Update paths for the next iteration
        if failedSample:
            path_to_prepend = os.path.dirname(paths_to_remaining_files[0])
            paths_to_remaining_files = [os.path.join(path_to_prepend, file_name) for file_name in failedSample]
            num_classes += 1  # Increase the number of classes for the next iteration
        else:
            break  # Exit loop if no failed samples
    
    # Sort the master DataFrame based on the first iteration results, from largest to smallest
    first_iteration_column = f"{first_num_classes}_class_OTSU"
    if not master_df.empty and first_iteration_column in master_df.columns:
        master_df.sort_values(by=first_iteration_column, ascending=False, inplace=True)
    
    # Save master_df that contains the cumulative results with num_classes iterations as columns
    results_folder = os.path.join(outputFolder, 'results')
    # Create the 'results' folder if it does not exist
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    # Specify the filename for saving the DataFrame
    filename = 'master_results.csv'
    # Construct the full path to the file
    file_path = os.path.join(results_folder, filename)
    # Save the master_df DataFrame to CSV in the 'results' folder
    master_df.to_csv(file_path, index=True)
    if verbose:
        print("---------------------------------------------")
        print(f"Master DataFrame saved to: {file_path}")
        print(f"Thresholded Images saved to: {outputFolder}")
    
    # return data
    return master_df

