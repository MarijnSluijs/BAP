import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def gru_split_inputs(learning_rate=0.001, decay_rate=0):
    # inputs and batch normalization
    a_inputs = keras.Input(shape=(None, 3))
    g_inputs = keras.Input(shape=(None, 3))
    a_batch = keras.layers.BatchNormalization()(a_inputs)
    g_batch = keras.layers.BatchNormalization()(g_inputs)

    # first a dense layer
    a_dense = layers.Dense(16, activation='relu')(a_batch)
    g_dense = layers.Dense(16, activation='relu')(g_batch)

    # combine the layers and add some dropout regularization
    combined = layers.Concatenate(axis=-1)([a_dense, g_dense])
    dropout = layers.Dropout(.5)(combined)

    # GRU layers
    gru = layers.GRU(128, activation='tanh', return_sequences=True)(dropout)
    gru = layers.GRU(64, activation='tanh')(gru)

    # output layer, compiling the model and returning it
    outputs = layers.Dense(5, activation='softmax')(gru)

    model = keras.Model(inputs=[a_inputs, g_inputs], outputs=outputs)
    model.compile(
        loss=keras.losses.SparseCategoricalCrossentropy(),
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate, decay=decay_rate),
        metrics=['accuracy']
    )
    # model.summary()
    return model
