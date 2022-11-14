from Sidebar import Sidebar
from Content import Content

class BeginTranslationSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "Begin Translation",*args, **kwargs)

        self.add_button(text="Return",command=lambda: self.master.set_page("home"))


class BeginTranslationContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
