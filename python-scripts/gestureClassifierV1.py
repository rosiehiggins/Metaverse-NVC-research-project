#Basic version binary classifier, 80/20/test split
#trained v00,v01,v02

import os
#manually add dll directories because they can't be found in system path
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
os.add_dll_directory("C:/tools/cuda/bin")

from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# define the model
#note softmax for multiclass, sigmoid for binary
def GestureClassifier():
    model = Sequential()
    model.add(Dense(50, input_dim=63, activation='relu'))
    model.add(Dense(50, input_dim=63, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # compile the keras model
    #different loss for multiple categories
    #TODO look up how to get precision and recall in
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

#load dataset
df = pd.read_csv("../training-data/dataset/dataset.csv",dtype=np.float32)
dataset = df.to_numpy()
#all rows, -1 cols
X = dataset[:,0:63]
#all rows, last col
y = dataset[:,-1]

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=42)

#create model
model = GestureClassifier()

#fit model - look up a good number of epochs and batches
model.fit(X_train, y_train, epochs=150, batch_size=10,validation_data=(X_test, y_test))

# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")
results = model.evaluate(X_test, y_test, batch_size=128)
print("test loss, test acc:", results)

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`
print("Generate predictions for 3 samples")
predictions = model.predict(X_test[:3])
print("predictions shape:", predictions.shape)

#evaluate
#_, accuracy = model.evaluate(X, y)
#print('Accuracy: %.2f' % (accuracy*100))

model.summary()
model.save(filepath='../model/gestureClassifier/v02/model.h5',)