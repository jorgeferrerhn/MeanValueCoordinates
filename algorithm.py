import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


#Source
source = cv.imread('img/polar_bear.png')
canny = cv.Canny(source,100,200)

#Target
#target = cv.imread('img/black_beach.jpg')

#Draw the contours



px = source.shape


print(px)

plt.subplot(121),plt.imshow(source,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(canny,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()