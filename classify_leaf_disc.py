#!/usr/bin/env python

import os
import sys
import keras
import image_slicer
from keras.preprocessing.image import load_img, img_to_array
import shutil
import time

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

start = time.time()

# Parse the input from run_classification
if len(sys.argv) == 5:
    leaf_discs = sys.argv[1]
    model_leaf_vs_back = keras.models.load_model(sys.argv[2])
    model_nospo_vs_spo = keras.models.load_model(sys.argv[3])
    exp_name=sys.argv[4]
else:
    print(sys.argv)
    exit("Usage: python /path/to/leaf/disc /path/to/CNN_model_leaf_vs_back /path/to/CNN_model_nospo_vs_spo")

# Initialize sample name variable
sample = 0
i = 0

# Specify the image type
valid_img = [".jpg"]

# Check the number of images
num_img = 0
for image in os.listdir(leaf_discs):
    if image.endswith('.jpg'):
        num_img = num_img + 1
    else:
        continue

# Print the run parameters
print("[info]\t\tNumber of leaf discs:\t"+str(num_img))
print("[info]\t\tFolder:\t\t"+leaf_discs)
print("[info]\t\tModel 1:\t"+sys.argv[2])
print("[info]\t\tModel 2:\t"+sys.argv[3])

# Open the output file for the results
with open(leaf_discs+"classify_results.txt", 'w') as results:

    # Print the header of the results file
    results.write("Exp_name\tSample\tNumber\tLeaf_disc\tAgar\tperc_leaf_disc\tperc_agar\tspo\tno_spo\tperc_spo\tperc_no_spo\n")

    # Print the progress bar to stdout
    printProgressBar(0, num_img, prefix = '[info]  Progress:', suffix = 'Complete', length = 50)

    # Start iterating over the images in the directory
    for image in os.listdir(leaf_discs):

        # Only do somthing with files that are a image
        if image.endswith('.jpg'):

            # Create a temporary directory for the image slices
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

            # First CNN for leaf disc vs background
            for f in os.listdir(leaf_discs + "tmp"):
                if f.endswith('.png'):
                    path_file = leaf_discs + "tmp/" + f
                    img = load_img(path_file)
                    x = img_to_array(img)
                    x = x.reshape((1,) + x.shape)

                    classes = model_leaf_vs_back.predict_classes(x)

                    count = count + 1
                    if classes[0, 0] == 1:
                        count_1 = count_1 + 1
                        leafdisc.append(path_file)
                    else:
                        count_0 = count_0 + 1
                    continue
                else:
                    continue

            count_11 = 0
            count_1_1 = 0
            count_0_1 = 0
            spo = []
            no_spo = []

            # Second CNN for sporangia vs no sporangia
            for l in leafdisc:
                img = load_img(l)
                x = img_to_array(img)
                x = x.reshape((1,) + x.shape)

                classes = model_nospo_vs_spo.predict_classes(x)
                count_11 = count_11 + 1
                if classes[0, 0] == 1:
                    count_1_1 = count_1_1 + 1
                    spo.append(l)
                else:
                    count_0_1 = count_0_1 + 1
                    no_spo.append(l)
                continue

            # Open a coordinate file for images with sporangia
            with open(leaf_discs+image+"spo_coord.txt", 'w') as f:
                for k in spo:
                    if k.endswith('.png'):
                        # Copy the file to the folder spo/ for later inspection
                        shutil.copy2(k, leaf_discs+"spo")
                        # Split the
                        n = k.split("/")
                        n1 = n[-1].split(".")
                        n2 = n1[1].split("_")
                        n3 = 24-int(n2[1])
                        f.write(str(n3)+"\t"+n2[2]+"\n")
                    else:
                        continue

            sample = sample + 1

            results.write(exp_name+"\t"+image+"\t"+str(sample)+"\t"+str(count_1) + "\t" + str(count_0) + "\t" + str(round((count_1 / count) * 100))
                  + "\t" + str(round((count_0 / count) * 100)) + "\t" + str(count_1_1)
                  + "\t" + str(count_0_1) + "\t" + str(round((count_1_1 / count_11) * 100)) + "\t" + str(round((count_0_1 / count_11) * 100)) + "\n")

            # Clear the content of tmp/ directory
            shutil.rmtree(leaf_discs+'tmp')
        else:
            continue
        i=i+1
        printProgressBar(i, num_img, prefix = '[info]  Progress:', suffix = 'Complete', length = 50)

end = time.time()
print("[info] Elapsed time: " + str(round((end - start)/60))+" min")
