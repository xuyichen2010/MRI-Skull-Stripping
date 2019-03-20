DIR_DIVIDER = '\\' # windows: '' + DIR_DIVIDER + '' + DIR_DIVIDER + ''; linux: '/'
PREDICT_PATH = '..' + DIR_DIVIDER + 'unet' + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'predict'
TRUTH_PATH = '..' + DIR_DIVIDER + 'unet' + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'truth'

import numpy as np
import os
os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras.preprocessing.image import array_to_img, img_to_array, load_img

def getAccuracy():
    predictNames = os.listdir(PREDICT_PATH)
    count = 0
    accuracy = 0.0
    for name in predictNames:
        if name.split('.')[-1] != 'jpg':
            continue
        else:
            pMatrix = img_to_array(load_img(PREDICT_PATH + DIR_DIVIDER + name, grayscale=True))
            tMatrix = img_to_array(load_img(TRUTH_PATH + DIR_DIVIDER + name, grayscale=True))
            pMatrix.shape = (pMatrix.shape[0], pMatrix.shape[1])
            tMatrix.shape = (tMatrix.shape[0], tMatrix.shape[1])
            correct1 = np.sum(pMatrix/255 * tMatrix/255)
            correct0 = np.sum((1-(pMatrix/255) * 1-(tMatrix/255)))
            accuracy += (correct1 + correct0)/(pMatrix.shape[0] * pMatrix.shape[1])
            count += 1

    print('average accuracy of testing data: ' + str(accuracy/count))
    return accuracy/count

