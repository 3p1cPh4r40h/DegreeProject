# Class Ear: Listens to audio and creates spectrograms

import pandas as pd
import numpy as np
import librosa

class Ear:

    audio = np.array

    def __init__(self):
        pass

    def __init__(self, audio):
    # This constructor sets the audio for ear.
        self.audio = audio
    
    def setAudio(self, audio):
    # Set audio to be listened to by ear
        self.audio = audio

    def getAudio(self):
    # Get audio from ear
        return self.audio

    def melScaleSpec(self, audio, sr):
    # Create Mel Scale Spectrogram from audio
        
        melSpec = librosa.feature.melspectrogram(audio, sr=sr, n_mels=128, fmax=8000)
        return melSpec

    def melScaleCepstralCoefficients(self, audio, sr):
    # Find Mel Scale Cepstral Coefficients (correlated to tambre) for a song

        # Compute the MFCCs
        melCepstralCoeff = librosa.feature.mfcc(audio, sr=sr, n_mfcc=13)
        # Normalize the MFCCs
        melCepstralCoeff = np.mean(melCepstralCoeff, axis=1)
        return melCepstralCoeff

    def getSpectrograms(self):
    # Returns array with spectrogram and cepstral coefficients
        spectrograms = np.asarray([self.melScaleSpec(), self.melScaleCepstralCoefficients])