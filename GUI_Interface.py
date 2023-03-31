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
        self.ap.setAudio(self.audio2)
        spectrogram2 = self.ap.melScaleSpec()

        self.audio_segments_1 = ts.chop_audio(self.audio1)
        self.audio_segments_2 = ts.chop_audio(self.audio2)

        # Determine the maximum length along the second axis
        max_length = max(spectrogram1.shape[1], spectrogram2.shape[1])

        # Pad arrays to maximum length along second axis
        spectrogram1 = np.pad(spectrogram1, ((0, 0), (0, max_length - spectrogram1.shape[1])), 'constant')
        spectrogram2 = np.pad(spectrogram2, ((0, 0), (0, max_length - spectrogram2.shape[1])), 'constant')

        # subtract spectrograms for comparison
        layeredSpectrogram = spectrogram1 - spectrogram2
        '''
        #normalize the spectrograms
        normalized_spec1 = (spectrogram1 - np.mean(spectrogram1)) / np.std(spectrogram1)
        normalized_spec2 = (spectrogram2 - np.mean(spectrogram2)) / np.std(spectrogram2)
        
        
        print('before crosscor')
        #get the cross correlation between them
        crosscor = correlate2d(normalized_spec1, normalized_spec2, mode='same')
        print('after crosscor')
        '''

        #the similarity is equal to the maximum value of the cross correlation
        similarity = "Placeholder until we speed up crosscor"
        score = str(similarity)

        return layeredSpectrogram, score

'''
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

        
        
        return similarity
'''
