class PageElement:
    def __init__(self,type=None, settings = {
        "text":None,
        "row":None,
        "column":None,
        "callback":None,
        "num_to":None,
        "num_from":None,
        "num_increment":None
    }):
        self.type = type
        self.settings = settings

    


    def debug(self):
        print(self.type)
        print(self.settings)
