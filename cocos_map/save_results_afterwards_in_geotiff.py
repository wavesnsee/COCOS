"""
Created on Thu May 29 16:42:25 2023

@author: ffournier
"""

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from pathlib import Path
from glob import glob
import numpy as np
import cv2
import pdb
import collections


def get_grid_resolution(results):
    resolution = results['grid_X'][0, 1] - results['grid_X'][0, 0]
    print(f'resolution: {resolution} m')
    return resolution

def rotate_vector(data, theta):
    # make rotation matrix
    co = np.cos(theta)
    si = np.sin(theta)
    rotation_matrix = np.array(((co, -si), (si, co)))

    # rotate data vector
    return data.dot(rotation_matrix)

def rotateAndScale(img, scaleFactor=0.5, degreesCCW=30):
    oldY, oldX, channels = img.shape  # note: numpy uses (y,x) convention but most OpenCV functions use (x,y)
    M = cv2.getRotationMatrix2D(center=(oldX / 2, oldY / 2), angle=degreesCCW,
                                scale=scaleFactor)  # rotate about center of image.

    # choose a new image size.
    newX, newY = oldX * scaleFactor, oldY * scaleFactor
    # include this if you want to prevent corners being cut off
    r = np.deg2rad(degreesCCW)
    newX, newY = (abs(np.sin(r) * newY) + abs(np.cos(r) * newX), abs(np.sin(r) * newX) + abs(np.cos(r) * newY))

    # the warpAffine function call, below, basically works like this:
    # 1. apply the M transformation on each pixel of the original image
    # 2. save everything that falls within the upper-left "dsize" portion of the resulting image.

    # So I will find the translation that moves the result to the center of that region.
    (tx, ty) = ((newX - oldX) / 2, (newY - oldY) / 2)
    M[0, 2] += tx  # third column of matrix holds translation, which takes effect after rotation.
    M[1, 2] += ty

    rotatedImg = cv2.warpAffine(img, M, dsize=(int(newX), int(newY)))
    return rotatedImg



# execution options
plot_only_bathy = True
plot_all_results = True
date = '20230208'
hour = '16h'
# date = '20220323'
# hour = '15h'
# date = '20220709'
# hour = '11h'
vertical_ref = 'IGN69'#'WL' or 'IGN69'
# vertical_ref = 'WL'#'WL' or 'IGN69'

# configuration corresponding to given results
fieldsite = 'wavecams_palavas_stpierre'
cam_names = ['St_Pierre_1']

# resolution of input projected images
proj_imgs_res = 1.0

# bathy grid resolutions
bathy_grid_resolutions = [8]
calcdmd = 'standard' # standard or robust

for cam_name in cam_names:
    print(cam_name)
    
    # define WL_ref_IGN69
    if date == '20220314':
        WL_ref_IGN69 = 0.60 - 0.307
    elif date == '20220323':
        WL_ref_IGN69 = 0.19 - 0.307
    elif date == '20230208':
        WL_ref_IGN69 = 0.112 - 0.307

    # for bathy_grid_resolution in bathy_grid_resolutions:
    for bathy_grid_resolution in bathy_grid_resolutions:
        # load results
        output_dir = f'/home/florent/shared/florent/Projects/Palavas/Surfreef_project/results/{fieldsite}/{cam_name}/{date}/{hour}/'
        try:
            # f_results = glob(output_dir + f'/results_CPU_speed_{cpu_speed}_calcdmd_{calcdmd}_exec_time_*.npz')[0]
            f_results = glob(output_dir + f'/results_grid_res_{bathy_grid_resolution}_calcdmd_{calcdmd}_exec_time_*.npz')[0]
        except IndexError:
            continue

        results = np.load(f_results)
        basename = Path(f_results).stem


        # get grid resolution
        resolution = get_grid_resolution(results)
        
        pdb.set_trace()

        

