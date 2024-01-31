# Image Blending using Laplacian Pyramids

This project implements image blending using Laplacian pyramids. The goal is to seamlessly blend two images based on a user-defined region of interest (ROI) using a Gaussian mask.

## Overview

The implementation includes the following main components:

1. **Laplacian Pyramids:**
   - `laplacian_pyramid`: Generates Laplacian pyramids for two input images.
   - `pyrUp` and `pyrDown`: Functions for upsampling and downsampling images in the pyramid.

2. **Gaussian Pyramids:**
   - `build_gaussian_pyramid`: Constructs a Gaussian pyramid for the user-defined mask.

3. **Blending:**
   - `blend_pyramids`: Combines the Laplacian pyramids based on the Gaussian pyramid of the mask.

4. **Collapsing:**
   - `collapse_pyramid`: Reconstructs the final blended image from the blended Laplacian pyramids.

5. **User Interaction:**
   - `calling`: Takes input images, user-defined parameters, and displays intermediate results for visualization.

6. **Main Functionality:**
   - `main`: Loads images, prompts the user to select a region of interest, and performs the blending.

## Dependencies

- OpenCV (cv2)
- NumPy

## Usage

1. Install the required dependencies:

   ```bash
   pip install opencv-python numpy

2. Releated Links (Google Drive links):
	
	-input target images:
	https://drive.google.com/drive/folders/1s-lSPJQJWiXayn-aagLQ3bN_C-sJFGgU?usp=drive_link
	
	This link includes the target images which we blend the mask region with, you should paste the paths of images after downloading the folder to the "image2 = cv2.imread("target image path here")" part of the code.

	-input source images:
	https://drive.google.com/drive/folders/1CmtDTdTr2ChPgfZbnGAnusDP8BHulcEr?usp=drive_link

	This link includes the source images which i create the images by cropping this images to get the mask regions.

	-edited images to get mask:
	https://drive.google.com/drive/folders/1fBdSG4zODeUnUxPwvO0phKe41QsYtlEM?usp=drive_link

	This link includes the images where i select the mask regions with using selectROI. You should paste the paths of the images after downloading the folder to the "image1 = cv2.imread("source image here")" part of the code.

	-mask regions:
	https://drive.google.com/drive/folders/12HGpgNuRpUO8YSIkHOIfjTOmAO-i_RtB?usp=drive_link

	This link includes the selected mask regions.

	-output images:
	https://drive.google.com/drive/folders/1sZJXg9EwxL6CpFXfs2X7QhFNVDlO6Kwr?usp=drive_link

	This link includes the reconstructed blended images(final outputs.)

