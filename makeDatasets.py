# File that makes datasets for the neural networks in neuralNetwork.py
import random
import midiDriver

# simple dataset: using only Wt-position, Intensity & Amp knobs.
def make_simple_dataset(num_examples=100):

    # array of arrays
    dataset = []

    # generate random parameter configurations
    for n in range(num_examples):
        for p in range(3):
            # append [(control number, control state)]
            dataset.append([])
            dataset[n].append((p, random.randint(0, 127)))

    return dataset

# render a dataset: generate the corresponding sound files for
# each parameter configuration
# def render_dataset():