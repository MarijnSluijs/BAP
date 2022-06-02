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
#
# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def init_model(name_model):
    # name_model = 'split_gru_128_64_acc96.h5'
    return tf.keras.models.load_model(f'{name_model}')


def predict(model, x):
    y = np.argmax(model([x[:, :, :3], x[:, :, 3:]]), axis=-1)
    labels = ['A', 'B', 'C', 'D', 'E']
    names = ['Walking','Jogging','stairs','sitting','standing']
    #print(names[y[0]])
    return labels[y[0]]


def update_counter(prediction, counter):
    n = len(counter)
    if prediction == counter[0]:
        if n < 3:
            counter += prediction
    else:
        if n > 1:
            counter = counter[:n]
            prediction = counter[0]     # ignore prediction by model
        else:
            counter = prediction
    return prediction, counter


def run_pipeline(model, x, counter):
    prediction = predict(model, x)
    # classification, counter = update_counter(prediction, counter)
    # print(counter)
    return prediction, counter


if __name__ == '__main__':
    num_samples = 40
    sat_counter = 'X'
    Model = init_model('split_gru_128_64_acc96.h5')

    while True:
        x_test = np.empty((1, num_samples, 6))
        result, sat_counter = run_pipeline(Model, x_test, sat_counter)
