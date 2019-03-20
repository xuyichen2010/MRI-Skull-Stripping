DIR_DIVIDER = '\\'
TRAIN_VOLUME_NUM = 5 # make sure there are at least TRAIN_VOLUME_NUM + 1 volume data pairs in the 'data' folder
RAW_VOLUME_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'raw'
MASK_VOLUME_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'mask'
TRAIN_IMAGE_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'train' + DIR_DIVIDER + 'image'
TRAIN_LABEL_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'train' + DIR_DIVIDER + 'label'
TEST_IMAGE_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'test'
TEST_LABEL_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'test_label'

from libtiff import TIFF3D,TIFF
import ctypes
imageCounter = 0
labelCounter = 0

def splitAndSave(image, path, counter):
    for piece in image.iter_images():
        namePath = path + DIR_DIVIDER + str(counter) + '.tif'
        sliceImage = TIFF.open(namePath, 'w')
        sliceImage.write_image(piece)
        counter += 1
    '''
    imageArray = image.read_image()
    for i in range(imageArray.shape[0]):
        namePath = path + DIR_DIVIDER + str(counter) + '.tif'
        sliceImage = TIFF.open(namePath, 'w')
        sliceImage.write_image(imageArray[i])
        counter += 1
    '''
    return counter

if __name__ == '__main__':
  import os
  fileNames = os.listdir(RAW_VOLUME_PATH)
  processed = 0
  for fileName in fileNames:
    if fileName.split('.')[-1] != 'tif':
        continue
    elif processed < TRAIN_VOLUME_NUM:
        trainRawVolumePath = RAW_VOLUME_PATH + DIR_DIVIDER + fileName
        print('processing ' + trainRawVolumePath)
        trainRawVolume = TIFF.open(trainRawVolumePath)
        imageCounter = splitAndSave(trainRawVolume, TRAIN_IMAGE_PATH, imageCounter)

        trainMaskVolumePath = MASK_VOLUME_PATH + DIR_DIVIDER + fileName
        print('processing ' + trainMaskVolumePath)
        trainMaskVolume = TIFF.open(trainMaskVolumePath)
        labelCounter = splitAndSave(trainMaskVolume, TRAIN_LABEL_PATH, labelCounter)
        processed += 1
    # the volume data after the last training volume data will be considered as the testing volume data
    elif processed == TRAIN_VOLUME_NUM: 
        print('processing testing data')
        testRawVolume = TIFF.open(RAW_VOLUME_PATH + DIR_DIVIDER + fileName)
        splitAndSave(trainRawVolume, TEST_IMAGE_PATH, 0)
        testMaskVolume = TIFF.open(MASK_VOLUME_PATH + DIR_DIVIDER + fileName)
        splitAndSave(trainMaskVolume, TEST_LABEL_PATH, 0)

  print('All files under ' + RAW_VOLUME_PATH + ' and ' + MASK_VOLUME_PATH + ' have been processed.')
  #exit()