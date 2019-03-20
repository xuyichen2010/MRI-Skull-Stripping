DIR_DIVIDER = '\\' # windows: '\\'; linux: '/'
from unet import *
from data import *

mydata = dataProcess(512,512)

imgs_test = mydata.load_test_data()

myunet = myUnet()

model = myunet.get_unet()

model.load_weights('unet.hdf5')

imgs_mask_test = model.predict(imgs_test, verbose=1)

np.save(DIR_DIVIDER + 'unet' + DIR_DIVIDER + 'results' + DIR_DIVIDER + 'imgs_mask_test.npy', imgs_mask_test)