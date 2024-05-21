import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread

a = imread("PIV_DATA/15deg/B00001.tif")
b = imread("PIV_DATA/15deg/B00001.tif")

a = a[:a.shape[0]//2]
b = b[b.shape[0]//2+1:]

fig, axs = plt.subplots(1, 2, figsize=(9, 4))
axs[0].imshow(a, cmap=plt.cm.gray)
axs[1].imshow(b, cmap=plt.cm.gray)
plt.show()

win_size = 32

a_win = a[:win_size, :win_size].copy()
b_win = b[:win_size, :win_size].copy()

fig, axs = plt.subplots(1, 2, figsize=(9, 4))
axs[0].imshow(a_win, cmap=plt.cm.gray)
axs[1].imshow(b_win, cmap=plt.cm.gray)
plt.show()