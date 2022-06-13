import matplotlib.pyplot as plt


def plot_history(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['accuracy'], label='accuracy')
    try:
        plt.plot(history.history['val_loss'], label='val_loss')
        plt.plot(history.history['val_accuracy'], label='val_accuracy')
    except KeyError:
        pass
    plt.xlabel('epochs')
    plt.ylim([0, 1])
    plt.legend(loc='lower left')
    plt.show()
