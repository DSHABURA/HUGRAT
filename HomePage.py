import customtkinter as ct
from Sidebar import Sidebar
from Content import Content

class HomeSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "Home",*args, **kwargs)

        self.add_button(text="Create New Model",command=lambda: self.master.set_page("new_dataset"))
        self.add_button(text="Begin Translation", command=lambda: self.master.set_page("begin_translation"))





class HomeContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.welcome_label = ct.CTkLabel(self, text="Welcome to the HUGRAT translation software.")
        self.welcome_label.grid(row=0, column=0, sticky="nsew")
