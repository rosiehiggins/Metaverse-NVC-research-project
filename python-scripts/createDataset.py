#Python module with a series of functions to facilitate generate datasets for training and testing gesture classifier models

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
import glob
import numpy as np
import pandas as pd
import math 
import random
from gestureFeatures import angle_two_vectors

#rebuild landmark list from np array
def lm_array_landmarklist(lmarray):
    landmark_list = []
    #build list
    for i in range(0,len(lmarray),3):
        kp = {"x":lmarray[i],"y":lmarray[i+1],"z":lmarray[i+2]}
        landmark_list.append(kp) 
    return landmark_list

#balance dataset by undersampling
def balance_dataset_by_min(df):
    if 'class' in df:
        g = df.groupby('class')
        print(g.head())
        return pd.DataFrame(g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True)))
    else:
        return None

#convert mediapipe landmark output to numpy array
def landmarks_tonumpy(landmarks,xscale=1):
    lms = []
    for landmark in landmarks:
        lm_np = np.array([landmark.x*xscale,landmark.y,landmark.z])
        lms.append(lm_np)
    return lms

#convert mediapipe landmakr output to features
def landmarks_to_features(landmarks,xscale=1):
    features = []
    lms = landmarks_tonumpy(landmarks,xscale)
    #angle seg thumb0
    seg0_t0 = lms[2]-lms[0]
    seg1_t0 = lms[3]-lms[2]
    angle_t0 = angle_two_vectors(seg0_t0,seg1_t0)
    features.append(angle_t0)

    #angle seg thumb1
    seg0_t1 = lms[3]-lms[2]
    seg1_t1 = lms[4]-lms[3]
    angle_t1 = angle_two_vectors(seg0_t1,seg1_t1)
    features.append(angle_t1)

    #angle seg index 0
    seg0_i0 = lms[5]-lms[0]
    seg1_i0 = lms[6]-lms[5]
    angle_i0 = angle_two_vectors(seg0_i0,seg1_i0)
    features.append(angle_i0)

    #angle seg index 1
    seg0_i1 = lms[6]-lms[5]
    seg1_i1 = lms[7]-lms[6]
    angle_i1 = angle_two_vectors(seg0_i1,seg1_i1)
    features.append(angle_i1)

    #angle seg index 2
    seg0_i2 = lms[7]-lms[6]
    seg1_i2 = lms[8]-lms[7]
    angle_i2 = angle_two_vectors(seg0_i2,seg1_i2)
    features.append(angle_i2)

    #angle seg middle 0
    seg0_m0 = lms[9]-lms[0]
    seg1_m0 = lms[10]-lms[9]
    angle_m0 = angle_two_vectors(seg0_m0,seg1_m0)
    features.append(angle_m0)

    #angle seg middle 1
    seg0_m1 = lms[10]-lms[9]
    seg1_m1 = lms[11]-lms[10]
    angle_m1 = angle_two_vectors(seg0_m1,seg1_m1)
    features.append(angle_m1)

    #angle seg middle 2
    seg0_m2 = lms[11]-lms[10]
    seg1_m2 = lms[12]-lms[11]
    angle_m2 = angle_two_vectors(seg0_m2,seg1_m2)
    features.append(angle_m2)

    #angle seg ring 0
    seg0_r0 = lms[13]-lms[0]
    seg1_r0 = lms[14]-lms[13]
    angle_r0 = angle_two_vectors(seg0_r0,seg1_r0)
    features.append(angle_r0)

    #angle seg ring 1
    seg0_r1 = lms[14]-lms[13]
    seg1_r1 = lms[15]-lms[14]
    angle_r1 = angle_two_vectors(seg0_r1,seg1_r1)
    features.append(angle_r1)

    #angle seg ring 2
    seg0_r2 = lms[15]-lms[14]
    seg1_r2 = lms[16]-lms[15]
    angle_r2 = angle_two_vectors(seg0_r2,seg1_r2)
    features.append(angle_r2)

    #angle seg little 0
    seg0_l0 = lms[17]-lms[0]
    seg1_l0 = lms[18]-lms[17]
    angle_l0 = angle_two_vectors(seg0_l0,seg1_l0)
    features.append(angle_l0)

    #angle seg little 1
    seg0_l1 = lms[18]-lms[17]
    seg1_l1 = lms[19]-lms[18]
    angle_l1 = angle_two_vectors(seg0_l1,seg1_l1)
    features.append(angle_l1)

    #angle seg little 2
    seg0_l2 = lms[19]-lms[18]
    seg1_l2 = lms[20]-lms[19]
    angle_l2 = angle_two_vectors(seg0_l2,seg1_l2)
    features.append(angle_l2)

    #palm direction
    palm_to_wrist = lms[9] - lms[0]
    palm_dir = (palm_to_wrist)/np.linalg.norm(palm_to_wrist)
    features.append(palm_dir[0])
    features.append(palm_dir[1])
    features.append(palm_dir[2])

    #knuckle direction
    knuckle_to_knuckle = lms[5] - lms[17]
    knuckle_dir = (knuckle_to_knuckle)/np.linalg.norm(knuckle_to_knuckle)
    features.append(knuckle_dir[0])
    features.append(knuckle_dir[1])
    features.append(knuckle_dir[2])

    #thum dir
    thumb_middle_to_tip = lms[4] - lms[3]
    thumb_dir = (thumb_middle_to_tip)/np.linalg.norm(thumb_middle_to_tip)
    features.append(thumb_dir[0])
    features.append(thumb_dir[1])
    features.append(thumb_dir[2])

    return features


