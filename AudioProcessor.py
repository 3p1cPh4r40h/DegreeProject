# Class AudioProcessor: Listens to audio and creates spectrograms

import numpy as np
import librosa

class AudioProcessor:

    audio = []

    def __init__(self, audio=None):
    # This constructor sets the audio for processing.
    # Audio is optional and can be added later.
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
        # Normalize the spectrogram
        min = np.min(melSpec)
        max = np.max(melSpec)
        for i in range(len(melSpec)):
            melSpec[i] = (melSpec[i] - min) / (max - min)
        return melSpec

    def melScaleCepstralCoefficients(self):
    # Find Mel Scale Cepstral Coefficients (correlated to tambre) for a song

        # 22050 is the default sample rate for librosa
        # and is the SR for all audio we use in this project
        # Compute the MFCCs
        melCepstralCoeff = librosa.feature.mfcc(self.audio, sr=22050, n_mfcc=128)
        # Normalize the MFCCs
        min = np.min(melCepstralCoeff)
        max = np.max(melCepstralCoeff)
        for i in range(len(melCepstralCoeff)):
            melCepstralCoeff[i] = (melCepstralCoeff[i] - min) / (max - min)
        return melCepstralCoeff

    def getSpectrograms(self):
    # Returns array with spectrogram and cepstral coefficients
        mspec = self.melScaleSpec()
        mfcc = self.melScaleCepstralCoefficients()
        spectrograms = [mspec, mfcc]
        spectrograms = np.concatenate(([mspec], [mfcc]), axis=2)
        spectrograms = spectrograms.reshape(spectrograms.shape[0], spectrograms.shape[1], spectrograms.shape[2], 1)

        return spectrograms