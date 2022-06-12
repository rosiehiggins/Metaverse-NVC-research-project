from createDataset import map_file_to_ranges
from createDataset import get_sequences
import numpy as np
import pandas as pd

#
#wave sequences
#
#get frame ranges
fr_wave = map_file_to_ranges(pathname="../training-data/wave_sequences.csv",indexcol="file",\
                                usecols=["file","wavestart","wavestop","hand","seq"],dtype={'nonstart': int, 'nonstop': int,'hand':str,'seq': int,})

wave_data = get_sequences("../training-videos/wave",fr_wave,norm=False)

wave_df = pd.DataFrame.from_dict(wave_data, orient='index')

wave_df.to_csv("../training-data/dataset/wave_sequences.csv",index=False)


#
#non-gesture
#
#get frame ranges

fr_ng = map_file_to_ranges(pathname="../training-data/nongestures_sequences.csv",indexcol="file",\
                                usecols=["file","nonstart","nonstop","hand","seq"],dtype={'nonstart': int, 'nonstop': int,'hand':str,'seq': int,})

ng_data = get_sequences("../training-videos/non-gesture",fr_ng,norm=False)

ng_df = pd.DataFrame.from_dict(ng_data, orient='index')

ng_df.to_csv("../training-data/dataset/nongesture_sequences.csv",index=False)