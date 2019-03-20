import cv2
import numpy as np
from PIL import Image
from scipy.misc import toimage


img = cv2.imread('/Users/yichenxu/Desktop/280source/' + '3_raw.jpg')
# redImag = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# cv2.imwrite('/Users/yichenxu/Desktop/280source/test1.png',color_image1)

mask = cv2.imread('/Users/yichenxu/Desktop/280source/' + '3.jpg',0)
res = cv2.bitwise_and(img,img,mask = mask)
cv2.imwrite('/Users/yichenxu/Desktop/280source/testMask.png',res)

color_img = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
color_img = cv2.addWeighted(color_img, 1, img, 1, 0, img)

cv2.imwrite('/Users/yichenxu/Desktop/280source/test.png',color_img)
