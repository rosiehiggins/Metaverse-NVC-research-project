import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
import numpy as np
import pandas as pd
import time
import glob
import resultsQueue as rq


state = "idle"
prev_state = ""
last_result = None
h_results = []
resultsQueue = rq.ResultsQueue(8)
results_map = {0:"idle",1:"thumbsup"}


#input array of landmarks [A,B,C,D]
def getFingerStraight(landmarks):
    A = np.array([landmarks[0].x,landmarks[0].y,landmarks[0].z])
    B = np.array([landmarks[1].x,landmarks[1].y,landmarks[1].z])
    C = np.array([landmarks[2].x,landmarks[2].y,landmarks[2].z])
    D = np.array([landmarks[3].x,landmarks[3].y,landmarks[3].z])
    
    distAB = np.linalg.norm(A - B)
    distBC = np.linalg.norm(B - C)
    distCD = np.linalg.norm(C - D)
    distAD = np.linalg.norm(A - D)

    sumDists = distAB+distBC+distCD
    absdiff = abs(sumDists-distAD)

    if absdiff <= 0.009:
        return True
    else:
        return False

def getFingerStates(landmarks):
        fingerStates = []
        index = getFingerStraight([landmarks.landmark[5],landmarks.landmark[6],landmarks.landmark[7],landmarks.landmark[8]])   
        middle = getFingerStraight([landmarks.landmark[9],landmarks.landmark[10],landmarks.landmark[11],landmarks.landmark[12]])
        ring = getFingerStraight([landmarks.landmark[13],landmarks.landmark[14],landmarks.landmark[15],landmarks.landmark[16]])
        little = getFingerStraight([landmarks.landmark[17],landmarks.landmark[18],landmarks.landmark[19],landmarks.landmark[20]])

        fingerStates.append(index)
        fingerStates.append(middle)
        fingerStates.append(ring)
        fingerStates.append(little)
        return fingerStates

def getDirection(lA,lB,dir):
    A = np.array([lA.x,lA.y,lA.z])
    B = np.array([lB.x,lB.y,lB.z])
    ABnorm = (A-B)/np.linalg.norm(A-B)
    direction = np.dot(ABnorm,dir)
    return direction

def isThumbsUp(fingerStates,thumbDirection,knuckleDirection):
    if knuckleDirection>0.70 and thumbDirection>0.65 and not fingerStates[0] and not fingerStates[1] and not fingerStates[2] and not fingerStates[3]:
        return True
    
    else:
        return False

def getDelta():
    delta = 0 
    if last_result is not None:
        delta = (time.time()*1000)-last_result
    return delta

test_files = []

#map input and targets together
for file_ in glob.glob("../training-videos/thumbs-up/*"): 
    file_ =  file_.replace("\\","/")  
    test_files.append(file_)

for test_file in test_files:
    #from https://google.github.io/mediapipe/solutions/hands.html
    # For webcam input:
    cap = cv2.VideoCapture(test_file)

    if cap.isOpened() == False:
        print("Error File Not Found")
        continue

    i = 0
    #variable for results
    h_result=[]

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands = 2) as hands:
    
        while cap.isOpened():       
            success, image = cap.read()
            if not success:
                break

            prev_state = state

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
                for hand_landmarks in results.multi_hand_landmarks:
                    fingerStates = getFingerStates(hand_landmarks)
                    thumbDirection = getDirection(hand_landmarks.landmark[3],hand_landmarks.landmark[4],np.array([0,1,0]))
                    knuckleDirection = getDirection(hand_landmarks.landmark[17],hand_landmarks.landmark[5],np.array([0,1,0]))
                    last_result = time.time() * 1000
                    if isThumbsUp(fingerStates,thumbDirection,knuckleDirection):
                        resultsQueue.enqueue(1)
                    
                    else:
                       resultsQueue.enqueue(0)
            
            #get time difference since last hand result   
            if getDelta() > 200:
                resultsQueue.enqueue(0)                    

            qmode = resultsQueue.getResult()
            #set state from current queue buffer
            state = results_map[qmode]
            
            if state == "thumbsup" and prev_state != state:
                print("thumbs up start")
                h_result = [test_file,i]

            elif state == "idle" and prev_state != state:
                #debounce thumbs up stop
                print("thumbs up stop")
                h_result.append(i)
                rt = tuple(h_result)
                h_results.append(rt)
                h_result=[]
            
            i += 1

            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()

if len(h_results)>0:
    #print(h_results)
    df = pd.DataFrame(h_results,columns=["file","thumbsup start","thumbsup stop"])
    df.to_csv("../heuristic-results/results.csv",index=False)