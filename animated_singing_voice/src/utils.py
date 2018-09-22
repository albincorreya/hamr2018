import numpy as np


def pitch_to_freq(p, ref=440.0):
    return ref * 2 ** ((p-69) / 12.0)


def freq_to_pitch(freq, ref=440.0):
    return 12 * np.log2(freq / ref) + 69
