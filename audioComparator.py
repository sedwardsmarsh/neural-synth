# A file that contains utility functions for comparing audio files
# - Source for audio comparison idea, thank you atzz: 
# - https://stackoverflow.com/questions/3172911/compare-two-audio-files
# --------------------------------------------------------------------------

import wave
from numba.core.decorators import njit
import numpy as np

# function that normalizes an array containing:
# - a Mono, 16 bit, 48KHz wav file
# uses numba to speed things up
@njit
def normalize(audio):
    audio = audio.astype(np.float32)
    audio = audio / (2.**15)
    return audio

# function that compares .wav file and numpy array
# file format: Mono, 16 bit, 48KHz
# returns the difference between the files as a sum
@njit
def cmp_mono_16bit_48kHz_numba(filepath, array):
    # open files
    w1 = wave.open(filepath, 'r')

    # get the parameters
    nchannels = w1.getnchannels()
    nframes = w1.getnframes()

    # read the data
    data1 = w1.readframes(nframes)

    # close the files
    w1.close()

    # convert the data
    data1 = wave.struct.unpack("%dh"%nframes*nchannels, data1)

    # normalize the filedata & array
    data1 = normalize(data1)
    data2 = normalize(array)

    # calculate the difference
    difference = 0
    for i in range(0, nframes):
        difference += abs(data1[i] - data2[i])

    # return the difference
    return difference