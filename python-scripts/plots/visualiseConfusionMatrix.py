import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#load in cm
# heuristics table
#cm_df = pd.read_csv("../../results/heuristic-results/confusion_matrix.csv",index_col=0,dtype= {"thumbs-up": np.int32, "raise-hand": np.int32, "ok": np.int32,"non-gesture": np.int32})
#neural network table - feature set
cm_df = pd.read_csv("../../results/neuralnetwork-results/confusion_matrix_23.csv",index_col=0,dtype= {"thumbs-up": np.int32, "raise-hand": np.int32, "ok": np.int32,"non-gesture": np.int32})

print(cm_df)

#Plotting the confusion matrix
plt.figure(figsize=(5,4))
sns.heatmap(cm_df, annot=True, fmt='g')
plt.title('Static gestures 23 features')
plt.ylabel('Actual Values')
plt.xlabel('Predicted Values')
plt.show()


cm_df = pd.read_csv("../../results/neuralnetwork-results/confusion_matrix_60.csv",index_col=0,dtype= {"thumbs-up": np.int32, "raise-hand": np.int32, "ok": np.int32,"non-gesture": np.int32})

print(cm_df)

#Plotting the confusion matrix
plt.figure(figsize=(5,4))
sns.heatmap(cm_df, annot=True, fmt='g')
plt.title('Static gestures 60 features')
plt.ylabel('Actual Values')
plt.xlabel('Predicted Values')
plt.show()