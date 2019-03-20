Run a Python script with Slicer:
Run w/o a Slicer window: Slicer --no-main-window --python-script <Python file>
Run w/ a Slicer window: Slicer --python-script <Python file>
Run w/ a Slicer Python Interactor only: Slicer --show-python-interactor --no-main-window --python-script <Python file>

Sample: Slicer  --show-python-interactor  --no-main-window --python-script autoSwissSkullStripper.py

Now you can run with the command "sh run.sh".
Remember to change "FOLDER_PATH" before you run it.
Delete all generated data by "sh clean.sh".