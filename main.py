import tifffile as tiff
import numpy as np
from scipy.signal import correlate
import matplotlib.pyplot as plt
from scipy import stats
from scipy.ndimage import median_filter


tif_array = tiff.imread("B00001.tif")
win_size = 16

twoimages = np.array(tif_array)
img1 = twoimages[:twoimages.shape[0]//2, :]
img2 = twoimages[twoimages.shape[0]//2 :, : ]

delta_t = 6e-6
pix_density = 81_000

# def replace_outliers(data, win_size=3, threshold=1.3):
#     count = 0
#     z = stats.zscore(data, nan_policy='omit')
#     data_out = data.copy()
#     for i in range(data.shape[0]):
#         for j in range(data.shape[1]):
#             if z[i, j] > threshold:
#                 # Calculate local mean
#                 count += 1
#                 local_mean = np.mean(data[max(0, i-win_size):min(data.shape[0], i+win_size+1),
#                                               max(0, j-win_size):min(data.shape[1], j+win_size+1)])
#                 data_out[i, j] = local_mean
#     print('Total outliers removed:', count)
#     return data_out


def convolution(img1, img2, win_size):
    ys = np.arange(0, img1.shape[0], win_size)
    xs = np.arange(0, img1.shape[1], win_size)
    dys = np.zeros((len(ys), len(xs)))
    dxs = np.zeros((len(ys), len(xs)))
    
    for iy, y in enumerate(ys):
        for ix, x in enumerate(xs):
            int_win = img1[y:y + win_size, x:x + win_size]
            search_win = img2[y:y + win_size, x:x + win_size]
            cross_corr = correlate(search_win - search_win.mean(), int_win - int_win.mean(), method="fft")
            #cross_corr = correlate(search_win, int_win, method="fft")
            max_pos = np.unravel_index(np.argmax(cross_corr), cross_corr.shape)
            dy, dx = max_pos - np.array([win_size, win_size]) + 1
            dys[iy, ix] = dy
            dxs[iy, ix] = dx
    
    return dxs, dys

dxs, dys = convolution(img1, img2, win_size)

u = dxs/delta_t/pix_density
v = dys/delta_t/pix_density

velocity_magnitude = np.sqrt(u**2 + v**2) 

velocity_original = np.copy(velocity_magnitude)

for i in range(1):
    velocity_magnitude_filtered = median_filter(velocity_magnitude, size=3)
    velocity_magnitude = velocity_magnitude_filtered


levels = [ -.5, 0.0, 0.4, 0.7, 1, 2, 4, 6, 8, 10, 11, 12, 14, 16,18,20]


fig, ax = plt.subplots(1, 2, figsize=(10, 5))

# Plot total velocity magnitude using imshow
im3 = ax[0].contourf(velocity_original, cmap='plasma', levels = levels)
ax[0].set_title('Total Velocity Magnitude')
ax[0].axis('off')
fig.colorbar(im3, ax=ax[0])

# Plot total velocity magnitude using contourf
cf3 = ax[1].contourf(velocity_magnitude_filtered, cmap='plasma', levels = levels)
ax[1].set_title('Total Velocity Magnitude filtered')
ax[1].axis('off')
fig.colorbar(cf3, ax=ax[1])

plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
