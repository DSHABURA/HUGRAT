from Sidebar import Sidebar
from Content import Content
from PIL import Image, ImageTk
import customtkinter as ct
import cv2
import mediapipe as mp

class NewDatasetSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "New Dataset",*args, **kwargs)
        self.add_button(text="Return",command=lambda: self.master.set_page("create_new_model"))
        #self.add_slider(label="Delay",from_=0,to=3,increment=0.25)





class NewDatasetContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        #label to capture video stream
        self.label = ct.CTkLabel(master=self)
        self.label.grid(row=0,column=0,sticky="nsew")
        self.cap =cv2.VideoCapture(0,cv2.CAP_DSHOW)

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands




        self.show_frame()
    def close(self):
        if self.cap:
            self.cap.release()

    
    '''def show_frame(self):
        with self.mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            while self.cap.isOpened():
                success,image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                image.flags.writeable=True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style())
                cv2image = cv2.resize(image,(640,480))
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
                self.label.after(10, self.show_frame)'''

        # Get the latest frame and convert into Image
        #cv2image= cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
        #cv2image = cv2.resize(cv2image, (self.webw, self.webh))
        #img = Image.fromarray(cv2image)
        # Convert image to PhotoImage
        #imgtk = ImageTk.PhotoImage(image = img)
        #self.label.imgtk = imgtk
        #self.label.configure(image=imgtk)
        # Repeat after an interval to capture continiously
        #self.label.after(20, self.show_frame)

    def show_frame(self):
        self.cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        with self.mp_hands.Hands(model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while self.cap.isOpened():
                success,image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                    
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                image.flags.writeable=True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style())
                cv2image = cv2.resize(image,(640,480))
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        self.cap.relase()