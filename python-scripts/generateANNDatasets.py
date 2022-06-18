from createDataset import balance_dataset_by_min
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
#non gestures
#
#get frame ranges
frame_ranges_ng = map_file_to_ranges(pathname="../training-data/labelled-data/nongestures.csv",indexcol="file",\
                                usecols=["file","nonstart","nonstop","hand"],dtype={'nonstart': int, 'nonstop': int,'hand':str})
nongesture_data, nongesture_data60 = get_feature_data("../training-videos/non-gesture",frame_ranges_ng,[0,0,0,1],"nongesture")
print("non gesture 23")
print(len(nongesture_data))
print("non gesture 60")
print(len(nongesture_data60))

#img data from public dataset
raul_fist_data, raul_fist_data60 = get_feature_data_from_images("../training-images/raul/fist","Left",[0,0,0,1],"nongesture")
print("fist raul 23")
print(len(raul_fist_data))

raquel_non_data, raquel_non_data60 = get_feature_data_from_images("../training-images/raquel/non-gesture","Left",[0,0,0,1],"nongesture")
print("raquel nons 23")
print(len(raquel_non_data))

tomas_non_data, tomas_non_data60 = get_feature_data_from_images("../training-images/tomas/non-gesture","Left",[0,0,0,1],"nongesture")
print("tomas nons 23")
print(len(tomas_non_data))

#
#raise hand
#

