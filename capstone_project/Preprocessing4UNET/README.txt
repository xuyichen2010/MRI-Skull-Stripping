Guide:
run clear_all.py
    This code deleted all old files.
	
run concise_auto_swiss.py: 
Slicer --show-python-interactor --no-main-window --python-script concise_auto_swiss.py
    This code will generate necessary intermediate files under the folder 'data' for train_test_maker.py

OR	run Oxford_data_adapter.py:
	Slicer --show-python-interactor --no-main-window --python-script Oxford_data_adapter.py
    		This code will generate necessary intermediate files under the folder 'data' for train_test_maker.py

run train_test_maker.py
python train_test_maker.py // python 3.6
    This code will generate resultant files under the folder 'data4UNET'. 

OR 	run reduced_train_test_maker.py
	python reduced_train_test_maker.py
		The training set generated by this code will not include images without any brain region.

