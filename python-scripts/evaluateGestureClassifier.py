import os
#manually add dll directories because they can't be found in system path
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
os.add_dll_directory("C:/tools/cuda/bin")

from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
import numpy as np
import pandas as pd

# Load in the model
model = load_model('../model/gestureClassifier/v13/model.h5')

# Show the model architecture
model.summary()

#load dataset
df = pd.read_csv("../test-data/dataset/test_dataset_multiclass0.csv",dtype=np.float32)
dataset = df.to_numpy()
#all rows, -1 cols
X = dataset[:,0:24]
#all rows, last 4 cols
Y = dataset[:,-4:]
print(Y)


# Evaluate the model
loss, acc = model.evaluate(X, Y, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(100 * acc))