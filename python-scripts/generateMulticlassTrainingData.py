from createDataset import map_file_to_ranges
from createDataset import get_data_from_images
from createDataset import get_data
import numpy as np
import pandas as pd

#
#build data set from data
#
dataset = []

#
#OK
#

#get frame ranges
ok_frame_ranges = map_file_to_ranges(pathname="../training-data/oks.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
ok_data = get_data("../training-videos/ok",ok_frame_ranges,[0,1])
print("raise hand video")
print(len(ok_data))

#img data from public dataset
raul_ok_data = get_data_from_images("../training-images/raul/ok","Left",0.5,[0,1])
print("ok raul")
print(len(raul_ok_data))

samira_ok_data = get_data_from_images("../training-images/samira/ok","Left",0.5,[0,1])
print("ok samira")
print(len(samira_ok_data))


#
#raise hand
#

#img data from public dataset
# raul_rh_data = get_data_from_images("../training-images/raul/raise-hand","Left",0.5,[0,1,0])
# print("raise hand raul")
# print(len(raul_rh_data))

# samira_rh_data = get_data_from_images("../training-images/samira/raise-hand","Left",0.5,[0,1,0])
# print("raise hand samira")
# print(len(samira_rh_data))

# #get frame ranges
# rh_frame_ranges = map_file_to_ranges(pathname="../training-data/raisehand.csv",indexcol="file",\
#                                 usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
# rh_data = get_data("../training-videos/raise-hand",rh_frame_ranges,[0,1,0])
# print("raise hand video")
# print(len(rh_data))


#
#thumbs up
#
#get frame ranges
frame_ranges = map_file_to_ranges(pathname="../training-data/thumbsups.csv",indexcol="file",\
                                usecols=["file","thumbsupstart","thumbsupstop","hand"],dtype={'thumbsupstart': int, 'thumbsupstop': int,'hand':str})
thumbsup_data = get_data("../training-videos/thumbs-up",frame_ranges,[1,0])
print("thumbs up")
print(len(thumbsup_data))



#
#non gestures
#
#get frame ranges
frame_ranges_ng = map_file_to_ranges(pathname="../training-data/nongestures.csv",indexcol="file",\
                                usecols=["file","nonstart","nonstop","hand"],dtype={'nonstart': int, 'nonstop': int,'hand':str})
nongesture_data = get_data("../training-videos/non-gesture",frame_ranges_ng,[0,0])
print("non gesture")
print(len(nongesture_data))

dataset = [*raul_ok_data, *samira_ok_data,*ok_data,*thumbsup_data,*nongesture_data] 

#
#save dataset to csv
#
if len(dataset)>0:
    dataset_df = pd.DataFrame(dataset)
    dataset_df.to_csv("../training-data/dataset/dataset_multiclass1.csv",index=False)