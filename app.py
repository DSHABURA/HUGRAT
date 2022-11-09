import tkinter as tk
from Page import Page
from Pages import HomePage
from Pages import NewModelPage
from Pages import ChooseTranslationModelPage
from Pages import ModelFromNewDatasetPage
class App:
    def show_page(self,page):
        if self.current_page != None:
            self.current_page.hide()
        self.current_page = page
        self.current_page.show()
        self.root.title(self.current_page.title)

    def create_pages(self):
        self.home_page = HomePage.create(self)
        self.new_model_page = NewModelPage.create(self)
        self.choose_translation_model_page = ChooseTranslationModelPage.create(self)
        self.model_from_new_dataset_page = ModelFromNewDatasetPage.create(self)

        pass

    def __init__(self):
        self.root = tk.Tk()
        self.current_page = None
        self.create_pages()
        self.show_page(self.home_page)
        self.root.mainloop()