DIR_DIVIDER = '\\' # windows: '\\'; linux: '/'
SLICE_DIMENSION = 256
DELETE_TYPES = ['tif', 'csv', 'npy', 'jpg']
RAW_VOLUME_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'raw'
MASK_VOLUME_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'mask'
TRAIN_IMAGE_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'train' + DIR_DIVIDER + 'image'
TRAIN_LABEL_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'train' + DIR_DIVIDER + 'label'
TEST_IMAGE_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'test'
TEST_LABEL_PATH = '..' + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data4UNET' + DIR_DIVIDER + 'test_label'
import os
def clearAll():
    targets = [RAW_VOLUME_PATH, MASK_VOLUME_PATH, TRAIN_IMAGE_PATH, TRAIN_LABEL_PATH, TEST_IMAGE_PATH, TEST_LABEL_PATH]
    for target in targets:
        print('deleting old files under: '+target)
        fileNames = os.listdir(target)
        for fileName in fileNames:
            if fileName.split('.')[-1] in DELETE_TYPES:
                os.remove(target + DIR_DIVIDER + fileName)
def clear():
    targets = [TRAIN_IMAGE_PATH, TRAIN_LABEL_PATH, TEST_IMAGE_PATH, TEST_LABEL_PATH]
    for target in targets:
        print('deleting old files under: '+target)
        fileNames = os.listdir(target)
        for fileName in fileNames:
            if fileName.split('.')[-1] in DELETE_TYPES:
                os.remove(target + DIR_DIVIDER + fileName)

if __name__ == '__main__':
    clearAll()
