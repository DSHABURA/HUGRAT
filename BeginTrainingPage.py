from Sidebar import Sidebar
from Content import Content
import customtkinter as ct
import csv
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tkinter import filedialog
import os
import shutil



def start_training(name):
    RANDOM_SEED = 42

    dir = './data/' + name
    print(dir)

    dataset = './data/training_data.csv'
    labelset = './data/labels.csv'
    model_save_path = dir + '/classifier.hdf5'
    tflite_save_path = dir + '/classifier.tflite'
    NUM_CLASSES = sum(1 for row in csv.reader(open(labelset)))

    #dataset reading
    X_dataset = np.loadtxt(dataset, delimiter=',', dtype='float32', usecols=list(range(1, (21 * 2) + 1)))
    y_dataset = np.loadtxt(dataset, delimiter=',', dtype='int32', usecols=(0))
    X_train, X_test, y_train, y_test = train_test_split(X_dataset, y_dataset, train_size=0.75, random_state=RANDOM_SEED)


    #model building
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input((21 * 2, )),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(20, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    print(model.summary())  # tf.keras.utils.plot_model(model, show_shapes=True)
    # Model checkpoint callback
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
    model_save_path, verbose=1, save_weights_only=False)
    # Callback for early stopping
    es_callback = tf.keras.callbacks.EarlyStopping(patience=20, verbose=1)

    # Model compilation
    model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
    )

    model.fit(
    X_train,
    y_train,
    epochs=1000,
    batch_size=128,
    validation_data=(X_test, y_test),
    callbacks=[cp_callback, es_callback]
    )
    # Model evaluation
    val_loss, val_acc = model.evaluate(X_test, y_test, batch_size=128)


    # Loading the saved model
    model = tf.keras.models.load_model(model_save_path)

    # Inference test
    predict_result = model.predict(np.array([X_test[0]]))
    #print(np.squeeze(predict_result))
    #print(np.argmax(np.squeeze(predict_result)))


    # Save as a model dedicated to inference
    model.save(model_save_path, include_optimizer=False)


    # Transform model (quantization)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_quantized_model = converter.convert()


    f = filedialog.asksaveasfile(initialfile=name + '.tflite', initialdir=dir, defaultextension=".tflite", filetypes=[("TFLite", "*.tflite")])
    
    print("============")
    #print(f.name)
    #print(os.path.splitext(f.name)[0])
    shutil.copy("./data/labels.csv", dir + "/labels.csv")
    shutil.copy("./data/training_data.csv", dir + "/training_data.csv")
    #shutil.copyfile("./data/labels.csv", )
    print("=============")
    tflite_save_path = f.name
    open(tflite_save_path, 'wb').write(tflite_quantized_model)
    



class BeginTrainingSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "Train New Model",*args, **kwargs)

        self.add_button(text="Cancel",command=lambda: self.master.set_page("home"))

        self.name_label = ct.CTkLabel(self, text="Model Name:")
        self.name_label.grid(row=2, column=0, sticky="ew")
        self.label_field = ct.CTkEntry(self, width=20)
        self.label_field.grid(row=3, column=0, sticky="ew")


        self.start_training_button = ct.CTkButton(self,text="Start Training", command=lambda: self.nameCheck())
        self.start_training_button.grid(row=4,column=0,sticky="ew")
        self.error_label = ct.CTkLabel(self, text=":")
        self.error_label.grid(row=5, column=0, sticky="ew")
        #self.add_button(text="Start Training",command=lambda: start_training())
    def nameCheck(self):
        name=self.label_field.get()
        dir = './data/' + name
        self.error_label.configure(text = '')
        if(name == ""):
            self.name_label.configure(text_color = 'Red')
            self.error_label.configure(text = 'Must have a model name')
        else: 
            if(os.path.exists(dir)):
                self.error_label.configure(text = 'Model name already exists')
            else:
                start_training(name = name)


        

class BeginTrainingContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)


        self.wait_label = ct.CTkLabel(self, text="Click 'Start Training' to begin training a new model. This may take a while.")
        self.wait_label.grid(row=0, column=0, sticky="nsew")

        self.wait_label2 = ct.CTkLabel(self, text="Once training is complete, you will be prompted to save the model.")
        self.wait_label2.grid(row=1, column=0, sticky="nsew")

        self.wait_label3 = ct.CTkLabel(self, text="You must save the model in a new folder.")
        self.wait_label3.grid(row=2,column=0, sticky="nsew")

        self.wait_label4 = ct.CTkLabel(self, text="While training, the program may appear to be frozen. This is normal.")
        self.wait_label4.grid(row=3,column=0, sticky="nsew")









