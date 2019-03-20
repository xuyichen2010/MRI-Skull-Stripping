from data_configurator import config_data
from unet import *
from compute_accuracy import *
from clear_all import clearAll
from postprocess import makeImageMaskVolume

if __name__ == '__main__':
    clearAll()
    config_data()
    myunet = myUnet()
    myunet.train()
    myunet.save_img()
    getAccuracy()
    makeImageMaskVolume()