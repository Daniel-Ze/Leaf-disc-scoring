# CNN leaf disc scoring

Objective and high-throughput calssification of leaf disc images form artificial
inoculation experiments with grapevine downy mildew (_Plasmopara viticola_).

## What does it do

The program slices pictures of leaf discs into 506 pictures and classifies the
slices into infected and not infected with a trained CNN. After classification
it calculates the percentage as a standardized score representing percent
infected leaf disc area.

<img src="https://github.com/Daniel-Ze/Leaf-disc-scoring/blob/main/run_classification.png?raw=true" width="300">

## What it needs

  - Python 3.6
  - Tensorflow
  - Keras
  - R
    - ggplot2
    - R.utils
    - readr
  - Rscript

## How to get it running

Recommended installation:
  - Install miniconda3 (if not already installed) and install mamba
  - Make a conda environment called Keras with python 3.6 installed
```
$ mamba create -n keras python=3.6
$ conda activate keras
```
  - Next upgrade pip and setuptools
```
$ pip install --upgrade pip setuptools
```
  - Install Tensorflow
```
$ pip install tensorflow
```
  - Install Keras
```
$ pip install keras
```
  - Install R
```
$ mamba install R
```
  - Install all libraries for R
```
$ R
> install.packages(c("ggplot2","R.utils","readr"))
> q()
Save workspace image? [y/n/c]: n
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

Before running the program make sure to activate the conda environment with all
the necessary programs installed.
```
$ conda activate Keras
$ run_classification
Running from /path/of/install/CNN/.

Usage: run_classification -f path/to/leaf/disc/dir/ -e Inoculation1 -l model_l_vs_b.h5 -s model_s_vs_no-s.h5
	-f Path to leaf disc containing folder. Don't forget the / at the end
	-e Give your experiment a name
	-l Path to custom Keras model: leaf vs background (if not supplied standard model will be used)
	-s Path to custom Keras model: sporangia vs no-sporangia (if notsupplied standard model will be used)
```

If you intend to use the classification for images of the size **XY** and you
want to use the pre-trained models for the classification the flags **-l** and
**-s** can be ignored. The program will then use the models supplied in the
programs folder.

To Check if the program runs properly a set of test images is supplied. In
total four leaf discs with different degrees of infection severity are
supplied.
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

```
Exp_name	Sample	Number	Leaf_disc	Agar	perc_leaf_disc	perc_agar	spo	no_spo	perc_spo	perc_no_spo
Test	score7_4_Plate_6_II_s77.jpg	1	376	130	74	26	162	214	43	57
Test	score1_3_Plate_1_II_s47.jpg	2	339	167	67	33	12	327	4	96
Test	score5_1_Plate_3_I_s03.jpg	3	369	137	73	27	35	334	9	91
Test	score9_3_Plate_6_I_s18.jpg	4	442	64	87	13	156	286	35	65
```

The program also generates a plot indicating the leaf disc slices which were
classified as infected in a folder called **results**.
![results](https://github.com/Daniel-Ze/Leaf-disc-scoring/blob/main/results_combined.png?raw=true)
