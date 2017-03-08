# -*- coding: utf-8 -*-
"""
Created on Saturday, Jan 21 12:17:10 2017
Last modified FMonday, March 7, 2017

@author: Anthony Ortiz, Olac Fuentes
"""
import numpy as np
from PIL import Image
from pylab import *
import time
import glob
import cv2
import keras
import keras.activations
from keras import backend as K

def abs_val_rect(x):
    return K.abs(x)

def scale_stretch_rot(I,sc,st,theta):
#    print(sc,st,theta)
    c,r = I.shape
    r_out = int(r*sc)
    c_out = int(c*sc*st)
    out = cv2.resize(I,(r_out, c_out), interpolation = cv2.INTER_LINEAR)
    M = cv2.getRotationMatrix2D((c/2,r/2),theta,1)
    out = cv2.warpAffine(I,M,(c_out,r_out))
    return out

def scale_stretch_rotColor(I,sc,st,theta):
#    print(sc,st,theta)
    c,r,d = I.shape
    r_out = int(r*sc)
    c_out = int(c*sc*st)
    out = cv2.resize(I,(r_out, c_out), interpolation = cv2.INTER_LINEAR)
    M = cv2.getRotationMatrix2D((c/2,r/2),theta,1)
    out = cv2.warpAffine(I,M,(c_out,r_out))
    return out

def best_match(I, model):
    best_prob = -1
    min_r, min_c = 0, 0
    rows_image,cols_image = I.shape
    rows_pattern = 224
    cols_pattern = 224
    img_rows, img_cols = 50, 50
    img_total_rows = 224
    img_channels = 1
    delta_rows = int((img_total_rows - img_rows) / 2)
    for r in range(0,rows_image - rows_pattern,5): #Sliding size
        for c in range(0,cols_image - cols_pattern,5):
            window = I[r:r+rows_pattern,c:c+cols_pattern]
            windowFishNoFish = window[delta_rows:delta_rows+img_rows, delta_rows:delta_rows+img_rows]
            X = np.array(windowFishNoFish, dtype=float);
            X = X.reshape(1, img_rows, img_cols,1)
            #Scaling input
            X /= 255
            result = model.predict_proba(batch_size=1, x=X, verbose=1)[0][0] 
            print (result)
            if result > best_prob:
                min_r = r
                min_c =c
                best_prob = result
            #if(result >= 0.995):
                #return min_r, min_c, best_prob          
    return min_r, min_c, best_prob

def backproject(rows_box,cols_box, rot_angle, scale, stretch, width, height):
    center_row = height/2
    center_col = width/2
    rot_angle_rad = rot_angle*pi/180
    R = np.array([[cos(rot_angle_rad), sin(rot_angle_rad), center_row], [-sin(rot_angle_rad), cos(rot_angle_rad), center_col],[0,0,1]],dtype=float32)
    rows_box_centered = np.asarray(rows_box) - center_row
    cols_box_centered = np.asarray(cols_box) - center_col
    C =  np.array([rows_box_centered ,cols_box_centered,[1,1,1,1,1] ],dtype=float32)
    rows_box_centered = np.asarray(rows_box) - center_row
    Cp = np.dot(R,C)/scale
    Cp[1,:] = Cp[1,:]/stretch
    rows_orig = Cp[0,:].tolist()
    cols_orig = Cp[1,:].tolist()
    return rows_orig, cols_orig

start_time = time.time()
#Loading Model FishNoFish
model = keras.models.load_model('fish_nofish.h5', custom_objects={'abs_val_rect': abs_val_rect})
#Loading Model Classifier
modelClass = keras.models.load_model('cnnv4_400epochs_adadelta_abs_value_no_data_aug_100training_seed3.h5', custom_objects={'abs_val_rect': abs_val_rect})
image_list = []
resultArr = []
image_color_list = []
imCounter = 0
for filename in glob.glob('/home/anthony/FishCompetition/test_stg1/*.jpg'):
    i0=cv2.imread(filename, 0)
    imColor = cv2.imread(filename)
    image_list.append(i0)
    image_color_list.append(imColor)
    imshow(i0)

    imCounter +=1

# Selecting an arbitrary pattern
    rows_pattern = 224
    cols_pattern = 224
    min_row = 0
    min_col = 0
    min_rot = -20
    b=1.5
    min_sc = math.pow(b, 1)
    min_st = math.pow(b, -0.5)
    
    #Search for best match
    
    frames =0
    best_prob = -10000.0
    for rot in range(-20,340,20):        # Extend range to 360 degrees
        for sc in np.arange(-0.5,0.6,0.5):
            for st in np.arange(-0.5,0.6,0.5):
                print (rot,sc,st)
                #i1 = scale_stretch_rot(i0,math.pow(b, sc),math.pow(b, st),rot)
                i1 = scale_stretch_rot(i0,math.pow(b, sc),math.pow(b, st),rot)
                #i1_r = np.array(i1,dtype=float)
                frames = frames +1
                r,c,m = best_match(i1, model)
                print(m)
                if m>best_prob:
                    width, height = i1.shape
                    best_prob = m
                    min_row = r
                    min_col = c
                    min_rot = rot
                    min_sc = math.pow(b, sc)
                    min_st = math.pow(b, st)
                    print ("Better match found")
                    print(best_prob,min_sc,min_st,min_rot,min_row,min_col)
            #if(best_prob > 0.995):
                #break
        #if(best_prob > 0.995):
            #break
    
    r=min_row
    c=min_col
    rows_orig, cols_orig =  backproject([r, r, r+rows_pattern, r+rows_pattern, r],[c, c+cols_pattern, c+cols_pattern, c, c], min_rot, min_sc, min_st, width, height)
    if (best_prob >= 0.995):
        i1 = scale_stretch_rotColor(imColor,min_sc,min_st,min_rot)
        img_rows, img_cols = 76, 224
        img_total_rows = 224
        img_channels = 3
        delta_rows = int((img_total_rows - img_rows) / 2)
        window = i1[r:r+rows_pattern,c:c+cols_pattern, :]
        X = np.empty((1,img_rows,img_cols, 3))
        X[0] = window[delta_rows:delta_rows+img_rows, :, :]
        X /= 255
        print(X)
        result = modelClass.predict_proba(batch_size=1, x=X, verbose=1)
        print ("Done with Diego");
        print (result[0,:]) 
        with open('Output2.txt', 'a+') as f:
            for x in result:
                f.write('%f,%f,%f,%f,%f,%f,%f\n' % tuple(x))
        
    else:
        with open('Output.txt', 'a+') as f:
            f.write("No fish found in this image");
            print ("No fish found in this image")
    
    
    
    elapsed_time = time.time() - start_time
    
    print('Frames processed:', frames)
    print('Elapsed time:', elapsed_time)
    print('Time per frame:', elapsed_time/frames)
