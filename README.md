# Mass Deepfake Video Generation Using DeepFaceLab Tool

This repository is an adaptation of the [DeepFaceLab](https://github.com/iperov/DeepFaceLab) GitHub project in order to mass generate deepfake videos instead of one.

This project is not finished and might cause some error during the process of video generation.

The purpose is to generate deepfake between each video with each other.

## Getting Started

### Prerequisites

- Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- Install ffmpeg
- Install visual studio c++
- Environment creation :

```bash
$ conda create -n deepfacelab python=3.7

$ conda activate deepfacelab

# Install your GPU lib Nvidia or AMD
$ conda install -c conda-forge cudatoolkit cudnn

$ pip install -r requirements.txt


```

- Define a temporary folder to place your raw video, a folder for the different processes output (subjects) and finally a folder for the *SAEHD* model to use for training:

    Create and name your three folders: TMP_RAW_VIDEOS SUBJECTS_DIR MODEL_DIR
    Place the RTT models from [this link](https://drive.google.com/file/d/1auhf7Wtuwygi8rGFx4EJ4OEgVp1LtQpj/view) into the MODEL_DIR folder

### First step: Workspace creation

Organize your video into subject folder tree :

```bash
# Usage


$ python auto_main.py to_subject \
--videos_dir $TMP_RAW_VIDEOS \
--subjects_dir $SUBJECTS_DIR
```

At the end of this script you should have a number of subject equivalent of the number of raw videos. Moreover, the original videos inside the subject's folder should be renamed **output.***.



### Second step: Extract Frames and Alignments

Make frames from the *original videos* and extract the *alignment* :

```bash

$ python auto_main.py extract \
--subjects_dir $SUBJECTS_DIR \
--dim_output_faces 1024 \
--png_quality 90
```

The better the dimension is the better the deepfake quality will be, same for the png quality.


## Third step: Train on Subjects and Merge the Frames

Two processes are available to execute this step:

- auto training and auto merging.
- auto training and manual merging.

1. Auto training with Auto merging :

This method will **automatically** train on 2 subjects and merge the predicted face into frames and a video. The **chose parameters** can be adapted by modifying the code **line 213**, for instance, in the file [MergerConfig.py](merger/MergerConfig.py).

Usage example :
```bash
# Usage
$ python auto_main.py swap_auto -h

# The argument iteration_goal does not work and could be a nice feature to add.
# The program will open a new terminal where you will be ask to choose the parameters, remember to change the 
# iteration goal and pretrain value to false !!
$ python auto_main.py swap_auto \
--subjects_dir $SUBJECTS_DIR \
--model_dir $MODEL_DIR
```

2. Auto training with Manual merging :

This method will **automatically** train all the necessary model to predict faces and save them (it can easily reach a hundred of GB), and then will ask you to **manually** merge the different subjects.

Usage example :

```bash
# Usage to train models
$ python auto_main.py swap_flexible_train -h

# The argument iteration_goal does not work and could be a nice feature to add.
# The program will open a new terminal where you will be ask to choose the parameters, remember to change the 
# iteration goal and pretrain value to false !!
$ python auto_main.py swap_flexible_train \
--subjects_dir $SUBJECTS_DIR \
--model_dir $MODEL_DIR
```

```bash
# Usage to merge faces
$ python auto_main.py swap_flexible_merge -h

# The program will automatically select the remaining subject to merge and will open a new 
# terminal for you te execute the merge process, then you will have to close the terminal when the 
# merging status reach 100% because it does not properly close (that is why a new terminal is needed to
# avoid restarting the program for every subjects)
# Remember to set the interactive merger to true every time a new terminal is open.
$ python auto_main.py swap_flexible_merge \
--subjects_dir $SUBJECTS_DIR \
--model_dir $MODEL_DIR
```

*OPTIONAL*: to clean all the trained models you can do : ```$ python auto_main.py clean_flexible_train -h```

You can also test the merged frames to see if they bypass a face recognition algorithm :

```bash
# Usage
$ python auto_main.py frames_generated_benchmark -h
```

this algorithm uses the [YuNet](YuNet_model_face_recognition) onxx model. You can modify the face extraction / face recognition algorithm if you want.
