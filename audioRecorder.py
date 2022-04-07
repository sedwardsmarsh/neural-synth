# Script for managing audio recording
# Source: https://python-sounddevice.readthedocs.io/en/0.4.1/usage.html#recording

import sounddevice as sd
import midiDriver
import time


def rec_mono_16bit(duration=2.0, samplerate=44100, channels=1):
    '''Return recorded audio as an array.

    Keyword args:
    duration -- recording length in seconds
    samplerate -- sample rate
    channels -- number of audio channels
    '''
    # don't forget to turn on Loopback: "Massive Internal Audio"
    sd.default.device = 'Massive Internal Audio'
    # record and wait for the recording to finish
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
    sd.wait()
    return myrecording, samplerate


# simple function that sends midi to Massive and records audio
def play_and_rec():
    # start test tone
    midiDriver.start_test_tone()
    # record audio and wait
    recording, samplerate = rec_mono_16bit(duration=0.05)
    # stop test tone
    midiDriver.stop_test_tone()
    return recording, samplerate