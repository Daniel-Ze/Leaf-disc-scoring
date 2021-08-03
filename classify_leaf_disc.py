#!/usr/bin/env python

import os
import sys
import keras
import image_slicer
from keras.preprocessing.image import load_img, img_to_array
import shutil
import time
import random
import datetime

# Version 0.2
# license http://creativecommons.org/licenses/by-nc-sa/4.0/

# Print iterations progress (https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console)
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = 'X', printEnd = "\r"):
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
    bar = fill * filledLength + ' ' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


# Parse the input from run_classification
def input():
    if len(sys.argv) == 5:
        if os.path.isdir(sys.argv[1]) == True:
            f_leaf_discs = sys.argv[1]
        else:
            print("Leaf disc image folder does not exist")
            exit()

        try:
            f_model_leaf_vs_back = keras.models.load_model(sys.argv[2])
            # Do something with the file
        except IOError:
            print("Model file leaf vs back not accessible")
            exit()

        try:
            f_model_nospo_vs_spo = keras.models.load_model(sys.argv[3])
            # Do something with the file
        except IOError:
            print("Model file nospo vs spo not accessible")
            exit()

        if sys.argv[4] == '':
            print("No experiment name given.")
            exit()
        else:
            f_exp_name=sys.argv[4]

        return f_leaf_discs, f_model_leaf_vs_back, f_model_nospo_vs_spo, f_exp_name
    else:
        print(sys.argv)
        exit("Usage: python /path/to/leaf/disc /path/to/CNN_model_leaf_vs_back /path/to/CNN_model_nospo_vs_spo experiment_name")


# Run CNN1 for leaf vs back
def predict_1(x):
    global model_leaf_vs_back
    img = load_img(x)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
    return (model_leaf_vs_back.predict(x)> 0.5).astype("int32")


# Run CNN2 for spo vs nospo
def predict_2(x):
    global model_nospo_vs_spo
    img = load_img(x)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
    return (model_nospo_vs_spo.predict(x)> 0.5).astype("int32")


# Generate a random string for the temp folder
def get_random_string():
    sample_letters = 'abcdefghi'
    result_str = ''.join((random.choice(sample_letters) for i in range(5)))
    return result_str


# Do the image classification
def classify_img_slices(f_image):
    global sample
    sample = sample + 1

    # get the path and file name
    leaf_discs_path = os.path.dirname(f_image)+"/"
    leaf_disc_name = os.path.basename(f_image)
    rnd = get_random_string()

    # Create a temporary directory for the image slices
    try:
        os.mkdir(leaf_discs_path + "tmp"+rnd+"/")
    except OSError:
        print ("[warning]\t\tCreation of the directory %s/tmp/ failed" % leaf_discs_path)

    # Slice the leaf disc image in 500 pieces and save them in the tmp file
    tiles = image_slicer.slice(f_image, 500, save=False)
    image_slicer.save_tiles(tiles, directory=leaf_discs_path + "tmp" + rnd, prefix=leaf_disc_name, format='png')

    # Set the counter to zero and initialize the variables
    count = 0
    count_1 = 0
    count_0 = 0
    leafdisc = []
    back = []
    images = []

    # First CNN for leaf disc vs background (CNN1)
    for f in os.listdir(leaf_discs_path + "tmp" + rnd):
        if f.endswith('.png'):
            path_file = leaf_discs_path + "tmp" + rnd + "/" + f

            classes = predict_1(path_file)

            count = count + 1
            if classes[0, 0] == 1:
                count_1 = count_1 + 1
                leafdisc.append(path_file)
            else:
                count_0 = count_0 + 1
                back.append(path_file)
            continue
        else:
            continue

    # Set counter 0 and initialize variables
    count_11 = 0
    count_1_1 = 0
    count_0_1 = 0
    spo = []
    no_spo = []

    # Second CNN for sporangia vs no sporangia (CNN2)
    for l in leafdisc:
        # Call predict_2() function
        classes = predict_2(l)

        count_11 = count_11 + 1
        if classes[0, 0] == 1:
            count_1_1 = count_1_1 + 1
            spo.append(l)
        else:
            count_0_1 = count_0_1 + 1
            no_spo.append(l)
        continue

    # Open a coordinate file for images with sporangia
    with open(f_image+"spo_coord.txt", 'w') as f:
        for k in spo:
            if k.endswith('.png'):
                # Copy the file to the folder spo/ for later inspection
                shutil.copy2(k, leaf_discs_path+"spo/")
                # Split the
                n = k.split("/")
                n1 = n[-1].split(".")
                n2 = n1[1].split("_")
                y = 23-int(n2[1])
                x = int(n2[2])
                f.write(str(x)+"\t"+str(y)+"\n")
            else:
                continue

    # Open the created results file in 'append' mode
    with open(leaf_discs_path+"classify_results.txt", 'a') as results:
        # Write the results from the classification to file
        results.write(input()[3]+"\t"+f_image+"\t"+str(sample)+"\t"+str(count_1) + "\t" + str(count_0) + "\t" + str(round((count_1 / count) * 100))
              + "\t" + str(round((count_0 / count) * 100)) + "\t" + str(count_1_1)
              + "\t" + str(count_0_1) + "\t" + str(round((count_1_1 / count_11) * 100)) + "\t" + str(round((count_0_1 / count_11) * 100)) + "\n")
    results.close()

    # Clear the content of tmp/ directory
    shutil.rmtree(leaf_discs_path+"tmp"+rnd)