#flatten landmarks to list
def landmarks_to_list(landmarks):
    lm_list = []

    for lms in landmarks:
        lm_list.append(lms.x)
        lm_list.append(lms.y)
        lm_list.append(lms.z)

    return lm_list

#flatten and normalise landmarks
def landmarks_to_list_norm(landmarks,scalekp=9,xscale=1):
    lm_list = []

    #translate hand with wrist at origin
    wrist_x = landmarks[0].x
    wrist_y = landmarks[0].y
    wrist_z = landmarks[0].z

    slm = landmarks[scalekp]
    #translate scale point
    slmt = {'x':slm.x - wrist_x, 'y': slm.y - wrist_y, 'z': slm.z - wrist_z}
    #calculate scale factor
    scalefactor = 1/(math.sqrt(math.pow(slmt['x'],2) + math.pow(slmt['y'],2) + math.pow(slmt['z'],2)))  

    i = 0
    #normalise and append each landmark x,y and z to landmark list, skip 0 (wrist as always 0,0,0)
    for lms in landmarks:
        if i != 0:
            lm_list.append(((lms.x-wrist_x)*scalefactor)*xscale)
            lm_list.append((lms.y-wrist_y)*scalefactor)
            lm_list.append((lms.z-wrist_z)*scalefactor)
        i += 1

    return lm_list

#Return handedness int
def get_hand_int(hand):
    if hand == "Right":
        return 1
    else: 
        return 0

#check if given frame number falls with a labelled range
def in_range(fn,ranges,hand):
    for r in ranges:
        #if frame number in range and hand is the same
        if fn in r["r"] and hand == r["h"]:
            return True
    return False

#TODO will at some point improve the data structure for sequences 
#so this is not necessary
#Get sequence number from frame ranges
def get_seq(fn,ranges):
    for r in ranges:
        #if frame number in range and hand is the same
        if fn in r["r"]:
            return r["s"]
    return -1

#For each file in list of ranges, map all corresponding ranges to file
def map_file_to_ranges(pathname,indexcol,usecols=None,dtype=None):
    #load labelled data
    #load in test data 
    true_df = pd.read_csv(filepath_or_buffer=pathname,index_col=indexcol,usecols=usecols,dtype = dtype)
    frame_ranges = {}

    #map ranges for each file name
    for filename, row in true_df.iterrows():
        frame_range = range(row[0],row[1]+1)
        r = {"r":frame_range,"h":row[2]}
        #add sequence if sequence
        if len(row)==4:
            r["s"] = row[3]
        
        #if index in frame_ranges
        #append new range onto list
        if filename not in frame_ranges:
            frame_ranges[filename] = []
        
        frame_ranges[filename].append(r)
        
    return frame_ranges

