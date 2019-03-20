import cv2
import glob
import numpy as np
from PIL import Image
import tifffile

import glob, os


os.chdir("/Users/yichenxu/Desktop/280source")
OUT_NAME = "test.tiff"
files = glob.glob("*.png")
# iterate over the list getting each file
arrays = []
for fle in files:
   im = cv2.imread(fle, cv2.IMREAD_GRAYSCALE)
   print(im.shape)
   arrays.append(im)
with tifffile.TiffWriter(OUT_NAME) as tiff:
    for img in arrays:
        tiff.save(img,  compress=6)
