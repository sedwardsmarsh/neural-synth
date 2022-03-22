from posixpath import split
from typing import List, Tuple
import tensorflow as tf
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import InputLayer, GRU, Dense
import time
import glob
import os
from scipy.io.wavfile import read

def esr(y_path: str, y_hat_path: str) -> float:
    '''Returns the Error-to-Signal Ratio.

    Keyword arguments:
    y -- the groundtruth file
    y_hat -- the prediction file
    '''
    y_sample_rate, y = read(y_path)
    y_hat_sample_rate, y_hat = read(y_hat_path)
    power = 2.0
    numerator = sum(abs(y - y_hat)**power)
    denominator = sum(abs(y)**power)
    return numerator / denominator  


def construct_dataset(data_path: str='data/simple_dataset/*', train_perc: float=0.8) -> Tuple[List, List, List, List]: 
    '''Construct the train, train_labels & test, test_labels datasets.

    Keyword arguments:
    data_path -- where the data lives
    '''
    assert train_perc < 1, 'train_perc must be less than 1'
    data_paths = glob.glob(data_path)
    split_idx = int(0.8 * len(data_paths))
    train_paths, test_paths = data_paths[:split_idx], data_paths[split_idx:]
    train_data, test_data = [], []
    train_labels, test_labels = [], []
    for file in train_paths:
        _, data = read(file)
        train_data.append(data)
        train_labels.append(os.path.basename(file).split('.')[0])
    for file in test_paths:
        _, data = read(file)
        test_data.append(data)
        test_labels.append(os.path.basename(file).split('.')[0])
    return train_data, train_labels, test_data, test_labels

train_data, train_labels, test_data, test_labels = construct_dataset()
print(f'{len(train_data)=}')
print(f'{len(train_labels)=}')
print(f'{train_labels[0:3]=}')
print(f'{train_data[0:2]=}')

print(f'{len(test_data)=}')
print(f'{len(test_labels)=}')
print(f'{test_labels[0:3]=}')
print(f'{test_data[0:2]=}')

# normalize images
# train_images = train_images / 255.0
# test_images = test_images / 255.0

# #create ML model
# model = Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(32, activation='relu'),
#     tf.keras.layers.Dense(16, activation='relu'),
#     tf.keras.layers.Dense(10)
# ])

# #compile ML model
# model.compile(optimizer='adam',
#               loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#               metrics=['accuracy'])

# #train ML model
# model.fit(train_images, train_labels, epochs=10)

# #evaluate ML model on test set
# test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

# #setup stop time
# t1 = time.time()
# total_time = t1-t0

# #print results
# print('\n')
# print(f'Training set contained {train_set_count} images')
# print(f'Testing set contained {test_set_count} images')
# print(f'Model achieved {test_acc:.2f} testing accuracy')
# print(f'Training and testing took {total_time:.2f} seconds')