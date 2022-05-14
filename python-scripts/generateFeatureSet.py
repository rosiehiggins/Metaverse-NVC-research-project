from createDataset import map_file_to_ranges
from createDataset import get_feature_data_from_images
from createDataset import get_feature_data
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
thumbsup_data = get_feature_data("../training-videos/thumbs-up",frame_ranges,1)
thumbs_data_df = pd.DataFrame(thumbsup_data)
print("thumbs up")
print(len(thumbsup_data))

#non gestures
#get frame ranges
frame_ranges_ng = map_file_to_ranges(pathname="../training-data/nongestures.csv",indexcol="file",\
                                usecols=["file","nonstart","nonstop","hand"],dtype={'nonstart': int, 'nonstop': int,'hand':str})
nongesture_data = get_feature_data("../training-videos/non-gesture",frame_ranges_ng,0)
print("non gesture")
print(len(nongesture_data))

dataset = [*thumbsup_data, *nongesture_data] 

#save data set to csv
if len(dataset)>0:
    dataset_df = pd.DataFrame(dataset)
    dataset_df.to_csv("../training-data/dataset/dataset_features0.csv",index=False)
