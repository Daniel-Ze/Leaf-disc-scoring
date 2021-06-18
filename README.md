![title](https://github.com/Daniel-Ze/Leaf-disc-scoring/blob/main/git_title.png)

Objective and high-throughput calssification of leaf disc images form inoculation experiments.

If you use this code please cite:\
**High-throughput phenotyping of leaf discs infected with grapevine downy mildew using shallow convolutional neural networks**\
Zendler D, Malagol N, Schwandner A, Hausmann L, Zyprian E


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Leaf disc scoring pipeline</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/Daniel-Ze/Leaf-disc-scoring" property="cc:attributionName" rel="cc:attributionURL">Daniel Zendler</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

<img align="left" src="https://github.com/Daniel-Ze/Leaf-disc-scoring/blob/main/run_classification.png?raw=true" width="300">

## The general pipeline

The CNNs were trained with images with a resolution of **2752 × 2208 pixels**. Using other resolutions than this has not been tested with the supplied model files and therefore no garuntee for success is given when using different resolutions.\
The whole pipeline is written in python and R. The two scripts are wrapped in a bash script for consecutive execution. The pipeline can therefore be run on any given UNIX system with all the depencies installed. It was tested and worked on:

  - MacOS Mojave
  - Ubuntu 18 LTS, 20 LTS.

The leaf disc scoring pipeline first slices the supplied leaf disc image into 506 sub images using image_slicer. The scoring pipeline itself then consists of two trained CNNs with binary output:

  1. CNN1: Group slices into background and leaf disc itself
  2. CNN2: Group classified leaf disc slices into infected and not infected

The resulting number of leaf disc slices infected and not infected are expressed as percentage and are included in the final result. The pipeline will iterate over all images in a given folder. The pipeline outputs the raw results as a tab delimited text file that can be further used with R. Further the pipeline produces plots of the original RGB image overlaid with the slcies classified as infected with downy mildew and a boxplot showing the overall phenotypic distribution in the given dataset.\

## What it needs

  - Python > 3.6
  - Tensorflow == 2.4.0
  - Keras == 2.4.3
  - R > 3.6, Rscript
    - ggplot2
    - R.utils
    - readr
    - stringr
    - jpeg
    - data.table

## How to install all dependencies

Recommended installation:
  - Clone repository
  - Install miniconda3 (if not already installed) and install mamba
  - Make a conda environment called Keras with python 3.6 installed
```shell
$ git clone https://github.com/Daniel-Ze/Leaf-disc-scoring.git
$ mamba create -n keras python=3.6
$ conda activate keras
```
  - Next upgrade pip and setuptools
```shell
(keras)$ pip install --upgrade pip setuptools
```
  - Install python requirements
```shell
(keras)$ cd ~/Leaf-disc-scoring/
(keras)$ pip install -r requirements.txt
```

  - Install R
```shell
(keras)$ mamba install R
```
  - Install all libraries for R
```shell
(keras)$ R
> install.packages(c("ggplot2","R.utils","readr","stringr","jpeg","data.table"))
> q()
Save workspace image? [y/n/c]: n
```
  - Make the bash script executable
```shell
$ cd ~/leaf-disc-scoring
$ chmod a+x run_classification
```
  - If you want to have the programm accessible from everywhere (! **make sure to
    adjust the path** !)
```shell
# MacOS:
$ echo 'export PATH=~/Leaf-disc-scoring:$PATH' >>~/.bash_profile
# Linux
$ echo 'export PATH=~/Leaf-disc-scoring:$PATH' >>~/.bashrc
```
  - Restart the terminal and you're all set

## Running the pipeline

Before running the program make sure to activate the conda environment with all the necessary depencies installed.
```shell
$ conda activate Keras
(keras)$ run_classification
Running from /path/of/install/CNN/.

Usage: run_classification -f path/to/leaf/disc/dir/ -e Inoculation1 -l model_l_vs_b.h5 -s model_s_vs_no-s.h5
	-f Path to leaf disc containing folder. Don't forget the / at the end
	-e Give your experiment a name
	-l Path to custom Keras model: leaf vs background (if not supplied standard model will be used)
	-s Path to custom Keras model: sporangia vs no-sporangia (if notsupplied standard model will be used)
```

If you intend to use the classification for images of the size **2752 × 2208 pixels** and you want to use the pre-trained models for the classification the flags **-l** and **-s** can be ignored. The program will then use the models supplied in the programs folder.

To Check if the program runs properly a set of test images is supplied. In total four leaf discs with different degrees of infection severity are supplied.\
Running the test:
```shell
$ run_classification -f test/ -e test_git
/Users/daniel/miniconda3/etc/profile.d/conda.sh exists.
[info]	Running from /Users/daniel/PostDoc/Programs/CNN/CNN/.
[warning] No conda environment name given. Defaulting to: keras
[info]	Running Keras in version: 2.4.3
[info]	Leaf disc folder exists.
[info]	Experiment name : test_git
[info]	No -l option. Using standard model: CNN1_model.h5
[info]	No -S option. Using standard model: CNN2_model.h5
[info]	Running classify_leaf_disc.py. This might take some time.
[info]		# leaf discs:	4
[info]		Folder:		test/
[info]		Model 1:	/Users/daniel/PostDoc/Programs/CNN/CNN/CNN1_model.h5
[info]		Model 2:	/Users/daniel/PostDoc/Programs/CNN/CNN/CNN2_model.h5
[info]  Progress: |██████████████████████████████████████████████████| 100.0% Complete
[info] Elapsed time: 2 min
[info]	Running plot_coords.R
[info]		Plotting score1_3_Plate_1_II_s47.jpg
[info]		Plotting score5_1_Plate_3_I_s03.jpg
[info]		Plotting score7_4_Plate_6_II_s77.jpg
[info]		Plotting score9_3_Plate_6_I_s18.jpg
```
Running the program should yield the following results:

The program also generates a plot indicating the leaf disc slices which were classified as infected in a folder called **results**. In the same folder a plot should be present showing the percentage leaf disc covered with sporangiophore distribution of the analyzed leaf disc images. The raw results can be found in a tab delimited text file in the main folder called **classify_results.txt**
![results](https://github.com/Daniel-Ze/Leaf-disc-scoring/blob/main/results_combined_git.png?raw=true)

## "Oh no my images are not in the right resolution" , "My samples are not infected with downy mildew and I don't work with grapevine" or "I want to train my own models"

With the main pipeline a folder with additional scripts is supplied. The python scripts should help you to set your stuff up with another pathogen or if you just want to train your models on image data from yoour experiments. So please go to scripts and read the README.
