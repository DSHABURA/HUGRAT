from PageElement import PageElement
import tkinter as tk
import cv2
from WebcamFrame import WebCamFrame
class Page:
    def __init__(self, root, title):
        #self.size = size
        self.title = title
        self.content = []
        self.root = root
        self.frame = tk.Frame(self.root)
        #self.root.geometry(size)


    def add_label(self,text, row, column):
        self.content.append(PageElement(type=tk.Label, 
        settings = {"text":text, "row":row, "column":column}
        ))
    def add_button(self, text, callback, row, column):
        self.content.append(PageElement(type=tk.Button, settings={
            "text":text,
            "callback":callback,
            "row":row,
            "column":column
        }))
    def add_entry(self, row, column):
        self.content.append(PageElement(type=tk.Entry, settings={
            "row":row,
            "column":column
        }))

    def add_spinbox(self, row, column, num_from, num_to, num_increment):
        self.content.append(PageElement(type = tk.Spinbox, settings = {
            "row":row,
            "column":column,
            "num_from":num_from,
            "num_to":num_to,
            "num_increment":num_increment
        }))

    def add_webcam(self):
        webcam = WebCamFrame(self.frame)
       # self.content.append(PageElement(type="webcam", settings = {}))

    def hide(self):
        self.frame.grid_forget()


    def show(self):
        for c in self.content:
            self.render_element(c.type,**c.settings)
            #c.debug()
        self.frame.grid(row=0,column=0)

    def render_element(self,type,**settings):
        element = None
        if type == tk.Label:
            element = tk.Label(self.frame)
        elif type==tk.Button:
            element = tk.Button(self.frame)
        elif type== tk.Entry:
            element =tk.Entry(self.frame)
        elif type== tk.Spinbox:
            element = tk.Spinbox(self.frame)
        #elif type=="webcam":
         #   element = WebCamFrame(self.frame)

            #self.frame.grid_forget()
            #self.frame.pack()
            #element = webcam.Box(self.root, width=100, height=100)
            #element.show_frames()
            #return


        if settings.get("text") != None:
            element.configure(text= settings["text"])
        
        if settings.get("callback") !=None:
            element.configure(command= settings["callback"])

        if settings.get("num_from") != None and settings.get("num_to")!= None and settings.get("num_increment")!=None:
            element.configure(from_ = settings["num_from"], to=settings["num_to"])

        
        if settings.get("row") !=None and settings.get("column") !=None:
            element.grid(row=settings["row"], column=settings["column"])
        else:
            element.grid(row=0,column=0)





