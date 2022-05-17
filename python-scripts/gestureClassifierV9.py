#multi class, experimented with further reduced feature set 
#excluded thumb direction to try and remove raise hand tuhmb direction bias - and generally see if it's needed

import os
#manually add dll directories because they can't be found in system path
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
os.add_dll_directory("C:/tools/cuda/bin")

from keras.models import Sequential
from keras.layers import Dense
from keras.losses import CategoricalCrossentropy
from keras.callbacks import EarlyStopping

from tensorflow.keras.optimizers import Adam
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# define the model
#note softmax for multiclass, sigmoid for binary
def GestureClassifier():
    optimizer = Adam(learning_rate=0.00001)

    model = Sequential()
    model.add(Dense(50, input_dim=21, activation="relu"))
    model.add(Dense(50, activation="relu"))
    model.add(Dense(4, activation='softmax'))
    # compile the keras model
    #'categorical_crossentropy'
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=['categorical_accuracy'])
    return model

#load dataset
df = pd.read_csv("../training-data/dataset/dataset_multiclass_features6.csv",dtype=np.float32)

train_dataset = df.to_numpy()
#all rows, -1 cols
X_train = train_dataset[:,0:21]
print(X_train[1:5])
#all rows, last 4 cols
Y_train = train_dataset[:,-4:]
print(Y_train[1:5])

#load testset
t_df = pd.read_csv("../test-data/dataset/test_dataset_multiclass1.csv",dtype=np.float32)

test_dataset = t_df.to_numpy()
#all rows, -1 cols
X_test = test_dataset[:,0:21]
print(X_test[1:5])
#all rows, last 4 cols
Y_test = test_dataset[:,-4:]
print(Y_test[1:5])

#create model
model = GestureClassifier()

#set up early stopping callback
callback = EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0011)

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


model.summary()
model.save(filepath='../model/gestureClassifier/v16/model.h5',)