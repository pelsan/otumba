# Otumba

# Project: AI on Cloud Distribuited Systems

### Introduction

This project, we train agents on diferents scenarios in order to control the sizing with high load transaction. 

A reward is provided when the agent get a stable systems, thats no drops on the petition of the systems and get a minimal of pods in order to save costs.

The state space  has diferents dimentions depends the kind of pods to watch.


### Getting Started

The instructions are for to configurate the best scenario that i tested and needs less tricks that is on Ubuntu 20.04.2 LTS Linux , i tested it on windows 10 too and i will give the tricks needed in order to work  this project.

We have two parts
Core Instructions: The principal configuration that we need to have kubernetes, prometheus, jupyter notebook (machine learning with pytorch) and Instruction Scenarios: we configure the diferents scenarios ( simple web server,  web/mobile application, payments application)

    
The instruccion 1 is for Windows 10 Users with NVIDIA VideoCards, another S.O. please refer [this link](https://pytorch.org/get-started/locally/) and then  go to the number 2 Instruccion.


### Core Instructions

1.- NVIDIA CARDS : If you have a Nvidia VidCard you can use Pytorch and train your model faster, follow this intructions for Windows:
	
Install the latest nvidia driver [here](https://www.nvidia.com/es-la/geforce/drivers/)

Install Visual Studio 2019 16x (needed for CUDA) [here](https://visualstudio.microsoft.com/es/downloads/)

Install CUDA Kit [here, and note the version to be 11.0 ](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html)

2.- Install AnaConda [here](https://www.anaconda.com/products/individual)

3.- Create a kernel "drlnd" on AnaConda and install pytorch, torchvision with cuda support, gym enviroment, mlagents and unityagents: 

	on your menu on windows , select "Anaconda3" - and then "Anaconda Prompt" it will open a new command window then 
     (For another S.O. please refer  (https://docs.anaconda.com/anaconda/install/verify-install/) ):

	conda create --name drlnd python=3.6

	conda activate drlnd

	conda install -c anaconda ipykernel
	
	python -m ipykernel install --user --name drlnd --display-name "drlnd"

	pip install mlagents

	pip install unityagents --user

	pip install torchvision===0.8.2 -f https://download.pytorch.org/whl/torch_stable.html


4.- Download the github project (git clone https://github.com/pelsan/Continuous-Control.git) and open Continuous_Control.ipynb on Jupyter


5.- Download the environment from one of the links below.  You need only select the environment that matches your operating system:
    - Linux: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/Reacher_Linux.zip)
    - Mac OSX: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/Reacher.app.zip)
    - Windows (32-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/Reacher_Windows_x86.zip)
    - Windows (64-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/Reacher_Windows_x86_64.zip)
    
    (_For Windows users_) Check out [this link](https://support.microsoft.com/en-us/help/827218/how-to-determine-whether-a-computer-is-running-a-32-bit-version-or-64) if you need help with determining if your computer is running a 32-bit version or 64-bit version of the Windows operating system.

    (_For AWS_) If you'd like to train the agent on AWS (and have not [enabled a virtual screen](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-on-Amazon-Web-Service.md)), then please use [this link](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Linux_NoVis.zip) to obtain the environment.

6-. Place the file in the DRLND GitHub repository, in the `Continuous-Control/` folder, and unzip (or decompress) the file. 


5.- Select drlnd Kernel:

	On Jupyter Menu select "Kernel" - "Change Kernel" - "drlnd"

6.- Run the Notebook `Continuous_Control.ipynb` 
