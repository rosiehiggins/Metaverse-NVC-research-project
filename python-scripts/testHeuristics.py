import numpy as np
import pandas as pd
from sklearn.metrics import multilabel_confusion_matrix
from createDataset import lm_array_landmarklist
from gestureHeuristics import predict

#load test set
df = pd.read_csv("../test-data/dataset/heuristics_testset.csv",dtype=np.float32)

dataset = df.to_numpy()
#all rows, -1 cols
X_true = dataset[:,0:63]

#all rows, last 4 cols
Y_true = dataset[:,-4:]

Y_pred = []
#iterate over x and get predictions
i= 0
for hand in X_true:
    landmarks = lm_array_landmarklist(hand)
    print(i)
    prediction = predict(landmarks,"Left")   
    Y_pred.append(prediction)
    i+=1

Y_pred = np.array(Y_pred)
#generate confusion matrix with Y true and Y pred

cm = multilabel_confusion_matrix(Y_true, Y_pred)
print(cm)



