import tkinter
import customtkinter
from PIL import Image, ImageTk
import cv2


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


        # ==== create two frames ====

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.sidebar_left.grid(row=0, column=0, sticky="nswe")

        self.content_right = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.content_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)




        self.change_page("home")


        # ==== sidebar_left ====
        #self.sidebar_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing

        #self.sidebar_label = customtkinter.CTkLabel(master=self.sidebar_left, text="Home", text_font=("Roboto Medium", -16)) #font name and size in px
        #self.sidebar_label.grid(row=1, pady=10, padx=10)

        #self.create_new_model_button = customtkinter.CTkButton(master=self.sidebar_left, text="Create New Model", command=self.replace_sidebar("create_new_model"))
        #self.create_new_model_button.grid(row=2, column=0, pady=10, padx=20)

        #self.begin_translation_button = customtkinter.CTkButton(master=self.sidebar_left, text="Begin Translation", command=self.button_event)
        #self.begin_translation_button.grid(row=3, column=0, pady=10, padx=20)

    def button_event(self):
        print("event")

    def change_page(self, page):
        self.replace_sidebar(page)
        self.replace_content(page)

    def replace_sidebar(self, new_sidebar):
        self.sidebar_left.grid_forget()
        self.sidebar_left = self.sidebar_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.sidebar_left.grid(row=0, column=0, sticky="nswe")
        if new_sidebar =="home":
            self.sidebar_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
            self.sidebar_label = customtkinter.CTkLabel(master=self.sidebar_left, text="Home", text_font=("Roboto Medium", -16)) #font name and size in px
            self.sidebar_label.grid(row=1, pady=10, padx=10)

            self.create_new_model_button = customtkinter.CTkButton(master=self.sidebar_left, text="Create New Model", command=lambda:self.change_page("create_new_model"))
            self.create_new_model_button.grid(row=2, column=0, pady=10, padx=20)

            self.begin_translation_button = customtkinter.CTkButton(master=self.sidebar_left, text="Begin Translation", command=lambda:self.change_page("begin_translation"))
            self.begin_translation_button.grid(row=3, column=0, pady=10, padx=20)

            return
        if new_sidebar == "create_new_model":
            self.sidebar_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
            self.sidebar_label = customtkinter.CTkLabel(master=self.sidebar_left, text="Create New Model", text_font=("Roboto Medium", -16)) #font name and size in px
            self.sidebar_label.grid(row=1, pady=10, padx=10)

            self.create_new_model_button = customtkinter.CTkButton(master=self.sidebar_left, text="Return", command=lambda:self.change_page("home"))
            self.create_new_model_button.grid(row=2, column=0, pady=10, padx=20)

            self.begin_translation_button = customtkinter.CTkButton(master=self.sidebar_left, text="Create Dataset", command=self.button_event)
            self.begin_translation_button.grid(row=3, column=0, pady=10, padx=20)

            self.begin_translation_button = customtkinter.CTkButton(master=self.sidebar_left, text="Import Dataset", command=self.button_event)
            self.begin_translation_button.grid(row=4, column=0, pady=10, padx=20)
            return

        if new_sidebar == "begin_translation":
            self.sidebar_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
            self.sidebar_label = customtkinter.CTkLabel(master=self.sidebar_left, text="Begin Translation", text_font=("Roboto Medium", -16)) #font name and size in px
            self.sidebar_label.grid(row=1, pady=10, padx=10)

            self.create_new_model_button = customtkinter.CTkButton(master=self.sidebar_left, text="Return", command=lambda:self.change_page("home"))
            self.create_new_model_button.grid(row=2, column=0, pady=10, padx=20)

            #self.begin_translation_button = customtkinter.CTkButton(master=self.sidebar_left, text="Choose Translation Model", command=self.button_event)
            #self.begin_translation_button.grid(row=3, column=0, pady=10, padx=20)
            #return


    def replace_content(self, new_content):
        self.content_right.grid_forget()
        self.content_right = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.content_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.content_right.grid_rowconfigure(0, weight=1)
        self.content_right.grid_columnconfigure(0,weight=1)
        if new_content == "home":
            pass
        if new_content == "begin_translation":


            def list_ports():
                #from https://stackoverflow.com/questions/57577445/list-available-cameras-opencv-python
                #
                #Test the ports and returns a tuple with the available ports and the ones that are working.
                #
                non_working_ports = []
                dev_port = 0
                working_ports = []
                available_ports = []
                while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
                    camera = cv2.VideoCapture(dev_port,cv2.CAP_DSHOW)
                    if not camera.isOpened():
                        non_working_ports.append(str(dev_port))
                        #print("Port %s is not working." %dev_port)
                    else:
                        is_reading, img = camera.read()
                        w = camera.get(3)
                        h = camera.get(4)
                        if is_reading:
                            #print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                            working_ports.append(str(dev_port))
                        else:
                            #print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                            available_ports.append(str(dev_port))
                    dev_port +=1
                return available_ports,working_ports,non_working_ports

            
            settings_frame = customtkinter.CTkFrame(master=self.content_right)


            settings_frame.grid(row=0, column=0, sticky="nswe",)


            webcam_frame = customtkinter.CTkFrame(master=self.content_right)

            webcam_frame.grid(row=1,column=0)


            combobox_label = customtkinter.CTkLabel(master=settings_frame, text="Webcam Port")
            combobox_label.grid(row=0, column=0)

            available_ports,working_ports,non_working_ports = list_ports()
            selected_port = customtkinter.StringVar(value="0")
            combobox = customtkinter.CTkComboBox(master =settings_frame,values = working_ports,variable = selected_port)
            combobox.grid(row=0, column = 1)

            delay_label = customtkinter.CTkLabel(master=settings_frame, text="Delay")
            delay_label.grid(row=1, column=0)

            delay = customtkinter.CTkSlider(master=settings_frame, from_ =0, to=5, number_of_steps=5)
            delay.grid(row=1, column=1)




    
            

            frame_label = tkinter.Label(webcam_frame)
            frame_label.grid(row=0,column=0)
            self.cap =cv2.VideoCapture(int(selected_port.get()))
            # Define function to show frame
            def show_frames():
                # Get the latest frame and convert into Image
                cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
                cv2image = cv2.resize(cv2image, (800, 650))
                img = Image.fromarray(cv2image)
                # Convert image to PhotoImage
                imgtk = ImageTk.PhotoImage(image = img)
                frame_label.imgtk = imgtk
                frame_label.configure(image=imgtk)
                # Repeat after an interval to capture continiously
                frame_label.after(20, show_frames)

            def start_cam():
                if self.cap:
                    self.cap.release()
                    self.cap =cv2.VideoCapture(int(selected_port.get()))
                    show_frames()

            start = customtkinter.CTkButton(master=settings_frame, text="Start Webcam" ,
            command=lambda:start_cam())
            start.grid(row=2,column=0)



            #create a label to caputre the video frames
            #frame_label = customtkinter.CTkLabel(master=self.content_right)
            #frame_label.grid(row=2, column=0, pady=20)
            #cap = cv2.VideoCapture(int(selected_port.get()))

            #def show_frames():
             #   cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
              #  cv2image = cv2.resize(cv2image,(self.content_right.winfo_width(),self.content_right.winfo_height()))
               # img = Image.fromarray(cv2image)
               # imgtk = ImageTk.PhotoImage(image = img)
               # frame_label.imgtk = imgtk
               # frame_label.configure(image=imgtk)
                
                #frame_label.after(20, show_frames)

          #  show_frames()


            #entry = customtkinter.CTkLabel(master= self.content_right,text="Text")
            #entry.grid(row=0, column=0)



if __name__ == "__main__":
    app = App()
    app.mainloop()