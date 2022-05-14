#first attempt at multi-class classifier. Thumbs up and Raise hand

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
    loss = CategoricalCrossentropy(from_logits=True)
    optimizer = Adam(learning_rate=0.00001)

    model = Sequential()
    model.add(Dense(50, input_dim=24, activation="relu"))
    model.add(Dense(50, activation="relu"))
    model.add(Dense(3, activation='softmax'))
    # compile the keras model
    #'categorical_crossentropy'
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=['categorical_accuracy'])
    return model

#load dataset
df = pd.read_csv("../training-data/dataset/dataset_multiclass_features1_test.csv",dtype=np.float32)
dataset = df.to_numpy()
#all rows, -1 cols
X = dataset[:,0:24]
print(X[1:5])
#all rows, last 3 cols
y = dataset[:,-3:]
print(y[1:5])

#Note may load in separate test set here and train on whole dataset
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.1,random_state=42)

#create model
model = GestureClassifier()

#fit model - look up a good number of epochs and batches
model.fit(X_train, y_train, epochs=30, batch_size=10,validation_data=(X_test, y_test))

# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")
results = model.evaluate(X_test, y_test, batch_size=10)
print("test loss, test acc:", results)

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`
print("Generate predictions for 3 samples")
predictions = model.predict(X_test[:3])
print("predictions shape:", predictions.shape)


model.summary()
model.save(filepath='../model/gestureClassifierV1/v10/model.h5',)