# A file that contains utility functions for comparing audio files
# - Source for audio comparison idea, thank you atzz: 
# - https://stackoverflow.com/questions/3172911/compare-two-audio-files
# --------------------------------------------------------------------------

import wave
import numpy as np

# function that normalizes an array containing:
# - a Mono, 16 bit, 8KHz wav file
def normalize(audio):
    audio = audio.astype(np.float32)
    audio = audio / (2.**15)
    return audio

# function that compares .wav file and numpy array
# file format: Mono, 16 bit, 8KHz
# returns the difference between the files as a sum
def cmp_mono_16bit_4kHz_numba(filepath, array):
    # open files
    w1 = wave.open(filepath, 'r')

    # get the parameters
    nchannels = w1.getnchannels()
    nframes = w1.getnframes()

    # read the data
    data1 = w1.readframes(nframes)

    # close the files
    w1.close()

    # # convert the data
    # data1 = wave.struct.unpack("%dh"%nframes*nchannels, data1)

    # convert byte array to numpy array
    data1 = np.frombuffer(data1, dtype=np.float32)

    # normalize the filedata & array
    data1 = normalize(data1)
    data2 = normalize(array)

    # calculate the difference
    difference = 0
    for frame1, frame2 in zip(data1, data2):
        difference += abs(frame1 - frame2)

    # return the difference
    return difference

import audioRecorder
import sounddevice as sd
import soundfile as sf
import midiDriver

midiDriver.test_tone()
rec, samplerate = audioRecorder.rec_mono_16bit_8kHz()
# rec, samplerate = sf.read('target sound.wav')
sd.play(rec, samplerate)
sd.stop()

# testing function
# corr = cmp_mono_16bit_48kHz_numba('target sound.wav', rec)
# print(f'corr is {corr}')