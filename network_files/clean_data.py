# Import necessary libraries
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from librosa.feature import mfcc, melspectrogram

# Load the train_df and test_df dataframes
train_df = pd.read_pickle('network_files/train_df.pkl')
test_df = pd.read_pickle('network_files/test_df.pkl')

# Extract the audio and chord columns from the dataframes
train_audio = train_df['audio']
train_chords = train_df['chord']
test_audio = test_df['audio']
test_chords = test_df['chord']

# Extract the Mel Spectrogram and MFCC features for the audio
train_mspec = [melspectrogram(y=a) for a in train_audio]
train_mfcc = [mfcc(y=a, n_mfcc=128) for a in train_audio]
test_mspec = [melspectrogram(y=a) for a in test_audio]
test_mfcc = [mfcc(y=a, n_mfcc=128) for a in test_audio]


# Calculate the min and max values from the training data
min_train = np.min(train_mspec)
max_train = np.max(train_mspec)


# Normalize the training data
for i in range(len(train_mspec)):
    train_mspec[i] = (train_mspec[i] - min_train) / (max_train - min_train)

# Normalize the test data using the min and max values from the training data
for i in range(len(test_mspec)):
    test_mspec[i] = (test_mspec[i] - min_train) / (max_train - min_train)

# Repeat the same process for train_mfcc and test_mfcc
min_train = np.min(train_mfcc)
max_train = np.max(train_mfcc)

for i in range(len(train_mfcc)):
    train_mfcc[i] = (train_mfcc[i] - min_train) / (max_train - min_train)
    
for i in range(len(test_mfcc)):
    test_mfcc[i] = (test_mfcc[i] - min_train) / (max_train - min_train)


# Encode the chords as integers
le = LabelEncoder()
train_chords_enc = le.fit_transform(train_chords)
test_chords_enc = le.transform(test_chords)

# Convert the chords to one-hot encoded format
train_chords_ohe = to_categorical(train_chords_enc)
test_chords_ohe = to_categorical(test_chords_enc)

# Concatenate the Mel Spectrogram and MFCC features
train_data = np.concatenate((train_mspec, train_mfcc), axis=2)
test_data = np.concatenate((test_mspec, test_mfcc), axis=2)

# Split the training data into training and validation sets
x_train, x_val, y_train, y_val = train_test_split(train_data, train_chords_ohe, test_size=0.2, shuffle=True)

# Define x_test and y_test
x_test = test_data
y_test = test_chords_ohe

# Define label_set
label_set = np.unique(train_chords)

# Save the preprocessed data as pickle files
with open('network_files/x_train.pkl', 'wb') as f:
    pickle.dump(x_train, f)
with open('network_files/y_train.pkl', 'wb') as f:
    pickle.dump(y_train, f)
with open('network_files/x_val.pkl', 'wb') as f:
    pickle.dump(x_val, f)
with open('network_files/y_val.pkl', 'wb') as f:
    pickle.dump(y_val, f)
with open('network_files/x_test.pkl', 'wb') as f:
    pickle.dump(x_test, f)
with open('network_files/y_test.pkl', 'wb') as f:
    pickle.dump(y_test, f)
with open('network_files/label_set.pkl', 'wb') as f:
    pickle.dump(label_set, f)

print("Train and test data for network have been generated.")