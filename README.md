# Non verbal communication for 3D virtual worlds

## Contents

1. model
2. python-scripts
3. results
4. test-data
5. training-data
6. web-app

## model

Weights files (h5) for for 23 and 60 input ANN models trained in Keras

## python-scripts
Contains all python scripts used in the project for data pre-processing, training ANN, testing and evaluating heuristics, generating plots, calculating test metrics and demos of all hand and body pose models tested

version prerequisite for TensorFlow v 3.7-3.10

## results
Contains confusion matrices for all tests of classification performance and outputs of speed tests as JSON

## test-data

## training-data

## web-app


### Installation
To run locally
install npm
go to web-app/irp-web-app
npm install in this directory to install packages

to start test server go npm start
to try live version of web-app go to: https://metaversenvcdemo.web.app/


### Keras model coversion instructions

How to use tensorFlow.js converter to convert Keras model to tensorFlow.js web version
Useful blog: https://medium.com/@mandava807/importing-a-keras-model-into-tensorflow-js-b09600a95e40

See: https://github.com/tensorflow/tfjs/tree/master/tfjs-converter

##### Steps:
install pyenv : https://github.com/pyenv-win/pyenv-win
Then set up your local python to be 3.6.8
pyenv install 3.6.8
pyenv local 3.6.8

Install virtualenv: https://stackoverflow.com/questions/48911582/virtualenv-to-path-on-windows-10
pip install --user virtualenv

Then set up a virtual environment, see: https://docs.python.org/3/library/venv.html
python3 -m venv /path/to/new/virtual/environment

The activate virtual env by running activate script
run venv/Scripts/activate.bat

NOTE!! in Windows 10 you need to run ./activate.PS1
and you may need to set permissions see this post for more info: https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows

within venv: command to convert model
tensorflowjs_converter --input_format keras model/pathname/model.h5 converted/model/pathname

e.g.
tensorflowjs_converter --input_format keras model/model.h5 model/converted

The JSON contains the model architecture and the binary file contains the weights.




