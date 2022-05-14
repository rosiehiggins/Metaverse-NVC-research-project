import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


#return max frame number from two lists of frame ranges
def get_max_frame(f1,f2):
    end_f1 = 0
    if f1:
        end_f1 = f1[-1][1]
    end_f2 = 0
    if f2:
        end_f2 = f2[-1][1]
    
    return max(end_f1,end_f2)

def build_results_vector(framelist,max):
    pass
    
#maps the true and predicted frames together by file name
def map_by_filename(true,pred):
    data_map={}
    for x in true:
        filename = x[0]
        if filename in data_map:
            if "true" in data_map[filename]:
                frames = data_map[filename]["true"]
                frames.append([x[1],x[2]])
                data_map[filename]["true"] = frames
            else:
                data_map[filename]["true"] = []
                frames = [x[1],x[2]]
                data_map[filename]["true"].append(frames)
        else:
            data_map[filename] = {}
            data_map[filename]["true"] = []
            frames = [x[1],x[2]]
            data_map[filename]["true"].append(frames)

    for y in pred:
        filename = y[0]
        if filename in data_map:
            if "pred" in data_map[filename]:
                frames = data_map[filename]["pred"]
                frames.append([y[1],y[2]])
                data_map[filename]["pred"] = frames
            else:
                data_map[filename]["pred"] = []
                frames = [y[1],y[2]]
                data_map[filename]["pred"].append(frames)
        else:
            data_map[filename] = {}
            data_map[filename]["pred"] = []
            frames = [y[1],y[2]]
            data_map[filename]["pred"].append(frames)
    
    return data_map

#encode predicted and true from data map into binary vectors of equal length
def one_hot_encode(data_map):
    y_true=None
    y_pred=None

    #iterate over dictionary
    for filename in data_map:
        #get true
        t = data_map[filename]["true"]
        
        #get pred
        p = []
        if "pred" in data_map[filename]:
            p = data_map[filename]["pred"]

        #get max frame from 2 files
        maxframe = get_max_frame(t,p)  
        
        #TODO simplify into build vector function
        #Build true vector
        f_true = np.zeros(maxframe,dtype=np.int8)
        #iterate over each frame range
        for r in t:
            #get length of range
            n = r[1]-r[0]+1
            #create np array of 1s of length n
            hits = np.ones(n,dtype=np.int8)
            #access ground truth values for file and replace 0s with 1s
            f_true[r[0]-1:r[1]] = hits
        #concatenate to list of ground truth vals    
        if y_true is not None:
            y_true = np.concatenate([y_true,f_true])
        else:
            y_true = f_true
        
        #Build predicted vector
        f_pred = np.zeros(maxframe,dtype=np.int8)
        #iterate over each frame range
        for r in p:
            #get length of range
            n = r[1]-r[0]+1
            #create np array of 1s of length n
            hits = np.ones(n,dtype=np.int8)
            #access predicted values for file and replace 0s with 1s
            f_pred[r[0]-1:r[1]] = hits
        #concatenate to list of predictions    
        if y_pred is not None:
            y_pred = np.concatenate([y_pred,f_pred])
        else:
            y_pred = f_pred

    return y_true,y_pred   



# from sklearn docs : tn, fp, fn, tp
#accuracy (TP+TN)/(TP+TN+FP+FN)
def accuracy(cm):
    return (cm[3]+cm[0])/sum(cm)

#precision (TP)/(TP+FP)
def precision(cm):    
    return cm[3]/(cm[3]+cm[1])

#recall (TP)/(TP+FN)
def recall(cm):
    return cm[3]/(cm[3]+cm[2])



#load in test data 
true_df = pd.read_csv("../training-data/thumbsups.csv")
true_ = true_df.to_numpy()


#load in results
pred_df = pd.read_csv("../heuristic-results/results.csv")
pred = pred_df.to_numpy()

data_map = map_by_filename(true_,pred)

y_true,y_pred = one_hot_encode(data_map)

# from sklearn docs : tn, fp, fn, tp
cm = confusion_matrix(y_true, y_pred).ravel()

print("confusion matrix")
print("tn, fp, fn, tp")
print(cm)

print("accuracy")
print(accuracy(cm))
print("precision")
print(precision(cm))
print("recall")
print(recall(cm))

