"""
Pipeline:
    -load tensorflow and the trained model
    -take last x samples
    -predict based on those samples
    -check with saturating counter
    -output classification
"""
import tensorflow as tf
import numpy as np

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def init_model(name_model):
    # name_model = 'split_gru_128_64_acc96.h5'
    return tf.keras.models.load_model(f'Trained_Models/{name_model}')


def predict(model, x):
    y = np.argmax(model(x), axis=-1)
    labels = ['A', 'B', 'C', 'D', 'E']
    acts = ['walking', 'stairs', 'jogging', 'sitting', 'standing']
    return labels[y[0]]
