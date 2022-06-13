import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import pandas as pd
from helper_functions.filters import filter_df
from helper_functions.filters import down_sample_df


def train_test_segments(data=None, length=40, skip=10, data_types='all', test_size=0.5, down_sample=False, filt=False):
    """
    Gets data from the wisdm_dataset_complete.pkl file, splits it into windows and shuffles for train and test data
    :param data: if you want to pass your own data that's fine, else it will just use the pkl file since that's probably
    faster anyway. (note: the .pkl file has to be in the same folder as the script you are importing this from)
    :param length: window size, in amount of samples
    :param skip: amount the window shifts every step, in amount of samples
    :param data_types: 'all', 'gyro' or 'accel'
    :param test_size: param for train_test_split, defines fraction of data to be used for testing
    :param down_sample: down sample data
    :return: x_train, x_test, y_train and y_test,   x_train.shape = (... , length, 6) for data_types = 'all'
                                                    x_train.shape = (... , length, 3) for data_types = 'accel' or 'gyro'
    """
    if not isinstance(data, pd.DataFrame):
        data = pd.read_pickle('wisdm_dataset_complete.pkl')
    if down_sample:
        data = down_sample_df(data)
    if filt:
        data = filter_df(data, filt='high_pass')
    if data_types == 'all':
        columns = ["Accel_X", "Accel_Y", "Accel_Z", "Gyro_X", "Gyro_Y", "Gyro_Z"]
    elif data_types == 'accel':
        columns = ["Accel_X", "Accel_Y", "Accel_Z"]
    elif data_types == 'gyro':
        columns = ["Gyro_X", "Gyro_Y", "Gyro_Z"]
    else:
        print('please use "all", "accel", or "gyro" data_type')
        raise ValueError

    x = []
    y = []
    activity_to_label = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    list_index = 0
    window_index = 0
    while window_index < (len(data) - length - skip):
        x.append(data.loc[window_index: window_index + length - 1, columns].to_numpy(dtype=np.float32))
        y.append(activity_to_label[data.at[window_index, 'Activity']])
        if y[list_index] != activity_to_label[data.at[window_index+length, 'Activity']]:
            window_index += length
        list_index += 1
        window_index += skip
    x = np.stack(x, axis=0)
    y = np.array(y)
    if test_size != 0:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)
        print(f'shape x_train: {x_train.shape}, y_train: {y_train.shape}')
        print(f'shape x_test: {x_test.shape}, y_test: {y_test.shape}')
        return (x_train, y_train), (x_test, y_test)
    else:
        # no need for test_samples, so just return shuffled x and y windows
        x, y = shuffle(x, y, random_state=42)
        print(f'shape x: {x.shape}, y: {y.shape}')
        return x, y
