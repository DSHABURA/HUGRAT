import tkinter as tk



#Define tab/page functionality layout here


class Tab:
    def __init__(self,window, title:str = "Tab", geometry:str = "200x200"):
        self.window = window
        self.window.title(title)
        self.window.geometry(geometry)