#get frame ranges
rh_frame_ranges = map_file_to_ranges(pathname="../training-data/labelled-data/raisehand.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
rh_data, rh_data60 = get_feature_data("../training-videos/raise-hand",rh_frame_ranges,[0,1,0,0],"raisehand")
print("raise hand video 23")
print(len(rh_data))
print("raise hand video 60")
print(len(rh_data60))

#img data from public dataset
raul_rh_data, raul_rh_data60 = get_feature_data_from_images("../training-images/raul/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand raul 23")
print(len(raul_rh_data))
print("raise hand raul 60")
print(len(raul_rh_data60))

samira_rh_data, samira_rh_data60 = get_feature_data_from_images("../training-images/samira/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand samira 23")
print(len(samira_rh_data))
print("raise hand samira 60")
print(len(samira_rh_data60))

arturo_rh_data, arturo_rh_data60 = get_feature_data_from_images("../training-images/arturo/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand arturo 23")
print(len(arturo_rh_data))
print("raise hand arturo 60")
print(len(arturo_rh_data60))

carlos_c_rh_data, carlos_c_rh_data60 = get_feature_data_from_images("../training-images/carlos_c/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand carlos c 23")
print(len(carlos_c_rh_data))
print("raise hand carlos c 60")
print(len(carlos_c_rh_data60))

esther_rh_data, esther_rh_data60 = get_feature_data_from_images("../training-images/esther/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand esther 23")
print(len(esther_rh_data))
print("raise hand esther 60")
print(len(esther_rh_data60))

jesus_rh_data, jesus_rh_data60 = get_feature_data_from_images("../training-images/jesus/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand jesus 23")
print(len(jesus_rh_data))

raquel_rh_data, raquel_rh_data60 = get_feature_data_from_images("../training-images/raquel/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand raquel 23")
print(len(raquel_rh_data))

tomas_rh_data, tomas_rh_data60  = get_feature_data_from_images("../training-images/tomas/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand tomas 23")
print(len(tomas_rh_data))

madr1_rh_data, madr1_rh_data60 = get_feature_data_from_images("../training-images/madrid1/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand madr1 23")
print(len(madr1_rh_data))

madr2_rh_data, madr2_rh_data60 = get_feature_data_from_images("../training-images/madrid2/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand madr2 23")
print(len(madr2_rh_data))

madr3_rh_data, madr3_rh_data60 = get_feature_data_from_images("../training-images/madrid3/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand madr3 23")
print(len(madr3_rh_data))

madr4_rh_data,madr4_rh_data60  = get_feature_data_from_images("../training-images/madrid4/raise-hand","Left",[0,1,0,0],"raisehand")
print("raise hand madr4 23")
print(len(madr4_rh_data))


#
#thumbs up
#
#get frame ranges
frame_ranges = map_file_to_ranges(pathname="../training-data/labelled-data/thumbsups.csv",indexcol="file",\
                                usecols=["file","thumbsupstart","thumbsupstop","hand"],dtype={'thumbsupstart': int, 'thumbsupstop': int,'hand':str})
thumbsup_data, thumbsup_data60  = get_feature_data("../training-videos/thumbs-up",frame_ranges,[1,0,0,0],"thumbsup")

print("thumbs up video 23")
print(len(thumbsup_data))

#img data from public dataset
raul_tu_data, raul_tu_data60  = get_feature_data_from_images("../training-images/raul/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs up raul 23")
print(len(raul_tu_data))

samira_tu_data, samira_tu_data60 = get_feature_data_from_images("../training-images/samira/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs up samira 23")
print(len(samira_tu_data))

alfredo_tu_data, alfredo_tu_data60  = get_feature_data_from_images("../training-images/alfredo/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs up alfredo 23")
print(len(alfredo_tu_data))

ana_tu_data, ana_tu_data60 = get_feature_data_from_images("../training-images/ana/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs up ana 23")
print(len(ana_tu_data))

ana_m_tu_data, ana_m_tu_data60  = get_feature_data_from_images("../training-images/ana_m/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs up ana m 23")
print(len(ana_m_tu_data))

arturo_tu_data, arturo_tu_data60  = get_feature_data_from_images("../training-images/arturo/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs-up arturo 23")
print(len(arturo_tu_data))

carlos_c_tu_data, carlos_c_tu_data60  = get_feature_data_from_images("../training-images/carlos_c/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs-up carlos c 23")
print(len(carlos_c_tu_data))

esther_tu_data, esther_tu_data60  = get_feature_data_from_images("../training-images/esther/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs-up esther 23")
print(len(esther_tu_data))

jesus_tu_data, jesus_tu_data60  = get_feature_data_from_images("../training-images/jesus/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs-up jesus 23")
print(len(jesus_tu_data))

raquel_tu_data, raquel_tu_data60  = get_feature_data_from_images("../training-images/raquel/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs-up raquel 23")
print(len(raquel_tu_data))

tomas_tu_data, tomas_tu_data60  = get_feature_data_from_images("../training-images/tomas/thumbs-up","Left",[1,0,0,0],"thumbsup")
print("thumbs-up tomas 23")
print(len(tomas_tu_data))

#
#OK
#

#get frame ranges
ok_frame_ranges = map_file_to_ranges(pathname="../training-data/labelled-data/oks.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
ok_data, ok_data60 = get_feature_data("../training-videos/ok",ok_frame_ranges,[0,0,1,0],"ok")
print("ok video 23")
print(len(ok_data))

#img data from public dataset
raul_ok_data, raul_ok_data60 = get_feature_data_from_images("../training-images/raul/ok","Left",[0,0,1,0],"ok")
print("ok raul 23")
print(len(raul_ok_data))

samira_ok_data, samira_ok_data60  = get_feature_data_from_images("../training-images/samira/ok","Left",[0,0,1,0],"ok")
print("ok samira 23")
print(len(samira_ok_data))

alfredo_ok_data, alfredo_ok_data60  = get_feature_data_from_images("../training-images/alfredo/ok","Left",[0,0,1,0],"ok")
print("ok alfredo 23")
print(len(alfredo_ok_data))

ana_ok_data, ana_ok_data60 = get_feature_data_from_images("../training-images/ana/ok","Left",[0,0,1,0],"ok")
print("ok ana 23")
print(len(ana_ok_data))

ana_m_ok_data, ana_m_ok_data60 = get_feature_data_from_images("../training-images/ana_m/ok","Left",[0,0,1,0],"ok")
print("ok ana m 23")
print(len(ana_m_ok_data))

arturo_ok_data, arturo_ok_data60  = get_feature_data_from_images("../training-images/arturo/ok","Left",[0,0,1,0],"ok")
print("ok arturo 23")
print(len(arturo_ok_data))

carlos_c_ok_data, carlos_c_ok_data60 = get_feature_data_from_images("../training-images/carlos_c/ok","Left",[0,0,1,0],"ok")
print("ok carlos c 23")
print(len(carlos_c_ok_data))

esther_ok_data, esther_ok_data60  = get_feature_data_from_images("../training-images/esther/ok","Left",[0,0,1,0],"ok")
print("ok esther 23")
print(len(esther_ok_data))

jesus_ok_data, jesus_ok_data60 = get_feature_data_from_images("../training-images/jesus/ok","Left",[0,0,1,0],"ok")
print("ok jesus 23")
print(len(jesus_ok_data))

raquel_ok_data, raquel_ok_data60 = get_feature_data_from_images("../training-images/raquel/ok","Left",[0,0,1,0],"ok")
print("ok raquel")
print(len(raquel_ok_data))

tomas_ok_data, tomas_ok_data60= get_feature_data_from_images("../training-images/tomas/ok","Left",[0,0,1,0],"ok")
print("ok tomas")
print(len(tomas_ok_data))



#
#balance and save dataset to csv
#
#23 features
seed = 29

dataset = [*raul_ok_data, *samira_ok_data, *ok_data, *arturo_ok_data, *alfredo_ok_data, *ana_ok_data, *ana_m_ok_data, *carlos_c_ok_data, *esther_ok_data, *jesus_ok_data, *raquel_ok_data, *tomas_ok_data,\
            *raul_rh_data,*rh_data, *samira_rh_data,  *arturo_rh_data, *carlos_c_rh_data, *esther_rh_data, *jesus_rh_data, *raquel_rh_data, *tomas_rh_data,\
            *madr1_rh_data, *madr2_rh_data, *madr3_rh_data, *madr4_rh_data, \
            *thumbsup_data, *raul_tu_data, *samira_tu_data,*alfredo_tu_data,*ana_tu_data,*ana_m_tu_data,*arturo_tu_data,*carlos_c_tu_data, *esther_tu_data, *jesus_tu_data, *raquel_tu_data, *tomas_tu_data,\
            *nongesture_data, *raul_fist_data, *raquel_non_data, *tomas_non_data] 



columns = [*range(0, 27)]
columns.append("class")
dataset_df = pd.DataFrame(dataset, columns=columns)

#balance
sample = balance_dataset_by_min(dataset_df)

#shuffle and drop class
sample = sample.sample(frac = 1,random_state=29)
sample = sample.drop('class', 1)

#sample.to_csv("../training-data/dataset/dataset_multiclass_23f.csv",index=False)
sample.to_csv("../training-data/dataset/dataset_multiclass_23f_test.csv",index=False)

#
#balance and save dataset to csv
#
#60 features

dataset60 = [*raul_ok_data60, *samira_ok_data60, *ok_data60, *arturo_ok_data60, *alfredo_ok_data60, *ana_ok_data60, *ana_m_ok_data60, *carlos_c_ok_data60, *esther_ok_data60, *jesus_ok_data60, *raquel_ok_data60, *tomas_ok_data60,\
            *raul_rh_data60,*rh_data60, *samira_rh_data60,  *arturo_rh_data60, *carlos_c_rh_data60, *esther_rh_data60, *jesus_rh_data60, *raquel_rh_data60, *tomas_rh_data60,\
            *madr1_rh_data60, *madr2_rh_data60, *madr3_rh_data60, *madr4_rh_data60, \
            *thumbsup_data60, *raul_tu_data60, *samira_tu_data60,*alfredo_tu_data60,*ana_tu_data60,*ana_m_tu_data60,*arturo_tu_data60,*carlos_c_tu_data60, *esther_tu_data60, *jesus_tu_data60, *raquel_tu_data60, *tomas_tu_data60,\
            *nongesture_data60, *raul_fist_data60, *raquel_non_data60, *tomas_non_data60] 


columns60 = [*range(0, 64)]
columns60.append("class")
dataset_df_60 = pd.DataFrame(dataset60, columns=columns60)

#balance
sample60 = balance_dataset_by_min(dataset_df_60)

#shuffle and drop class
sample60 = sample60.sample(frac = 1,random_state=29)
sample60 = sample60.drop('class', 1)

sample60.to_csv("../training-data/dataset/dataset_multiclass_60f_test.csv",index=False)
#sample60.to_csv("../training-data/dataset/dataset_multiclass_60f.csv",index=False)