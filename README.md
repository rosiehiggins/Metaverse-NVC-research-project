# Non verbal communication for 3D virtual worlds

## Contents

1. File hierarchy 
2. model
3. python-scripts
4. results
5. test-data
6. training-data
7. web-app

## File Hierarchy

```
.
├── models                  # Saved Keras ANN model files
│   ├── 23-input            # Model file for 23 input ANN
│   └── 60-input            # Model file for 60 input ANN
├── python-scripts          # Contains Python code used for data preprocessing, testing and training models
│   ├── demos               # Demos for each hand, face and body pose model tested
│   └── plots               # Code to generate plots for results
├── results                 # csv files containing results from performance evaluation
│   ├── heuristic-results   # confusion matrices with heuristic results
│   ├── ANN-results         # confusion matrices with ANN results
│   └── realtime-perf       # JSON containing execution times from protoype testing
├── test-data               # Test datasets used for heuristic testing
├── training-data           # All landmark datasets created from video and image files
│   └── dataset             # Source files (alternatively `lib` or `app`)    
├── web-app                 # Web app prototype
│   └── irp-web-app         # Client directory
│       ├── build           # built web app (what is deployed to firebase)
│       ├── public          # local public folder with assets and model
│       │   ├── assets      # hand gesture images used in prototype
│       │   └── model       # tensorflow.js converted models are here
│       └── src                       # Source code files for prototype app
│           ├── ResultsQueue.js       # FIFO queue to hold prediction results
│           ├── Main.js               # Main page in prototype containing UI elements and MediaPipe
│           ├── LandmarksHelper.js    # Helper class for calculating hand landmark properties
│           ├── GestureHeuristics.js  # Contains heuristic calculations and prediction method for heuristics
│           ├── GestureClassifier.js  # Loads Keras ANN models and runs predictions
│           └── App.js                # Main app (would hold routes to pages if app expanded)
└── README.md
```

## model

Contains weights (h5) output files for both 23f and 60f Keras ANN models.

## python-scripts

*version prerequisite for TensorFlow v 3.7-3.10*

Contains all python scripts used in the project for data pre-processing, training ANN, testing and evaluating heuristics, generating plots, calculating test metrics and demos of all hand and body pose models tested.

* **createDataset.py**:
* **generateANNDatasets.py**
* **generateHeuristicsDataset.py**
* **generateWaveSequences.py**
* **gestureClassifier23f.py**



## results
Contains confusion matrices for all tests of classification performance and outputs of speed tests as JSON

## test-data
Contains test datasets for heuristics,
Test data for ANNs was split in place during training with the same random seed

## training-data
Contains all landmark datasets created from video and image files

## web-app

Contains source code for web app prototype, for main app source code go to /src

### Installation

To run locally
Install npm then:
-cd web-app
-cd irp-web-app
-npm install

To start test server run:
-npm start

go to http://localhost:3000

Or go to live version here: https://metaversenvcdemo.web.app/


### Keras model conversion instructions

How to use tensorFlow.js converter to convert Keras model to tensorFlow.js web version
Useful blog: https://medium.com/@mandava807/importing-a-keras-model-into-tensorflow-js-b09600a95e40

See: https://github.com/tensorflow/tfjs/tree/master/tfjs-converter
**Note** to run converter we need to use python 3.6.8, this clashes with the tensor-flow  requirement of 3.7-3.10
So we need to run converter from virtual env

#### Steps:

install pyenv : https://github.com/pyenv-win/pyenv-win
Then set up your local python to be 3.6.8
-pyenv install 3.6.8
-pyenv local 3.6.8

Install virtualenv: https://stackoverflow.com/questions/48911582/virtualenv-to-path-on-windows-10
-pip install --user virtualenv

Then set up a virtual environment, see: https://docs.python.org/3/library/venv.html
-python3 -m venv /path/to/new/virtual/environment

The activate virtual env by running activate script
-cd venv
-cd Scripts
-activate.bat

**NOTE!!** in Windows 10 powershell you need to run ./activate.PS1
and you may need to set permissions, see this post for more info: https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows

once activated in Windows Powershell you will see a little "(venv)" before the directory name
next install tensorflowjs in your venv 

-pip install tensorflowjs

Then you can convert model using either converter or wizard, converter is used here:
-tensorflowjs_converter --input_format keras model/pathname/model.h5 converted/model/pathname

e.g.
tensorflowjs_converter --input_format keras model/model.h5 model/converted

The output JSON contains the model architecture and the binary file contains the weights, both are needed in the webapp




