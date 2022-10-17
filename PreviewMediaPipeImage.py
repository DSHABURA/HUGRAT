from Tab import Tab
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import MediaPipeProcessing
import numpy as np
import copy


class PreviewMediaPipeImage(Tab):
    def __init__(self,window, title:str = "Tab", geometry:str = "200x200", path=""):
        super().__init__(window, title,geometry)
        self.window = window
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.title(title)
        self.window.geometry(geometry)
        self.path = path
        self.arr = np.fromfile(self.path, count=-1, sep="", offset=0)

        self.frame_capture_label = tk.Label(self.window)
        self.frame_capture_label.pack()
        self.print_image()


    def print_image(self):
        img = cv2.imread(self.path)
        img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
      #  img = Image.fromarray(img)
       # print(self.arr)
       #self.arr.reshape()
        #img = Image.fromarray(self.arr)
        #print(img)
        #if img.mode != 'RGB':
        #    img = img.convert('RGB')
       # img.save("frames/test.jpg")
        # Convert image to PhotoImage
        #imgtk = ImageTk.PhotoImage(image = img)
        #self.frame_capture_label.imgtk = imgtk
        #self.frame_capture_label.configure(image=imgtk)
        #self.frame_capture_label.after(50, self.print_image)


                # Get the latest frame and convert into Image
        #cv2image =self.cap.read()[1]
       # cv2image= cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
       # cv2image = cv2.flip(cv2image,1)
       # self.last_frame = cv2image

        mp_image = MediaPipeProcessing.get_gesture_overlay(copy.deepcopy(img))
        mp_image = Image.fromarray(mp_image)
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image = mp_image)
        self.frame_capture_label.imgtk = imgtk
        self.frame_capture_label.configure(image=imgtk)
        # Repeat after an interval to capture continiously
        self.frame_capture_label.after(50, self.show_frames)

    def on_closing(self):
        self.window.destroy()



