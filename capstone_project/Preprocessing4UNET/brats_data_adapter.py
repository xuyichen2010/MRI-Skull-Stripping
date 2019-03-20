# pylint: disable = E0602, W0612, E0401
# More info: https://www.slicer.org/wiki/Documentation/Nightly/Developers/Python_scripting#Python_Interactor
# Sample Codes: https://www.slicer.org/wiki/Documentation/Nightly/ScriptRepository#Export_labelmap_node_from_segmentation_node
INPUT_FOLDER_PATH = 'C:\\Users\\hyifa\\Desktop\\BRATS2015_Training\\HGG'
GIT_REPO_PATH = 'C:\\Users\\hyifa\\Desktop\\capstone_project'
DIR_DIVIDER = '\\'
ACCEPTED_SLICE_DIMENSION = 240
RAW_VOLUME_PATH = GIT_REPO_PATH + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'raw'
MASK_VOLUME_PATH = GIT_REPO_PATH + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'mask'
import numpy as np
import time
import slicer
import os

def dataReader(filePath):
    [success, loadedVolumeNode] = slicer.util.loadVolume(filePath, returnNode=True)
    return loadedVolumeNode

def matrixMaker(rawVolumeNode, maskVolumeNode, levelOneFolderName):
    if dimensionChecker(maskVolumeNode):
        rawVolumeMatrix = array(rawVolumeNode.GetID())
        maskVolumeMatrix = array(maskVolumeNode.GetID())
        maskVolumeMatrix = (maskVolumeMatrix > 0).astype(int)
        # Save dimensions in the file name
        np.save(RAW_VOLUME_PATH + DIR_DIVIDER + levelOneFolderName + '.npy', rawVolumeMatrix)
        np.save(MASK_VOLUME_PATH + DIR_DIVIDER + levelOneFolderName + '.npy', maskVolumeMatrix)
        print('\nprocessed %s: %s'%(levelOneFolderName, str(rawVolumeMatrix.shape)))

def dimensionChecker(volumeNode):
    volumeMatrix = array(volumeNode.GetID())
    return volumeMatrix.shape[1] == ACCEPTED_SLICE_DIMENSION

if __name__ == '__main__':
    levelOneFolderNames = os.listdir(INPUT_FOLDER_PATH)
    for levelOneFolderName in levelOneFolderNames:
        rawVolumeNode = None
        maskVolumeNode = None
        levelTwoFolderNames = os.listdir(INPUT_FOLDER_PATH + DIR_DIVIDER + levelOneFolderName)
        for levelTwoFolderName in levelTwoFolderNames:
            if levelTwoFolderName.split('_')[-1][0] == 'F':
                fileNames = os.listdir(INPUT_FOLDER_PATH + DIR_DIVIDER + levelOneFolderName + DIR_DIVIDER + levelTwoFolderName)
                for fileName in fileNames:
                    if fileName.split('.')[-1] == 'mha':
                        rawVolumeNode = dataReader(INPUT_FOLDER_PATH + DIR_DIVIDER + levelOneFolderName + DIR_DIVIDER + levelTwoFolderName + DIR_DIVIDER + fileName)
            elif levelTwoFolderName.split('_')[-1][1] == 'm':
                fileNames = os.listdir(INPUT_FOLDER_PATH + DIR_DIVIDER + levelOneFolderName + DIR_DIVIDER + levelTwoFolderName)
                for fileName in fileNames:
                    if fileName.split('.')[-1] == 'mha':
                        maskVolumeNode = dataReader(INPUT_FOLDER_PATH + DIR_DIVIDER + levelOneFolderName + DIR_DIVIDER + levelTwoFolderName + DIR_DIVIDER + fileName)     
        if rawVolumeNode != None and maskVolumeNode != None:
            matrixMaker(rawVolumeNode, maskVolumeNode, levelOneFolderName)
        else:
            print('\n%s is not accepted.'%(INPUT_FOLDER_PATH + DIR_DIVIDER + levelOneFolderName))
        # Clear the scene anyway
        slicer.mrmlScene.Clear(0)
      
    print('All accepted files under ' + INPUT_FOLDER_PATH + ' have been processed.')
    #exit()