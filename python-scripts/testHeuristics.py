import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from createDataset import lm_array_landmarklist
from gestureHeuristics import predict

#load test set
df = pd.read_csv("../test-data/dataset/heuristics_testset.csv")

dataset = df.to_numpy()
#all rows, -1 cols
X_true = dataset[:,0:63]

#all rows, last 4 cols
Y_true = dataset[:,-1]

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
cm = confusion_matrix(Y_true, Y_pred,labels = ["raise-hand","thumbs-up","ok","non-gesture"])

#classification report
metrics = classification_report(Y_true, Y_pred, digits=3)
print(metrics)

cm_df = pd.DataFrame(cm,
                     index = ["raise-hand","thumbs-up","ok","non-gesture"], 
                     columns = ["raise-hand","thumbs-up","ok","non-gesture"])
                    
print(cm_df)

cm_df.to_csv("../results/heuristic-results/confusion_matrix.csv")