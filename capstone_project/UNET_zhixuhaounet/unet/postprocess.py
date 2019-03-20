DIR_DIVIDER = '\\' # windows: '\\'; linux: '/'
MASTER_PATH = '..' + DIR_DIVIDER + 'unet'
PREDICT_PATH = MASTER_PATH + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'predict'
PREDICT_COMBINE_PATH = MASTER_PATH + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'predict_combine'
TRUTH_COMBINE_PATH = MASTER_PATH + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'truth_combine'
TRUTH_PATH = MASTER_PATH + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'truth'
NPY_PATH = '..' + DIR_DIVIDER + 'unet' + DIR_DIVIDER + 'npydata'
TEST_IMAGE_PATH = '..' + DIR_DIVIDER + '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'test'
# pylint: disable = E1101
import numpy as np
import os
os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import cv2
import tifffile
def makeImageMaskVolume():
    print('postprocessing...')
    maskNames = os.listdir(PREDICT_PATH)
    arrays = []
    arrays4truth = []
    validCount = 0
    for maskName in maskNames:
        if maskName.split('.')[-1] == 'jpg':
            validCount += 1
    for i in range(0, validCount):
        predictMaskPath = PREDICT_PATH + DIR_DIVIDER + str(i) + '.jpg'
        testSlicePath = TEST_IMAGE_PATH + DIR_DIVIDER + str(i) + '.jpg'
        truthMaskPath = TRUTH_PATH + DIR_DIVIDER + str(i) + '.jpg'
        mask = cv2.imread(predictMaskPath, 0)
        img = cv2.imread(testSlicePath) # mask name and image name should be the same
        res = cv2.bitwise_and(img, img, mask = mask)
        color_img = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
        color_img = cv2.addWeighted(color_img, 1, img, 1, 0, img)
        cv2.imwrite(PREDICT_COMBINE_PATH + DIR_DIVIDER + str(i) + '_' + str(getAccuracy(predictMaskPath, truthMaskPath)) + '.jpg', color_img)
        arrays.append(color_img)
    
    for i in range(0, validCount):
        testSlicePath = TEST_IMAGE_PATH + DIR_DIVIDER + str(i) + '.jpg'
        truthMaskPath = TRUTH_PATH + DIR_DIVIDER + str(i) + '.jpg'
        truthMask = cv2.imread(truthMaskPath, 0)
        img = cv2.imread(testSlicePath) # mask name and image name should be the same
        truthRes = cv2.bitwise_and(img, img, mask = truthMask)
        truth_color_img = cv2.cvtColor(truthRes, cv2.COLOR_BGR2HSV)
        truth_color_img = cv2.addWeighted(truth_color_img, 1, img, 1, 0, img)
        cv2.imwrite(TRUTH_COMBINE_PATH + DIR_DIVIDER + str(i) + '.jpg', truth_color_img)
        arrays4truth.append(truth_color_img)

    with tifffile.TiffWriter(PREDICT_COMBINE_PATH + DIR_DIVIDER + 'predict_combine.tif') as tiff:
        for img in arrays:
            tiff.save(img,  compress=6)

    with tifffile.TiffWriter(TRUTH_COMBINE_PATH + DIR_DIVIDER + 'truth_combine.tif') as tiff:
        for img in arrays4truth:
            tiff.save(img,  compress=6)

def getAccuracy(predictMaskPath, truthMaskPath):
    pMatrix = img_to_array(load_img(predictMaskPath, grayscale=True))
    tMatrix = img_to_array(load_img(truthMaskPath, grayscale=True))
    pMatrix.shape = (pMatrix.shape[0], pMatrix.shape[1])
    tMatrix.shape = (tMatrix.shape[0], tMatrix.shape[1])
    correct1 = np.sum(pMatrix/255 * tMatrix/255)
    correct0 = np.sum((1-(pMatrix/255) * 1-(tMatrix/255)))
    return (correct1 + correct0)/(pMatrix.shape[0] * pMatrix.shape[1])

if __name__ == '__main__':
    makeImageMaskVolume()
    