# The script responsible for generating the datasets from Massive
# run with conda environment: env_tf_and_audio
# -*- NOTICE -*-
# set Massive Audio/Midi setup to the following settings:
# Device: Massive Internal Audio
# Sample Rate: 44100
# Latency: 32 Samples
# Make sure loopback's Massive Internal Audio is turned on
import random
import midiDriver
import audioRecorder
import os
import soundfile as sf
import pandas as pd
import time


DATA_DIR = './data'
SIMPLE_DATASET_CSV = 'simple_dataset.csv'


def make_simple_dataset(num_examples: int=100) -> list[list[tuple[int, int]]]:
    '''Generates datasets using only Wt-position, Intensity & Amp knobs. There are 127 * 127 * 127 = 127^3 = 2,048,383 configurations.
    
    Dataset is in the form: [[(control number, control state), ..., num_examples-1]]
    '''
    # create directory
    try:
        os.makedirs(f'{DATA_DIR}/simple_dataset/')
    except FileExistsError:
        pass
    # create SIMPLE_DATASET_CSV
    if os.path.exists(f'{DATA_DIR}/simple_dataset/{SIMPLE_DATASET_CSV}'):
        existing_data = pd.read_csv(f'{DATA_DIR}/simple_dataset/{SIMPLE_DATASET_CSV}')
    else:
        existing_data = {'file name':[]}
        existing_data = pd.DataFrame(existing_data)
    # generate parameter configurations
    dataset = []
    for _ in range(num_examples):
        example = [(param_num, random.randint(0, 127)) for param_num in range(3)]
        if str(example) not in existing_data['file name']:
            temp_df = pd.DataFrame({'file name':[str(example)]})
            existing_data = pd.concat([existing_data, temp_df], ignore_index=True)
            dataset.append(example)
    existing_data.to_csv(f'{DATA_DIR}/simple_dataset/{SIMPLE_DATASET_CSV}')
    return dataset


def render_dataset(dataset: list[list[tuple[int, int]]], data_dir: str=DATA_DIR) -> None:
    '''Generate the corresponding sound files for each parameter configuration.

    Sound file names are the corresponding parameter configuration
    '''
    for i, n in enumerate(dataset):
        if i % (len(dataset) * .1) == 0:
            print(f'{i/len(dataset):.2f}% complete')
        midiDriver.update_controls(n)
        data, samplerate = audioRecorder.play_and_rec()
        sf.write(f'{data_dir}/simple_dataset/{n}.wav', data, samplerate)


number_of_examples = 1000
start_time = time.time()
param_configs = make_simple_dataset(number_of_examples)
print(f'parameter configurations generation took: {time.time() - start_time} seconds')
start_time = time.time()
render_dataset(param_configs)
print(f'dataset rendering took: {time.time() - start_time} seconds')