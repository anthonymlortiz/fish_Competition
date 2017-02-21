##  Made by Gerardo Uranga ##
##  guranga@miners.utep.edu ##
##  Last Modified: 2/21/2017 ##
##                           ##
##  Small script to place images in correct folders for competition. ##
##  Runs from command line. To change, simply uncomment direc and output to ##
##  suit your needs. ##
import os, sys
#from PIL import Image
import shutil
import cv2

#direc = 'your\\directory\\here'
direc = sys.argv[1]
#output = 'your\\directory\\here'
output = sys.argv[2]
image_folders = os.listdir(direc)
file_names = []
for i in range(0,len(sys.argv)-3):
    file_names.append(sys.argv[i+3])

for folders in image_folders:
    for fil in os.listdir(direc + '\\' + folders):
        InFileName = direc + '\\' + folders + '\\' + fil
        image = cv2.imread(InFileName)
        cv2.imshow("",image)
        x = cv2.waitKey()
        x = int(chr(x))-1
        if not (os.path.exists(output + '\\' +file_names[x])):
            os.makedirs(output+'\\'+file_names[x])
            shutil.move(InFileName, output+ '\\' +file_names[x])
        else:
            shutil.move(InFileName, output+ '\\'+file_names[x])
