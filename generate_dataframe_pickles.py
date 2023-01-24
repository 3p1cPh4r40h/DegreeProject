import os
import librosa # for audio processing
import matplotlib.pyplot as plt # used with librosa for data visualization
import pandas as pd # for dataframe
import numpy as np # used for math and data structures
from librosa import display # used to display files imported from librosa

# create empty lists for Test and Training
test_list = []
train_list = []

# iterate over Test and Training Folders
for folder in ['Test', 'Training']:
    # iterate over subfolders
    for subfolder in os.listdir(folder):
        # iterate over audio files in subfolder
        for file in os.listdir(f'{folder}/{subfolder}'):
            # load audio file
            audio, sr = librosa.load(f'{folder}/{subfolder}/{file}')
            # create new row in appropriate list
            if folder == 'Test':
                test_list.append({'audio': audio, 'chord': subfolder, 'sr': sr})
            else:
                train_list.append({'audio': audio, 'chord': subfolder, 'sr': sr})

# create dataframes from lists
test_df = pd.DataFrame(test_list, columns=['audio', 'chord', 'sr'])
train_df = pd.DataFrame(train_list, columns=['audio', 'chord', 'sr'])

test_df.to_pickle('test_df.pkl')
train_df.to_pickle('train_df.pkl')

