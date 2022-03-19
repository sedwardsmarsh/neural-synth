# File that makes datasets for the neural networks in neuralNetwork.py
import random
import midiDriver
import audioRecorder
import os
import soundfile as sf

# simple dataset: using only Wt-position, Intensity & Amp knobs.
def make_simple_dataset(num_examples=100):

    # array of arrays of tuples
    # innermost array are examples
    # tuples are (control number, control state) pairs
    dataset = []

    # generate random parameter configurations
    for n in range(num_examples):
        example = [(e, random.randint(0, 127)) for e in range(3)]
        dataset.append(example)

    return dataset

# render a dataset: generate the corresponding sound files for
# each parameter configuration
def render_dataset(dataset):

    try:
        os.mkdir('simple_dataset')
    except FileExistsError:
        for f in os.listdir('simple_dataset'):
            os.remove(f'simple_dataset/{f}')

    for n in dataset:
        # send parameter updates to massive
        midiDriver.update_controls(n)
        # record audio and write sound file
        data, samplerate = audioRecorder.play_and_rec()
        sf.write(f'simple_dataset/{n}.wav', data, samplerate)


render_dataset(make_simple_dataset(100))