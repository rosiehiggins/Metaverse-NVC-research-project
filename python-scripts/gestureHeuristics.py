import numpy as np
from gestureFeatures import get_direction, get_finger_states, get_x_velocity

'''Class for calculating and predicting gesture heuristics'''

class GestureHeuristics:

    prev_pos = np.zeros(3)

    '''Heuristics functions'''

    def isThumbsUp(self,fingerStates,thumbTipY,knuckleY):
        if knuckleY>0.70 and thumbTipY>0.55 and not fingerStates[0] and not fingerStates[1] and not fingerStates[2] and not fingerStates[3]:
            return True    
        else:
            return False

    def isRaiseHand(self,fingerStates,knuckleX,palmY,hand,velocity=0):
        if (palmY>0.85) and ((knuckleX>0.75 and hand == "Right") or (knuckleX<-0.75 and hand == "Left")) and fingerStates[0] and fingerStates[1] and fingerStates[2] and fingerStates[3]:
            return True    
        else:
            return False

    def isOK(self,fingerStates,distIT,knuckleX,palmY,hand):
        if ((palmY>0.85) and 
            ((knuckleX>0.50 and hand == "Right") or (knuckleX<-0.50 and hand == "Left")) 
            and distIT <= 0.06 
            and not fingerStates[0] and fingerStates[1] and fingerStates[2] and fingerStates[3]):
            return True    
        else:
            return False

    def isWave(self,fingerStates,handVelocity,knuckleX,palmY,hand):
        if ((handVelocity>0.1) and
            (palmY >0.5) and
            ((knuckleX>0.4 and hand == 1) or (knuckleX<-0.4 and hand == 0)) and
            fingerStates[0] and fingerStates[1] and fingerStates[2] and fingerStates[3]):
            return True    
        else:
            return False

    #Used to clear previous position each time a new sequence begins
    def clear_prev_pos(self):
        self.prev_pos = np.zeros(3)

    '''Predict gesture given landmarks and handeness'''

    def predict(self,landmarks,hand,static_only = False):
        #finger states array
        fingerStates = get_finger_states(landmarks)

        #directions
        knuckleDir = get_direction(landmarks[5],landmarks[17])
        knuckleX = knuckleDir[0]
        knuckleY = knuckleDir[1]
        palmY = get_direction(landmarks[9],landmarks[0])[1]
        thumbTipY = get_direction(landmarks[4],landmarks[3])[1]

        #distance between index and thumb tip
        indexTip = np.array([landmarks[8]['x'],landmarks[8]['y'],landmarks[8]['z']])
        thumbTip = np.array([landmarks[4]['x'],landmarks[4]['y'],landmarks[4]['z']])                
        distIT = np.linalg.norm(indexTip-thumbTip)

        #x velocity middle finger tip
        middleTip = np.array([landmarks[12]['x'],landmarks[12]['y'],landmarks[12]['z']])
        
        #calculate velocity assuming 30fs
        mx_velocity = get_x_velocity(middleTip,self.prev_pos,33.33)
        self.prev_pos = middleTip

        #Test each heuristic
        if self.isThumbsUp(fingerStates,thumbTipY,knuckleY):
            return "thumbs-up"
        elif self.isRaiseHand(fingerStates,knuckleX,palmY,hand):
            return "raise-hand"
        elif self.isOK(fingerStates,distIT,knuckleX,palmY,hand):
            return "ok"
        elif self.isWave(fingerStates,mx_velocity,knuckleX,palmY,hand) and not static_only:
            return "wave"
        else:
            return "non-gesture"