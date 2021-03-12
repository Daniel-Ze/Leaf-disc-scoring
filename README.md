# Leaf disc scoring

Objective and high-throughput calssification of leaf disc images form artificial
inoculation experiments with grapevine downy mildew (_Plasmopara viticola_).

If you use this code please cite:\
**High-throughput phenotyping of leaf discs infected with grapevine downy mildew using trained convolutional neural networks**\
Zendler D, Nagarjun M, Schwandner A, Hausmann L, Zyprian E\
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
\
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
```
$ git clone https://github.com/Daniel-Ze/Leaf-disc-scoring.git
$ mamba create -n keras python=3.6
$ conda activate keras
```
  - Next upgrade pip and setuptools
```
(keras)$ pip install --upgrade pip setuptools
```
  - Install python requirements
```
(keras)$ cd ~/Leaf-disc-scoring/
(keras)$ pip install -r requirements.txt
```

  - Install R
```
(keras)$ mamba install R
```
  - Install all libraries for R
```
(keras)$ R
> install.packages(c("ggplot2","R.utils","readr","stringr","jpeg","data.table"))
> q()
Save workspace image? [y/n/c]: n
```
  - Make the bash script executable
```
$ cd ~/leaf-disc-scoring
$ chmod a+x run_classification
```
  - If you want to have the programm accessible from everywhere (! **make sure to
    adjust the path** !)
```
# MacOS:
$ echo 'export PATH=/usr/local/bin:$PATH' >>~/.bash_profile
# Linux
$ echo 'export PATH=/usr/local/bin:$PATH' >>~/.bashrc
```
  - Restart the terminal and you're all set

## Running the pipeline

Before running the program make sure to activate the conda environment with all the necessary depencies installed.
```
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
```
run_classification -f ~/path/to/program/CNN/test/ -e Test
Running from /Users/daniel/PostDoc/Programs/CNN/CNN/.
[info]	Leaf disc folder exists.
[info]	Experiment name : Test
[info]	No -l option. Using standard model: leaf_vs_back_acc98_model.h5
[info]	No -S option. Using standard model: spo_vs_nospo_acc92_model.h5
[info]	Running classify_leaf_disc.py. This might take some time.
[info]		Number of leaf discs:	4
[info]		Folder:		/Users/daniel/PostDoc/Programs/CNN/CNN/test/
[info]		Model 1:	/Users/daniel/PostDoc/Programs/CNN/CNN/leaf_vs_back_acc98_model.h5
[info]		Model 2:	/Users/daniel/PostDoc/Programs/CNN/CNN/spo_vs_nospo_acc92_model.h5
[info]  Progress: |██████████████████████████████████████████████████| 100.0% Complete
[info]	Running plot_coords.R
[info]		Plotting score1_3_Plate_1_II_s47.jpgspo_coord.txt
[info]		Plotting score5_1_Plate_3_I_s03.jpgspo_coord.txt
[info]		Plotting score7_4_Plate_6_II_s77.jpgspo_coord.txt
[info]		Plotting score9_3_Plate_6_I_s18.jpgspo_coord.txt
```
Running the program should yield the following results:

The program also generates a plot indicating the leaf disc slices which were
classified as infected in a folder called **results**.
![results](https://github.com/Daniel-Ze/Leaf-disc-scoring/blob/main/results_combined_git.png?raw=true)
