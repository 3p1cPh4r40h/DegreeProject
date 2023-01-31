# Class AudioProcessor: Listens to audio and creates spectrograms

import numpy as np
import librosa

class AudioProcessor:

    audio = None

    def __init__(self):
        pass

    def __init__(self, audio):
    # This constructor sets the audio for processing.
        self.audio = audio
    
    def setAudio(self, audio):
    # Set audio for processing
        self.audio = audio

    def getAudio(self):
    # Get audio from AudioProcessor object
        return self.audio

    def melScaleSpec(self):
    # Create Mel Scale Spectrogram from audio
        
        # 22050 is the default sample rate for librosa
        # and is the SR for all audio we use in this project
        melSpec = librosa.feature.melspectrogram(self.audio, sr=22050, n_mels=128, fmax=8000)
        return melSpec

    def melScaleCepstralCoefficients(self):
    # Find Mel Scale Cepstral Coefficients (correlated to tambre) for a song

        # 22050 is the default sample rate for librosa
        # and is the SR for all audio we use in this project
        # Compute the MFCCs
        melCepstralCoeff = librosa.feature.mfcc(self.audio, sr=22050, n_mfcc=128)
        # Normalize the MFCCs
        melCepstralCoeff = np.mean(melCepstralCoeff, axis=1)
        return melCepstralCoeff

    def getSpectrograms(self):
    # Returns array with spectrogram and cepstral coefficients
        spectrograms = np.asarray([self.melScaleSpec(), self.melScaleCepstralCoefficients])