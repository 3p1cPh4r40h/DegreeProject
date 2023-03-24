# Class GUI_Interface: Holds the functions that are called by the GUI

from AudioProcessor import AudioProcessor as ap
from Transcriber import Transcriber as ts
import librosa 
import numpy as np
from scipy.signal import correlate2d


class GUI_Interface:

    def __init__(self, audio1=None, audio2=None):
    # GUI has a placeholder for two audio files,
    # an AudioProcessor object, and a Transcriber object
        if audio1 != None:
            a1, _ = librosa.load(audio1)
            self.audio1 = a1
        if audio2 != None:
            a2, _ = librosa.load(audio2)
            self.audio2 = a2
        self.ap = ap()
        self.ts = ts()



    # Set and get functions


    def setAudio1(self, audio):

    # Set audio for processing
        a1, _ = librosa.load(audio)
        self.audio1 = a1

    def getAudio1(self):

    # Get audio from GUI interface
        return self.audio1

    def setAudio2(self, audio):

    # Set audio for processing
        a2, _ = librosa.load(audio)
        self.audio2 = a2

    def getAudio2(self):

    # Get audio from GUI interface
        return self.audio2

    def remove_consecutive_duplicates(self, list):

        new_list = []
        for i, item in enumerate(list):
            if i == 0 or item != list[i-1]:
                new_list.append(item)

        return new_list



    # Interfacing functions for the GUI driver.py


    def getTranscribedAudio(self):

    # Transcribe the audio and return a list of chords
        self.ts.setAudio(self.audio1)
        chords = self.ts.findChords()
        chords = self.remove_consecutive_duplicates(chords)
        return chords

    def getComparedSpectrograms(self):
        
    # Create spectrogram of both audio files and compare them
        self.ap.setAudio(self.audio1)
        spectrogram1 = self.ap.melScaleSpec()
        self.ap.setAudio(self.audio2)
        spectrogram2 = self.ap.melScaleSpec()
        
        # Determine the maximum length along the second axis
        max_length = max(spectrogram1.shape[1], spectrogram2.shape[1])

        # Pad arrays to maximum length along second axis
        spectrogram1 = np.pad(spectrogram1, ((0, 0), (0, max_length - spectrogram1.shape[1])), 'constant')
        spectrogram2 = np.pad(spectrogram2, ((0, 0), (0, max_length - spectrogram2.shape[1])), 'constant')

        # subtract spectrograms for comparison
        layeredSpectrogram = spectrogram1 - spectrogram2

        return layeredSpectrogram


    #function to get the score of similarity between spectrograms todo: use more advanced comparison
    def getComparedScore(self):

        self.ap.setAudio(self.audio1)
        spec1 = self.ap.melScaleSpec()
        self.ap.setAudio(self.audio2)
        spec2 = self.ap.melScaleSpec()
        
        # Determine the maximum length along the second axis
        max_length = max(spec1.shape[1], spec2.shape[1])

        # Pad arrays to maximum length along second axis
        spec1 = np.pad(spec1, ((0, 0), (0, max_length - spec1.shape[1])), 'constant')
        spec2 = np.pad(spec2, ((0, 0), (0, max_length - spec2.shape[1])), 'constant')

        #normalize the spectrograms
        spec1 = (spec1 - np.mean(spec1)) / np.std(spec1)
        spec2 = (spec2 - np.mean(spec2)) / np.std(spec2)

        #get the cross correlation between them
        crosscor = correlate2d(spec1, spec2, mode='same')

        #the similarity is equal to the maximum value of the cross correlation
        similarity = np.max(crosscor)
        
        return similarity
