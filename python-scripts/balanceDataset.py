from createDataset import balance_dataset_by_min
import numpy as np
import pandas as pd


#import dataset
df = pd.read_csv("../training-data/dataset/dataset_multiclass_features2.csv")



#balance by min
sample = balance_dataset_by_min(df)

sample = sample.sample(frac = 1)

sample = sample.drop('class', 1)

#save dataset
if sample is not None:
    sample.to_csv("../training-data/dataset/dataset_multiclass_features2.csv",index=False)

