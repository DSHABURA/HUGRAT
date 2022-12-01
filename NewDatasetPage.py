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
import random



current_label = "TESTLABEL"
label_list = []
current_results = []
min_detection_confidence = 0.7
min_tracking_confidence = 0.7

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence,
    max_num_hands = 1,
    static_image_mode = False)

class NewDatasetSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "New Dataset",*args, **kwargs)
        self.add_button(text="Home",command=lambda: self.go_back())
        self.add_button(text="Finish",command = lambda: self.begin_training())
    
        self.label = None
        self.label_list = []

        self.label_field = ct.CTkEntry(self, width=20)
        self.label_field.grid(row=3, column=0, sticky="ew")


        self.error_label = ct.CTkLabel(self, text="", text_color= 'red')
        self.error_label.grid(row=6, column=0, sticky="ew")

        self.info_label = ct.CTkLabel(self, text="F1 to capture")
        self.info_label.grid(row=5, column=0, sticky="ew")

        self.capture_button = ct.CTkButton(self,text="Capture", command=lambda: self.capture(self.error_label))
        self.capture_button.grid(row=4,column=0,sticky="ew")
        self.master.bind('<F1>', lambda event: self.capture(self.error_label))


    def go_back(self):
        if self.webcam.cap:
            self.webcam.cap.release()
        self.master.set_page("home")

    def begin_training(self):
        if self.webcam.cap:
            self.webcam.cap.release()
        self.master.set_page("begin_training")
    def connect_webcam(self,webcam):
        self.webcam = webcam

    def capture(self, label):
        self.set_label(self.label_field.get())
        self.webcam.capture_data(label)
    
    def set_label(self, label):
        corrected_label = label.lower()
        if corrected_label and corrected_label not in self.label_list:
            self.label_list.append(corrected_label)
            #print(self.label_list.index(corrected_label))

        with open("./data/labels.csv", "w") as f:
            for label in self.label_list:
                f.write( label+ "\n")

        self.label = corrected_label
        self.webcam.label = corrected_label
        self.webcam.label_list = self.label_list

class NewDatasetContent(Content):
    def frame_rgb_to_bgr(self,frame):
        return cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    def frame_bgr_to_rgb(self,frame):
        return cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    def flip_frame(self,frame):
        return cv.flip(frame, 1)
    def calc_landmark_list(self,image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            # landmark_z = landmark.z

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point
    def calc_relative_landmarks(self,landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list





    def add_noise_items(self, landmark_list):
        #add noise:
        noise_landmark_list = copy.deepcopy(landmark_list)
        random.seed()
        for i in range(2, len(noise_landmark_list)):
            noise = random.uniform(-0.05, 0.05)
            noise_landmark_list[i] += noise

        return noise_landmark_list

    def logging_csv(self, label, relative_landmarks):
        csv_path = 'data/training_data.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(([label, *relative_landmarks]))


            for i in range(4):
                noise_landmark_list = self.add_noise_items(relative_landmarks)
                writer.writerow(([label, *noise_landmark_list]))

        return
    def capture_data(self, label):
        if self.label:
            self.logging_csv(self.label_list.index(self.label), self.relative_list)
        else:

            label.configure(text='Name required for capture')
   
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

        self.label = None
        self.label_list = []
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)


        #clear training data
        with open("./data/training_data.csv", "w") as f:
            f.write("")
        #clear labels
        with open("./data/labels.csv", "w") as f:
            f.write("")
            

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

            #frame pre-processing
            frame = self.frame_rgb_to_bgr(frame)
            frame = self.flip_frame(frame)

            #hand detection
            frame = self.frame_bgr_to_rgb(frame)
            frame.flags.writeable = False
            results = hands.process(frame)
            frame.flags.writeable = True

            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
                    
                    
                    #Convert from 0-1 to pixel coordinates (step 1)
                    landmark_list = self.calc_landmark_list(frame, hand_landmarks)
                    #convert to relative coordinates (step 2) (relative to wrist, or id 0)
                    #flattent to 1d array (step 3)
                    #normalize (step 4)
                    self.relative_list = self.calc_relative_landmarks(landmark_list)


                    #if the capture button is pressed, it will call capture_frame

                    self.mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style())

            

            frame = self.frame_rgb_to_bgr(frame)
            #final render
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))

            self.canvas.create_image(0, 0, image = self.photo, anchor = "nw")
        self.after(15, self.update)