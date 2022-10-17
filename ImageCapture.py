from Tab import Tab
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import MediaPipeProcessing
import numpy as np
import copy


class ImageCapture(Tab):
    def __init__(self,window, title:str = "Tab", geometry:str = "200x200", port:int=0):
        super().__init__(window, title,geometry)
        self.window = window


        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.cap_port = port
        self.window.title(title)
        self.window.geometry(geometry)
        self.frame_capture_label = tk.Label(self.window)
        self.frame_capture_label.pack()
        self.last_frame = None
        self.frame_capture_index = 0
        self.last_frame_label = None


        self.cap = cv2.VideoCapture(self.cap_port, cv2.CAP_DSHOW)
        #gets the camera dimensions by taking a frame from the camera and checking the size
        cap_x,cap_y = self.get_image_size(self.cap.read()[1])


        #format the size as a string "x,y" that tkinter needs
        self.window.geometry(self.format_image_size(cap_x,cap_y+75))
        tk.Button(self.window, text="Capture Gesture",command=self.capture_gesture).pack()
        tk.Label(self.window, text="Label:").pack()
        self.label_input = tk.Text(self.window, height=5, width=20)
        self.label_input.pack()

        self.show_frames()


    def capture_gesture(self):
        self.last_frame_label = self.label_input.get(1.0, "end-1c")
        if self.last_frame_label:
            cv2image= cv2.cvtColor(self.last_frame,cv2.COLOR_RGB2BGR)
            cv2.imwrite("frames/"+str(self.frame_capture_index) +"_"+self.last_frame_label +".jpg", cv2image)
            #np.save("frames/"+str(self.frame_capture_index) +"_"+self.last_frame_label, self.last_frame)
           # np.savetxt("frames/"+str(self.frame_capture_index) +"_"+self.last_frame_label, self.last_frame[...,2],fmt="%d")
            self.frame_capture_index +=1
        else:
            print("empty label")
       # with open('gesture_frames+'+str(self.frame_capture_index), 'a') as f:
         #   f.write(str(self.last_frame))
        #self.frame_capture_index +=1
        #results = MediaPipeProcessing.process_frame(self.last_frame)
        #if results:
         #   print(results)
          #  for r in results:

            #with open('gestures.txt', 'a') as f:
             #   f.write(str(results))

    def get_image_size(self,frame):
        x = frame.shape[1]
        y = frame.shape[0]
        return x,y


    def format_image_size(self,x,y):
        return "{x}x{y}".format(x=x,y=y)
    def on_closing(self):
        self.cap.release()
        self.window.destroy()

    def show_frames(self):
        if self.cap:

            if self.cap.isOpened():
                # Get the latest frame and convert into Image
                #cv2image =self.cap.read()[1]
                cv2image= cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
                cv2image = cv2.flip(cv2image,1)
                self.last_frame = cv2image

                mp_image = MediaPipeProcessing.get_gesture_overlay(copy.deepcopy(self.last_frame))
                img = Image.fromarray(mp_image)
                # Convert image to PhotoImage
                imgtk = ImageTk.PhotoImage(image = img)
                self.frame_capture_label.imgtk = imgtk
                self.frame_capture_label.configure(image=imgtk)
                # Repeat after an interval to capture continiously
                self.frame_capture_label.after(50, self.show_frames)