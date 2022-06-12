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


### model coversion instructions

How to use tensorFlow.js converter to convert h5 model to tensorFlow.js web version

install pyenv
install python v.6
https://github.com/tensorflow/tfjs/tree/master/tfjs-converter
install virtual env
create venv 
run activate
https://stackoverflow.com/questions/48911582/virtualenv-to-path-on-windows-10
NOTE. in Windows 10 you need to run ./activate.PS1
and you may need to set permissions see this post:
https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows
this bin file that accompanies the model once converted is important!


https://medium.com/@mandava807/importing-a-keras-model-into-tensorflow-js-b09600a95e40

within venv: command to convert model
tensorflowjs_converter --input_format keras model/pathname/model.h5 converted/model/pathname

e.g.
tensorflowjs_converter --input_format keras model/model.h5 model/converted
