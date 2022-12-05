from Sidebar import Sidebar
from Content import Content
from tkinter import Canvas
import cv2 as cv
import mediapipe as mp
from PIL import Image, ImageTk
import csv
import os
import customtkinter as ct
import utils
import tensorflow as tf
import numpy as np
from tkinter import filedialog as fd


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


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence,
    max_num_hands=1,
    static_image_mode=False)


def flip_frame(frame):
    return cv.flip(frame, 1)


def frame_rgb_to_bgr(frame):
    return cv.cvtColor(frame, cv.COLOR_RGB2BGR)


class BeginTranslationSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading="Begin Translation", *args, **kwargs)

        self.add_button(text="Home", command=lambda: self.back())

    def connect_webcam(self, webcam):
        self.webcam = webcam

    def back(self):
        try:
            if self.webcam.cap:
                self.webcam.cap.release()
            self.master.set_page("home")
        except:
            self.master.set_page("home")


class BeginTranslationContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        f = fd.askopenfilename(initialdir="./data/", title="Select model file",
                               filetypes=((".tflite", "*.tflite"), ("all files", "*.*")))

        self.keypoint_classifier = KeyPointClassifier(model_path=f)

        self.label_list = []
        self.keypoint_classifier_labels = []

        # Read labels ###########################################################
        with open(os.path.dirname(os.path.abspath(f)) + "/labels.csv", encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [
                row[0] for row in self.keypoint_classifier_labels
            ]

        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)

        self.canvas = Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")

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
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):

                    brect = utils.calc_bounding_rect(frame, hand_landmarks)
                    landmark_list = utils.calc_landmark_list(
                        frame, hand_landmarks)
                    # Conversion to relative coordinates / normalized coordinates
                    pre_processed_landmark_list = utils.pre_process_landmark(
                        landmark_list)

                    # Hand sign classification
                    hand_sign_id = self.keypoint_classifier(
                        pre_processed_landmark_list)

                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style())

                    frame = draw_info_text(
                        frame, brect, handedness, self.keypoint_classifier_labels[hand_sign_id])

            frame = frame_rgb_to_bgr(frame)
            # final render
            frame = cv.resize(frame, (self.canvas.winfo_width(), self.canvas.winfo_height()))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.after(15, self.update)


def draw_info_text(image, brect, handedness, hand_sign_text):
    #cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
     #            (0, 0, 0), -1)

    info_text = handedness.classification[0].label[0:]
    if hand_sign_text != "":
        info_text = info_text + ':' + hand_sign_text
    #cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
     #          cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

    h,w,c = image.shape
    offset = int(h/20)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.rectangle(image, (0,0),(w,offset),(0,0,0),-1)
    cv.putText(image, info_text, (20,offset-5), font, 0.6, (255,255,255),1,cv.LINE_AA)
    
    #cv.putText(image, info_text, (int(image.shape[1]/2),15),cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
    return image
 