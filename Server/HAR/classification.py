import tensorflow as tf
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def init_model(name_model):
    return tf.keras.models.load_model(f'{os.path.abspath(os.getcwd())}\\HAR\\trained_models\\{name_model}')
    #return tf.keras.models.load_model('/trained_models\\{name_model}')


def predict(model, x):
    y = np.argmax(model(x), axis=-1)
    labels = ['A', 'B', 'C', 'D', 'E']
    actions = ['walking', 'stairs', 'jogging', 'sitting', 'standing']
    return actions[y[0]]
