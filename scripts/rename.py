#!/usr/bin/env python

import os
import sys
import imghdr

# Function to rename multiple files
def main():
    #Some variables
    test = ''
    names_img = ''
    count = 1
    count_img = 0
    count_names = 0

    #Read in the filename file and the directory
    #1. only name file and image directory
    if len(sys.argv) == 3:
        with open(sys.argv[1], 'r') as f:
            names = f.readlines()
        dir = sys.argv[2]
        prefix = ''
        print("[warning]\tNo prefix supplied.")
    #2. name file, image directory and prefix
    #   Get the prefix for the images: 1dpi, 4dpi, 6dpi, 8dpi
    elif len(sys.argv) == 4:
        with open(sys.argv[1], 'r') as f:
            names = f.readlines()
        dir = sys.argv[2]
        prefix = sys.argv[3]
    #3. If none of the above works quit.
    else:
        exit("[error]\t\tPlease give a name file and the directory of the images. Optional a prefix can be supplied.\
              \n[info]\t\tpython rename.py namefile /Path/to/images.tiff prefix")

    #Get the contents of the indidcated directory and sort it alphanumerical
    dir_sort = sorted(os.listdir(dir))

    #Count the images in the directory
    for file in os.listdir(dir):
        count_img = count_img + 1
    print("[info]\t\tNumber of images:\t" + str(count_img))

    #Count the names in the name file
    for lines in names:
        count_names = count_names + 1
    print("[info]\t\tNumber of names:\t" + str(count_names))

    #Check if there are the same amount of pictures and names in the directory
    #and in the name file
    if count_img != count_names:
        exit("[error]\t\tNumber of images and names don't match.")

    print("[info]\t\tFound " + str(count_img) + " images and " + \
          str(count_names) + " names. Continuing renaming.")

    #Go through all the images and names and rename
    for filename, name in zip(dir_sort,names):
        #Check what image type the images are
        img_type = imghdr.what(dir+filename)
        #Only continue if the images are type .tiff
        if img_type == 'jpeg':
            #Indicate which file will be named differently
            #Creating the new filename
            if prefix != '':
                print("[info]\t\tRenaming: " + filename + " to " + prefix + \
                      "_img_" + str(count) + "_" + name.rstrip() + "." + img_type)
                new_name = prefix + "_img_" + str(count) + "_" + \
                name.rstrip() + "." + img_type
            else:
                print("[info]\t\tRenaming: " + filename + " to " + \
                      "img_" + str(count) + "_" + name.rstrip() + "." + img_type)
                new_name = "img_" + str(count) + "_" + \
                name.rstrip() + "." + img_type
            #Put filename and directory together for os.rename()
            dir_file = dir + filename
            #Put new filename and directory together for os.rename()
            dir_new_name = dir + new_name
            #Rename the file
            os.rename(dir_file, dir_new_name)
            count = count + 1
        #If it's no .tiff file in the directory, exit (somethings fishy).
        else:
            exit("[error]\t\tNo .tiff file found.")

# Driver Code
if __name__ == '__main__':

    # Calling main() function
    main()
