DIR_DIVIDER = '\\'
TRAIN_VOLUME_NUM = -1 # -1: use the last head volume as the testing data
RAW_VOLUME_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'raw'
MASK_VOLUME_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'mask'
TRAIN_IMAGE_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'train' + DIR_DIVIDER + 'image'
TRAIN_LABEL_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'train' + DIR_DIVIDER + 'label'
TEST_IMAGE_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'test'
TEST_LABEL_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'test_label'

import ctypes
import pandas as pd
import math
import numpy as np
from PIL import Image
from scipy.misc import toimage
import os
from clear_all import clear

imageCounter = 0
labelCounter = 0
ignores = []

def findSliceNumPosition(npyMatrix):
    [x, y, z] = npyMatrix.shape
    if x == y:
        return 2
    elif y == z:
        return 0

def npySplitAndSave(npyMatrix, path, counter, isLabel=False, isTest=False):
    if findSliceNumPosition(npyMatrix) == 0:
        return npySplitAndSave0(npyMatrix, path, counter, isLabel, isTest)
    elif findSliceNumPosition(npyMatrix) == 2:
        return npySplitAndSave2(npyMatrix, path, counter, isLabel, isTest)

def npySplitAndSave0(npyMatrix, path, counter, isLabel=False, isTest=False):
    for i in range(0, npyMatrix.shape[0]):
        #sliceMatrix = np.reshape(npyMatrix[i, :], (imageD, imageD))
        namePath = path + DIR_DIVIDER + str(counter) + '.jpg'
        if isLabel:
            # ignore slices without any tumor
            if isTest == False and np.sum(npyMatrix[i]) == 0:
                ignores.append(i)
                continue
            npyMatrix[i] = npyMatrix[i]*255
        else:
            if isTest == False and i in ignores:
                ignores.remove(i)
                continue
        img = toimage(npyMatrix[i])
        img.save(namePath)
        counter += 1
    return counter

def npySplitAndSave2(npyMatrix, path, counter, isLabel=False, isTest=False):
    for i in range(0, npyMatrix.shape[2]):
        #sliceMatrix = np.reshape(npyMatrix[i, :], (imageD, imageD))
        namePath = path + DIR_DIVIDER + str(counter) + '.jpg'
        if isLabel:
            # ignore slices without any tumor
            if isTest == False and np.sum(npyMatrix[i]) == 0:
                ignores.append(i)
                continue
            npyMatrix[:, :, i] = npyMatrix[:, :, i]*255
        else:
            if isTest == False and i in ignores:
                ignores.remove(i)
                continue
        img = toimage(npyMatrix[:, :, i])
        img.save(namePath)
        counter += 1
    return counter

if __name__ == '__main__':
    clear()
    fileNames = os.listdir(RAW_VOLUME_PATH)
    processed = 0
    validCount = 0
    for fileName in fileNames:
        if fileName.split('.')[-1] == 'npy':
            validCount += 1
    
    print('found: ' + str(validCount))
    
    if TRAIN_VOLUME_NUM < 0 or TRAIN_VOLUME_NUM >= validCount:
        TRAIN_VOLUME_NUM = validCount - 1

    print('num of train volume will be: ' + str(TRAIN_VOLUME_NUM))
    for fileName in fileNames:
        if fileName.split('.')[-1] != 'npy':
            continue
        elif processed < TRAIN_VOLUME_NUM:
            trainMaskVolumePath = MASK_VOLUME_PATH + DIR_DIVIDER + fileName
            print('processing ' + trainMaskVolumePath)
            trainMaskNpy = np.load(trainMaskVolumePath)
            labelCounter = npySplitAndSave(trainMaskNpy, TRAIN_LABEL_PATH, labelCounter, isLabel=True)

            trainRawVolumePath = RAW_VOLUME_PATH + DIR_DIVIDER + fileName
            print('processing ' + trainRawVolumePath)
            trainRawNpy = np.load(trainRawVolumePath)
            imageCounter = npySplitAndSave(trainRawNpy, TRAIN_IMAGE_PATH, imageCounter)
            processed += 1
        # the volume data after the last training volume data will be considered as the testing volume data
        elif processed == TRAIN_VOLUME_NUM: 
            print('processing testing data')
            testMaskNpy = np.load(MASK_VOLUME_PATH + DIR_DIVIDER + fileName)
            npySplitAndSave(testMaskNpy, TEST_LABEL_PATH, 0, isLabel=True, isTest=True)
            testRawNpy = np.load(RAW_VOLUME_PATH + DIR_DIVIDER + fileName)
            npySplitAndSave(testRawNpy, TEST_IMAGE_PATH, 0, isTest=True)
            break

    print('All files under ' + RAW_VOLUME_PATH + ' and ' + MASK_VOLUME_PATH + ' have been processed.')