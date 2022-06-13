"""
The purpose of this file is to determine all the features, so it can later be used for a classical machine learning algorithm like SVM.
The following features are determined from the raw data (3-dimenional axis of the accelerometer and gyroscope): See list in code.
The following Activities are used for classification:
    A = Walking
    B = Jogging
    C = Stairs
    D = Sitting
    E = Standing
 note:dataset 1616,1637 and between 1639-1644 has the following error: Runtimewarning: mean of empty slice.
"""
import sys
import pandas as pd
from cmath import sqrt
from scipy.stats import kurtosis
from helper_functions.sliding_window import train_test_windows
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import pywt


def plot_feature_importance(x, y):
    feature_names = ['mean_A', 'variance_A', 'median_A', 'std_A', 'maxima_A', 'minima_A', 'ptp_A', 'rms_A',
                     'Skewness_A', 'Kurtosis_A', 'Impuls factor_A', 'Crest factor_A', 'IQR_A', 'CC', 'mean_G',
                     'variance_G', 'median_G', 'std_G', 'maxima_G', 'minima_G', 'ptp_G', 'rms_G', 'Skewness_G',
                     'Kurtosis_G', 'Impuls factor_G', 'Crest factor_G', 'IQR_G', 'mean_dwt_A_ca', 'variance_dwt_A_ca',
                     'median_dwt_A_ca', 'std_dwt_A_ca', 'maxima_dwt_A_ca', 'minima_dwt_A_ca', 'ptp_dwt_A_ca',
                     'rms_dwt_A_ca',
                     'Skewness_dwt_A_ca', 'Kurtosis_dwt_A_ca', 'Impuls factor_dwt_A_ca', 'Crest factor_dwt_A_ca',
                     'IQR_dwt_A_ca',
                     'CC_dwt_A', 'mean_dwt_A_cd', 'variance_dwt_A_cd', 'median_dwt_A_cd', 'std_dwt_A_cd',
                     'maxima_dwt_A_cd',
                     'minima_dwt_A_cd', 'ptp_dwt_A_cd', 'rms_dwt_A_cd', 'Skewness_dwt_A_cd', 'Kurtosis_dwt_A_cd',
                     'Impuls factor_dwt_A_cd', 'Crest factor_dwt_A_cd', 'IQR_dwt_A_cd', 'mean_dwt_G_ca',
                     'variance_dwt_G_ca',
                     'median_dwt_G_ca', 'std_dwt_G_ca', 'maxima_dwt_G_ca', 'minima_dwt_G_ca', 'ptp_dwt_G_ca',
                     'rms_dwt_G_ca',
                     'Skewness_dwt_G_ca', 'Kurtosis_dwt_G_ca', 'Impuls factor_dwt_G_ca', 'Crest factor_dwt_G_ca',
                     'IQR_dwt_G_ca', 'CC_dwt_G', 'mean_dwt_G_cd', 'variance_dwt_G_cd', 'median_dwt_G_cd',
                     'std_dwt_G_cd',
                     'maxima_dwt_G_cd', 'minima_dwt_G_cd', 'ptp_dwt_G_cd', 'rms_dwt_G_cd', 'Skewness_dwt_G_cd',
                     'Kurtosis_dwt_G_cd', 'Impuls factor_dwt_G_cd', 'Crest factor_dwt_G_cd', 'IQR_dwt_G_cd']
    forest = RandomForestClassifier(random_state=0)
    forest.fit(x, y)
    y_axis = range(len(feature_names))
    plt.bar(y_axis, forest.feature_importances_)
    plt.xticks(y_axis, feature_names, rotation=90)
    plt.show()


def feature_importance(x_train, x_test, y_train, number_of_features):
    sorted_x_test = np.full_like(x_test[:, 0:number_of_features], 1)
    sorted_x_train = np.full_like(x_train[:, 0:number_of_features], 1)
    forest = RandomForestClassifier(random_state=0)
    forest.fit(x_train, y_train)
    importances = forest.feature_importances_
    sorted_indices = np.argsort(importances)[::-1]
    for i in range(number_of_features):
        index_number = sorted_indices[i]
        for j in range(np.size(x_train, 0)):
            sorted_x_train[j, i] = x_train[j, index_number]
        for k in range(np.size(x_test, 0)):
            sorted_x_test[k, i] = x_test[k, index_number]
    return sorted_x_train[:, 0:number_of_features], sorted_x_test[:, 0:number_of_features]


def parameter_tuning(x_train, x_test, y_train, y_test, kernel):
    param_grid = {'C': [0.1, 1, 10, 100, 1000],
                  'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
                  'kernel': [kernel]}
    grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=3)
    model = SVC()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    print(classification_report(y_test, predictions))
    grid.fit(x_train, y_train)
    print(grid.best_params_)
    print(grid.best_estimator_)
    grid_predictions = grid.predict(x_test)
    print('Accuracy:', classification_report(y_test, grid_predictions))


def print_accuracy(x_train, x_test, y_train, y_test):
    svc_classifier = RandomForestClassifier(n_estimators=1000)
    svc_classifier.fit(x_train, y_train)
    print('Accuracy:', accuracy_score(y_test, svc_classifier.predict(x_test)))


def print_confusion_matrix(x_train, x_test, y_train, y_test):
    classifier = RandomForestClassifier(n_estimators=1000).fit(x_train, y_train)
    titles_options = [
        ("Confusion matrix, without normalization", None),
        ("Normalized confusion matrix", "true"),
    ]
    for title, normalize in titles_options:
        disp = ConfusionMatrixDisplay.from_estimator(
            classifier,
            x_test,
            y_test,
            cmap=plt.cm.Blues,
            normalize=normalize,
        )
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)

    plt.show()


