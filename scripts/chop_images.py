# Chop the leaf discs
import image_slicer
import os
import sys
import getopt

def usage():
    print("Usage: python chop_images.py -i /path/to/images/ -s 506 -e .jpg")
    print("-h print this help")
    print("-i / --input= input folder with images")
    print("-s / --slices= number of slices the image should be sliced into")
    print("-e / --extension= file type of the images: .jpg")
    exit()

input_folder = ""
slices = 0
extension = ""

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:s:e:", ["help", "input=","slices=","extension="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err) # will print something like "option -a not recognized"
    usage()

for o, a in opts:

    if o in ("-h", "--help"):
        usage()

    elif o in ("-i", "--input="):
        input_folder = a

    elif o in ("-s", "--slices="):
        slices = int(a)

    elif o in ("-e", "--extension="):
        extension = a

    else:
        assert False, "unhandled option"

if input_folder == "":
    print("[error]\tNo input folder")
    usage()

if slices == 0:
    print("[error]\tNumber of slices missing")
    usage()

if extension == "":
    print("[error]\tNo image type")
    usage()

print("[info]\tInput folder: " + input_folder)
print("[info]\tSlices:       " + str(slices))
print("[info]\tImage type:   " + extension)

leaf_discs = input_folder

for image in sorted(os.listdir(leaf_discs)):
    if image.endswith(extension):
        img = os.path.join(leaf_discs, image)
        suffix = "_slice"
        img_slice_folder = img + suffix
        try:
            os.mkdir(img_slice_folder)
        except OSError:
            print("Creating of the directory %s failed" % image)


        tiles = image_slicer.slice(img, slices, save = False)
        image_slicer.save_tiles(tiles, directory = img_slice_folder, prefix = image, format = 'png')
