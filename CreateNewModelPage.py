from Sidebar import Sidebar
from Content import Content

class CreateNewModelSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "Create New Model",*args, **kwargs)

        self.add_button(text="Return",command=lambda: self.master.set_page("home"))
        self.add_button(text="New Dataset",command=lambda: self.master.set_page("new_dataset"))
        #self.add_button(text="Import Dataset", command=lambda: self.master.set_page("import_dataset"))

        

class CreateNewModelContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
