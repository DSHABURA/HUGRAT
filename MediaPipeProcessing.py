import mediapipe as mp
import numpy as np
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
min_detect_conf = 0.8
min_track_conf = 0.5


def process_frame(frame):
    with mp_hand.Hands(min_detection_confidence = min_detect_conf,min_tracking_confidence = min_track_conf) as hands:
        proc_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        proc_image.flags.writeable = False
        results = hands.process(proc_image)
        proc_image.flags.writeable = True
        proc_image = cv2.cvtColor(proc_image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks
       # proc_image.flags.writeable = True
        #proc_image = cv2.cvtColor(proc_image, cv2.COLOR_RGB2BGR)







def get_label(index, hand, results,cam_size):
    output = None
    label = None
    coords = None
    if index ==0:
        label = results.multi_handedness[0].classification[0].label
        coords = tuple(np.multiply(
            np.array((hand.landmark[mp_hand.HandLandmark.WRIST].x, hand.landmark[mp_hand.HandLandmark.WRIST].y)),
            [cam_size[0], cam_size[1]]).astype(int))
    if index == 1:
        label = results.multi_handedness[1].classification[0].label
        coords = tuple(np.multiply(
            np.array((hand.landmark[mp_hand.HandLandmark.WRIST].x, hand.landmark[mp_hand.HandLandmark.WRIST].y)),
            [cam_size[0],cam_size[1]]).astype(int))
            
    
    output = label, coords
        
#     output = None
#     for idx, classification in enumerate(results.multi_handedness):
#         if classification.classification[0].index == index:
#             label = classification.classification[0].label
#             score = classification.classification[0].score
#             text = '{} {}'.format(label, round(score,2))
            
#             #extract coordinates
#             coords = tuple(np.multiply(
#                 np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
#             [640,480]).astype(int))
            
#             output = text, coords
    return output


def get_gesture_overlay(frame):
    with mp_hand.Hands(min_detection_confidence = min_detect_conf,min_tracking_confidence = min_track_conf) as hands:
        proc_image = frame
        #proc_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        proc_image.flags.writeable = False
        results = hands.process(proc_image)
        proc_image.flags.writeable = True
       # proc_image = cv2.cvtColor(proc_image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for num,hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(proc_image, hand, mp_hand.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style())

                #render left or right hand detection
                if get_label(num, hand,results, frame.shape):
                    text,coord = get_label(num,hand,results, frame.shape)
                    cv2.putText(proc_image, text, [coord[0]+25, 
                                                   coord[1]], cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2,cv2.LINE_AA)
            return proc_image
        else:
            return frame