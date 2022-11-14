from Sidebar import Sidebar
from Content import Content
from PIL import Image, ImageTk
import customtkinter as ct
import cv2
import mediapipe as mp
from tkinter import NW,Tk,Canvas, PhotoImage

class NewDatasetSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "New Dataset",*args, **kwargs)
        self.add_button(text="Return",command=lambda: self.master.set_page("create_new_model"))

        self.add_button(text="Capture",command=lambda:self.webcam.capture())


    def connect_webcam(self,webcam):
        self.webcam = webcam
        #self.add_slider(label="Delay",from_=0,to=3,increment=0.25)





class NewDatasetContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self, width = 640, height = 480)
        self.canvas.grid(row=0,column=0)


        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.c_frame = None
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        self.update()

    def get_frame(self):
        if self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                return (success, cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB))
            else: return (success,None)
        else:
            return (success,None)

    def update(self):
        success, frame = self.get_frame()
        self.c_frame = frame
        if success:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.after(15, self.update)

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
    def capture(self):
        cv2.imwrite("./SavedGestures/Test/" + str(self.photo) +".png", self.c_frame)


    def close(self):
        self.release()


