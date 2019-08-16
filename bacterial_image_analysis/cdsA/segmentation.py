import numpy as np
#import cv2
import os
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import skimage.filters as filt

from skimage import io
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops, find_contours
from skimage.morphology import closing, square
from skimage.color import label2rgb


dapi_file_name = 'img_channel000_position000_time000000000_z000.tif'
root_file_path = os.path.join(os.getcwd(),'data_sets/bacterial_image_analysis/2019/071919')
file_path = os.path.join(root_file_path, 'Pos0')
dapi_file_path = os.path.join(file_path, dapi_file_name)

output_path = os.path.join(root_file_path, 'outputs')

if not os.path.exists(output_path):
	os.makedirs(output_path)

image =  io.imread(dapi_file_path)
import pdb; pdb.set_trace()

#apply threshold
thresh = filt.threshold_otsu(image)
bw = closing(image > thresh, square(2))
bw_erode = 

#remove artifacts connected to image border

cleared = clear_border(bw)

#label image regions
label_image = label(cleared)
image_label_overlay = label2rgb(label_image, image=image)



#io.imsave(os.path.join(output_path, 'label_image_pos0.png'), label_image)
#io.imsave(os.path.join(output_path, 'image_label_overlay_pos0.png'), image_label_overlay)

props = regionprops(label_image)


#Trying out image countours instead of labels:
'''
contours = find_contours(label_image, 0.2)

fig, ax = plt.subplots(figsize = (12.80,10.80))
ax.imshow(image, cmap=plt.cm.gray)


for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=0.5)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
#plt.show()

fig.savefig(os.path.join(output_path, 'image_contours_pos0.tif'))


'''

