# Class GUI_Interface: Holds the functions that are called by the GUI

from AudioProcessor import AudioProcessor as ap
from Transcriber import Transcriber as ts
import librosa 

class GUI_Interface:

    audio1 = None
    audio2 = None

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
        spectrogram1 = self.ap.melScaleSpec()
        self.ap.setAudio(self.audio2)
        spectrogram2 = self.ap.melScaleSpec()
        self.ap.setAudio(self.audio1)
        layeredSpectrogram = spectrogram1 - spectrogram2
        return layeredSpectrogram

