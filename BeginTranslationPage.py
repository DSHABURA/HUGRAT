from Sidebar import Sidebar
from Content import Content
from tkinter import Canvas
import cv2 as cv
import mediapipe as mp
from PIL import Image, ImageTk
import itertools
import copy
import csv
import os
import customtkinter as ct
import utils
import tensorflow as tf
import numpy as np


min_detection_confidence = 0.7
min_tracking_confidence = 0.7
class KeyPointClassifier(object):
    def __init__(
        self,
        model_path='./data/classifier.tflite',
        num_threads=1,
    ):
        self.interpreter = tf.lite.Interpreter(model_path=model_path,
                                               num_threads=num_threads)

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __call__(
        self,
        landmark_list,
    ):
        input_details_tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([landmark_list], dtype=np.float32))
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]['index']

        result = self.interpreter.get_tensor(output_details_tensor_index)

        result_index = np.argmax(np.squeeze(result))

        return result_index





keypoint_classifier = KeyPointClassifier()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence,
    max_num_hands = 1,
    static_image_mode = False)

def flip_frame(frame):
    return cv.flip(frame, 1)

def frame_rgb_to_bgr(frame):
    return cv.cvtColor(frame, cv.COLOR_RGB2BGR)


class BeginTranslationSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "Begin Translation",*args, **kwargs)

        self.add_button(text="Return",command=lambda: self.master.set_page("home"))


class BeginTranslationContent(Content):
    def __init__(self, *args,  **kwargs):
            super().__init__(*args, **kwargs)
            self.grid_rowconfigure(0,weight=1)
            self.grid_columnconfigure(0,weight=1)
            

            self.label_list = []

            with open('./data/labels.csv', 'r') as f:
                reader = csv.reader(f)
                self.label_list= [row for row in reader]

            print(self.label_list)

            self.cap_width =900
            self.cap_height = 700
            self.canvas = Canvas(self, width = self.cap_width , height = self.cap_height)
            self.canvas.grid(row=0,column=0)


            
            self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
            self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.cap_width)
            self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.cap_height)
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_drawing_styles = mp.solutions.drawing_styles
            self.mp_hands = mp.solutions.hands



            if not self.cap.isOpened():
                raise IOError("Cannot open webcam")
            self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:

            frame = flip_frame(frame)
            

            frame.flags.writeable = False
            results = hands.process(frame)
            frame.flags.writeable = True

            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):

                    brect = utils.calc_bounding_rect(frame, hand_landmarks)
                    landmark_list = utils.calc_landmark_list(frame, hand_landmarks)
                    # Conversion to relative coordinates / normalized coordinates
                    pre_processed_landmark_list = utils.pre_process_landmark(
                        landmark_list)
                        

                    # Hand sign classification
                    hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                    print(hand_sign_id)


                    self.mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style())

            

            frame = frame_rgb_to_bgr(frame)
            #final render
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))

            self.canvas.create_image(0, 0, image = self.photo, anchor = "nw")
        self.after(15, self.update)