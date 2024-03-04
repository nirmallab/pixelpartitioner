---
hide:
  - toc        
  - navigation
---

[![Downloads](https://static.pepy.tech/badge/pixelpartitioner)](https://pepy.tech/project/pixelpartitioner)
[![docs](https://github.com/nirmallab/pixelpartitioner/actions/workflows/docs.yml/badge.svg)](https://github.com/nirmallab/pixelpartitioner/actions/workflows/docs.yml)
[![build-unix-mac-win](https://github.com/nirmallab/pixelpartitioner/actions/workflows/build-unix-mac-win.yml/badge.svg)](https://github.com/nirmallab/pixelpartitioner/actions/workflows/build-unix-mac-win.yml)


## Pixel Partitioner: Tools for pixel partitioning, intensity-based segmentation, and visualization.

Pixel Partitioner is a computational tool designed to facilitate the analysis of single-layer TIFF images by quantifying the presence of specific markers within these images. The primary objective of this package is to discern and quantify signal within images, returning the percentage of pixels that are positive for a designated marker.

**Input Specification**: The package processes single-layer TIFF images, catering to the requirements of image analysis in fields such as cancer biology, where accurate identification of markers is crucial for understanding disease initiation and progression.

**Methodological Approach**: Pixel Partitioner employs a multi-class Otsu thresholding method as its core algorithm. This technique is pivotal for its ability to differentiate between pixels positive for the marker of interest and the background. Initially, the package applies a two-class Otsu thresholding to segregate positive pixels. Recognizing the challenge of high background noise, which may result in overclassification, the package implements an innovative strategy to refine its analysis. It operates under the assumption that the expression of a given marker should not exceed a certain threshold - by default, set at 5% of the total pixels in any given image. If the percentage of positive pixels surpasses this threshold, indicating potential overclassification due to background noise, the software automatically escalates to a three-class Otsu thresholding. This process is iteratively conducted until the positive pixel percentage falls below the set threshold, ensuring robustness in signal identification.

**Adaptive Features**: An essential aspect of Pixel Partitioner is its adaptability. It records detailed information regarding the thresholding process and the resultant pixel classification in a dataframe, which is subsequently saved as a CSV file in a user-specified output directory. Moreover, to enhance user confidence in the results, the package generates modified copies of the original images, overlaying the classified positive pixels. This visual output allows users to verify the accuracy of the segmentation. In instances where the output does not meet the user's expectations, options are available to adjust the `percentPositiveThreshold` parameter or exclude particularly challenging images from the dataset, thereby offering flexibility in handling diverse image sets.

In summary, Pixel Partitioner stands as a tool that streamlines the quantification of specific markers in single-layer TIFF images through advanced thresholding techniques. Its capability to adaptively refine its approach based on the background noise and the specific requirements of the analysis makes it a valuable resource for scientists and researchers engaged in image analysis, particularly within the realms of cancer biology and other fields where precise marker quantification is imperative.