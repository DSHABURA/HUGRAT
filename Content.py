import customtkinter as ct
class Content(ct.CTkFrame):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=1, sticky="nsew", padx=2)
    def close(self):
        pass