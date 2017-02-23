##################################################################################################
<<<<<<< HEAD
Script created for Python 3.5, untested in older or newer forms
=======
Script created primarily for Python 3.5, untested in older or newer forms
>>>>>>> 0b96e6cb1eb5303f7092d35ea67ec35179849e56
of python. Uses os, sys, shutil, and cv2

To use:
1) Run the script on command line using the same directory the script is located in.

ex: <directory>python class_images.py

2) Make sure to type the directory of the input folder's location first
and output directory after calling class_images.py. 

<<<<<<< HEAD
ex: python class_images.py C:\\input\\directory\\folder_w_image_folders C:\\output\\directory

3) Afterwards, type out 1-9 folder names you'd like to classify the pictures for. (You don't have to do all 9.)

ex: python class_images.py <inputdirec> <outputdirec> <folder_1> <folder_2> ... <folder_9>

4) When running, just simply press a number from 1-9 corresponding to the file name locations <folder_1> = 1 
<folder_2> = 2, etc. whenever a picture pops up. You don't have to press a number on the command, just on the image window.
This moves the image to the specified folder.

NEW FEATURES: UNDO AND DELETE. 
Press 'u' on the keyboard and it will go back to the previuos picture for you to re-classify.
Press 'd' on the keyboard and it'll move the image to a trash folder that gets deleted once script is fully completed.

5) To stop, simply press any letter on the keyboard that isn't 'u' or 'd'. 
=======
ex: python class_images.py C:\\input\\directory\\folder-with-folders-containing-
-images C:\\output\\directory

3) Afterwards, type out 1-9 folder names you'd like to classify the pictures for.

ex: python class_images.py <inputdirec> <outputdirec> <fish1> <fish2> ... <fish9>

4) When running, just simply press a number from 1-9 corresponding to the file name locations as above
whenever a picture pops up. You don't have to press a number on the command, just on the image window.
It'll automatically prioritize the image windows so no back/forth action needed.

5) It'll stop iterating when there are no more folders or files, it might even throw an error. (at this point no matter)
If you wish to stop at any point, you'll have to bruteforce with CTRL C on cmd line and then close the image.
>>>>>>> 0b96e6cb1eb5303f7092d35ea67ec35179849e56

Note: The script was created only to account for numbers 1-9 when pressed on the keyboard.
It is possible to automate the script to have ALL keys in the keyboard be used for 
classification and additional folders, but it is not recommended. Best to kept short.

<<<<<<< HEAD
Ultimately looks like: python class_images.py <idirec> <odirec> <imgfolder1> <imgfolder2>

Ex I use: python class_images.py C:\Users\Jerry\FolderwithFoldersContainingImages C:\Users\Jerry\VLab dolphins sharks tahoes
=======
NOTE: SCRIPT WILL FOREVER LOOP IF OUTPUT IS EQUAL TO INPUT DIRECTORY

Ultimately looks like: python class_images.py <idirec> <odirec> <imgfolder1> <imgfolder2>

Ex I use: python class_images.py C:\Users\Jerry\Hello C:\Users\Jerry\VLab dolphins sharks tahoes
>>>>>>> 0b96e6cb1eb5303f7092d35ea67ec35179849e56

