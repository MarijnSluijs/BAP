import tensorflow as tf
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def init_model(name_model):
    return tf.keras.models.load_model(f'../HAR/trained_models/{name_model}')


def predict(model, x):
    y = np.argmax(model(x), axis=-1)
    labels = ['A', 'B', 'C', 'D', 'E']
    # ['walking', 'stairs', 'jogging', 'sitting', 'standing']
    return labels[y[0]]