#Given location of video files, iterate over each video, pass each frame through MediaPipe
#save arrays of keypoints for each frame, return data
def get_data(path,frame_ranges,data_class,class_label=None,norm=True):
    #load files
    true_files = []
    data = []
    for file_ in glob.glob(path+"/*"):   
        file_ =  file_.replace("\\","/")
        true_files.append(file_)

    for f in true_files:
        #from https://google.github.io/mediapipe/solutions/hands.html
        # For webcam input:
        cap = cv2.VideoCapture(f)
        if cap.isOpened() == False:
            print("Error File Not Found")
            continue

        print(f)
        
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands = 2) as hands:
            
            count=0
            while cap.isOpened():        
                #TODO make processed videos start at 0 not 1        
                fn = cap.get(cv2.CAP_PROP_POS_FRAMES) + 1
                success, image = cap.read()
                if not success:
                    break

                if f not in frame_ranges:
                    print("file not in ranges")
                    break

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                #infer landmarks from video frame
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                
                if results.multi_hand_world_landmarks:
                    #index to keep track of handedness
                    i = 0
                    for hand_landmarks in results.multi_hand_landmarks:                   
                        #frame is in result range? and correct hand

                        ranges = frame_ranges[f]
                        hand = results.multi_handedness[i].classification[0].label
                        if in_range(fn,ranges,hand):
                            xscale = 1
                            if hand == "Left":
                                xscale = -1
                            #flatten data to array, normalise if norm flag = true
                            lm_list=[]
                            if norm:
                                lm_list = landmarks_to_list_norm(hand_landmarks.landmark,9,xscale)
                            else:
                                lm_list = landmarks_to_list(hand_landmarks.landmark)
                                #add handedness
                                hand_num = get_hand_int(hand)
                                lm_list.append(hand_num)  

                            #if dataclass is array (multiclass) concatenate else append
                            if isinstance(data_class, list):
                                lm_list = [*lm_list,*data_class]
                            else:
                                lm_list.append(data_class)
                            
                            if class_label is not None:
                                lm_list.append(class_label) 
                                  
                            #add to dataset
                            data.append(lm_list)
                            count+=1
                        i+=1
                                        
                #show image
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()   
    return data

#Given location of video files, iterate over each video, pass each frame through MediaPipe
#save arrays of features for each frame, return data
def get_feature_data(path,frame_ranges,data_class,class_label=None):
    #load files
    true_files = []
    data23 = []
    data60 = []

    for file_ in glob.glob(path+"/*"):   
        file_ =  file_.replace("\\","/")
        true_files.append(file_)

    for f in true_files:
        #from https://google.github.io/mediapipe/solutions/hands.html
        # For webcam input:
        cap = cv2.VideoCapture(f)
        if cap.isOpened() == False:
            print("Error File Not Found")
            continue

        print(f)
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands = 2) as hands:
            
            count=0
            while cap.isOpened():        
                #TODO make processed videos start at 0 not 1        
                fn = cap.get(cv2.CAP_PROP_POS_FRAMES) + 1
                success, image = cap.read()
                if not success:
                    break
                if f not in frame_ranges:
                    print("file not in ranges")
                    break
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                #infer landmarks from video frame
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                
                if results.multi_hand_world_landmarks:
                    #index to keep track of handedness
                    i = 0
                    for hand_landmarks in results.multi_hand_landmarks:                   
                        #frame is in result range? and correct hand
                        ranges = frame_ranges[f]
                        hand = results.multi_handedness[i].classification[0].label
                        if in_range(fn,ranges,hand):
                            #convert data to array
                            #create list of features
                            xscale = 1
                            if hand == "Left":
                                xscale = -1

                            feature_list_23 = landmarks_to_features(hand_landmarks.landmark,xscale)
                            feature_list_60 = landmarks_to_list_norm(hand_landmarks.landmark,9,xscale)

                            #if dataclass is array (multiclass) concatenate else append
                            if isinstance(data_class, list):
                                feature_list_23 = [*feature_list_23,*data_class]
                                feature_list_60 = [*feature_list_60,*data_class]
                            else:
                                feature_list_23.append(data_class)
                                feature_list_60.append(data_class)

                            if class_label is not None:
                                feature_list_23.append(class_label)   
                                feature_list_60.append(class_label)   
                                                          
                            #add to datasets
                            data23.append(feature_list_23)
                            data60.append(feature_list_60)
                            count+=1
                        i+=1
                        
                
                #show image
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()   
    return data23,data60




#Given location of images files, iterate over each image and pass through MediaPipe
#save arrays of landmarks for each image, return data
def get_data_from_images(path,hand,data_class,class_label=None,norm=True):
    #load files
    true_files = []
    data = []
    for file_ in glob.glob(path+"/*"):   
        file_ =  file_.replace("\\","/")
        true_files.append(file_)
    
    for f in true_files:
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands = 2) as hands:
            
            count=0
            image = cv2.imread(f)
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            #infer landmarks from image
            results = hands.process(image)
            if results.multi_hand_world_landmarks:
                #index to keep track of handedness
                i = 0
                for hand_landmarks in results.multi_hand_landmarks:                   
                    pred_hand = results.multi_handedness[i].classification[0].label
                    if hand == pred_hand:
                        xscale = 1
                        if hand == "Left":
                            xscale = -1

                        #flatten data to array, normalise if norm flag = true
                        lm_list=[]
                        if norm:
                            lm_list = landmarks_to_list_norm(hand_landmarks.landmark,9,xscale)
                        else:
                            lm_list = landmarks_to_list(hand_landmarks.landmark)
                            #add handedness
                            hand_num = get_hand_int(hand)
                            lm_list.append(hand_num)                        

                        #if dataclass is array (multiclass) concatenate else append
                        if isinstance(data_class, list):
                            lm_list = [*lm_list,*data_class]
                        else:
                            lm_list.append(data_class) 
                        
                        if class_label is not None:
                            lm_list.append(class_label)    
                                                
                        #add to dataset
                        data.append(lm_list)
                        count+=1
                    i+=1
    return data  

