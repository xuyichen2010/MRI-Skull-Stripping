# pylint: disable = E0602, W0612, E0401
# More info: https://www.slicer.org/wiki/Documentation/Nightly/Developers/Python_scripting#Python_Interactor
# Sample Codes: https://www.slicer.org/wiki/Documentation/Nightly/ScriptRepository#Export_labelmap_node_from_segmentation_node
INPUT_FOLDER_PATH = 'C:\\Users\\hyifa\\Desktop\\Oxford'
ATLAS_FOLDER_PATH = 'C:\\Users\\hyifa\\Desktop\\atlas'
GIT_REPO_PATH = 'C:\\Users\\hyifa\\Desktop\\capstone_project'
DIR_DIVIDER = '\\'
PATH_SUFFIX = 'anat'
ACCEPTED_SLICE_DIMENSION = 192
RAW_VOLUME_PATH = GIT_REPO_PATH + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'raw'
MASK_VOLUME_PATH = GIT_REPO_PATH + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'mask'

import numpy as np
import time
import slicer
import os

def dataReader(filePath):
  [success, loadedVolumeNode] = slicer.util.loadVolume(filePath, returnNode=True)
  return loadedVolumeNode

def matrixMaker(rawVolumeNode, strippedVolumeNode):
  TIME_STAMP = time.strftime("%Y%m%d-%H%M%S")
  rawVolumeMatrix = array(rawVolumeNode.GetID())
  strippedVolumeMatrix = array(strippedVolumeNode.GetID())
  maskVolumeMatrix = strippedVolumeMatrix > 0
  maskVolumeMatrix = maskVolumeMatrix.astype(int)
  # Save dimensions in the file name
  np.save(RAW_VOLUME_PATH + DIR_DIVIDER + TIME_STAMP + '.npy', rawVolumeMatrix)
  np.save(MASK_VOLUME_PATH + DIR_DIVIDER + TIME_STAMP + '.npy', maskVolumeMatrix)
  print('\nprocessed ' + middlePath + str(rawVolumeMatrix.shape))

def dimensionChecker():
  rawVolumeMatrix = array('mprage_anonymized')
  return rawVolumeMatrix.shape[1] == ACCEPTED_SLICE_DIMENSION

if __name__ == '__main__':
  middlePaths = os.listdir(INPUT_FOLDER_PATH)
  for middlePath in middlePaths:
    if middlePath[0:3] == 'sub':
      rawVolumeNode = dataReader(INPUT_FOLDER_PATH + DIR_DIVIDER + middlePath + DIR_DIVIDER + PATH_SUFFIX + DIR_DIVIDER + 'mprage_anonymized.nii.gz')
      strippedVolumeNode = dataReader(INPUT_FOLDER_PATH + DIR_DIVIDER + middlePath + DIR_DIVIDER + PATH_SUFFIX + DIR_DIVIDER + 'mprage_skullstripped.nii.gz')
      matrixMaker(rawVolumeNode, strippedVolumeNode)
      # Clear the scene anyway
      slicer.mrmlScene.Clear(0)
      
  print('All accepted files under ' + INPUT_FOLDER_PATH + ' have been processed.')
  #exit()