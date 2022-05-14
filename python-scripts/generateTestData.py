#functions for creating dataset from images and videos
from createDataset import get_data_from_images
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
#get data from https://sites.google.com/view/handgesturedb/home
alberto_thumbsup_data = get_data_from_images("../test-images/alberto/thumbs-up","Left",0,1)
print("alberto thumbs up")
print(len(alberto_thumbsup_data))

susana_thumbsup_data = get_data_from_images("../test-images/susana/thumbs-up","Left",0,1)
print("susana thumbs up")
print(len(susana_thumbsup_data))

lorena_thumbsup_data = get_data_from_images("../test-images/lorena/thumbs-up","Left",0,1)
print("lorena thumbs up")
print(len(lorena_thumbsup_data))

#
#Non gesture
#get frame ranges
frame_ranges_ng = map_file_to_ranges(pathname="../test-data/nongestures_test.csv",indexcol="file",\
                                usecols=["file","nonstart","nonstop","hand"],dtype={'nonstart': int, 'nonstop': int,'hand':str})

print(frame_ranges_ng)
#get data from video
nongesture_data = get_data("../test-videos/nongesture",frame_ranges_ng,0)
print("non gesture")
print(len(nongesture_data))

#concatenate all lists into a dataset
dataset = [*alberto_thumbsup_data, *susana_thumbsup_data, *lorena_thumbsup_data, *nongesture_data] 

#save dataset to csv
if len(dataset)>0:
    dataset_df = pd.DataFrame(dataset)
    dataset_df.to_csv("../test-data/dataset/test_dataset_norm1.csv",index=False)