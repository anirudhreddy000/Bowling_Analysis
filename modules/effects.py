import cv2
import numpy as np

def apply_vignette(frame, sigma=250):
    rows, cols = frame.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, sigma)
    kernel_y = cv2.getGaussianKernel(rows, sigma)
    kernel = kernel_y * kernel_x.T
    mask = kernel / kernel.max()
    vignette = frame.copy()
    for i in range(3):
        vignette[:, :, i] = vignette[:, :, i] * mask
    return vignette
