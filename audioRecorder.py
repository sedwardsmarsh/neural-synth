# Script for managing audio recording
# Source: https://python-sounddevice.readthedocs.io/en/0.4.1/usage.html#recording

import sounddevice as sd
import midiDriver
import time

# don't forget to turn on Loopback: "Massive Internal Audio"
sd.default.device = 'Massive Internal Audio'

# Record audio to an array
# - duration:   recording length in seconds
# - samplerate: sample rate
# - channels:   number of audio channels
# Returns a numpy array of the audio recording
def rec_mono_16bit_8kHz(duration=2., samplerate=8000, channels=1):
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
    # wait for recording to finish
    sd.wait()

    return myrecording, samplerate


# simple function that sends midi to Massive and records audio
def play_and_rec():
    # start test tone
    midiDriver.start_test_tone()
    # record audio and wait
    recording, samplerate = rec_mono_16bit_8kHz(duration=0.1)
    # stop test tone
    midiDriver.stop_test_tone()

    return recording, samplerate