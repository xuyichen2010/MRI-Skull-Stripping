DIR_DIVIDER = '\\' # windows: '\\'; linux: '/'
DELETE_TYPES = ['tif', 'npy', 'jpg', 'hdf5', 'png']
MASTER_PATH = '..' + DIR_DIVIDER + 'unet'
NPY_PATH = MASTER_PATH + DIR_DIVIDER + 'npydata'
PREDICT_PATH = MASTER_PATH + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'predict'
PREDICT_COMBINE_PATH = MASTER_PATH + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'predict_combine'
TRUTH_COMBINE_PATH = MASTER_PATH + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'truth_combine'
TRUTH_PATH = MASTER_PATH + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'truth'
import os
def clearAll():
    targets = [NPY_PATH, PREDICT_PATH, PREDICT_COMBINE_PATH, TRUTH_PATH, TRUTH_COMBINE_PATH]
    for target in targets:
        print('deleting old files under: '+target)
        fileNames = os.listdir(target)
        for fileName in fileNames:
            if fileName.split('.')[-1] in DELETE_TYPES:
                os.remove(target + DIR_DIVIDER + fileName)

if __name__ == '__main__':
    clearAll()