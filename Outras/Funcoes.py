import numpy as np
from sklearn.preprocessing import MinMaxScaler


def featurescaling(arr):
    # weights = numpy.array([[115.], [140.], [175.]])
    scaler = MinMaxScaler(feature_range=(0.2, 0.5))
    rescaled_arr = scaler.fit_transform(arr)
    # print rescaled_weight

    return rescaled_arr


def pol2cart(r, theta):
    x = r * np.cos(np.deg2rad(theta))
    y = r * np.sin(np.deg2rad(theta))
    return x, y


def movingaverage(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')
