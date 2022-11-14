import customtkinter as ct
class Sidebar(ct.CTkFrame):
    def __init__(self,heading, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.content_count = 0
        self.heading = heading
        self.label = ct.CTkLabel(master=self, text=heading, text_font=("Roboto Medium", -16))
        self.label.grid(row=0,column=0)
        self.grid(row=0, column=0, sticky="nsew", padx=10)

    def set_heading(self,new_heading):
        self.heading = new_heading
        self.label.config(text=self.heading)

    def add_button(self,text,command):
        button = ct.CTkButton(master=self, text=text, command=command)
        button.grid(row=self.content_count+1,column=0,pady=10)
        self.content_count += 1

    def add_slider(self, from_=0, to=3,increment=0.25, command=lambda:print("implement slider"),label="Slider"):
        l = ct.CTkLabel(master=self, text=label)
        l.grid(row=self.content_count+1,column=0,pady=10)
        slider = ct.CTkSlider(master=self, from_=from_, to=to, increment=increment, command=command)
        slider.grid(row=self.content_count+1,column=1,pady=10)
        self.content_count += 1
    def close(self):
        pass

