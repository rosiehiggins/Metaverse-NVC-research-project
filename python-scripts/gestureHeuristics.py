import numpy as np
from gestureFeatures import getDirection, getFingerStates

def isThumbsUp(fingerStates,thumbTipY,knuckleY):
    if knuckleY>0.70 and thumbTipY>0.55 and not fingerStates[0] and not fingerStates[1] and not fingerStates[2] and not fingerStates[3]:
        return True    
    else:
        return False

def isRaiseHand(fingerStates,knuckleX,palmY,hand,velocity=0):
    if (palmY>0.85) and ((knuckleX>0.75 and hand == "Right") or (knuckleX<-0.75 and hand == "Left")) and fingerStates[0] and fingerStates[1] and fingerStates[2] and fingerStates[3]:
        return True    
    else:
        return False


def isOK(fingerStates,distIT,knuckleX,palmY,hand):
    if ((palmY>0.85) and 
        ((knuckleX>0.50 and hand == "Right") or (knuckleX<-0.50 and hand == "Left")) 
        and distIT <= 0.06 
        and not fingerStates[0] and fingerStates[1] and fingerStates[2] and fingerStates[3]):
        return True    
    else:
        return False

#TODO update
def isWave(fingerStates,thumbDirection,knuckleDirection):
    if knuckleDirection>0.70 and thumbDirection>0.65 and not fingerStates[0] and not fingerStates[1] and not fingerStates[2] and not fingerStates[3]:
        return True    
    else:
        return False


def predict(landmarks,hand):
    #finger states array
    fingerStates = getFingerStates(landmarks)

    #directions
    knuckleDir = getDirection(landmarks[5],landmarks[17])
    knuckleX = knuckleDir[0]
    knuckleY = knuckleDir[1]
    palmY = getDirection(landmarks[9],landmarks[0])[1]
    thumbTipY = getDirection(landmarks[4],landmarks[3])[1]


    indexTip = np.array([landmarks[8]['x'],landmarks[8]['y'],landmarks[8]['z']])
    thumbTip = np.array([landmarks[4]['x'],landmarks[4]['y'],landmarks[4]['z']])
    
    #distance between index and thumb tip
    distIT = np.linalg.norm(indexTip-thumbTip)

    if isThumbsUp(fingerStates,thumbTipY,knuckleY):
        return "thumbs-up"
    elif isRaiseHand(fingerStates,knuckleX,palmY,hand):
        return "raise-hand"
    elif isOK(fingerStates,distIT,knuckleX,palmY,hand):
        return "ok"
    else:
        return "non-gesture"