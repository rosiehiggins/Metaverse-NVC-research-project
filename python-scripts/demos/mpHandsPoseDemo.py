import cv2
import mediapipe as mp

from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

#info on NormalizedLandmarkList manipulation https://github.com/google/mediapipe/issues/2031
def combine_hand_pose_lms(handlms,poselms):
    lm_list = []
    if handlms is not None:
        for hlm in handlms.landmark:
            lm_list.append(hlm)
    if poselms is not None:
        for plm in poselms.landmark:
            lm_list.append(plm)

    #hand_pose_lms = landmark_pb2.NormalizedLandmarkList(
      #landmark = [
        #lm_list
      #]
    #)   
    if lm_list:
        hand_pose_lms = landmark_pb2.NormalizedLandmarkList(
        landmark = lm_list
        )  
        return hand_pose_lms
    else:
        return None
    


#from https://google.github.io/mediapipe/solutions/hands.html
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  #set up pose
  pose = mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5)
  #while cap.isOpened()
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    poseresults = pose.process(image)
    
    #print("hands")
    #print(results.multi_hand_landmarks)
    #print("pose")
    #print(type(poseresults.pose_landmarks))
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        lms = combine_hand_pose_lms(hand_landmarks,poseresults.pose_landmarks)
        if lms is not None:
            mp_drawing.draw_landmarks(
                image,
                lms,
                #mp_hands.HAND_CONNECTIONS,
                #mp_drawing_styles.get_default_hand_landmarks_style(),
                #mp_drawing_styles.get_default_hand_connections_style()
                )
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()