from Sidebar import Sidebar
from Content import Content
from PIL import Image, ImageTk
import customtkinter as ct
import cv2
import mediapipe as mp
from tkinter import NW,Tk,Canvas, PhotoImage
import copy

class NewDatasetSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "New Dataset",*args, **kwargs)
        self.add_button(text="Return",command=lambda: self.master.set_page("create_new_model"))

        self.add_button(text="Capture",command=lambda:self.webcam.capture())


    def connect_webcam(self,webcam):
        self.webcam = webcam





class NewDatasetContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self, width = 640, height = 480)
        self.canvas.grid(row=0,column=0)


        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.c_frame = None
        self.m_frame = None
        
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands


        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        self.update()

    def get_frame(self):
        if self.cap.isOpened():
            success, frame = self.cap.read()
            self.c_frame = cv2.flip(copy.deepcopy(frame),1)
            if success:
                with self.mp_hands.Hands(model_complexity=1,min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
                    frame.flags.writeable=False
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(frame)
                    frame.flags.writeable=True
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                    if results.multi_hand_landmarks:
                        self.m_frame = results.multi_hand_landmarks
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(
                                        frame,
                                        hand_landmarks,
                                        self.mp_hands.HAND_CONNECTIONS,
                                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                        self.mp_drawing_styles.get_default_hand_connections_style())
                            

                        
                    return (success, cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB))
            else: return (success,None)
        else:
            return (success,None)

    def update(self):
        success, frame = self.get_frame()
        if success:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.after(15, self.update)

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
    def capture(self):
        data_string = ""
        if self.m_frame:
            hand_count = 0
            for hand in self.m_frame:
                data_string +="\n"
                data_string += "label,"
                data_string += str(hand_count) + ","
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(hand_count)
                hand_count +=1
                hand_landmarks = hand.landmark
                for landmark in hand_landmarks:
                    data_string += str(round(landmark.x,3)) + "," + str(round(landmark.y,3)) +","
            #data_string +="\n"
        #data_string += "\n"

        with open('./data/training_data.csv','a') as fd: fd.write(data_string)          

    def get_landmarks(self):
        if self.m_frame:
            return self.m_frame
    def close(self):
        self.release()


