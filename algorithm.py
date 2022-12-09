import cv2 as cv
import numpy as np


#Source
img = cv.imread('img/test1.jpg')

#Target
px = img.shape

print(px)

cv.imshow("Image",img)
cv.waitKey(0)