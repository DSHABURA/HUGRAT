import tkinter as tk
import customtkinter as ct

from HomePage import HomeSidebar, HomeContent
from CreateNewModelPage import CreateNewModelSidebar, CreateNewModelContent
from NewDatasetPage import NewDatasetSidebar, NewDatasetContent
from ImportDatasetPage import ImportDatasetSidebar, ImportDatasetContent
from BeginTranslationPage import BeginTranslationSidebar, BeginTranslationContent
class App(ct.CTk):
    WIDTH = 780
    HEIGHT = 520
    RESIZABLE = False
    TITLE = "HUGRAT"
    def __init__(self):
        super().__init__()
        self.title(App.TITLE)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(App.RESIZABLE, App.RESIZABLE)
        self.iconbitmap("favicon.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Takes up any extra space vertically
        self.grid_rowconfigure(0, weight=1)
        #second column(the right right) takes up any extra space horizontally
        self.grid_columnconfigure(1,weight=1)
        
        self.content = None
        self.sidebar = None

        self.set_page("home")

    
    def on_closing(self, event=0):
        if self.content != None:
            self.content.close()
        if self.sidebar != None:
            self.sidebar.close()
        self.destroy()


    def set_page(self, page):

        self.page = page
        if self.content != None:
            self.content.close()
            self.content.grid_forget()
            self.content = None
        if self.sidebar != None:
            self.sidebar.close()
            self.sidebar.grid_forget()
            self.sidebar = None

        self.create_sidebar()
        self.create_content()

    def create_sidebar(self):
        if self.page == "home":
            self.sidebar = HomeSidebar(master=self)
        if self.page == "create_new_model":
            self.sidebar = CreateNewModelSidebar(master=self)
        if self.page == "new_dataset":
            self.sidebar = NewDatasetSidebar(master=self)
        if self.page == "import_dataset":
            self.sidebar = ImportDatasetSidebar(master=self)
        if self.page == "begin_translation":
            self.sidebar = BeginTranslationSidebar(master=self)
    def create_content(self):            
        if self.page == "home":
            self.content = HomeContent(master=self, fg_color="red")
        if self.page == "create_new_model":
            self.content = CreateNewModelContent(master=self,fg_color="blue")
        if self.page == "new_dataset":
            self.content = NewDatasetContent(master=self, fg_color="green")
            self.sidebar.connect_webcam(self.content)
        if self.page == "import_dataset":
            self.content = ImportDatasetContent(master=self, fg_color="yellow")
        if self.page == "begin_translation":
            self.content = BeginTranslationContent(master=self, fg_color="cyan")
        


if __name__ == "__main__":
    app = App()
    app.mainloop()