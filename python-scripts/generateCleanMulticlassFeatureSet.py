from createDataset import map_file_to_ranges
from createDataset import get_feature_data_from_images
from createDataset import get_feature_data
import numpy as np
import pandas as pd

list_test = [1,2,3,\
            4,5,6,\
            7,8,9]

print(list_test)
#
#build data set from data
#
dataset = []

#
#raise hand
#

#get frame ranges
rh_frame_ranges = map_file_to_ranges(pathname="../training-data/subset/raisehand.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
rh_data = get_feature_data("../training-videos/raise-hand",rh_frame_ranges,[0,1,0])
print("raise hand video")
print(len(rh_data))

#img data from public dataset
raul_rh_data = get_feature_data_from_images("../training-images/raul/raise-hand","Left",0.5,[0,1,0])
print("raise hand raul")
print(len(raul_rh_data))

samira_rh_data = get_feature_data_from_images("../training-images/samira/raise-hand","Left",0.5,[0,1,0])
print("raise hand samira")
print(len(samira_rh_data))

alfredo_rh_data = get_feature_data_from_images("../training-images/alfredo/raise-hand","Left",0.5,[0,1,0])
print("raise hand alfredo")
print(len(alfredo_rh_data))

ana_rh_data = get_feature_data_from_images("../training-images/ana/raise-hand","Left",0.5,[0,1,0])
print("raise hand ana")
print(len(ana_rh_data))

ana_m_rh_data = get_feature_data_from_images("../training-images/ana_m/raise-hand","Left",0.5,[0,1,0])
print("raise hand ana m")
print(len(ana_m_rh_data))

arturo_rh_data = get_feature_data_from_images("../training-images/arturo/raise-hand","Left",0.5,[0,1,0])
print("raise hand arturo")
print(len(arturo_rh_data))

carlos_c_rh_data = get_feature_data_from_images("../training-images/carlos_c/raise-hand","Left",0.5,[0,1,0])
print("raise hand carlos c")
print(len(carlos_c_rh_data))

#get frame ranges
rh_frame_ranges = map_file_to_ranges(pathname="../training-data/subset/raisehand.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
rh_data = get_feature_data("../training-videos/raise-hand",rh_frame_ranges,[0,1,0])
print("raise hand video")
print(len(rh_data))


#
#thumbs up
#
#get frame ranges
frame_ranges = map_file_to_ranges(pathname="../training-data/subset/thumbsups.csv",indexcol="file",\
                                usecols=["file","thumbsupstart","thumbsupstop","hand"],dtype={'thumbsupstart': int, 'thumbsupstop': int,'hand':str})
thumbsup_data = get_feature_data("../training-videos/thumbs-up",frame_ranges,[1,0,0])

print("thumbs up video")
print(len(thumbsup_data))

#img data from public dataset
raul_tu_data = get_feature_data_from_images("../training-images/raul/thumbs-up","Left",0.5,[1,0,0])
print("thumbs up raul")
print(len(raul_tu_data))

samira_tu_data = get_feature_data_from_images("../training-images/samira/thumbs-up","Left",0.5,[1,0,0])
print("thumbs up samira")
print(len(samira_tu_data))

alfredo_tu_data = get_feature_data_from_images("../training-images/alfredo/thumbs-up","Left",0.5,[1,0,0])
print("thumbs up alfredo")
print(len(alfredo_tu_data))

ana_tu_data = get_feature_data_from_images("../training-images/ana/thumbs-up","Left",0.5,[1,0,0])
print("thumbs up ana")
print(len(ana_tu_data))

ana_m_tu_data = get_feature_data_from_images("../training-images/ana_m/thumbs-up","Left",0.5,[1,0,0])
print("thumbs up ana m")
print(len(ana_m_tu_data))

arturo_tu_data = get_feature_data_from_images("../training-images/arturo/thumbs-up","Left",0.5,[1,0,0])
print("thumbs-up arturo")
print(len(arturo_tu_data))

carlos_c_tu_data = get_feature_data_from_images("../training-images/carlos_c/thumbs-up","Left",0.5,[1,0,0])
print("thumbs-up carlos c")
print(len(carlos_c_tu_data))




# #balance thumbs up by randomly removing some
# remove_n = len(thumbsup_data) - len(rh_data)
# thumbsup_df = pd.DataFrame(thumbsup_data)
# drop_indices = np.random.choice(thumbsup_df.index, remove_n, replace=False)
# thumbsup_sample = thumbsup_df.drop(drop_indices)

# print("thumbs up")
# print(len(thumbsup_sample.index))

#
#OK
#

#get frame ranges
ok_frame_ranges = map_file_to_ranges(pathname="../training-data/oks.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
ok_data = get_feature_data("../training-videos/subset/ok",ok_frame_ranges,[0,0,1])
print("ok video")
print(len(ok_data))

#img data from public dataset
raul_ok_data = get_feature_data_from_images("../training-images/raul/ok","Left",0.5,[0,0,1])
print("ok raul")
print(len(raul_ok_data))

samira_ok_data = get_feature_data_from_images("../training-images/samira/ok","Left",0.5,[0,0,1])
print("ok samira")
print(len(samira_ok_data))

alfredo_ok_data = get_feature_data_from_images("../training-images/alfredo/ok","Left",0.5,[0,0,1])
print("ok alfredo")
print(len(alfredo_ok_data))

ana_ok_data = get_feature_data_from_images("../training-images/ana/ok","Left",0.5,[0,0,1])
print("ok ana")
print(len(ana_ok_data))

ana_m_ok_data = get_feature_data_from_images("../training-images/ana_m/ok","Left",0.5,[0,0,1])
print("ok ana m")
print(len(ana_m_ok_data))

arturo_ok_data = get_feature_data_from_images("../training-images/arturo/ok","Left",0.5,[0,0,1])
print("ok arturo")
print(len(arturo_ok_data))

carlos_c_ok_data = get_feature_data_from_images("../training-images/carlos_c/ok","Left",0.5,[0,0,1])
print("ok carlos c")
print(len(carlos_c_ok_data))



dataset = [*raul_ok_data, *samira_ok_data,*ok_data, *alfredo_ok_data, *ana_ok_data, *ana_m_ok_data, *arturo_ok_data, *carlos_c_ok_data,\
            *raul_rh_data,*rh_data,*samira_rh_data, *alfredo_rh_data, *ana_rh_data,*ana_m_rh_data, *arturo_rh_data, *carlos_c_rh_data,\
            *thumbsup_data, *raul_tu_data,*samira_tu_data,*alfredo_tu_data,*ana_tu_data,*ana_m_tu_data,*arturo_tu_data,*carlos_c_tu_data] 

#
#save dataset to csv
#
dataset_df = pd.DataFrame(dataset)
dataset_df.sample(frac = 1)

dataset_df.to_csv("../training-data/dataset/dataset_multiclass_features2.csv",index=False)