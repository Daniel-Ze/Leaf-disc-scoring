# Slect random images from folder for training and validation
import os
import random
import shutil
import getopt
import sys

def usage():
    print("Usage: python random_select_val_train.py -i /path/to/images/ -v 100 -t 500 -e .jpg")
    print("-h print this help")
    print("-i / --input= input folder with slices")
    print("-v / --val= number of slices for validation")
    print("-t / --train= number of slices for training")
    print("-e file extension of the slices")
    exit()

file_extensions = ""
input_folder = ""
nr_val = 0
nr_train = 0

if len(sys.argv) == 1:
    usage()

try:
    opts, args = getopt.getopt(sys.argv[1:], "v:t:hi:e:", ["val=","train=","cpoy", "move", "help", "input=", "extension="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err) # will print something like "option -a not recognized"
    usage()

for o, a in opts:
    if o in ("-v", "--val="):
        nr_val = int(a)
        #print(type(nr_val))

    elif o in ("-t", "--train="):
        nr_train = int(a)
        #print(type(nr_train))

    elif o in ("-h", "--help"):
        usage()

    elif o in ("-i", "--input="):
        input_folder = a

    elif o in ("-e", "--extension="):
        file_extension = a

    else:
        assert False, "unhandled option"

leaf_discs = input_folder
count = 0

for f in os.listdir(leaf_discs):
    count = count + 1

if input_folder == "":
    print("[error]\tNo input folder")
    usage()

if file_extension == "":
    print("[error]\tNo file extensions")
    usage()

if nr_val == 0:
    print("[error]\tNo number for validation")
    usage()

if nr_train == 0:
    print("[error]\tNo number for training")
    usage()

total = nr_val + nr_train

if total > count:
    print("[error]\tNot enough pictures in folder. Adjust number of validation and training pictures.")
    usage()

print("[info]\t# Img in folder: " + str(count))
print("[info]\t# Validation:    " + str(nr_val))
print("[info]\t# Training:      " + str(nr_train))
print("[info]\tImg type:        " + file_extension)
print("[info]\tInput folder:    " + input_folder)

try:
    os.mkdir(leaf_discs+"train/")
except:
    print("Creation of training dir in %s failed " % leaf_discs)
    usage()

try:
    os.mkdir(leaf_discs+"validation/")
except:
    print("Creation of validation dir in %s failed " % leaf_discs)
    usage()

files = sorted(os.listdir(leaf_discs))

count = 0

while (count < nr_val):
    d = random.choice(files)
    if d.endswith(file_extension):
        shutil.move(leaf_discs+d, leaf_discs+"validation/")
        files.remove(d)
        count = count + 1
    else:
        continue

files = sorted(os.listdir(leaf_discs))

count = 0

while (count < nr_train):
    d = random.choice(files)
    if d.endswith(file_extension):
        shutil.move(leaf_discs+d, leaf_discs+"train/")
        files.remove(d)
        count = count + 1
    else:
        continue
print("[info]\tSuccess.")
