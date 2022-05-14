#multi class, nons added a separate class, balanced shuffled dataset

import os
#manually add dll directories because they can't be found in system path
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
os.add_dll_directory("C:/tools/cuda/bin")

from keras.models import Sequential
from keras.layers import Dense
from keras.losses import CategoricalCrossentropy
from tensorflow.keras.optimizers import Adam
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# define the model
#note softmax for multiclass, sigmoid for binary
def GestureClassifier():
    optimizer = Adam(learning_rate=0.00001)

    model = Sequential()
    model.add(Dense(50, input_dim=24, activation="relu"))
    model.add(Dense(50, activation="relu"))
    model.add(Dense(4, activation='softmax'))
    # compile the keras model
    #'categorical_crossentropy'
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=['categorical_accuracy'])
    return model

#load dataset
df = pd.read_csv("../training-data/dataset/dataset_multiclass_features3.csv",dtype=np.float32)

dataset = df.to_numpy()
#all rows, -1 cols
X = dataset[:,0:24]
print(X[1:5])
#all rows, last 4 cols
Y = dataset[:,-4:]
print(Y[1:5])

#Note may load in separate test set here and train on whole dataset
X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size=0.1,random_state=42)

#create model
model = GestureClassifier()

#fit model - look up a good number of epochs and batches
model.fit(X_train, Y_train, epochs=30, batch_size=10,validation_data=(X_test, Y_test))

# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")
results = model.evaluate(X_test, Y_test, batch_size=10)
print("test loss, test acc:", results)

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`
print("Generate predictions for 3 samples")
predictions = model.predict(X_test[:3])
print("predictions shape:", predictions.shape)


model.summary()
model.save(filepath='../model/gestureClassifier/v13/model.h5',)