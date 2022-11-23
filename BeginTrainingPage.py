from Sidebar import Sidebar
from Content import Content

import csv
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split



def start_training():
    RANDOM_SEED = 42

    dataset = './data/training_data.csv'
    labelset = './data/labels.csv'
    model_save_path = './data/classifier.hdf5'
    NUM_CLASSES = sum(1 for row in csv.reader(open(labelset)))
    print(NUM_CLASSES)

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




class BeginTrainingSidebar(Sidebar):
    def __init__(self, *args,  **kwargs):
        super().__init__(heading = "Train New Model",*args, **kwargs)

        self.add_button(text="Cancel",command=lambda: self.master.set_page("home"))
        self.add_button(text="Start Training",command=lambda: start_training())
        

class BeginTrainingContent(Content):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)






