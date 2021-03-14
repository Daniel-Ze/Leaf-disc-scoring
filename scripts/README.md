# Set up your own models

This is a quick walk through for setting up your own trained models for image classification. For more detail please see this simple tutorial:\
https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html


You find several scripts in this folder that should help you set up the image data needed to train your own models. The first python script that we need is **chop_images.py**. To check if everythings fine with the script please change into the scripts folder and give it a dry run:
```
$ cd ~/Leaf-disc-scoring/
$ conda activate keras
(keras) ~/Leaf-disc-scoring/scripts $ python chop_images.py
[error]	No input folder
Usage: python chop_images.py -i /path/to/images/ -s 506 -e .jpg
-h print this help
-i / --input= input folder with images
-s / --slices= number of slices the image should be sliced into
-e / --extension= file type of the images in the folder: .jpg
```

As you can see this is a simple python script wrapped around image_slicer. It is intended to slice your images in n pieces for manual classification.\
The python script will take a folder with images as input (-i) as you will have to use multiple images to generate enough image slices for training a new model. Image slices are stored in a folder with the Image_name.tif_slice. The generated slices are stored as .png files.

```
$ cd ~/folder/with/images/
$ conda activate keras
(keras) ~/folder/with/images/ $ python ~/Leaf-disc-scoring/scripts/chop_images.py -i ./ -s 506 -e .jpg
```
The above command should slice all the images in your folder in 506 equal pieces (if it's possible). image_slicer will adjust the number of slices if it can devide it into the set number.\
Now that we have out images chopped into little pieces we have to sort them in their respective categories. For this we will use the tool image-sorter2_script.py. This tool was written by Nestak2 and is available on github: https://github.com/Nestak2/image-sorter2. Please clone the git repository and install the requirements from the requirements.txt file.

```
$ git clone https://github.com/Nestak2/image-sorter2.git
$ cd image-sorter2/
~/image-sorter2 $ conda activate keras
(keras) ~/image-sorter2/ $ pip install -r requirements.txt
```

After you have installed the requirements to this very useful tool you should be all set to run this tool. We will not run the original script but the adjusted one supplied in this scripts/ folder:
```
(keras) $ cd ~/Leaf-disc-scoring/scripts/
(keras) ~/Leaf-disc-scoring/scripts $ python image-sorter2_script.py
[error]	No input folder
Usage: python -i /path/to/images/ -m or -c -l bla,blubb,tralala -e .jpg
-h print this help
-i input folder for image_sorter2
-m move files
-c copy files
-l classes to sort images into: bla,blubb,tralala
-e file extensions that are accepted: e.g. .png
```
This should pop up if you run the script without any arguments. Now that we know that everything's fine with here we change to the images that have to be sorted into different categories and run the script on all image slices:
```
(keras) $ cd ~/folder/with/images/
(keras) ~/folder/with/images $ for f in */; do echo $f; python ~/Leaf-disc-scoring/scripts/image-sorter2_script.py -i $f -m -l class1,class2,class3 -e .png ; done
```

The command will loop over all folders with generated slices in the image folder. We specified -m which will move the image slices in a folder with the respective calss and we have specified the classes with -l. Please feel free to change the class names to something you like and recognize easily.\
Now that we have our images sliced and sorted into their respective classes we can continue with making datasets for the model training. First we combine all the folders with the same class into one folder per class. From these folders we will randomly draw images for the training and validation datasets. For this we have the script **random_select_val_train.py**. Give it a dry run:
```
(keras) $ cd ~/Leaf-disc-scoring/scripts/
(keras) ~/Leaf-disc-scoring/scripts $ python random_select_val_train.py
Usage: python random_select_val_train.py -i /path/to/images/ -v 100 -t 500 -e .jpg
-h print this help
-i / --input= input folder with slices
-v / --val= number of slices for validation
-t / --train= number of slices for training
-e file extension of the slices
```
To train our models later we will need a folder structure like this:
```
/image_data
          /training
                 /class1
                 /class2
          /validation
                 /class1
                 /class2
```
The ratio of training to validation should be around 60 - 40 % of images from the respective class. We are going to train binary CNNs therefore we will have two classes for training and validation later on.\
In the Keras tutorial a total of 1000 images per class were used for training the CNN and 400 images were used for validation. We will follow this tutorial with out random select python script. We will chose 1000 images for training and 400 images for validation for each class we have generated in a folder called combined/:
```
(keras) ~/folder/with/images $ python ~/Leaf-disc-scoring/scripts/random_select_val_train.py -i combined/class1/ -v 400 -t 1000 -e .png
```
This will generate two folders inside the class1 folder:
  - training with 1000 images
  - validation with 400

Repeat this step for the other classes that you have generated. If you want to train a model for leaf discs and you want to substract the image slices with background from the leaf disc then you have now three classes:
  - class1 = background
  - class2 = leaf_disc
  - class3 = leaf_disc_with_pathogen

As you might recall we have to train two CNNs, one for background vs. leaf disc and one for leaf disc with and without pathogen. Therefoore we have to generate a third folder in our combined folder:
```
(keras) ~/folder/with/images $ mkdir -p combined/class4/{training,validation}
```
You can name class4 instead leaf_disc_all. Copy 500 from the random class2(= leaf_disc)/training/ and 500 images from the random class3(= leaf_disc_with_pathogen)/training/ into class4(leaf_disc_all)/training/.\
We will do the same for the validation images: 200 images from random class2class2(= leaf_disc)/validation/ and 200 images from andom class3(= leaf_disc_with_pathogen)/validation/ into class4(=leaf_disc_all)/validation/.\
Out folder structure should look now like this:
```
image_data/combined
                /class1 (=background)
                      /training (1000 images)
                      /validation (400 images)
                /class2 (=leaf_disc)
                      /training (1000 images)
                      /validation (400 images)
                /class3 (=leaf_disc_with_pathogen)
                      /training (1000 images)
                      /validation (400 images)
                /class4 (leaf_disc_all)
                      /training (1000 images)
                      /validation (400 images)
```
Now we have all the data that we need to train our very own CNN models. First CNN model to train would be background vs. leaf disc. We therefore need the training and validation data of class1 and class4:
```
(keras) ~/folder/with/images $ mkdir -p CNN1/{training,validation}/{class1,class4}
(keras) ~/folder/with/images $ cp combined/class1/training CNN1/training/class1/
(keras) ~/folder/with/images $ cp combined/class4/training CNN1/training/class4/
(keras) ~/folder/with/images $ cp combined/class1/validation CNN1/validation/class1/
(keras) ~/folder/with/images $ cp combined/class4/validation CNN1/validation/class4/
```

Please follow these steps for the data for the second CNN2 and the two classes class2 and class3 for detection of leaf disc slices with and without pathogen.\

For the training of the first CNN we need the jupyter notebook from the scripts folder. Make sure to install jupyter:
```
$ conda activate keras
(keras) $ mamba install jupyter
(keras) $ pip install -U matplotlib
```
Now that we have jupyter installed in out keras conda environment we can open the script jupyter notebook:
```
(keras) $ jupyter notebook ~/Leaf-disc-scoring/scripts/CNN_training.ipynb
```
Follow the notes in the jupyter notebook. It will guid you through the process of model training. Once you're finished with the training and you're happy with the model accurracy and loss you can use the saved model to test it with your data. The run_classification script let's you take alternative models in different combinations for CNN1 and CNN2.
