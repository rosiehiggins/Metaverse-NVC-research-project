# Non verbal communication for 3D virtual worlds

## Live version of prototype

https://metaversenvcdemo.web.app/

## Contents

1. Project Hierarchy
2. model
3. python-scripts
4. results
5. test-data
6. training-data
7. web-app

## Project Hierarchy

```
.
├── demo-video                  # Prototype demo video
├── ethics-documents            
│   ├── fast-track-ethics-form  # Signed fast-track ethics form
│   └── participant-docs        # Information sheet and consent form give to participants
│       └── signed-consent-forms         
├── models                      # Saved Keras ANN model files
│   ├── 23-input                
│   └── 60-input                
├── python-scripts              # Contains Python code used for data preprocessing, 
│                               # testing and training models
│   ...
│   ├── demos                   # Demos for each hand, face and body pose model tested
│   └── plots                   # Code to generate plots for results
├── results                     # Files containing results from performance evaluation
│   ├── heuristic-results       # confusion matrices with heuristic results
│   ├── ANN-results             # confusion matrices with ANN results
│   └── realtime-perf           # JSON containing execution times from protoype testing
├── test-data                   # Test datasets used for heuristic testing
├── training-images             # Samples of all secondary image data used in dataset
│   ...
│   └── README.txt              # Location to download all secondary image data if required 
├── training-videos             # Samples of primary video data collected 
│   │                           #(participant videos not available due to anonymity requirement)
│   ├── non-gesture       
│   ├── ok             
│   ├── raise-hand             
│   ├── thumbs-up             
│   └── wave           
├── training-data               # 3x Landmark datasets created from video and image files
│   └── dataset                 # raw output for heuristics, 60 input and 23 input sets
├── web-app                     # Web app prototype
│   └── irp-web-app             # Client directory
│       ├── build               # built web app (bundle deployed to Firebase)
│       ├── public              # local public folder with assets and model
│       │   ├── assets          # hand gesture emoji images used in prototype
│       │   └── model           # tensorflow.js converted Keras ANN models are here
│       │       ├── 23-input    
│       │       └── 60-input    
│       └── src                       # Source code files for prototype app
│           ├── ResultsQueue.js       # FIFO queue to hold prediction results
│           ├── Main.js               # Main page in prototype containing UI elements and MediaPipe
│           ├── LandmarksHelper.js    # Helper class for calculating hand landmark properties
│           ├── GestureHeuristics.js  # Contains heuristic calculations and prediction method for heuristics
│           ├── GestureClassifier.js  # Loads Keras ANN models and runs predictions
│           └── App.js                # Main app (would hold routes to other pages if app expanded)
└── README.md
```

## model

Contains weights (h5) output files for both 23f and 60f Keras ANN models.

## python-scripts

**Notes**
* Python version prerequisite for TensorFlow  is v 3.7-3.10
* Libraries required: numpy, pandas, scikit-learn, keras, mediapipe, matplotlib, cv2, tensorflow

This folder Contains all python scripts used in the project for data pre-processing, training ANN, testing and evaluating heuristics, generating plots, calculating test metrics and demos of all hand and body pose models tested.

Scripts within the root folder are listed below:

* **createDataset.py**: Python module for carrying out operations on data, including functions for passing video files through Mediapipe and outputting landmarks
* **generateANNDatasets.py**: Script that uses functions from createDataset to generate both datasets for ANN models and save to csv
* **generateHeuristicsDataset.py**: Script that uses functions from createDataset to generate raw landmarks for static heuristics dataset
* **generateWaveSequences.py**: Script that uses functions from createDataset to generate raw landmarks for wave sequences heuristic dataset
* **gestureClassifier23f.py**: Defines, trains and saves Keras 23-input ANN model
* **gestureClassifier60f.py**:  Defines, trains and saves Keras 60-input ANN model
* **gestureFeatures.py** : Python module for calculating hand properties from landmarks, such as angle and finger states
* **gestureHeuristics.py**: Python class for calculating heuristics from hand properties
* **splitHeuristicsTestset.py**: Script to split raw data in to test set for testing heuristics, using same seed as ANN models
* **testGestureClassifier.py** : Script that loads test set for ANNs and predicts new values, these are used to generate metrics
* **testStaticHeuristics.py** : Script that loads test set for static heuristics and predicts new values, these are used to generate metrics
* **testWaveHeuristic.py** : Script that loads test set for the wave heuristic and predicts new values, these are used to generate metrics

## results

Contains confusion matrices for all tests of classification performance and outputs of speed tests as JSON

## test-data

Contains test datasets for heuristics,
Test data for ANNs was split in place during training with the same random seed

## training-data

Contains all landmark datasets generated from passing video and image files through MediaPipe

## web-app

Contains source code for web app prototype, for main app source code go to irp-web-app/src

The following javaScript files contain the source code for the prototype:

* **ResultsQueue.js**: Class which defines FIFO queue to hold prediction results, getResult returns the mode result each frame to smooth signal
* **Main.js**: Main class containing all UI components and MediaPipe Hands model
* **LandmarksHelper.js**: Helper class used for calculating hand properties from landmarks
* **GestureHeuristics.js**: Class containing gesture heuristics methods, including method for predicting heuristic given landmarks
* **GestureClassifier.js**: Class containing ANN models, loads Keras models from public/models, contains methods for preprocessing input and predicting

### Installation

To run locally:

Install  node.js and npm (https://radixweb.com/blog/installing-npm-and-nodejs-on-windows-and-mac) then in irp-web-app directory (web-app/irp-web-app) run: 

```
npm install
```

This will install all required packages, then to start test server run:

```
npm start
```

and go to http://localhost:3000

Or simply go to live version here: https://metaversenvcdemo.web.app/


### Keras model conversion instructions

How to use tensorFlow.js converter to convert Keras model to tensorFlow.js web version

Useful blog on the matter: https://medium.com/@mandava807/importing-a-keras-model-into-tensorflow-js-b09600a95e40

See: https://github.com/tensorflow/tfjs/tree/master/tfjs-converter

**Note** to run converter we need to use python 3.6.8, this clashes with the tensor-flow  requirement of 3.7-3.10
So we need to run converter from virtual env

#### Steps:

install pyenv : https://github.com/pyenv-win/pyenv-win

Then set up your local python to be 3.6.8

```
pyenv install 3.6.8
pyenv local 3.6.8
```

Install virtualenv: https://stackoverflow.com/questions/48911582/virtualenv-to-path-on-windows-10

```
pip install --user virtualenv
```

Then set up a virtual environment, see: https://docs.python.org/3/library/venv.html


```
python3 -m venv /path/to/new/virtual/environment
```

The activate virtual env by running activate script

```
cd venv
cd Scripts
activate.bat
```

**NOTE!!** in Windows 10 Powershell you need to run ./activate.PS1 and you may need to set permissions, see this post for more info: https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows

Once activated in Windows Powershell you will see a little *(venv)* before the directory name

next install tensorflowjs in your venv, install pip first if needed!

```
pip install tensorflowjs
```

Then you can convert model using either converter or wizard, converter example:

```
tensorflowjs_converter --input_format keras model/pathname/model.h5 converted/model/pathname
```

e.g.
tensorflowjs_converter --input_format keras model/model.h5 model/converted

The output JSON contains the model architecture and the binary file contains the weights, both are needed in the web app




