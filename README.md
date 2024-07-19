  # Image Manager Desktop App
A GUI application that can view images from a folder and manage them (perform delete, rename, and move). Made with Python3 using tkinter.

My intention with this app is to provide an easy UI to move around the images in a folder and quickly rename/delete/move them.

# Features include:
- Navigate through all images from a folder; can navigate using arrow keys; shows image name and the image position in the folder
- Rename image; adds a number at the end if an image file with similar name already exists in the same folder
- Move image to another specified folder; adds a number at the end if a similar name image file exists in the destination folder
- Delete image; moves image to the recycle bin


 # Running the App

I use poetry for managing my dependencies.

```
pip install poetry
poetry install
```

This app was built on Windows. If you are on MacOS, the easiest way to install Tkinter is through brew: `brew install python-tk`.

Then, you can run the app as follows: 

```
poetry run python main.py
```

# Screenshots

### Initial Screen
![screenshot 1](walkthroughs/ImageManager_sc1.png?raw=true)

### General Screen 
![screenshot 2](walkthroughs/ImageManager_sc2.png?raw=true)
