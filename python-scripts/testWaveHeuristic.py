import numpy as np
import pandas as pd
import json
from statistics import mode
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from createDataset import lm_array_landmarklist
import gestureHeuristics as gh


def get_sequence_predictions(df):
    pred = []
    #for each wave sequence
    for inx, sequence in df.iterrows():
        results = []
        seq = sequence.values
        #clear previous position
        gestureHeuristics.clear_prev_pos()

        #for each landmarks in sequence
        for res_str in seq:
            #convert string landmarks list for prediction
            try: 
                res = json.loads(res_str)
                landmarks = lm_array_landmarklist(np.array(res[:-1]))
                handedness = res[-1]
                #predict gesture
                prediction = gestureHeuristics.predict(landmarks,handedness)
                #add to prediction list
                if prediction == "wave":
                    results.append(prediction)
                else:
                    results.append("non-gesture")
            except:
                pass

        #get mode of prediction list
        mode_prediction = mode(results)
        #add to predictions
        pred.append(mode_prediction)   
    return pred


#load test sets
wave_df = pd.read_csv("../test-data/dataset/wave_sequences.csv")

ng_df = pd.read_csv("../test-data/dataset/nongesture_sequences.csv")

#create true values
waves = ["wave" for i in range(39)] 
nones = ["non-gesture" for i in range(34)]
Y_true = Y_pred = np.array([*waves,*nones])

#initialise gesture heuristics class
gestureHeuristics = gh.GestureHeuristics()

wave_pred = get_sequence_predictions(wave_df)
print(wave_pred)
ng_pred = get_sequence_predictions(ng_df)
print(ng_pred)

#create predicted valuess
Y_pred = np.array([*wave_pred,*ng_pred])

#generate confusion matrix with Y true and Y pred
cm = confusion_matrix(Y_true, Y_pred, labels = ["wave","non-gesture"])

#classification report
metrics = classification_report(Y_true, Y_pred, digits=3)
print(metrics)

cm_df = pd.DataFrame(cm,
                     index = ["wave","non-gesture"], 
                     columns = ["wave","non-gesture"])
                    
print(cm_df)

cm_df.to_csv("../results/heuristic-results/confusion_matrix_wave.csv")



    



