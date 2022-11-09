import cv2
import tkinter as tk
from PIL import Image, ImageTk
class WebCamFrame:
    def __init__(self,frame):
        self.frame = frame
        self.frame_capture_label = tk.Label(self.frame)
        self.frame_capture_label.grid(row=0, column=0)
        self.cap_port = 0
        self.cap = cv2.VideoCapture(self.cap_port, cv2.CAP_DSHOW)
        self.show_frames()


    def show_frames(self):
        if self.cap:
            if self.cap.isOpened():
                # Get the latest frame and convert into Image
                #cv2image =self.cap.read()[1]
                cv2image= cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
                cv2image = cv2.flip(cv2image,1)
                self.last_frame = cv2image

                #mp_image = MediaPipeProcessing.get_gesture_overlay(copy.deepcopy(self.last_frame))
                img = Image.fromarray(cv2image)
                # Convert image to PhotoImage
                imgtk = ImageTk.PhotoImage(image = img)
                self.frame_capture_label.imgtk = imgtk
                self.frame_capture_label.configure(image=imgtk)
                # Repeat after an interval to capture continiously
                self.frame_capture_label.after(50, self.show_frames)
