import os
#manually add dll directories because they can't be found in system path
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
os.add_dll_directory("C:/tools/cuda/bin")

from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
import numpy as np
import pandas as pd
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from createDataset import lm_array_landmarklist

def createConfusionMatrix(filepath,model,numfeatures):
    df = pd.read_csv(filepath,dtype=np.float32,encoding="utf-8")
    dataset = df.to_numpy()
    #all rows, -1 cols
    X = dataset[:,0:numfeatures]
    #all rows, last 4 cols
    Y = dataset[:,-4:]
    #Generate same test set as used in training
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size=0.2,random_state=42)
    #predict some values
    Y_pred = model.predict(X_test)
    #generate confusion matrix with Y test and Y pred
    #use arg max to get prediction
    cm = confusion_matrix(Y_test.argmax(axis=1), Y_pred.argmax(axis=1))

    #classification report
    #use arg max to get prediction
    metrics = classification_report(Y_test.argmax(axis=1), Y_pred.argmax(axis=1), digits=3)
    print(metrics)

    cm_df = pd.DataFrame(cm,
                        index = ["thumbs-up","raise-hand","ok","non-gesture"], 
                        columns = ["thumbs-up","raise-hand","ok","non-gesture"])
    print(cm_df)
    return cm_df

#23 features
model0 = load_model("../model/gestureClassifier/v24/model.h5")
#60 features
model1 = load_model("../model/gestureClassifier/v25/model.h5")

print("23 feature results")

cm_df_23 = createConfusionMatrix("../training-data/dataset/dataset_multiclass_23f.csv",model0,23)

cm_df_23.to_csv("../results/neuralnetwork-results/confusion_matrix_23.csv")

print("60 feature results")

cm_df_60 = createConfusionMatrix("../training-data/dataset/dataset_multiclass_60f.csv",model1,60)

cm_df_60.to_csv("../results/neuralnetwork-results/confusion_matrix_60.csv")


