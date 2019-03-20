import numpy
from numpy import genfromtxt
from PIL import Image
import numpy as np
import cv2

matrix = genfromtxt('resultTR.csv', delimiter=',')
b = matrix
print(b.shape)
B = np.reshape(b, (-1, 256))
print(B.shape)
cv2.imshow('Indices',B)
cv2.waitKey()
