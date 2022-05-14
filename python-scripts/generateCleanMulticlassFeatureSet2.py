from createDataset import balance_dataset_by_min
from createDataset import map_file_to_ranges
from createDataset import get_feature_data_from_images
from createDataset import get_feature_data
from createDataset import balance_dataset_by_min
import numpy as np
import pandas as pd


#
#build data set from data
#
dataset = []

#
#non gestures
#
#get frame ranges
frame_ranges_ng = map_file_to_ranges(pathname="../training-data/nongestures.csv",indexcol="file",\
                                usecols=["file","nonstart","nonstop","hand"],dtype={'nonstart': int, 'nonstop': int,'hand':str})
nongesture_data = get_feature_data("../training-videos/non-gesture",frame_ranges_ng,[0,0,0,1],"nongesture")
print("non gesture")
print(len(nongesture_data))

ng_df = pd.DataFrame(nongesture_data, columns=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','class'])
print(ng_df.head())
#
#raise hand
#

#get frame ranges
rh_frame_ranges = map_file_to_ranges(pathname="../training-data/subset/raisehand.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
rh_data = get_feature_data("../training-videos/raise-hand",rh_frame_ranges,[0,1,0,0],"raisehand")
print("raise hand video")
print(len(rh_data))

#img data from public dataset
raul_rh_data = get_feature_data_from_images("../training-images/raul/raise-hand","Left",0.5,[0,1,0,0],"raisehand")
print("raise hand raul")
print(len(raul_rh_data))

samira_rh_data = get_feature_data_from_images("../training-images/samira/raise-hand","Left",0.5,[0,1,0,0],"raisehand")
print("raise hand samira")
print(len(samira_rh_data))

alfredo_rh_data = get_feature_data_from_images("../training-images/alfredo/raise-hand","Left",0.5,[0,1,0,0],"raisehand")
print("raise hand alfredo")
print(len(alfredo_rh_data))

ana_rh_data = get_feature_data_from_images("../training-images/ana/raise-hand","Left",0.5,[0,1,0,0],"raisehand")
print("raise hand ana")
print(len(ana_rh_data))

ana_m_rh_data = get_feature_data_from_images("../training-images/ana_m/raise-hand","Left",0.5,[0,1,0,0],"raisehand")
print("raise hand ana m")
print(len(ana_m_rh_data))

arturo_rh_data = get_feature_data_from_images("../training-images/arturo/raise-hand","Left",0.5,[0,1,0,0],"raisehand")
print("raise hand arturo")
print(len(arturo_rh_data))

carlos_c_rh_data = get_feature_data_from_images("../training-images/carlos_c/raise-hand","Left",0.5,[0,1,0,0],"raisehand")
print("raise hand carlos c")
print(len(carlos_c_rh_data))


#
#thumbs up
#
#get frame ranges
frame_ranges = map_file_to_ranges(pathname="../training-data/subset/thumbsups.csv",indexcol="file",\
                                usecols=["file","thumbsupstart","thumbsupstop","hand"],dtype={'thumbsupstart': int, 'thumbsupstop': int,'hand':str})
thumbsup_data = get_feature_data("../training-videos/thumbs-up",frame_ranges,[1,0,0,0],"thumbsup")

print("thumbs up video")
print(len(thumbsup_data))

#img data from public dataset
raul_tu_data = get_feature_data_from_images("../training-images/raul/thumbs-up","Left",0.5,[1,0,0,0],"thumbsup")
print("thumbs up raul")
print(len(raul_tu_data))

samira_tu_data = get_feature_data_from_images("../training-images/samira/thumbs-up","Left",0.5,[1,0,0,0],"thumbsup")
print("thumbs up samira")
print(len(samira_tu_data))

alfredo_tu_data = get_feature_data_from_images("../training-images/alfredo/thumbs-up","Left",0.5,[1,0,0,0],"thumbsup")
print("thumbs up alfredo")
print(len(alfredo_tu_data))

ana_tu_data = get_feature_data_from_images("../training-images/ana/thumbs-up","Left",0.5,[1,0,0,0],"thumbsup")
print("thumbs up ana")
print(len(ana_tu_data))

ana_m_tu_data = get_feature_data_from_images("../training-images/ana_m/thumbs-up","Left",0.5,[1,0,0,0],"thumbsup")
print("thumbs up ana m")
print(len(ana_m_tu_data))

arturo_tu_data = get_feature_data_from_images("../training-images/arturo/thumbs-up","Left",0.5,[1,0,0,0],"thumbsup")
print("thumbs-up arturo")
print(len(arturo_tu_data))

carlos_c_tu_data = get_feature_data_from_images("../training-images/carlos_c/thumbs-up","Left",0.5,[1,0,0,0],"thumbsup")
print("thumbs-up carlos c")
print(len(carlos_c_tu_data))


#
#OK
#

#get frame ranges
ok_frame_ranges = map_file_to_ranges(pathname="../training-data/subset/oks.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
ok_data = get_feature_data("../training-videos/ok",ok_frame_ranges,[0,0,1,0],"ok")
print("ok video")
print(len(ok_data))

#img data from public dataset
raul_ok_data = get_feature_data_from_images("../training-images/raul/ok","Left",0.5,[0,0,1,0],"ok")
print("ok raul")
print(len(raul_ok_data))

samira_ok_data = get_feature_data_from_images("../training-images/samira/ok","Left",0.5,[0,0,1,0],"ok")
print("ok samira")
print(len(samira_ok_data))

alfredo_ok_data = get_feature_data_from_images("../training-images/alfredo/ok","Left",0.5,[0,0,1,0],"ok")
print("ok alfredo")
print(len(alfredo_ok_data))

ana_ok_data = get_feature_data_from_images("../training-images/ana/ok","Left",0.5,[0,0,1,0],"ok")
print("ok ana")
print(len(ana_ok_data))

ana_m_ok_data = get_feature_data_from_images("../training-images/ana_m/ok","Left",0.5,[0,0,1,0],"ok")
print("ok ana m")
print(len(ana_m_ok_data))

arturo_ok_data = get_feature_data_from_images("../training-images/arturo/ok","Left",0.5,[0,0,1,0],"ok")
print("ok arturo")
print(len(arturo_ok_data))

carlos_c_ok_data = get_feature_data_from_images("../training-images/carlos_c/ok","Left",0.5,[0,0,1,0],"ok")
print("ok carlos c")
print(len(carlos_c_ok_data))




dataset = [*raul_ok_data, *samira_ok_data,*ok_data, *alfredo_ok_data, *ana_ok_data, *ana_m_ok_data, *arturo_ok_data, *carlos_c_ok_data,\
            *raul_rh_data,*rh_data,*samira_rh_data, *alfredo_rh_data, *ana_rh_data,*ana_m_rh_data, *arturo_rh_data, *carlos_c_rh_data,\
            *thumbsup_data, *raul_tu_data,*samira_tu_data,*alfredo_tu_data,*ana_tu_data,*ana_m_tu_data,*arturo_tu_data,*carlos_c_tu_data,\
            *nongesture_data] 

#
#balance and save dataset to csv
#
dataset_df = pd.DataFrame(dataset, columns=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','class'])

#balance
sample = balance_dataset_by_min(dataset_df)

#shuffle and drop class
sample = sample.sample(frac = 1)
sample = sample.drop('class', 1)


sample.to_csv("../training-data/dataset/dataset_multiclass_features3.csv",index=False)