# Main function
def main():
    # Get global variables
    global model_leaf_vs_back
    global model_nospo_vs_spo
    global sample

    # Get the input
    input_1 = ()
    input_1 = input()
    leaf_discs = input_1[0]
    start = time.time()

    # Initialize sample name variable
    i = 0
    leaf_disc_imgs = []
    a = ''

    # Check the number of images
    num_img = 0
    for image in os.listdir(leaf_discs):
        if image.endswith('.jpg'):
            num_img = num_img + 1
        else:
            continue

    # Print the run parameters
    print("[info]\t\t# leaf discs:\t"+str(num_img))
    print("[info]\t\tFolder:\t\t"+leaf_discs)
    print("[info]\t\tModel 1:\t"+str(sys.argv[2]))
    print("[info]\t\tModel 2:\t"+str(sys.argv[3]))

    # Create a temporary directory for the image slices
    try:
        os.mkdir(leaf_discs + "spo/")
    except OSError:
        print ("[warning]\t\tCreation of the directory %s/spo/ failed" % leaf_discs)

    # Open the output file for the results (creates it if not existing)
    with open(leaf_discs+"classify_results.txt", 'w') as results:
        # Print the header of the results file: Date and time, the folder with leaf discs, CNN1 and CNN2
        results.write("# Date time: " + str(datetime.datetime.now()))
        results.write("# Folder:\t\t"+leaf_discs)
        results.write("# Model 1:\t"+sys.argv[2])
        results.write("# Model 1:\t"+sys.argv[3])
        results.write("Exp_name\tSample\tNumber\tLeaf_disc\tAgar\tperc_leaf_disc\tperc_agar\tspo\tno_spo\tperc_spo\tperc_no_spo\n")
    results.close()

    # Create a list with all the images in the folder
    for image in sorted(os.listdir(leaf_discs)):
        # Only do somthing with files that are a image
        if image.endswith('.jpg'):
            a = leaf_discs+image
            leaf_disc_imgs.append(a)
        else:
            continue

    # Print the progress bar to stdout
    printProgressBar(0, num_img, prefix = '[info]  Progress:', suffix = 'Complete', length = 50)

    # Start iterating over the images in the directory
    for image in leaf_disc_imgs:
        # Only do somthing with files that are a image
        if image.endswith('.jpg'):
            # Run function classify_img_slices()
            classify_img_slices(image)
            i = i + 1
            sample = sample + 1
            printProgressBar(i, num_img, prefix = '[info]  Progress:', suffix = 'Complete', length = 50)
        else:
            continue

    end = time.time()
    print("[info] Elapsed time: " + str(round((end - start)/60))+" min")


if __name__ == '__main__':
    model_leaf_vs_back = input()[1]
    model_nospo_vs_spo = input()[2]
    sample = 0
    main()
