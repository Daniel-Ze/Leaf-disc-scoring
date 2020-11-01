#!/usr/bin/env python

import os
import sys
import numpy as np
import keras
import image_slicer
from keras.preprocessing.image import load_img, img_to_array
import glob
import shutil

if len(sys.argv) == 4:
    leaf_discs = sys.argv[1]
    model_leaf_vs_back = keras.models.load_model(sys.argv[2])
    model_nospo_vs_spo = keras.models.load_model(sys.argv[3])
else:
    print(sys.argv)
    exit("Usage: python /path/to/leaf/disc /path/to/CNN_model_leaf_vs_back /path/to/CNN_model_nospo_vs_spo")

# Loading the CNN models for calssification
#model_leaf_vs_back = keras.models.load_model('/home/daniel.zendler/CNN/img_classify/data3/leaf_vs_back_acc98_model.h5')
#model_nospo_vs_spo = keras.models.load_model('/home/daniel.zendler/CNN/img_classify/data2/spo_vs_nospo_acc92_model.h5')

# Directory with images
#leaf_discs = '/home/daniel.zendler/CNN/img_classify/leaf_disc_test/'

# Initialize sample name variable
sample = 0

# Specify the image type
valid_img = [".jpg"]

num_img=0
for image in os.listdir(leaf_discs):
    if image.endswith('.jpg'):
        num_img=num_img+1
    else:
        continue
print("[info]\t\tNumber of leaf discs:\t"+str(num_img))
print("[info]\t\tFolder:\t\t"+leaf_discs)
print("[info]\t\tModel 1:\t"+sys.argv[2])
print("[info]\t\tModel 2:\t"+sys.argv[3])

with open(leaf_discs+"cassify_results.txt", 'w') as results:
    # Print the header
    results.write("Sample\tNumber\tLeaf disc\tAgar\t%Leaf disc\t%Agar\tspo\tno spo\t%spo\t%no spo\n")

    for image in os.listdir(leaf_discs):

        if image.endswith('.jpg'):
            try:
                os.mkdir(leaf_discs + "tmp/")
            except OSError:
                print ("Creation of the directory %s failed" % leaf_discs + "tmp/")

            # Slice the leaf disc image in 500 pieces and save them in the tmp file
            img = os.path.join(leaf_discs, image)
            tiles = image_slicer.slice(img, 500, save=False)
            image_slicer.save_tiles(tiles, directory=leaf_discs + "tmp", prefix=image, format='png')

            count = 0
            count_1 = 0
            count_0 = 0
            leafdisc = []

            for f in os.listdir(leaf_discs + "tmp"):
                if f.endswith('.png'):
                    path_file = leaf_discs + "tmp/" + f
                    img = load_img(path_file)
                    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
                    x = x.reshape((1,) + x.shape)

                    classes = model_leaf_vs_back.predict_classes(x)
                    #print(f+" - "+str(classes[0,0]))

                    count = count + 1
                    if classes[0,0] == 1:
                        count_1 = count_1 + 1      #counter plus one if class 1 (leaf disc)
                        leafdisc.append(path_file) #keep a list of the leaf disc pictures
                    else:
                        count_0 = count_0 + 1      #counter plus one if class 0 (background, agar)
                    continue
                else:
                    continue

            count_11 = 0
            count_1_1 = 0
            count_0_1 = 0
            spo = []
            no_spo = []

            for l in leafdisc:
                img = load_img(l)
                x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
                x = x.reshape((1,) + x.shape)

                classes = model_nospo_vs_spo.predict_classes(x)
                #print(f+" - "+str(classes[0,0]))
                count_11 = count_11 + 1
                if classes[0,0] == 1:
                    count_1_1 = count_1_1 + 1
                    spo.append(l)
                else:
                    count_0_1 = count_0_1 + 1
                    no_spo.append(l)
                continue

            with open(leaf_discs+image+"spo_coord.txt", 'w') as f:
                for k in spo:
                    if k.endswith('.png'):
                        n=k.split("/")
                        n1=n[-1].split(".")
                        n2=n1[1].split("_")
                        n3=24-int(n2[1])
                        f.write(str(n3)+"\t"+n2[2]+"\n")
                    else:
                        continue

            sample = sample + 1

            results.write(image+"\t"+str(sample)+"\t"+str(count_1) + "\t" + str(count_0) + "\t" + str(round((count_1 / count) * 100))
                  + "\t" + str(round((count_0 / count) * 100)) + "\t" + str(count_1_1)
                  + "\t" + str(count_0_1) + "\t" + str(round((count_1_1 / count_11) * 100)) + "\t" + str(round((count_0_1 / count_11) * 100)) + "\n")

            # Clear the content of tmp/ directory
            shutil.rmtree(leaf_discs+'tmp')
        else:
            continue
