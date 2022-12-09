import cv2 as cv
import numpy as np


#Source
source = cv.imread('img/polar_bear.png')
sourcegray = cv.cvtColor(source, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(sourcegray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

#Target
#target = cv.imread('img/black_beach.jpg')

#Draw the contours
cv.drawContours(source, contours, -1, (0,255,0), 3)


px = source.shape


print(px)

cv.imshow("Image",source)
cv.waitKey(0)