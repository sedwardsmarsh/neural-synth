# script for preprocessing audio files using librosa. Source: https://towardsdatascience.com/how-to-apply-machine-learning-and-deep-learning-methods-to-audio-analysis-615e286fcbbc
# run with the conda environment: cmpm152

import librosa
import numpy as np
import os
import glob
import pandas as pd
from datetime import datetime
from sklearn import preprocessing
import pickle


SIMPLE_DATASET_PATH = './data/simple_dataset'
DF_PATH = './data/preprocessed'


def normalize(array) -> list:
    '''Normalize array.
    '''
    weight = np.sqrt(np.sum(np.power(array,2)))
    normalized_array = array/weight
    # normalized_array = preprocessing.normalize(np.asarray(array).reshape(1,-1))
    return normalized_array.tolist(), weight


# TODO return a dataframe
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
        # TODO restructure dataset directory heirarchy so this check isn't necessary
        if file_name[-3:] in ['csv', 'pkl']:
            continue
        label = extract_labels(file_name)
        data = extract_features(file_name)
        # label, label_weight = normalize(label)
        # data, _ = normalize(data)
        example = []
        example.append(file_name)
        example.extend(data)
        example.extend(label)
        features.append(example)
        # features.append(label_weight)
        if i > 0 and i % (len(file_paths) * .1) == 0:
            print(f'{i/len(file_paths)}% complete')
    print('done')
    # Convert into a Pandas dataframe
    # TODO programmatically generate this list 
    df = pd.DataFrame(features, columns=[
        'file name',
        'mfcc1','mfcc2','mfcc3','mfcc4','mfcc5','mfcc6','mfcc7','mfcc8','mfcc9',
        'mfcc10','mfcc11','mfcc12','mfcc13','mfcc14','mfcc15','mfcc16',
        'rms1','rms2','rms3',
        'zcr1','zcr2','zcr3',
        'sc1','sc2','sc3','sc4','sc5','sc6','sc7','sc8','sc9','sc10','sc11',
        'sc12','sc13','sc14','sc15','sc16','sc17','sc18','sc19','sc20','sc21',
        'label1','label2','label3'])
    # normalize all the data columns. L2 normalization
    df.loc[:, 'mfcc1':'sc21']
    feature_weights = np.sqrt(np.sum(np.power(df.loc[:, 'mfcc1':'sc21'],2)))
    df.loc[:, 'mfcc1':'sc21'] = df.loc[:, 'mfcc1':'sc21']/feature_weights
    # noralize all label columns and save their de-normalization weight. L2 Normalization
    df.loc[:, 'label1':'label3']
    label_weights = np.sqrt(np.sum(np.power(df.loc[:, 'label1':'label3'],2)))
    df.loc[:, 'label1':'label3'] = df.loc[:, 'label1':'label3']/label_weights
    with open(f'{SIMPLE_DATASET_PATH}/label_denorm_weights.pkl', 'wb') as f:
        pickle.dump(list(label_weights), f)
    return df


# extract features and build dataframe
time_now = str(datetime.now())[:-7]
df = make_df()
df.to_csv(f'{DF_PATH}/datasetFeat&LabelL2Norm{time_now}.csv')