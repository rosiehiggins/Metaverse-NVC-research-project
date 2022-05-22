import numpy as np
from gestureFeatures import getDirection, getFingerStates

def isThumbsUp(fingerStates,thumbDirection,knuckleYDirection):
    if knuckleYDirection>0.70 and thumbDirection>0.65 and not fingerStates[0] and not fingerStates[1] and not fingerStates[2] and not fingerStates[3]:
        return True    
    else:
        return False

def isRaiseHand(fingerStates,knuckleXDirection,knuckleYDirection,hand,velocity=0):
    if (knuckleYDirection<0.60 and knuckleYDirection>-0.20) and ((knuckleXDirection>0.8 and hand == "Right") or (knuckleXDirection<-0.8 and hand == "Left")) and fingerStates[0] and fingerStates[1] and fingerStates[2] and fingerStates[3]:
        return True    
    else:
        return False


def isOK(fingerStates,distIT):
    if distIT <= 0.06 and not fingerStates[0] and fingerStates[1] and fingerStates[2] and fingerStates[3]:
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
    thumbDirection = np.dot(getDirection(landmarks[4],landmarks[3]),np.array([0,1,0]))
    knuckleYDirection = np.dot(getDirection(landmarks[5],landmarks[17]),np.array([0,1,0]))
    knuckleXDirection = np.dot(getDirection(landmarks[5],landmarks[17]),np.array([1,0,0]))

    indexTip = np.array([landmarks[8]['x'],landmarks[8]['y'],landmarks[8]['z']])
    thumbTip = np.array([landmarks[4]['x'],landmarks[4]['y'],landmarks[4]['z']])
    #distance between index and thumb tip
    distIT = np.linalg.norm(indexTip-thumbTip)

    if isThumbsUp(fingerStates,thumbDirection,knuckleYDirection):
        return "thumbs-up"
    elif isRaiseHand(fingerStates,knuckleXDirection,knuckleYDirection,hand):
        return "raise-hand"
    elif isOK(fingerStates,distIT):
        return "ok"
    else:
        return "non-gesture"