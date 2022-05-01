# script for preprocessing audio files using librosa. Source: https://towardsdatascience.com/how-to-apply-machine-learning-and-deep-learning-methods-to-audio-analysis-615e286fcbbc
# run with the conda environment: cmpm152

import librosa
import numpy as np
import os
import glob
import pandas as pd
from datetime import datetime


DATA_PATH = './data/simple_dataset/01/*'
DF_PATH = './data/processed/'


def extract_features(file_name) -> np.ndarray:
    '''Extracts features from the file and returns them'''
    audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=4)
    mfccs_processed = np.mean(mfccs.T,axis=0)
    return mfccs_processed

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