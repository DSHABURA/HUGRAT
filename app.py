import tkinter as tk
import video_capture
from ImageCapture import ImageCapture
from TabError import TabError
from PreviewMediaPipeImage import PreviewMediaPipeImage


#define main window logic here
class Window:
    def __init__(self,window, title:str = "Title", geometry:str = "200x200"):
        self.window = window
        self.window.title(title)
        self.window.geometry(geometry)
        image_capture_button = tk.Button(self.window, text="Start Image Capture", command=self.open_webcam).pack()
        preview_mp_image_button = tk.Button(self.window, text="Preview MediaPipe Image", command=self.preview_mp_image).pack()
        self.window.mainloop()
        pass

    def open_webcam(self):
        open_webcam_tab = None
        if video_capture.can_capture():
            open_webcam_tab =ImageCapture(tk.Toplevel(self.window), "Image Capture", "400x400")
        else:
            open_webcam_tab =TabError(tk.Toplevel(self.window), error_string ="No Available Ports Found.")

    def preview_mp_image(self):
        # numpy.fromfile("frames/0_test.npy", -1, sep="", offset=0)
        pmpi_tab = PreviewMediaPipeImage(tk.Toplevel(self.window), "Image Preview", "400x400", path="frames/0_Wave.jpg")

    








def main():
    root = tk.Tk()
    main = Window(root, "Home", "300x300")

    return None


main()
