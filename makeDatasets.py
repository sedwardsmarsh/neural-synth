# The script responsible for generating the datasets from Massive
# run with conda environment: env_tf_and_audio
import random
import midiDriver
import audioRecorder
import os
import soundfile as sf


def make_simple_dataset(num_examples: int=100):
    '''Generates datasets using only Wt-position, Intensity & Amp knobs.
    
    Dataset is in the form: [[(control number, control state), ..., num_examples-1]]
    '''
    dataset: list = []
    for n in range(num_examples):
        example = [(e, random.randint(0, 127)) for e in range(3)]
        dataset.append(example)
    return dataset

# render a dataset: generate the corresponding sound files for
# each parameter configuration
def render_dataset(dataset):

    sub_dir = random.randint(0, 1000000)

    try:
        os.mkdir(f'data/simple_dataset/{sub_dir}')
    except FileExistsError:
        print('Dumb luck: subdirectory already exists. Run again.')
        # for f in os.listdir('data/simple_dataset'):
        #     os.remove(f'data/simple_dataset/{f}')

    for i, n in enumerate(dataset):
        if i % (len(dataset) * .1) == 0:
            print(f'{i/len(dataset):.2f}% complete')
        midiDriver.update_controls(n)
        data, samplerate = audioRecorder.play_and_rec()
        sf.write(f'data/simple_dataset/{sub_dir}/{n}.wav', data, samplerate)

number_of_examples = 1000
render_dataset(make_simple_dataset(number_of_examples))