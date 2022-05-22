from createDataset import balance_dataset_by_min
from createDataset import map_file_to_ranges
from createDataset import get_data_from_images
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

#img data from heuristics test set
non_gesture_data = get_data_from_images("../heuristics-test-images/non-gestures","Left",0,"non-gesture",norm = False)
print("non gesture")
print(len(non_gesture_data))


#
#thumbs up
#

#img data from heuristics test set
thumbsup_data = get_data_from_images("../heuristics-test-images/thumbs-up","Left",0,"thumbs-up",norm = False)
print("thumbs up")
print(len(thumbsup_data))


#
#raise hand
#

#img data from heuristics test set
raisehand_data = get_data_from_images("../heuristics-test-images/raise-hand","Left",0,"raise-hand",norm = False)
print("raise hand")
print(len(raisehand_data))


#
#ok
#

#img data from heuristics test set
ok_data = get_data_from_images("../heuristics-test-images/ok","Left",0,"ok",norm = False)
print("ok")
print(len(ok_data))


dataset = [*non_gesture_data,*thumbsup_data,*raisehand_data,*ok_data]

df = pd.DataFrame(dataset)

df.to_csv("../test-data/dataset/heuristics_testset.csv",index=False)
