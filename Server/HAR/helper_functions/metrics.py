import tensorflow as tf
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import recall_score, precision_score, accuracy_score


def plot_conf_matrix(y_pred, y_true):
    labels = ['Walking', 'Jogging', 'Stairs', 'Sitting', 'Standing']
    conf_mat = tf.math.confusion_matrix(y_true, y_pred)
    sns.heatmap(conf_mat, annot=True, xticklabels=labels, yticklabels=labels)
    plt.show()


def precision_recall_accuracy(y_pred, y_true):
    pre = precision_score(y_true, y_pred, average='macro')
    rec = recall_score(y_true, y_pred, average='macro')
    acc = accuracy_score(y_true, y_pred)
    return pre, rec, acc
