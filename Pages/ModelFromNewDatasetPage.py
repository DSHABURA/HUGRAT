from Page import Page
from tkinter import *
from PIL import Image, ImageTk
import cv2
def _capture():
    pass


def create(app):
    model_from_new_dataset_page = Page(app.root, "New Model Setup")
    model_from_new_dataset_page.add_button(
        text="Return"
        , callback=lambda: app.show_page(app.home_page)
        , row=0
        , column=0
    )


   # model_from_new_dataset_page.add_button(
   #     text="Capture"
   #     , callback=lambda: _capture()
   #     , row=0
   #     , column = 1
    #)
    model_from_new_dataset_page.add_label(text="Delay:", row=1, column=0)
    model_from_new_dataset_page.add_spinbox(row=1, column=1, num_from=0, num_to=5, num_increment=1)

    model_from_new_dataset_page.add_label(text="Label:", row=2, column=0)
    model_from_new_dataset_page.add_entry(row=2, column=1)
    model_from_new_dataset_page.add_webcam()




    return model_from_new_dataset_page




