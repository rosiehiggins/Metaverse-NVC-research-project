#60 feature multiclass test with default parameters of SGD

import os
#manually add dll directories because they can't be found in system path
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
os.add_dll_directory("C:/tools/cuda/bin")

from keras.models import Sequential
from keras.layers import Dense
from keras.losses import CategoricalCrossentropy
from keras.callbacks import EarlyStopping

from tensorflow.keras.optimizers import SGD
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# define the model
#note softmax for multiclass, sigmoid for binary
def GestureClassifier():
    optimizer = SGD()

    model = Sequential()
    model.add(Dense(50, input_dim=60, activation="relu"))
    model.add(Dense(50, activation="relu"))
    model.add(Dense(4, activation='softmax'))
    # compile the keras model
    #'categorical_crossentropy'
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=['categorical_accuracy'])
    return model

#load dataset
df = pd.read_csv("../training-data/dataset/dataset_multiclass_60f.csv",dtype=np.float32)

dataset = df.to_numpy()
#all rows, -1 cols
X = dataset[:,0:60]
print(X[1:5])
#all rows, last 4 cols
Y = dataset[:,-4:]
print(Y [1:5])

#set up test train split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size=0.2,random_state=42)

#create model
model = GestureClassifier()

#set up early stopping callback
callback = EarlyStopping(
    monitor="val_loss",
    min_delta=0,
    patience=0,
    verbose=0,
    mode="auto",
    baseline=None,
    restore_best_weights=True,
)

#fit model - look up a good number of epochs and batches
model.fit(X_train, Y_train, epochs=100, batch_size=10,validation_data=(X_test, Y_test), callbacks=[callback])

# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")
results = model.evaluate(X_test, Y_test, batch_size=10)
print("test loss, test acc:", results)

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`
print("Generate predictions for 3 samples")
predictions = model.predict(X_test[:3])
print("predictions shape:", predictions.shape)

#show summary and save model
model.summary()
model.save(filepath='../model/60-input/model.h5',)

