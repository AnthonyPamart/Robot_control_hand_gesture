#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from toolbox.fourier_descriptors import truncate, normalize, get_descriptors
from toolbox.preprocess import threshold, get_contour
import cv2

from os import listdir
from os.path import isfile, join
path = '../DATA/ALL/'
files = [path+f for f in listdir(path) if isfile(join(path, f))]


all_descriptors = []
kmax = 35
open('../dataset.csv', 'w').close()
resultFile = open("../dataset.csv",'a')
name_of_inputs_to_store = 'move_type,'
for k in range(kmax+1): 
    name_of_inputs_to_store += 'descr_number_{}_x,descr_number_{}_y,'.format(k,k)

for k in range(kmax-1): 
    name_of_inputs_to_store += 'descr_number_{}_x,descr_number_{}_y,'.format(-(kmax-k),-(kmax-k))
name_of_inputs_to_store += 'descr_number_{}_x,descr_number_{}_y,'.format(-(kmax-(kmax-1)),-(kmax-(kmax-1)))
 
resultFile.write(name_of_inputs_to_store + "\n")
resultFile.close()
    
for i in range (len(files)): 
    print("iteration : {}".format(i))
    img_bgr = cv2.imread(files[i])

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_rgb = threshold(img_rgb)
    
    hand_contour = get_contour(img_rgb)    
        
    fourier_descriptors,freqs = get_descriptors(hand_contour)
    
    selected_descriptors, selected_freqs = truncate(fourier_descriptors, freqs, kmax)
    
    normalized_descriptors = normalize(selected_descriptors, kmax)
    
    all_descriptors.append(normalized_descriptors)
    
    # Open File
    
    resultFile = open("../dataset.csv",'a')

    
    # Write data to file
    descriptors_to_store = files[i].split('/')[-1].split('-')[0]+','
    for i_desc in range(len(normalized_descriptors)-1):
        descriptors_to_store += '{},{},'.format(normalized_descriptors[i_desc].real ,normalized_descriptors[i_desc].imag)
    descriptors_to_store += '{},{}'.format(normalized_descriptors[len(normalized_descriptors)-1].real ,normalized_descriptors[len(normalized_descriptors)-1].imag)
    resultFile.write(descriptors_to_store + "\n")
    resultFile.close()
