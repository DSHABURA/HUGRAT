import tkinter
import os
from tkinter import ttk
import customtkinter
class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520
    RESIZABLE = False
    TITLE = "HUGRAT"
    def __init__(self):
        super().__init__()
        self.title(App.TITLE)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(App.RESIZABLE, App.RESIZABLE)
        
        self.content = None
        self.sidebar = None

        self.set_page("home")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)

    def set_page(self,page):
        self.page = page
        self.create_sidebar()
        self.create_content()

    def create_sidebar(self):
        _master = self
        _corner_radius = 0
        if self.sidebar != None:
            self.sidebar.grid_forget()
            self.sidebar = None

        if self.page == "home":
            self.sidebar = HomeSidebar(master=_master,corner_radius=_corner_radius)
        if self.page == "create_new_model":
            self.sidebar = CreateNewModelSidebar(master=_master, corner_radius = _corner_radius)
        if self.page == "new_dataset":
            self.sidebar = NewDatasetSidebar(master=_master, corner_radius=_corner_radius)
        if self.page == "import_dataset":
            self.sidebar = ImportDatasetSidebar(master=_master, corner_radius = _corner_radius)

        self.sidebar.grid(row=0, column=0,sticky="nsew",padx=10)
        pass
    def create_content(self):
        _master = self
        
        if self.content != None:
            self.content.grid_forget()
            self.content = None

        if self.page == "home":
            self.content = HomeContent(master=_master, fg_color="red")
        if self.page == "create_new_model":
            self.content = CreateNewModelContent(master=_master,fg_color="blue")
        if self.page == "new_dataset":
            self.content = NewDatasetContent(master=_master, fg_color="green")
        if self.page == "import_dataset":
            self.content = ImportDatasetContent(master=_master, fg_color="yellow")
        self.content.grid(row=0, column=1, sticky="nsew", padx=2)
        pass

class HomeContent(customtkinter.CTkFrame):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

class HomeSidebar(customtkinter.CTkFrame):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        #self.grid_rowconfigure(3,weight=1)
        self.grid_columnconfigure(0,weight=1)

        label = customtkinter.CTkLabel(master=self,text="Home",text_font=("Roboto Medium", -16))
        label.grid(row=0,column=0,pady=10)

        self.grid_rowconfigure(1, minsize=60) #empty row for spacing
    
        create_new_model_button = customtkinter.CTkButton(master=self, text="Create New Model", command=lambda:self.master.set_page("create_new_model"))
        create_new_model_button.grid(row=2, column=0,pady=20)

        begin_translation_button = customtkinter.CTkButton(master=self, text="Begin Translation")
        begin_translation_button.grid(row=3,column=0,pady=10)

class CreateNewModelContent(customtkinter.CTkFrame):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0,weight=1)

class CreateNewModelSidebar(customtkinter.CTkFrame):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0,weight=1)

        label = customtkinter.CTkLabel(master=self,text="Create New Model",text_font=("Roboto Medium", -16))
        label.grid(row=0,column=0,pady=10)

        self.grid_rowconfigure(1, minsize=60) #empty row for spacing
    
        return_button = customtkinter.CTkButton(master=self, text="Return", command=lambda:self.master.set_page("home"))
        return_button.grid(row=2, column=0,pady=20)

        create_new_model_button = customtkinter.CTkButton(master=self, text="New Dataset", command=lambda:self.master.set_page("new_dataset"))
        create_new_model_button.grid(row=3, column=0,pady=20)

        begin_translation_button = customtkinter.CTkButton(master=self, text="Import Dataset", command=lambda:self.master.set_page("import_dataset"))
        begin_translation_button.grid(row=4,column=0,pady=10)

class NewDatasetContent(customtkinter.CTkFrame):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        label = customtkinter.CTkLabel(master=self, text="TEST")
        label.grid(row=0,column=0)

class NewDatasetSidebar(customtkinter.CTkFrame):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0,weight=1)

        label = customtkinter.CTkLabel(master=self,text="New Dataset",text_font=("Roboto Medium", -16))
        label.grid(row=0,column=0,pady=10)

        self.grid_rowconfigure(1, minsize=60) #empty row for spacing
    
        create_new_model_button = customtkinter.CTkButton(master=self, text="Return", command=lambda:self.master.set_page("create_new_model"))
        create_new_model_button.grid(row=2, column=0,pady=20)


class ImportDatasetContent(customtkinter.CTkFrame):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        path = "SavedGestures"
      #  self.grid_rowconfigure(0,weight=1)
        labelpreview_frame = customtkinter.CTkFrame(master=self)
        labelpreview_frame.grid(row=0,column=0,sticky="ns")

        ri=0
        for file in os.listdir("./SavedGestures"):
            label = customtkinter.CTkLabel(master = labelpreview_frame,text = file)
            label.grid(row=ri,column=0)
            if os.path.isdir("./SavedGestures/"+file):
                count = 0
                for innerfile in os.listdir("./SavedGestures/"+file):
                    count +=1
                countlabel = customtkinter.CTkLabel(master=labelpreview_frame, text = str(count))
                countlabel.grid(row=ri, column=1)
                action = customtkinter.CTkButton(master=labelpreview_frame, text="Preview", command=lambda:print("implement this"))
                action.grid(row=ri, column=2)

            ri+=1
           # d = os.path.join("./SavedGestures", file)
            #if os.path.isdir(d):
             #   print(d)
                #label = customtkinter.CTkLabel(text=)

class ImportDatasetSidebar(customtkinter.CTkFrame):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0,weight=1)

        label = customtkinter.CTkLabel(master=self,text="Import Dataset",text_font=("Roboto Medium", -16))
        label.grid(row=0,column=0,pady=10)

        self.grid_rowconfigure(1, minsize=60) #empty row for spacing
    
        create_new_model_button = customtkinter.CTkButton(master=self, text="Return", command=lambda:self.master.set_page("create_new_model"))
        create_new_model_button.grid(row=2, column=0,pady=20)

app = App()
app.mainloop()