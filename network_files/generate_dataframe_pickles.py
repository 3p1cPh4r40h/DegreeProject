# Importing required libraries
import os
import librosa # for audio processing
import pandas as pd # for dataframe
import numpy as np # used for mathematical operations and data structures

# Creating empty lists for Test and Training datasets
test_list = []
train_list = []

# Length of the shortest audio clip in the dataset
smallest_shape = 24775

# Iterating over the 'Test' and 'Training' folders
for folder in ['Test', 'Training']:
    # Iterating over sub-folders within the folder
    for subfolder in os.listdir(folder):
        # Iterating over audio files in the subfolder
        for file in os.listdir(f'{folder}/{subfolder}'):
            # Loading the audio file
            audio, sr = librosa.load(f'{folder}/{subfolder}/{file}')
            
            # If the length of the audio clip is greater than the smallest shape
            if audio.shape[0] > smallest_shape:
                # Cutting the audio into as many pieces of the smallest shape as possible, discarding the rest
                num_pieces = audio.shape[0] // smallest_shape
                audio = audio[:num_pieces * smallest_shape]
                audio = audio.reshape(-1, smallest_shape)
                
                # Appending each piece to the appropriate list
                for piece in audio:
                    if folder == 'Test':
                        test_list.append({'audio': piece, 'chord': subfolder, 'sr': sr})
                    else:
                        train_list.append({'audio': piece, 'chord': subfolder, 'sr': sr})
            else:
                # Appending the audio clip to the appropriate list
                if folder == 'Test':
                    test_list.append({'audio': audio, 'chord': subfolder, 'sr': sr})
                else:
                    train_list.append({'audio': audio, 'chord': subfolder, 'sr': sr})

# Creating dataframes from the lists
test_df = pd.DataFrame(test_list, columns=['audio', 'chord', 'sr'])
train_df = pd.DataFrame(train_list, columns=['audio', 'chord', 'sr'])

# Saving the dataframes to disk as .pkl files
test_df.to_pickle('test_df.pkl')
train_df.to_pickle('train_df.pkl')

# Printing a message indicating the dataframes have been saved successfully
print("Dataframes test_df.pkl and train_df.pkl have been created in this directory")
