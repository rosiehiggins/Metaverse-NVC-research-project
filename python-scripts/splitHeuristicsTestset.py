
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd



df = pd.read_csv("../training-data/dataset/dataset_multiclass_raw.csv",encoding="utf-8")
#print(df.head())
dataset = df.to_numpy()
#all rows, -1 cols
X = dataset[:,0:64]
#all rows, last 4 cols
Y = dataset[:,-1:]

#Generate same test set as used in training
X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size=0.2,random_state=42)

testset = pd.DataFrame(X_test)
testset = testset.assign(col_name= Y_test)
#print(Y_test.shape)
print(testset.head())

testset.to_csv("../test-data/dataset/raw_testset.csv",index=False)