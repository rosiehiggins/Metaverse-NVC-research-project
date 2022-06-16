import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from createDataset import lm_array_landmarklist
import gestureHeuristics as gh

#load test set
df = pd.read_csv("../test-data/dataset/raw_testset.csv")

dataset = df.to_numpy()
#all rows, -1 cols
X_true = dataset[:,0:64]

#all rows, last 4 cols
Y_true = dataset[:,-1]

Y_pred = []

#initialise gesture heuristics class
gestureHeuristics = gh.GestureHeuristics()

#iterate over x and get predictions
i= 0
for hand in X_true:
    landmarks = lm_array_landmarklist(hand[:-1])
    handedness = hand[-1]
    prediction = gestureHeuristics.predict(landmarks,handedness,True)   
    Y_pred.append(prediction)
    i+=1

Y_pred = np.array(Y_pred)

#generate confusion matrix with Y true and Y pred
cm = confusion_matrix(Y_true, Y_pred,labels = ["raise-hand","thumbs-up","ok","non-gesture"])

#classification report
metrics = classification_report(Y_true, Y_pred, digits=3)
print(metrics)

cm_df = pd.DataFrame(cm,
                     index = ["raise-hand","thumbs-up","ok","non-gesture"], 
                     columns = ["raise-hand","thumbs-up","ok","non-gesture"])
                    
print(cm_df)

cm_df.to_csv("../results/heuristic-results/confusion_matrix_static.csv")