# function to get all data from every axis
def get_features(data_a, data_g):
    mean_a = np.mean(data_a)  # compute mean through numpy
    var_a = np.var(data_a)  # compute variance through numpy
    median_a = np.median(data_a)  # compute median through numpy
    std_a = np.std(data_a)  # compute standard deviation through numpy
    max_a = np.max(data_a)  # compute maximum through numpy
    min_a = np.min(data_a)  # compute minimum deviation through numpy
    ptp_a = np.ptp(data_a)  # compute peak to peak deviation through numpy
    rms_a = np.real(sqrt(np.sum(data_a ** 2) / len(data_a)))  # rms value
    sv_a = (3 * (mean_a - median_a)) / std_a  # skewness
    kv_a = kurtosis(data_a, fisher=False)  # kurtosis
    if_a = max_a / mean_a  # impuls factor
    cf_a = max_a / rms_a  # crest factor
    q3, q1 = np.percentile(data_a, [75, 25])  # interquartile range
    iqr_a = q3 - q1

    mean_g = np.mean(data_g)  # compute mean through numpy
    var_g = np.var(data_g)  # compute variance through numpy
    median_g = np.median(data_g)  # compute median through numpy
    std_g = np.std(data_g)  # compute standard deviation through numpy
    max_g = np.max(data_g)  # compute maximum through numpy
    min_g = np.min(data_g)  # compute minimum deviation through numpy
    ptp_g = np.ptp(data_g)  # compute peak to peak deviation through numpy
    rms_g = np.real(sqrt(np.sum(data_g ** 2) / len(data_g)))  # rms value
    sv_g = (3 * (mean_g - median_g)) / std_g  # skewness
    kv_g = kurtosis(data_g, fisher=False)  # kurtosis
    if_g = max_g / mean_g  # impuls factor
    cf_g = max_g / rms_g  # crest factor
    q3, q1 = np.percentile(data_g, [75, 25])  # interquartile range
    iqr_g = q3 - q1
    cc_ag = np.corrcoef(data_a, data_g)  # coorelation coefficient
    feature_data = [mean_a, var_a, median_a, std_a, max_a, min_a, ptp_a, rms_a, sv_a, kv_a, if_a, cf_a, iqr_a,
                    cc_ag[0, 1], mean_g, var_g, median_g, std_g, max_g, min_g, ptp_g, rms_g, sv_g, kv_g, if_g, cf_g,
                    iqr_g]
    return feature_data


def get_feature_windows(x):
    # Sort all data by person,activity,measurement tool and dimensional axis
    feature_data = np.empty((len(x), 81), dtype=np.float32)
    for j in range(len(x)):
        # calculate the absolute value of the vector from the x, y, and z vectors
        mag_accel = np.sqrt(x[j, :, 0] ** 2 + x[j, :, 1] ** 2 + x[j, :, 2] ** 2)
        mag_gyro = np.sqrt(x[j, :, 3] ** 2 + x[j, :, 4] ** 2 + x[j, :, 5] ** 2)
        # get the features in time domain
        features_new = get_features(mag_accel, mag_gyro)
        # calculate the corresponding values of the vector in time-frequency domain by using the
        # first level discrete wavelet transform
        (data_A_dwt_ca, data_A_dwt_cd) = pywt.dwt(mag_accel, 'db1')
        (data_G_dwt_ca, data_G_dwt_cd) = pywt.dwt(mag_gyro, 'db1')
        # fixes divide by zero error:
        if not np.sum(data_A_dwt_cd):
            data_A_dwt_cd[0] += 1e-15
        if not np.sum(data_G_dwt_cd):
            data_G_dwt_cd[0] += 1e-15
        # get the features in time-frequency domain
        features_new_dwt_a = np.asarray(get_features(data_A_dwt_ca, data_A_dwt_cd), dtype=np.float32)
        features_new_dwt_g = np.asarray(get_features(data_G_dwt_ca, data_G_dwt_cd), dtype=np.float32)
        # put the time domain and time-frequency domain features into an 1d array
        features_new = np.append(features_new, features_new_dwt_a, 0)
        features_new = np.append(features_new, features_new_dwt_g, 0)
        # normalize the features
        norm = np.linalg.norm(features_new)
        features_new = features_new / norm
        # put add the the 1d array into a 2d array as column
        feature_data[j, :] = features_new
        # let every set of 1d features have a corresponding activity.
    return feature_data


if __name__ == "__main__":
    data = pd.read_pickle(
        'C:/Users/rcava/OneDrive/Documenten/questa/Documents/BAP/gitlab extension/code/Classification/Code/wisdm_dataset_complete.pkl')
    (x_train_window, y_train), (x_test_window, y_test) = train_test_windows(data=data, length=40, skip=40, filt=True)
    X_train = get_feature_windows(x_train_window)
    X_test = get_feature_windows(x_test_window)
    # plot_feature_importance(X_train, y_train)
    sorted_X_train, sorted_X_test = feature_importance(X_train, X_test, y_train, number_of_features=20)
    # parameter_tuning(sorted_X_train, sorted_X_test, y_train, y_test, kernel='rbf')
    print_accuracy(sorted_X_train, sorted_X_test, y_train, y_test)
    # print_confusion_matrix(sorted_X_train,sorted_X_test, y_train, y_test, kernel = 'rbf', c = 1000, gamma = 1)
