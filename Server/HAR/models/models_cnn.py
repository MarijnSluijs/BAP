import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Conv1D
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd


def fnn_model(shape):
    inputs = keras.Input(shape=shape)
    x = keras.layers.Flatten()(inputs)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(512, activation="relu")(x)
    x = layers.Dense(512, activation="relu")(x)
    outputs = layers.Dense(5, activation="softmax")(x)
    model = keras.Model(inputs=inputs, outputs=outputs)

    return model


def fcn_model(shape):
    inputs = keras.Input(shape=shape)
    x = Conv1D(128, kernel_size=8, padding="same")(inputs)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)

    x = Conv1D(256, kernel_size=5, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)

    x = Conv1D(128, kernel_size=3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)

    x = layers.GlobalMaxPool1D()(x)

    outputs = layers.Dense(5, activation="softmax")(x)
    model = keras.Model(inputs=inputs, outputs=outputs, name="FCN_model")

    return model


def fcn_model_with_regularisation(shape):
    inputs = keras.Input(shape=shape)
    x = Conv1D(128, kernel_size=8, padding="same")(inputs)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.Dropout(0.5)(x)

    x = Conv1D(256, kernel_size=5, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.Dropout(0.5)(x)

    x = Conv1D(128, kernel_size=3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)

    x = layers.GlobalMaxPool1D()(x)

    outputs = layers.Dense(5, activation="softmax")(x)
    model = keras.Model(inputs=inputs, outputs=outputs, name="FCN_model")

    return model


def res_net(shape):
    model = keras.models.Sequential()
    model.add(keras.layers.Conv1D(64, 3, strides=2, input_shape=shape, padding="same", use_bias=False))

    prev_filters = 64
    for filters in [64] * 1 + [128] * 2:
        strides = 1 if filters == prev_filters else 2
        model.add(ResidualUnit(filters, strides=strides))
        prev_filters = filters
    model.add(keras.layers.GlobalAvgPool1D())
    model.add(keras.layers.Dense(5, activation="softmax"))

    return model


class ResidualUnit(keras.layers.Layer):
    def __init__(self, filters, strides=1, activation="relu", **kwargs):
        super().__init__(**kwargs)
        self.activation = keras.activations.get(activation)
        self.main_layers = [
            keras.layers.Conv1D(filters, 3, strides=strides, padding="same", use_bias=False),
            keras.layers.BatchNormalization(),
            self.activation,

            keras.layers.Conv1D(filters, 3, strides=1, padding="same", use_bias=False),
            keras.layers.BatchNormalization(),
            self.activation,

            keras.layers.Conv1D(filters, 3, strides=1, padding="same", use_bias=False),
            keras.layers.BatchNormalization()]

        self.skip_layers = []

        if strides > 1:
            self.skip_layers = [
                keras.layers.Conv1D(filters, 1, strides=strides, padding="same", use_bias=False),
                keras.layers.BatchNormalization()]

    def call(self, inputs):
        z = inputs
        for layer in self.main_layers:
            z = layer(z)
            skip_z = inputs
        for layer in self.skip_layers:
            skip_z = layer(skip_z)
        return self.activation(z + skip_z)
