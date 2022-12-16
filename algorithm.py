import cv2 as cv
import numpy as np

img = cv.imread('img/test1.jpg')

hwc = img.shape


for px in img:
    print(px)

cv.imshow("Image",img)
cv.waitKey(0)