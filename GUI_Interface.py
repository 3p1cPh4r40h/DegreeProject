# Class GUI_Interface: Holds the functions that are called by the GUI

from AudioProcessor import AudioProcessor as ap
from Transcriber import Transcriber as ts
import librosa 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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

        # Placeholder variables for segments of loaded librosa audio
        # These are used for playback
        self.audio_segments_1 = None
        self.audio_segments_2 = None



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

    def getAudioSegments1(self):
        
        # Get audio from GUI interface
        return self.audio_segments_1
    
    def getAudioSegments2(self):

        # Get audio from GUI interface
        return self.audio_segments_2

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
        chords, segments = self.ts.findChords()
        self.audio_segments_1 = segments
        chords = self.remove_consecutive_duplicates(chords)
        return chords

    def getComparedSpectrogramsAndScore(self):
        
    # Create spectrogram of both audio files and compare them
        self.ap.setAudio(self.audio1)
        spectrogram1 = self.ap.melScaleSpec()
        self.audio_segments_1 = self.ts.chop_audio(self.ap.getAudio())
        self.ap.setAudio(self.audio2)
        spectrogram2 = self.ap.melScaleSpec()
        self.audio_segments_2 = self.ts.chop_audio(self.ap.getAudio())

        # Determine the maximum length along the second axis
        max_length = max(spectrogram1.shape[1], spectrogram2.shape[1])

        # Pad arrays to maximum length along second axis
        spectrogram1 = np.pad(spectrogram1, ((0, 0), (0, max_length - spectrogram1.shape[1])), 'constant')
        spectrogram2 = np.pad(spectrogram2, ((0, 0), (0, max_length - spectrogram2.shape[1])), 'constant')

        # subtract spectrograms for comparison
        layeredSpectrogram = spectrogram1 - spectrogram2

        normalized_spec1 = (spectrogram1 - np.mean(spectrogram1)) / np.std(spectrogram1)
        normalized_spec2 = (spectrogram2 - np.mean(spectrogram2)) / np.std(spectrogram2)
        
        # Compute the spectral contrast matrices for the two audio files
        contrast1 = librosa.feature.spectral_contrast(S=normalized_spec1)
        contrast2 = librosa.feature.spectral_contrast(S=normalized_spec2)

        # Compute the cosine similarity between the spectral contrast matrices
        similarity = cosine_similarity(contrast1.T, contrast2.T)

        score = str(100*similarity[0][0]) + "%"

        return layeredSpectrogram, score
