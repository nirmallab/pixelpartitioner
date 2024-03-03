#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Created on Sun Mar  3 14:05:51 2024
#@author: Ajit johnson Nirmal

"""
The `pp.getImages` function retrieves image file paths from a specified directory, 
with an optional filter for file extensions. It simplifies collecting images for analysis, 
allowing for specific format selection in folders with multiple elements. 

"""
# import 
import os


# function

def getImages (folderPath, 
               extension=None):

    """
Parameters:
    folderPath (str):
        The path to the directory from which files will be listed. This directory should already exist and be accessible at the time of function invocation.
        
    extension (str, optional):
        The file extension used to filter the files listed by the function. If specified, the function will only return files that end with the given extension (e.g., 'tif' ). The extension should not include the leading period ('.'). If None or not provided, all files in the directory will be listed. Default is None.

Returns:
    list (list): 
        A list containing the full paths to the files that meet the criteria. If an extension is specified, only files with that extension will be included in the list.


Example:
    ```python
    
    # Listing all `tif` files in a directory called 'documents':

    imagePaths = pp.getImages(directory='/path/to/dir/documents', extension = 'tif')
    
    ```
    
    
"""
    
    files = []  # List to store the paths of files
    # Normalize the extension to ensure it starts with a dot
    if extension and not extension.startswith('.'):
        extension = '.' + extension

    for file in os.listdir(folderPath):
        file_path = os.path.join(folderPath, file)
        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            # If extension is provided, filter files by the extension
            if extension:
                if file.endswith(extension):
                    files.append(file_path)
            else:
                files.append(file_path)

    return files
