import numpy as np
import math

#norm angle between 2 3D numpy arrays
def angle_two_vectors(seg0,seg1):
    #normalise
    seg0norm = (seg0)/np.linalg.norm(seg0)
    seg1norm = (seg1)/np.linalg.norm(seg1)
    #dot product 
    cos = np.dot(seg0norm,seg1norm)
    #cos to norm
    angle = math.acos(cos)/math.pi
    #return angle
    return angle

#Get directional vector given two landmarks
def getDirection(lA,lB):
    A = np.array([lA['x'],lA['y'],lA['z']])
    B = np.array([lB['x'],lB['y'],lB['z']])
    direction = (B-A)/np.linalg.norm(B-A)
    return direction

#input finger landmarks A,B,C,D
#output boolean indicating whether finger is straight
def getFingerStraight(A,B,C,D):
    #create numpy 3D arrays from landmarks
    A = np.array([A['x'],A['y'],A['z']])
    B = np.array([B['x'],B['y'],B['z']])
    C = np.array([C['x'],C['y'],C['z']])
    D = np.array([D['x'],D['y'],D['z']])
    
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

#returns an array of finger states to be used to calculate heuristics
def getFingerStates(landmarks):
        fingerStates = []
        index = getFingerStraight(landmarks[5],landmarks[6],landmarks[7],landmarks[8])   
        middle = getFingerStraight(landmarks[9],landmarks[10],landmarks[11],landmarks[12])
        ring = getFingerStraight(landmarks[13],landmarks[14],landmarks[15],landmarks[16])
        little = getFingerStraight(landmarks[17],landmarks[18],landmarks[19],landmarks[20])

        fingerStates.append(index)
        fingerStates.append(middle)
        fingerStates.append(ring)
        fingerStates.append(little)

        return fingerStates 