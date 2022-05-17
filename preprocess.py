# script for preprocessing audio files using librosa. Source: https://towardsdatascience.com/how-to-apply-machine-learning-and-deep-learning-methods-to-audio-analysis-615e286fcbbc
# run with the conda environment: cmpm152

import librosa
import numpy as np
import os
import glob
import pandas as pd
from sklearn import preprocessing
from datetime import datetime


SIMPLE_DATASET_PATH = './data/simple_dataset'
DF_PATH = './data/preprocessed'


def normalize(features) -> list:
    '''Normalize features.
    '''
    weight = np.sqrt(np.sum(np.power(features,2)))
    normalized_features = features/weight
    return normalized_features.tolist(), weight


def extract_features(file_name: str) -> list[int]:
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
    return features.tolist()


def extract_labels(file_name: str) -> list[int]:
    '''Extracts the labels from a file name.
    '''
    label_str = os.path.basename(file_name).split('.')[0]
    label_list = [param_pair[1] for param_pair in eval(label_str)]
    return label_list


def make_df(data_path: str=SIMPLE_DATASET_PATH) -> pd.DataFrame:
    features = []
    # Iterate through each sound file and extract the features
    file_paths = glob.glob(f'{data_path}/*')
    for i, file_name in enumerate(file_paths):
        if file_name[-3:] == 'csv':
            continue
        label = extract_labels(file_name)
        data = extract_features(file_name)
        label, label_weight = normalize(label)
        data, _ = normalize(data)
        features.append([file_name, data, label, label_weight])
        if i > 0 and i % (len(file_paths) * .1) == 0:
            print(f'{i/len(file_paths)}% complete')
    print('done')
    # Convert into a Pandas dataframe 
    return pd.DataFrame(features, columns=['file name','features','labels','label norm weight'])


# extract features and build dataframe
time_now = str(datetime.now())[:-7]
df = make_df()
df.to_csv(f'{DF_PATH}/datasetFeat&LabelL2Norm{time_now}.csv')