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


min_detection_confidence = 0.7
min_tracking_confidence = 0.7

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence,
    max_num_hands = 1,
    static_image_mode = False)

class BeginTranslationSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "Begin Translation",*args, **kwargs)

        self.add_button(text="Return",command=lambda: self.master.set_page("home"))


class BeginTranslationContent(Content):
    def __init__(self, *args,  **kwargs):
            super().__init__(*args, **kwargs)
            self.grid_rowconfigure(0,weight=1)
            self.grid_columnconfigure(0,weight=1)


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
            frame.flags.writeable = False
            results = hands.process(frame)
            frame.flags.writeable = True

            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
                    self.mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style())

            


            #final render
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))

            self.canvas.create_image(0, 0, image = self.photo, anchor = "nw")
        self.after(15, self.update)