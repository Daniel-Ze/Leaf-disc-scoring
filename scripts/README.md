![title](https://github.com/Daniel-Ze/Leaf-disc-scoring/blob/main/scripts/script_title.png)

# Set up your own models

This is a quick walk through for setting up your own trained models for image classification. For more detail please see this simple tutorial:\
https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html


Tensorflow: https://www.tensorflow.org/learn


Keras: https://keras.io/about/


As we're not using super deep neural networks like GoogLeNet, Inception, Xception etc. and as we will have only a small set of images we will be able to do all model trainings on a standard laptop. Everything presented here was either trained on a MacBook Pro or a Computer running Ubuntu:
  - MacBook Pro, 8 core cpu (multi threaded), 16gb ram
  - PC, 12 core cpu (multi threaded), 32 gb ram

**Note:** I did not invent any of this. The process of classifying images is well documented out there in the world wide web. Remember: Using your favorite search engine is most of the time the best problem solver. The scripts supplied are just a suggestion. If there's a simpler and better solution to the problem use it :)

## 1. Image preparation

You find several scripts in this folder that should help you set up the image data needed to train your own models. The first python script that we need is **chop_images.py**. To check if everything's fine with the script please change into the scripts folder and give it a dry run:
```shell
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

As you can see this is a simple python script using image_slicer. It is intended to slice your images in n pieces for manual classification.\
The python script will take a folder with images as input (-i) as you will have to use multiple images to generate enough image slices for training a new model. Image slices are stored in a folder with the Image_name.tif_slice. The generated slices are stored as .png files.

```shell
$ cd ~/folder/with/images/
$ conda activate keras
(keras) ~/folder/with/images/ $ python ~/Leaf-disc-scoring/scripts/chop_images.py -i ./ -s 506 -e .jpg
```
The above command should slice all the images in your folder in 506 equal pieces (if it's possible). image_slicer will adjust the number of slices if it can devide it into the set number.\
**Note:** You might want to change the number of image slices according to your image data. Higher resolution will alow you to make smaller slices (in theory) or you want to have less slices. It's up to you.\

## 2. Image sorting

Now that we have our images chopped into little pieces we have to sort them into their respective categories. For this we will use the python script **image-sorter2_script.py**. This tool was written by Nestak2 and is available on github: https://github.com/Nestak2/image-sorter2. Please clone the git repository and install the requirements from the requirements.txt file.

```shell
$ git clone https://github.com/Nestak2/image-sorter2.git
$ cd image-sorter2/
~/image-sorter2 $ conda activate keras
(keras) ~/image-sorter2/ $ pip install -r requirements.txt
```

After you have installed the requirements to this very useful tool you should be all set to run this tool. We will not run the original script but the adjusted one supplied in this scripts/ folder:
```shell
(keras)$ cd ~/Leaf-disc-scoring/scripts/
(keras)~/Leaf-disc-scoring/scripts$ python image-sorter2_script.py
[error]	No input folder
Usage: python -i /path/to/images/ -m or -c -l class1,class2,class3 -e .jpg
-h print this help
-i input folder for image_sorter2
-m move files
-c copy files
-l classes to sort images into: bla,blubb,tralala
-e file extensions that are accepted: e.g. .png
```
This should pop up if you run the script without any arguments. Now that we know that everything's fine with the script we change to the images that have to be sorted into different categories and run the script on all image slices. As we have chopped several images into little pieces we can now iterate over the folders with those image pieces:
```shell
(keras) $ cd ~/folder/with/images/
(keras) ~/folder/with/images $ for f in */; do echo $f; python ~/Leaf-disc-scoring/scripts/image-sorter2_script.py -i $f -m -l class1,class2,class3 -e .png ; done
```

We specified -m which will move the image slices in a folder with the respective calss and we have specified the classes with -l. Please feel free to change the class names to something you like and recognize easily. Additionally you can add more classes e.g. a class for images that say nothing because they are out of focus.


**Note:** This is one of the most important steps in training your model.
  - There's this wisdom: Garbage in garbage out. The better the images are sorted the better the model training will be.
  - Make sure you're consistent during your sorting.
  - This step should be done by the person who has the most experience with the pathogen or trait to be analyzed.
  - The small images can be challenging to sort some times. It is wise to exclude the ones that you can't sort.
  - Human brains get tired from repetitive tasks (or at least mine). Therefore, it is wise to recheck your sorted images.

## 3. Create training and validation datasets

Now that we have our images sliced and sorted into their respective classes we can continue with making datasets for the model training. First we combine all the folders with the same class into one folder per class. From these folders we will randomly draw images for the training and validation datasets. For this we have the script **random_select_val_train.py**. Give it a dry run:
```shell
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
The ratio of training to validation should be around 60 : 40 % of images from the respective class. We are going to train binary CNNs therefore we will have two classes for training and validation later on.\
In the Keras tutorial a total of 1000 images per class were used for training the CNN and 400 images were used for validation. We will follow this tutorial with our random select python script. We will chose 1000 images for training and 400 images for validation for each class we have generated in a folder called combined/:
```shell
(keras) ~/folder/with/images $ python ~/Leaf-disc-scoring/scripts/random_select_val_train.py -i combined/class1/ -v 400 -t 1000 -e .png
```
This will generate two folders inside the class1 folder:
  - training with 1000 images
  - validation with 400

Repeat this step for the other classes that you have generated. If you want to train a model for leaf discs and you want to substract the image slices with background from the leaf disc then you have now three classes:
  - class1 = background
  - class2 = leaf_disc
  - class3 = leaf_disc_with_pathogen


**Note:** This is just a suggestion. You can use different amounts of images for your training.

## 4. Create the folder structure

As you might recall we have to train two CNNs, one for background vs. leaf disc and one for leaf disc with and without pathogen. Therefoore we have to generate a third folder in our combined folder:
```shell
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
```shell
(keras) ~/folder/with/images $ mkdir -p CNN1/{training,validation}/{class1,class4}
(keras) ~/folder/with/images $ cp combined/class1/training/* CNN1/training/class1/
(keras) ~/folder/with/images $ cp combined/class4/training/* CNN1/training/class4/
(keras) ~/folder/with/images $ cp combined/class1/validation/* CNN1/validation/class1/
(keras) ~/folder/with/images $ cp combined/class4/validation/* CNN1/validation/class4/
```

Please follow these steps for the data for the second CNN2 and the two classes class2 and class3 for detection of leaf disc slices with and without pathogen.

## 5. Evaluation data

You have created datasets for training your models. During the training of the models they will be validated with the generated validation data which will give you an idea how well your trained model will perform. However, it is important to perform an evaluation of the model with unrelated data. Therefore, we will generate for both CNN1 and CNN2 a third dataset called 'eval'. This dataset consists again of two classes each (class1, class4 - CNN1; class2, class3 - CNN2). So take some more images from your dataset and follow the steps 1 to 4. For this dataset it is not importatnt to have the same amount of pictures per class.
Our final 'CNN1' and 'CNN2' folders should look as follows at the end:
```
image_data/CNN1
            /training
                  /class1 (1000 images)
                  /class4 (1000 images)
            /validation
                  /class1 (400 images)
                  /class4 (400 images)
            /eval
                  /class1
                  /class4
image_data/CNN2
            /training
                  /class2 (1000 images)
                  /class3 (1000 images)
            /validation
                  /class2 (400 images)
                  /class3 (400 images)
            /eval
                  /class2
                  /class3
```

## 6. Training the CNN models

For the training of the CNNs we need the jupyter notebook from the scripts folder. Make sure to install jupyter in the keras conda environment:
```shell
$ conda activate keras
(keras) $ mamba install jupyter
(keras) $ pip install -U matplotlib
(keras) $ pip install pandas
(keras) $ pip install numpy
```
Now that we have jupyter installed in out keras conda environment we can open the script jupyter notebook:
```shell
(keras) $ jupyter notebook ~/Leaf-disc-scoring/scripts/leaf-disc-scoring_CNN_training.ipynb
```
Follow the notes in the jupyter notebook. It will guide you through the process of model training. Once you're finished with the training, you're happy with the model accurracy and loss and the model evaluation went fine you can use the saved model to test it with your data. The run_classification script let's you take alternative models in different combinations for CNN1 and CNN2 with the flags -l and -s.


### References

Image-Sorter2:
Arsenov, N. 2020, image-sorter2: One-click image sorting/labelling script. https://github.com/Nestak2/image-sorter2


