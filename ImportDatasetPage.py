from Sidebar import Sidebar
from Content import Content

class ImportDatasetSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "Import Dataset",*args, **kwargs)

        self.add_button(text="Return",command=lambda: self.master.set_page("create_new_model"))


class ImportDatasetContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
