from createDataset import map_file_to_ranges
from createDataset import get_data
import numpy as np
import pandas as pd

#
#build data set from data
#
dataset = []

#
#thumbs up
frame_ranges = map_file_to_ranges(pathname="../training-data/thumbsups.csv",indexcol="file",\
                                usecols=["file","thumbsupstart","thumbsupstop","hand"],dtype={'thumbsupstart': int, 'thumbsupstop': int,'hand':str})
thumbsup_data = get_data("../training-videos/thumbs-up",frame_ranges,1)
thumbs_data_df = pd.DataFrame(thumbsup_data)
print("thumbs up")
print(len(thumbsup_data))

#non gestures
#get frame ranges
frame_ranges_ng = map_file_to_ranges(pathname="../training-data/nongestures.csv",indexcol="file",\
                                usecols=["file","nonstart","nonstop","hand"],dtype={'nonstart': int, 'nonstop': int,'hand':str})
nongesture_data = get_data("../training-videos/non-gesture",frame_ranges_ng,0)
print("non gesture")
print(len(nongesture_data))

#balance non gesture data
#remove_n = len(nongesture_data) - len(thumbsup_data)
non_gest_df = pd.DataFrame(nongesture_data)
#drop_indices = np.random.choice(non_gest_df.index, remove_n, replace=False)

#nongest_sample = non_gest_df.drop(drop_indices)

#print("sample")
#print(len(nongest_sample.index))

# dataset = [*thumbsup_data, *nongesture_data] 
dataset = pd.concat([thumbs_data_df,non_gest_df], ignore_index=True)

#save data set to csv
if len(dataset)>0:
    dataset_df = pd.DataFrame(dataset)
    dataset_df.to_csv("../training-data/dataset/dataset_norm1.csv",index=False)