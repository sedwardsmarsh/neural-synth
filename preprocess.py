# script for preprocessing audio files using librosa. Source: https://towardsdatascience.com/how-to-apply-machine-learning-and-deep-learning-methods-to-audio-analysis-615e286fcbbc
# run with the conda environment: cmpm152

from typing import Union
import librosa
import numpy as np
import os
import glob
import pandas as pd
from sklearn import preprocessing
from datetime import datetime


DATA_PATH = './data/simple_dataset/01/*'
DF_PATH = './data/processed/'


def extract_features(file_name: str) -> list:
    '''Extracts features from the file.
    '''
    features = np.empty((0))
    audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
    # calculate mel-frequency cepstral coefficients
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=16)
    mfccs_processed = np.mean(mfccs.T,axis=0)
    features = np.append(features, mfccs_processed)
    # calculate mel-spectrogram
    # ms = librosa.feature.melspectrogram(y=audio, sr=sample_rate, fmin='C4')
    # ms = np.append(features, ms)
    # calculate root mean square
    rms = librosa.feature.rms(y=audio)
    features = np.append(features, rms)
    # calculate zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y=audio)
    features = np.append(features, zcr)
    # calculate spectral contrast
    sc = librosa.feature.spectral_contrast(y=audio)
    features = np.append(features, sc)
    # normalize features
    features = preprocessing.normalize(features.reshape(1,-1))
    return features.tolist()[0]


def extract_labels(file_name: str) -> list:
    '''Extracts the labels from a file_name.
    '''
    label_str = os.path.basename(file_name).split('.')[0]
    label_list = [param_pair[1] for param_pair in eval(label_str)]
    label_array = preprocessing.normalize(np.asarray(label_list).reshape(1,-1))
    return label_array.tolist()[0]


def make_df(data_path: str=DATA_PATH) -> pd.DataFrame:
    features = []
    # Iterate through each sound file and extract the features
    file_paths = glob.glob(data_path)
    for i, file_name in enumerate(file_paths):
        label = extract_labels(file_name)
        data = extract_features(file_name)
        features.append([data, label])
        if i > 0 and i % (len(file_paths) * .1) == 0:
            print(f'{i/len(file_paths)}% complete')
    print('done')
    # Convert into a Pandas dataframe 
    return pd.DataFrame(features, columns=['features','label'])


# extract features and build dataframe
time_now = str(datetime.now())[:-7]
df = make_df()
df.to_csv(DF_PATH + f'dataset{time_now}.csv')