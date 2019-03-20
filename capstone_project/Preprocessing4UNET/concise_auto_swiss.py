# pylint: disable = E0602, W0612, E0401
# More info: https://www.slicer.org/wiki/Documentation/Nightly/Developers/Python_scripting#Python_Interactor
# Sample Codes: https://www.slicer.org/wiki/Documentation/Nightly/ScriptRepository#Export_labelmap_node_from_segmentation_node
# SwissSkullStripper XML: https://github.com/lorensen/SwissSkullStripperExtension/blob/master/SwissSkullStripper/SwissSkullStripper.xml
INPUT_FOLDER_PATH = 'C:\\Users\\hyifa\\Desktop\\training sets-20180406T023141Z-001\\training sets'
ATLAS_FOLDER_PATH = 'C:\\Users\\hyifa\\Desktop\\atlas'
GIT_REPO_PATH = 'C:\\Users\\hyifa\\Desktop\\capstone_project'
DIR_DIVIDER = '\\'
ACCEPTED_SLICE_DIMENSION = 256
RAW_VOLUME_PATH = GIT_REPO_PATH + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'raw'
MASK_VOLUME_PATH = GIT_REPO_PATH + DIR_DIVIDER + 'Preprocessing4UNET' + DIR_DIVIDER + 'data' + DIR_DIVIDER + 'mask'
ACCEPTED_FILE_TYPES = ['nii']

import numpy as np
import time
import slicer
import os

def swissSkullStripper(volumeNode):
    atlasImageNode = dataReader(ATLAS_FOLDER_PATH + DIR_DIVIDER + 'atlasImage.mha')
    atlasMaskNode = dataReader(ATLAS_FOLDER_PATH + DIR_DIVIDER + 'atlasMask.mha')
    parameters = {}
    parameters["patientVolume"] = volumeNode.GetID()
    outVolume = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(outVolume)
    parameters["patientOutputVolume"] = outVolume.GetID()
    labelVolume = slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(labelVolume)
    parameters["patientMaskLabel"] = labelVolume.GetID()
    parameters["atlasMRIVolume"] = atlasImageNode.GetID()
    parameters["atlasMaskVolume"] = atlasMaskNode.GetID()
    return (slicer.cli.runSync(slicer.modules.swissskullstripper, None, parameters))

def dataReader(filePath):
  [success, loadedVolumeNode] = slicer.util.loadVolume(filePath, returnNode=True)
  return loadedVolumeNode

def matrixMaker(fileName):
  rawVolumeMatrix = array(fileName)
  labelMaskMatrix = array('LabelMapVolume')
  # Save dimensions in the file name
  np.save(RAW_VOLUME_PATH + DIR_DIVIDER + fileName + '.npy', rawVolumeMatrix)
  np.save(MASK_VOLUME_PATH + DIR_DIVIDER + fileName + '.npy', labelMaskMatrix)
  print('\nprocessed ' + fileName + str(rawVolumeMatrix.shape))

def typeChecker(fileNames):
  typeName = fileName.split('.')[-1]
  if typeName in ACCEPTED_FILE_TYPES:
    #print(typeName + ' is accepted.')
    return True
  else:
    #print(typeName + ' is NOT accepted.')
    return False

def dimensionChecker(fileName):
  rawVolumeMatrix = array(fileName.split('.')[0])
  return rawVolumeMatrix.shape[1] == ACCEPTED_SLICE_DIMENSION

if __name__ == '__main__':
  fileNames = os.listdir(INPUT_FOLDER_PATH)
  for fileName in fileNames:
    if typeChecker(fileName):
      rawVolumeNode = dataReader(INPUT_FOLDER_PATH + DIR_DIVIDER + fileName)
      if dimensionChecker(fileName):
        start = time.time()
        cliNode = swissSkullStripper(rawVolumeNode)
        print('time elapsed for %s is %s'%(fileName, str(time.time() - start)))
        matrixMaker(fileName.split('.')[0])
      # Clear the scene anyway
      slicer.mrmlScene.Clear(0)
      
  print('All accepted files under ' + INPUT_FOLDER_PATH + ' have been processed.')
  #exit()