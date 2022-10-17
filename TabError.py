from Tab import Tab
import tkinter as tk

class TabError(Tab):
    def __init__(self,window, title:str = "Error", geometry:str ="250x50", error_string:str = "An error occured."):
        super().__init__(window, title,geometry)
        self.error_string = error_string
        tk.Label(self.window,text=self.error_string).pack()
