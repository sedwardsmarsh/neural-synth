# Script for managing audio recording
# Source: https://python-sounddevice.readthedocs.io/en/0.4.1/usage.html#recording

import sounddevice as sd

# Record audio to an array
# - duration:   recording length in seconds
# - samplerate: sample rate
# - channels:   number of audio channels
# Returns a numpy array of the audio recording
def rec_mono_16bit_48kHz(duration=2, samplerate=48000, channels=1):

    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)

    # wait for recording to finish
    sd.wait()
    
    return myrecording