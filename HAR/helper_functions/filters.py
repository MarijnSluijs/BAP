from scipy import signal
import math as m
import matplotlib.pyplot as plt


def low_pass(unfiltered_signal, fs=20, cutoff=25, order=5):
    sos = signal.butter(N=order, Wn=cutoff, fs=fs, output='sos')
    return signal.sosfilt(sos, unfiltered_signal)


def high_pass(unfiltered_signal, fs=20, cutoff=0.3, order=5):
    sos = signal.butter(N=order, Wn=cutoff, fs=fs, output='sos', btype='highpass')
    return signal.sosfilt(sos, unfiltered_signal)


def filter_df(data_frame, filt='high_pass', fs=20):
    if filt == 'low_pass':
        for column in ["Accel_X", "Accel_Y", "Accel_Z", "Gyro_X", "Gyro_Y", "Gyro_Z"]:
            data_frame[column] = low_pass(data_frame[column].to_numpy(dtype=float), fs=fs)
    elif filt == 'high_pass':
        for column in ["Accel_X", "Accel_Y", "Accel_Z"]:
            data_frame[column] = high_pass(data_frame[column].to_numpy(dtype=float), fs=fs)
    return data_frame


def down_sample_df(data_frame, fs=50, factor=2):
    cutoff = m.floor(fs / 2 / factor)
    for column in ["Accel_X", "Accel_Y", "Accel_Z", "Gyro_X", "Gyro_Y", "Gyro_Z"]:
        data_frame[column] = low_pass(data_frame[column].to_numpy(dtype=float), fs=fs, cutoff=cutoff)
    return data_frame[data_frame.reset_index().index % factor == 0].reset_index()


def plot_high_pass(fs=50, cutoff=0.3, order=5):
    b, a = signal.butter(N=order, Wn=cutoff, fs=fs, output='ba', btype='highpass')
    w, h = signal.freqz(b, a)
    plt.plot(w, abs(h))
    plt.grid(which='both', axis='both')
    plt.xlim([0, 1.5])
    plt.show()


if __name__ == '__main__':
    plot_high_pass()
