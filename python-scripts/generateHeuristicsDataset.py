from createDataset import balance_dataset_by_min
from createDataset import map_file_to_ranges
from createDataset import get_data_from_images
from createDataset import get_data
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
frame_ranges_ng = map_file_to_ranges(pathname="../training-data/labelled-data/nongestures.csv",indexcol="file",\
                                usecols=["file","nonstart","nonstop","hand"],dtype={'nonstart': int, 'nonstop': int,'hand':str})
nongesture_data = get_data("../training-videos/non-gesture",frame_ranges_ng,[0,0,0,1],"nongesture",norm=False)
print("non gesture")
print(len(nongesture_data))

#img data from public dataset
raul_fist_data = get_data_from_images("../training-images/raul/fist","Left",[0,0,0,1],"nongesture",norm=False)
print("fist raul")
print(len(raul_fist_data))

raquel_non_data  = get_data_from_images("../training-images/raquel/non-gesture","Left",[0,0,0,1],"nongesture",norm=False)
print("raquel nons")
print(len(raquel_non_data))

tomas_non_data = get_data_from_images("../training-images/tomas/non-gesture","Left",[0,0,0,1],"nongesture",norm=False)
print("tomas nons ")
print(len(tomas_non_data))

#
#raise hand
#

#get frame ranges
rh_frame_ranges = map_file_to_ranges(pathname="../training-data/labelled-data/raisehand.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
rh_data = get_data("../training-videos/raise-hand",rh_frame_ranges,[0,1,0,0],"raisehand",norm=False)
print("raise hand video")
print(len(rh_data))


#img data from public dataset
raul_rh_data = get_data_from_images("../training-images/raul/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand raul")
print(len(raul_rh_data))


samira_rh_data = get_data_from_images("../training-images/samira/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand samira")
print(len(samira_rh_data))


arturo_rh_data = get_data_from_images("../training-images/arturo/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand arturo")
print(len(arturo_rh_data))


carlos_c_rh_data = get_data_from_images("../training-images/carlos_c/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand carlos c")
print(len(carlos_c_rh_data))


esther_rh_data = get_data_from_images("../training-images/esther/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand esther")
print(len(esther_rh_data))


jesus_rh_data = get_data_from_images("../training-images/jesus/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand jesus ")
print(len(jesus_rh_data))

raquel_rh_data = get_data_from_images("../training-images/raquel/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand raquel")
print(len(raquel_rh_data))

tomas_rh_data = get_data_from_images("../training-images/tomas/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand tomas")
print(len(tomas_rh_data))

madr1_rh_data = get_data_from_images("../training-images/madrid1/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand madr1")
print(len(madr1_rh_data))

madr2_rh_data = get_data_from_images("../training-images/madrid2/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand madr2")
print(len(madr2_rh_data))

madr3_rh_data = get_data_from_images("../training-images/madrid3/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand madr3")
print(len(madr3_rh_data))

madr4_rh_data = get_data_from_images("../training-images/madrid4/raise-hand","Left",[0,1,0,0],"raisehand",norm=False)
print("raise hand madr4")
print(len(madr4_rh_data))


#
#thumbs up
#
#get frame ranges
frame_ranges = map_file_to_ranges(pathname="../training-data/labelled-data/thumbsups.csv",indexcol="file",\
                                usecols=["file","thumbsupstart","thumbsupstop","hand"],dtype={'thumbsupstart': int, 'thumbsupstop': int,'hand':str})
thumbsup_data  = get_data("../training-videos/thumbs-up",frame_ranges,[1,0,0,0],"thumbsup",norm=False)

print("thumbs up video")
print(len(thumbsup_data))

#img data from public dataset
raul_tu_data  = get_data_from_images("../training-images/raul/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs up raul")
print(len(raul_tu_data))

samira_tu_data = get_data_from_images("../training-images/samira/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs up samira")
print(len(samira_tu_data))

alfredo_tu_data = get_data_from_images("../training-images/alfredo/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs up alfredo")
print(len(alfredo_tu_data))

ana_tu_data = get_data_from_images("../training-images/ana/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs up ana")
print(len(ana_tu_data))

ana_m_tu_data = get_data_from_images("../training-images/ana_m/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs up ana m")
print(len(ana_m_tu_data))

arturo_tu_data = get_data_from_images("../training-images/arturo/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs-up arturo")
print(len(arturo_tu_data))

carlos_c_tu_data  = get_data_from_images("../training-images/carlos_c/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs-up carlos c")
print(len(carlos_c_tu_data))

esther_tu_data = get_data_from_images("../training-images/esther/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs-up esther")
print(len(esther_tu_data))

jesus_tu_data = get_data_from_images("../training-images/jesus/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs-up jesus")
print(len(jesus_tu_data))

raquel_tu_data  = get_data_from_images("../training-images/raquel/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs-up raquel")
print(len(raquel_tu_data))

tomas_tu_data = get_data_from_images("../training-images/tomas/thumbs-up","Left",[1,0,0,0],"thumbsup",norm=False)
print("thumbs-up tomas")
print(len(tomas_tu_data))

#
#OK
#

#get frame ranges
ok_frame_ranges = map_file_to_ranges(pathname="../training-data/labelled-data/oks.csv",indexcol="file",\
                                usecols=["file","start","stop","hand"],dtype={'start': int, 'stop': int,'hand':str})
ok_data = get_data("../training-videos/ok",ok_frame_ranges,[0,0,1,0],"ok",norm=False)
print("ok video")
print(len(ok_data))

#img data from public dataset
raul_ok_data= get_data_from_images("../training-images/raul/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok raul")
print(len(raul_ok_data))

samira_ok_data = get_data_from_images("../training-images/samira/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok samira")
print(len(samira_ok_data))

alfredo_ok_data = get_data_from_images("../training-images/alfredo/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok alfredo")
print(len(alfredo_ok_data))

ana_ok_data = get_data_from_images("../training-images/ana/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok ana")
print(len(ana_ok_data))

ana_m_ok_data = get_data_from_images("../training-images/ana_m/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok ana m")
print(len(ana_m_ok_data))

arturo_ok_data = get_data_from_images("../training-images/arturo/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok arturo")
print(len(arturo_ok_data))

carlos_c_ok_data = get_data_from_images("../training-images/carlos_c/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok carlos c")
print(len(carlos_c_ok_data))

esther_ok_data = get_data_from_images("../training-images/esther/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok esther ")
print(len(esther_ok_data))

jesus_ok_data = get_data_from_images("../training-images/jesus/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok jesus")
print(len(jesus_ok_data))

raquel_ok_data = get_data_from_images("../training-images/raquel/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok raquel")
print(len(raquel_ok_data))

tomas_ok_data = get_data_from_images("../training-images/tomas/ok","Left",[0,0,1,0],"ok",norm=False)
print("ok tomas")
print(len(tomas_ok_data))



#
#balance and save dataset to csv
#
seed = 29

dataset = [*raul_ok_data, *samira_ok_data, *ok_data, *arturo_ok_data, *alfredo_ok_data, *ana_ok_data, *ana_m_ok_data, *carlos_c_ok_data, *esther_ok_data, *jesus_ok_data, *raquel_ok_data, *tomas_ok_data,\
            *raul_rh_data,*rh_data, *samira_rh_data,  *arturo_rh_data, *carlos_c_rh_data, *esther_rh_data, *jesus_rh_data, *raquel_rh_data, *tomas_rh_data,\
            *madr1_rh_data, *madr2_rh_data, *madr3_rh_data, *madr4_rh_data, \
            *thumbsup_data, *raul_tu_data, *samira_tu_data,*alfredo_tu_data,*ana_tu_data,*ana_m_tu_data,*arturo_tu_data,*carlos_c_tu_data, *esther_tu_data, *jesus_tu_data, *raquel_tu_data, *tomas_tu_data,\
            *nongesture_data, *raul_fist_data, *raquel_non_data, *tomas_non_data] 



columns = [*range(0, 68)]
columns.append("class")
dataset_df = pd.DataFrame(dataset, columns=columns)

#balance
sample = balance_dataset_by_min(dataset_df)

#shuffle and drop class
sample = sample.sample(frac = 1,random_state=29)
sample = sample.drop('class', 1)

#sample.to_csv("../training-data/dataset/dataset_multiclass_raw.csv",index=False)
sample.to_csv("../training-data/dataset/dataset_multiclass_raw_test.csv",index=False)

