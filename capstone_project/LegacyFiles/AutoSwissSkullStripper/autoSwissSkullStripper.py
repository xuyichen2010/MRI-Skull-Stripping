# pylint: disable = E0602, W0612, E0401
# More info: https://www.slicer.org/wiki/Documentation/Nightly/Developers/Python_scripting#Python_Interactor
# Sample Codes: https://www.slicer.org/wiki/Documentation/Nightly/ScriptRepository#Export_labelmap_node_from_segmentation_node
# SwissSkullStripper XML: https://github.com/lorensen/SwissSkullStripperExtension/blob/master/SwissSkullStripper/SwissSkullStripper.xml
USE_SAMPLE_DATA = 0
SAVE_RESULT_SCENE = 1
FOLDER_PATH = ''
DIR_DIVIDER = ''
ACCEPTED_FILE_TYPES = ['nii']

import numpy as np
import time
TIME_STAMP = time.strftime("%Y%m%d-%H%M%S")

def swissSkullStripper(volumeNode):
    parameters = {}
    parameters["patientVolume"] = volumeNode.GetID()
    outVolume = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(outVolume)
    parameters["patientOutputVolume"] = outVolume.GetID()
    labelVolume = slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(labelVolume)
    parameters["patientMaskLabel"] = labelVolume.GetID()
    return (slicer.cli.runSync(slicer.modules.swissskullstripper, None, parameters))

def dataReader(filePath):
  # Test with a sample data
  if USE_SAMPLE_DATA == 1:
    # Import SampleData
    import SampleData
    sampleDataLogic = SampleData.SampleDataLogic()
    sampleDataLogic.downloadMRBrainTumor1()
    loadedVolumeNode = getNode('MRBrainTumor1')
  else:
    [success, loadedVolumeNode] = slicer.util.loadVolume(filePath, returnNode=True)
  return loadedVolumeNode

def mrbDataSaver(fileName):
  # Save the file
  # Generate file name
  if SAVE_RESULT_SCENE == 1:
    sceneSaveFilename = "saved-scene-swiss-" + TIME_STAMP + ".mrb"
    # Save scene
    if slicer.util.saveScene(sceneSaveFilename):
      logging.info("Scene saved")
    else:
      logging.error("Scene saving failed") 

def typeChecker(fileNames):
  typeName = fileName.split('.')[-1]
  if typeName in ACCEPTED_FILE_TYPES:
    print(typeName + ' is accepted.')
    return True
  else:
    print(typeName + ' is NOT accepted.')
    return False

def matrixMaker(fileName):
  rawVolumeMatrix = array(fileName)
  newRawVolumeMatrix = matrixReshaper(rawVolumeMatrix)
  labelMaskMatrix = array('LabelMapVolume')
  newLabelMaskMatrix = matrixReshaper(labelMaskMatrix)
  # Save dimensions in the file name
  np.savetxt('raw-matrix-' + str(rawVolumeMatrix.shape[0]) + 'x' + str(rawVolumeMatrix.shape[1]) + 'x' + str(rawVolumeMatrix.shape[2]) + '-' + TIME_STAMP + '.csv', newRawVolumeMatrix, delimiter = ',')
  np.savetxt('label-matrix-' + str(labelMaskMatrix.shape[0]) + 'x' + str(labelMaskMatrix.shape[1]) + 'x' + str(labelMaskMatrix.shape[2]) + '-' + TIME_STAMP + '.csv', newLabelMaskMatrix, delimiter = ',')

def matrixReshaper(matrix):
  rowLength = matrix.shape[1] * matrix.shape[2]
  resMatrix = np.empty([matrix.shape[0], rowLength])
  for i in range(0, matrix.shape[0]):
    resMatrix[i, :] = np.reshape(matrix[i, :, :], rowLength)
  return resMatrix

if __name__ == '__main__':
  import os
  fileNames = os.listdir(FOLDER_PATH)
  for fileName in fileNames:
    if typeChecker(fileName):
      filePath = FOLDER_PATH + DIR_DIVIDER + fileName
      cliNode = swissSkullStripper(dataReader(filePath))
      mrbDataSaver(fileName.split('.')[0])
      matrixMaker(fileName.split('.')[0])
      # Clear the scene anyway
      slicer.mrmlScene.Clear(0)
      
  print('All files under ' + FOLDER_PATH + ' have been processed.')
  exit()