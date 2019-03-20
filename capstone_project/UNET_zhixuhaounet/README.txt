Fixed version of unet from https://github.com/zhixuhao/unet
Change DIR_DIVIDER for your system
CUDA 9.0 and cuDNN 7 are supported
Work on Python 3.6+
Install all necessary packages (keras, tensorflow-gpu, ...)

Guide:
Under the 'unet' folder:
Execute test_unet.py
All resultant files will be saved to the 'results' folder

WARNING:
Make sure you use a computer with a CUDA9.0-enabled (as well as cuDNN 7) NVIDIA GPU to save time! 
(NVIDIA 1080 ti: 2~4s/epoch; AMD 1800X CPU (enabled all 16 threads): forever...)

Functionality has been checked on windows and MacOS (not a good idea since CUDA does not support AMD GPU...).