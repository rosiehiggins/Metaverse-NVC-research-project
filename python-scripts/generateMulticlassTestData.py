#functions for creating dataset from images and videos
from createDataset import get_feature_data_from_images
from createDataset import map_file_to_ranges
from createDataset import get_feature_data

import numpy as np
import pandas as pd

#
#build data set from data
#
dataset = []

#
#thumbs up
#get data from https://sites.google.com/view/handgesturedb/home
alberto_thumbsup_data = get_feature_data_from_images("../test-images/alberto/thumbs-up","Left",0.5,[1,0,0,0])
print("alberto thumbs up")
print(len(alberto_thumbsup_data))

susana_thumbsup_data = get_feature_data_from_images("../test-images/susana/thumbs-up","Left",0.5,[1,0,0,0])
print("susana thumbs up")
print(len(susana_thumbsup_data))

lorena_thumbsup_data = get_feature_data_from_images("../test-images/lorena/thumbs-up","Left",0.5,[1,0,0,0])
print("lorena thumbs up")
print(len(lorena_thumbsup_data))

#
#raise hand
#get data from https://sites.google.com/view/handgesturedb/home
alberto_rh_data = get_feature_data_from_images("../test-images/alberto/raise-hand","Left",0.5,[0,1,0,0])
print("alberto raise hand")
print(len(alberto_rh_data))

susana_rh_data = get_feature_data_from_images("../test-images/susana/raise-hand","Left",0.5,[0,1,0,0])
print("susana raise hand")
print(len(susana_rh_data))

lorena_rh_data = get_feature_data_from_images("../test-images/lorena/raise-hand","Left",0.5,[0,1,0,0])
print("lorena raise hand")
print(len(lorena_rh_data))

#
#ok
#get data from https://sites.google.com/view/handgesturedb/home
alberto_ok_data = get_feature_data_from_images("../test-images/alberto/ok","Left",0.5,[0,0,1,0])
print("alberto ok")
print(len(alberto_ok_data))

susana_ok_data = get_feature_data_from_images("../test-images/susana/ok","Left",0.5,[0,0,1,0])
print("susana ok")
print(len(susana_ok_data))

lorena_ok_data = get_feature_data_from_images("../test-images/lorena/ok","Left",0.5,[0,0,1,0])
print("lorena ok")
print(len(lorena_ok_data))



#
#Non gesture
#get frame ranges
frame_ranges_ng = map_file_to_ranges(pathname="../test-data/nongestures_test.csv",indexcol="file",\
                                usecols=["file","nonstart","nonstop","hand"],dtype={'nonstart': int, 'nonstop': int,'hand':str})

print(frame_ranges_ng)
#get data from video
nongesture_data = get_feature_data("../test-videos/nongesture",frame_ranges_ng,[0,0,0,1])
print("non gesture")
print(len(nongesture_data))

#concatenate all lists into a dataset
dataset = [*alberto_thumbsup_data, *susana_thumbsup_data, *lorena_thumbsup_data,\
            *alberto_rh_data, *susana_rh_data, *lorena_rh_data,\
            *alberto_ok_data, *susana_ok_data, *lorena_ok_data,\
             *nongesture_data] 

#save dataset to csv
if len(dataset)>0:
    dataset_df = pd.DataFrame(dataset)
    dataset_df.to_csv("../test-data/dataset/test_dataset_multiclass0.csv",index=False)