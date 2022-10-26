import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import video_capture
from ImageCapture import ImageCapture
from TabError import TabError
from PreviewMediaPipeImage import PreviewMediaPipeImage
import sys



class AppFrame:
    def __init__(self, window, parent,goback):
        self.parent = parent
        self.window = window
        self.goback = goback
        self.frame = tk.Frame(self.window)
        self.content = {}

    def add_button(self,text="Button", side=tk.LEFT, callback=lambda:print("Implement BUTTON")):
        new_button = tk.Button(self.frame, text=text,command=callback)
        new_button.pack(side=side)
        new_button.pack_forget()
        self.content[new_button] ={}
        self.content[new_button]["side"] = side
        return new_button

    def render_frame(self):
        for thing in self.content:
            thing.pack(side=self.content[thing]["side"])
        self.frame.pack()

    def go_back(self):
        self.parent.set_frame(self.goback)


class HomeFrame(AppFrame):
    def __init__(self,window,parent,goback):
        super().__init__(window,parent,goback)

        self.new_model_button = self.add_button(text="Create New Model", callback=lambda:parent.set_frame(parent.newModelSetupFrame))
        self.start_translation_button = self.add_button(text="Start Translation", callback=lambda:self.choose_model_directory())

    def choose_model_directory(self):
        self.file_name = filedialog.askopenfilename(initialdir="/", title="Choose Model Directory", filetypes=[("All types", "*.*")])

class NewModelSetupFrame(AppFrame):
    def __init__(self,window,parent,goback):
        super().__init__(window,parent,goback)

        self.import_dataset_button = self.add_button(text="Import Dataset", callback=lambda:parent.set_frame(parent.importDatasetFrame))
        self.create_new_dataset_button = self.add_button(text="Create New Dataset", callback=lambda:parent.set_frame(parent.createNewDatasetFrame))

        self.return_button =self.add_button(text="Back", callback=lambda:self.go_back())


    def open_webcam(self):
        open_webcam_tab = None
        if video_capture.can_capture():
            open_webcam_tab =ImageCapture(tk.Toplevel(self.window), "Image Capture", "400x400")
        else:
            open_webcam_tab =TabError(tk.Toplevel(self.window), error_string ="No Available Ports Found.")

class ImportDatasetFrame(AppFrame):
    def __init__(self,window,parent,goback):
        super().__init__(window,parent,goback)
        self.dataset_directory_name =tk.StringVar(self.frame)
        self.dataset_directory_location = None
        self.dataset_directory_label = tk.Label(self.frame, text="Dataset Directory").pack(side=tk.LEFT)
        self.dataset_directory_input = ttk.Entry(self.frame, textvariable=self.dataset_directory_name).pack(side=tk.LEFT)
        self.dataset_directory_button = self.add_button(text="Open Folder", callback=lambda:self.choose_dataset_directory())
        self.return_button =self.add_button(text="Back",callback=lambda:self.go_back(), side=tk.BOTTOM).pack(anchor=tk.W)
        self.confirm_button = self.add_button(text="Confirm", side=tk.BOTTOM,callback=lambda:parent.set_frame(parent.beginTrainingFrame)).pack(anchor=tk.W)




    def choose_dataset_directory(self):
        filename = filedialog.askdirectory(initialdir="/", title="Choose Dataset Directory")
        self.dataset_directory_name.set(filename)



class CreateNewDatasetFrame(AppFrame):
    def __init__(self,window,parent,goback):
        super().__init__(window,parent,goback)
        self.return_button =self.add_button(text="Back", callback=lambda:self.go_back())




class BeginTrainingFrame(AppFrame):
    def __init__(self,window,parent,goback):
        super().__init__(window,parent,goback)
        self.return_button =  self.add_button(text="Back", callback=lambda:self.go_back())

    def go_back(self):
        if self.parent.last_frame == self.parent.importDatasetFrame:
            self.parent.set_frame(self.parent.importDatasetFrame)
        if self.parent.last_frame == self.parent.createNewDatasetFrame:
            self.parent.set_frame(self.parent.createNewDatasetFrame)



#define main window logic here
class Window:
    def set_frame(self, new_frame_obj):            
        self.last_frame = self.current_frame_obj
        if self.current_frame_obj != None:
            self.current_frame_obj.frame.pack_forget()
        self.current_frame_obj = new_frame_obj
        self.current_frame_obj.render_frame()

    def setup_pages(self):
        self.homeFrame = HomeFrame(self.window, parent=self, goback=None)
        self.newModelSetupFrame = NewModelSetupFrame(self.window,parent=self, goback = self.homeFrame)
        self.importDatasetFrame = ImportDatasetFrame(self.window,parent=self,goback = self.newModelSetupFrame)
        self.createNewDatasetFrame = CreateNewDatasetFrame(self.window,parent=self, goback = self.newModelSetupFrame)
        self.beginTrainingFrame= BeginTrainingFrame(self.window,parent=self, goback=None)
        
    def __init__(self,window, title:str = "Title", geometry:str = "200x200"):
        self.last_frame = None
        self.current_frame_obj = None
        self.window = window
        self.window.title(title)
        self.window.geometry(geometry)
        self.setup_pages()
        self.set_frame(self.homeFrame)

        self.window.mainloop()





    #def preview_mp_image(self):
        # numpy.fromfile("frames/0_test.npy", -1, sep="", offset=0)
     #   pmpi_tab = PreviewMediaPipeImage(tk.Toplevel(self.window), "Image Preview", "400x400", path="frames/0_Wave.jpg")



    

def main():
    root = tk.Tk()
    main = Window(root, "HuGRAT", "300x300")

    return None
    
main()