#Given location of images files, iterate over each image and pass through MediaPipe
#save arrays of features for each image, return data
def get_feature_data_from_images(path,hand,data_class,class_label=None):
    #load files
    true_files = []
    data23 = []
    data60 = []

    for file_ in glob.glob(path+"/*"):   
        file_ =  file_.replace("\\","/")
        true_files.append(file_)
    
    for f in true_files:
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands = 2) as hands:
            
            count=0
            image = cv2.imread(f)
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            #infer landmarks from image
            results = hands.process(image)
            if results.multi_hand_world_landmarks:
                #index to keep track of handedness
                i = 0
                for hand_landmarks in results.multi_hand_landmarks:                   
                    pred_hand = results.multi_handedness[i].classification[0].label
                    if hand == pred_hand:

                        xscale = 1
                        #flip hand if left
                        if hand == "Left":
                            xscale = -1

                        feature_list_23 = landmarks_to_features(hand_landmarks.landmark,xscale)
                        feature_list_60 = landmarks_to_list_norm(hand_landmarks.landmark,9,xscale)

                        #if dataclass is array (multiclass) concatenate else append
                        if isinstance(data_class, list):
                            feature_list_23 = [*feature_list_23,*data_class]
                            feature_list_60 = [*feature_list_60,*data_class]
                        else:
                            feature_list_23.append(data_class) 
                            feature_list_60.append(data_class)

                        if class_label is not None:
                            feature_list_23.append(class_label)
                            feature_list_60.append(class_label)

                        data23.append(feature_list_23)
                        data60.append(feature_list_60)
                        count+=1
                    i+=1

    return data23,data60  

#Given location of video files, iterate over each video, pass each frame through MediaPipe
#save arrays of keypoint sequences for each seq in range, return data
def get_sequences(path,frame_ranges,norm=True):
    #load files
    true_files = []
    data = {}
    for file_ in glob.glob(path+"/*"):   
        file_ =  file_.replace("\\","/")
        true_files.append(file_)

    for f in true_files:
        #from https://google.github.io/mediapipe/solutions/hands.html
        # For webcam input:
        cap = cv2.VideoCapture(f)
        if cap.isOpened() == False:
            print("Error File Not Found")
            continue

        print(f)
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands = 2) as hands:
            
            count=0
            while cap.isOpened():        
                #TODO make processed videos start at 0 not 1        
                fn = cap.get(cv2.CAP_PROP_POS_FRAMES) + 1
                success, image = cap.read()
                if not success:
                    break

                if f not in frame_ranges:
                    print("file not in ranges")
                    break

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                #infer landmarks from video frame
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                
                if results.multi_hand_world_landmarks:
                    #index to keep track of handedness
                    i = 0
                    for hand_landmarks in results.multi_hand_landmarks:                   
                        #frame is in result range? and correct hand

                        ranges = frame_ranges[f]
                        hand = results.multi_handedness[i].classification[0].label
                        if in_range(fn,ranges,hand):

                            #get seq
                            seq = get_seq(fn,ranges)

                            #add sequence to data if not in
                            if seq not in data:
                                data[seq] = []
                            
                            xscale = 1
                            if hand == "Left":
                                xscale = -1
                            #flatten data to array, normalise if norm flag = true
                            lm_list=[]
                            if norm:
                                lm_list = landmarks_to_list_norm(hand_landmarks.landmark,9,xscale)
                            else:
                                lm_list = landmarks_to_list(hand_landmarks.landmark)
                                #add handedness
                                hand_num = get_hand_int(hand)
                                lm_list.append(hand_num)  
                                  
                            #add to dataset
                            data[seq].append(lm_list)
                            print("adding to seq " + str(seq))
                            count+=1
                        i+=1
                                       
                #show image
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()   
    return data