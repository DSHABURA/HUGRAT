import tkinter as tk






# class App:
#     def __init__(self):
#         self.current_page = None
#         self.root = tk.Tk()
#         self.root.title("Human Gesture Recognition And Translation")
#         self.root.geometry("200x200")

#         self.create_home()
#         self.create_create_new_model_page
#         self.show(self.home)
#         self.root.mainloop()

#     def show(self, page):
#         if self.current_page:
#             self.current_page.frame.grid_forget()
#             self.current_page = page
#             self.current_page.frame.grid(row=0, column=0)
#         else:
#             self.current_page = page
#             self.current_page.frame.grid(row=0,column=0)
    
#     def title(self, text=""):
#         self.root.title(text)



#     def create_home(self):
#         self.home = Page(self)
#         self.home.create_button(row=0,
#         column=0, 
#         text="Create New Model",
#         callback =lambda:self.create_new_model_page.show())

#         self.home.create_button(row=0,column=1, text="Start Translation")
        
        
#     def create_create_new_model_page(self):
#         self.create_new_model_page = Page(self)

#         self.create_new_model_page.create_button(row=0,
#         column= 0,
#         text="Import Existing Dataset",
#         callback = lambda:self.import_existing_dataset_page.show()
#         )

#         self.create_new_model_page.create_button(
#             row=0,
#             column=1,
#             text="Create New Dataset",
#             callback=lambda:self.create_new_dataset_page.show()
#         )
        

#     def create_import_existing_dataset_page(self):



# class Page:
#     def create_button():
#         pass
#     def __init__(self, app):
#         self.app = app
#         self.frame = tk.Frame(self.app.root)
#         self.app.root.title("Page")
        

#     def show(self):
#         self.app.show(self)



#     def create_button(self, row=0,column=0,text="BUTTON", callback=lambda:print("implement this button")):
#         button = tk.Button(self.frame, text=text, command=callback)
#         button.grid(row=row,column=column)


class App:
    def __init__(self):
        self.current_page = None
        self.root = tk.Tk()
        self.pages = {}

    def create_page(self, name,title):
        self.pages[name] = Page(self.root,title)

    def run(self):
        self.root.mainloop()

    def show(self,page):
        if self.current_page == None:
            self.current_page = page
            self.current_page.show()
        else:
            self.current_page.hide()
            self.current_page = page
            self.current_page.show()
        #if self.current_page:
         #   self.current_page.hide()
        #self.current_page = page
        #self.current_page.show()
        #print(self.current_page.title)
            


class Page:
    
    def __init__(self,root,title):
        self.title = title
        self.frame = tk.Frame(root)
        self.content = {}
        #print(title)

    def create_button(self, text, button_name,row=0, column=0):
        button = tk.Button(text=text)
        self.content[button] = { 
            "e_name":button_name,
            "row":row, 
            "column":column
            }

    def set_button_callback(self,button_name,callback):
        button = self.get_content(button_name)
        button.configure(command=callback)


    def get_content(self, e_name):
        for e in self.content:
            if self.content[e]["e_name"] == e_name:
                return e
            


    def show(self):
        self.frame.grid(row=0,column = 0)
        for element in self.content:
            element.grid(
                row=self.content[element]["row"],
                column = self.content[element]["column"])
    def hide(self):
        for element in self.content:
           element.grid_forget()
        self.frame.grid_forget()