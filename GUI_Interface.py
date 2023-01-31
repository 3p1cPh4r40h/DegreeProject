# Class GUI_Interface: Holds the functions that are called by the GUI

import AudioProcessor as ap
import Transcriber as ts
import librosa 

class GUI_Interface:

    audio1 = None
    audio2 = None

    def __init__(self):
    # Empty constructor only initilizes AudioProcessor and Transcriber
        self.ap = ap()
        self.ts = ts()
    
    def __init__(self, audio1, audio2):
    # GUI has a placeholder for two audio files,
    # an AudioProcessor object, and a Transcriber object
        self.audio1 = librosa.load(audio1)
        self.audio2 = librosa.load(audio2)
        self.ap = ap()
        self.ts = ts()



    # Set and get functions
    def setAudio1(self, audio):
    # Set audio for processing
        self.audio1 = audio

    def getAudio1(self):
    # Get audio from GUI interface
        return self.audio1

    def setAudio2(self, audio):
    # Set audio for processing
        self.audio2 = audio

    def getAudio2(self):
    # Get audio from GUI interface
        return self.audio2



    # Interfacing functions for the GUI driver.py
    def getTranscribedAudio(self):
    # Transcribe the audio and return the results
        chords = self.ts.findChords(self.audio1)
        return chords

    def getComparedSpectrograms(self):
    # Create spectrogram of both audio files and compare them
        spectrogram1 = self.ap.melScaleSpec()
        self.ap.setAudio(self.audio2)
        spectrogram2 = self.ap.melScaleSpec()
        self.ap.setAudio(self.audio1)
        layeredSpectrogram = spectrogram1 - spectrogram2
        return layeredSpectrogram

