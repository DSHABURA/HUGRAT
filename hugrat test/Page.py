from PageElement import PageElement
import tkinter as tk
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

    def hide(self):
        self.frame.grid_forget()


    def show(self):
        for c in self.content:
            self.render_element(c.type,**c.settings)
            c.debug()
        self.frame.grid(row=0,column=0)

    def render_element(self,type,**settings):
        element = None
        if type == tk.Label:
            element = tk.Label(self.frame)
        elif type==tk.Button:
            element = tk.Button(self.frame)
        elif type== tk.Entry:
            element =tk.Entry(self.frame)


        if settings.get("text") != None:
            element.configure(text= settings["text"])
        
        if settings.get("callback") !=None:
            element.configure(command= settings["callback"])
        
        if settings.get("row") !=None and settings.get("column") !=None:
            element.grid(row=settings["row"], column=settings["column"])
        else:
            element.grid(row=0,column=0)




