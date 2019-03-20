DIR_DIVIDER = '\\' # windows: '\\'; linux: '/'
SLICE_DIMENSION = 256
TRAIN_IMAGE_PATH = '..' + DIR_DIVIDER + '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'train' + DIR_DIVIDER + 'image'
TRAIN_LABEL_PATH = '..' + DIR_DIVIDER + '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'train' + DIR_DIVIDER + 'label'
TEST_IMAGE_PATH = '..' + DIR_DIVIDER + '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'test'
TEST_LABEL_PATH = '..' + DIR_DIVIDER + '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'test_label'
ACCEPTED_TYPE = 'jpg'
NPY_PATH = '..' + DIR_DIVIDER + 'unet' + DIR_DIVIDER + 'npydata'
# pylint: disable = E0602, W0612
import os
import numpy as np
os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

def npyMaker(inputFolderPath, outputName):
    fileNames = os.listdir(inputFolderPath)
    validCount = 0
    for fileName in fileNames:
        if fileName.split('.')[-1] == ACCEPTED_TYPE:
            validCount += 1
    print('found ' + str(validCount) + ' valid files')
    sliceStack = np.empty([validCount, SLICE_DIMENSION, SLICE_DIMENSION, 1])
    for i in range(0, validCount):
        filePath = inputFolderPath + DIR_DIVIDER + str(i) + '.' + ACCEPTED_TYPE
        sliceStack[i, :, :, :] = img_to_array(load_img(filePath, grayscale=True))
    np.save(NPY_PATH + DIR_DIVIDER + outputName, sliceStack)
    print('saved ' + NPY_PATH + DIR_DIVIDER + outputName)
  
def config_data():
    npyMaker(TRAIN_IMAGE_PATH, 'imgs_train.npy')
    npyMaker(TRAIN_LABEL_PATH, 'imgs_mask_train.npy')
    npyMaker(TEST_IMAGE_PATH, 'imgs_test.npy')
    npyMaker(TEST_LABEL_PATH, 'imgs_test_truth_label.npy')

