# Class Ear: Listens to audio and creates spectrograms

import pandas as pd
import numpy as np

class Ear:

    # Equivalent rectangular bandwidth (ERB) table holds bandwidth of 
    # human ear (used for filtering)
    tableERB = pd.DataFrame()
    # Variable for holding audio adjusted to human hearing bandwidth
    adjustedAudio = None

    def __init__(self, audio):
    # Takes Librosa audio file
        audio = self.audio        

    def setAudio(self, audio):
    # Set audio to be listened to by ear
        self.audio = audio

    def getAudio(self):
    # Get audio from ear
        return self.audio


    def criticalBand(self):
    # Filter audio with ERB
    
        self.adjustedAudio = self.audio * self.tableERB
        return self.adjustedAudio


    def melScaleSpec(self):
    # Create Mel Scale Spectrogram from audio
        
        melSpec = self.adjustedAudio
        return melSpec

    def melScaleCepstralCoefficients(self):
    # Find Mel Scale Cepstral Coefficients (correlated to tambre) for a song

        melCepstralCoeff = self.adjustedAudio
        return melCepstralCoeff

    def getSpectrograms(self):
    # Returns array with spectrogram and cepstral coefficients
        spectrograms = np.asarray([self.melScaleSpec(), self.melScaleCepstralCoefficients])