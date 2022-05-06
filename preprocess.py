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


def normalize(array: list, scale_max: int=1, scale_min: int=0) -> list:
    '''Returns a normalized array.
    
    Keyword arguments:
    array -- array to normalize
    scale_max -- maximum value to scale between
    scale_min -- minimum value to scale between
    '''
    scaler = preprocessing.normalize(feature_range=(scale_min, scale_max))
    return scaler.fit_transform(array)


def extract_features(file_name) -> list:
    '''Extracts features from the file and returns them'''
    features = np.empty((0))
    audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
    # calculate mel-frequency cepstral coefficients
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=16)
    mfccs_processed = np.mean(mfccs.T,axis=0)
    features = np.append(features, mfccs_processed)
    # calculate mel-spectrogram
    ms = librosa.feature.melspectrogram(y=audio, sr=sample_rate)
    ms = np.append(features, ms)
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
    features = preprocessing.normalize(features.reshape(1, -1))
    return features.tolist()[0]


def make_feature_df(data_path: str=DATA_PATH) -> pd.DataFrame:
    features = []
    # Iterate through each sound file and extract the features
    file_paths = glob.glob(DATA_PATH)
    for i, file_name in enumerate(file_paths):
        label = os.path.basename(file_name).split('.')[0]
        data = extract_features(file_name)
        features.append([data, label])
        if i > 0 and i % (len(file_paths) * .1) == 0:
            print(f'{i/len(file_paths)}% complete')
    print('done')
    # Convert into a Pandas dataframe 
    return pd.DataFrame(features, columns=['features','label'])


# extract features and build dataframe
time_now = str(datetime.now())[:-7]
df = make_feature_df()
df.to_csv(DF_PATH + f'dataset{time_now}.csv')