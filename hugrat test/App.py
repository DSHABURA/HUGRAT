import tkinter as tk
from Page import Page
class App:

    def create_pages(self):
        self.home = Page(self.root, "HUGRAT")
        self.create_model = Page(self.root,"Create Model" )
        self.import_dataset = Page(self.root, "Import Dataset")
        self.create_dataset = Page(self.root, "Create Dataset")
        self.choose_translation_model =Page(self.root, "Choose Translation Model")
        self

    def show_page(self,page):
        if self.current_page != None:
            self.current_page.hide()
        self.current_page = page
        self.current_page.show()
        self.root.title(self.current_page.title)
    def __init__(self):
        self.root = tk.Tk()
        self.current_page = None
        self.create_pages()
        self.home_page()
        self.create_model_page()
        self.choose_translation_model_page()





        self.show_page(self.home)

        self.root.mainloop()



    def home_page(self):
        self.home.add_button(
            text="Create Model"
            , callback=lambda: self.show_page(self.create_model)
            , row=0
            , column=0)
        
        self.home.add_button(
            text="Start Translation"
            , callback=lambda:self.show_page(self.choose_translation_model)
            , row=0
            , column=1)

    def create_model_page(self):
        self.create_model.add_button(
            text="Import Dataset"
            , callback = lambda:self.show_page(self.import_dataset)
            , row=0
            , column=0
        )
        self.create_model.add_button(
            text="Create Dataset"
            , callback = lambda:self.show_page(self.create_dataset)
            , row=0
            , column=1
        )
        self.create_model.add_button(
            text="Return"
            , callback=lambda: self.show_page(self.home)
            , row=1
            , column=0
        )

    def choose_translation_model_page(self):
        self.choose_translation_model.add_button(
            text="Return"
            , callback=lambda: self.show_page(self.home)
            , row=1
            , column=0
        )
        self.choose_translation_model.add_label(
            text="Directory"
            , row=0
            , column=0
        )
        self.choose_translation_model.add_entry( row=0, column=1)
        self.choose_translation_model.add_button(
            text="Confirm",
            callback = lambda:print("IMPLEMENT")
            , row=1 
            ,column=1
        )
