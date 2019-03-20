FOLDER_PATH = ''
TEST_y_CSV_FILE_PATH = ''
TEST_X_CSV_FILE_PATH = ''
TEST_SLICE_NUM = 60
DIR_DIVIDER = ''

import pandas as pd
import numpy as np
import os
from sklearn.neural_network import MLPClassifier

def matrixReshaper(matrix):
    (N, D) = matrix.shape
    return np.reshape(matrix, (N*D, 1))

def MLPWrapper(raws, labels, testX):
    mlp = MLPClassifier()
    mlp.fit(raws.reshape(-1, 1), labels.reshape(-1, 1))
    return np.asarray(mlp.predict(testX.reshape(-1, 1)))

if __name__ == '__main__':
    fileNames = os.listdir(FOLDER_PATH)
    raws = np.empty(0)
    labels = np.empty(0)
    # Read in all raw volume matrices and label map matrices, then covert them into one column repectively
    for fileName in fileNames:
        fileType = fileName.split('-')[0]
        print('processing:' + fileName + ':' + fileType)
        filePath = FOLDER_PATH + DIR_DIVIDER + fileName
        csvMatrix = np.asarray(pd.read_csv(filePath, header=None))
        if fileType == 'label':
            labels = np.append(labels, matrixReshaper(csvMatrix))
        elif fileType == 'raw':
            raws = np.append(raws, matrixReshaper(csvMatrix))
    # Convert into numpy arrays
    labels = np.asarray(labels) # trainy
    raws = np.asarray(raws) # trainX
    # Read in testX and testy
    testXCsvMatrix = np.asarray(pd.read_csv(TEST_X_CSV_FILE_PATH, header=None))[TEST_SLICE_NUM, :]
    testyCsvMatrix = np.asarray(pd.read_csv(TEST_y_CSV_FILE_PATH, header=None))[TEST_SLICE_NUM, :]
    resMatrix = MLPWrapper(raws, labels, testXCsvMatrix)
    accuracy = np.dot(resMatrix, testyCsvMatrix)/sum(testyCsvMatrix)
    print('accuracy = ' +  str(accuracy))
