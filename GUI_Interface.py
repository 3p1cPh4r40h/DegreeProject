# Class GUI_Interface: Holds the functions that are called by the GUI

import numpy as np

class GUI_Interface:

    def __init__(self, audio1, audio2, ear, transcribe):
    # GUI has a placeholder for two audio files and an ear and transcribe object
        self.audio1 = audio1
        self.audio2 = audio2
        self.ear = ear(audio1)
        self.transcribe = transcribe(ear)

    def transcribeAudio(self):
    # Transcribe the audio and return the results
        notes = self.transcribe.findNotes()
        key = self.transcribe.findKey()
        chords = self.transcribe.findChords()
        notesKeyChords = np.asarray([notes, key, chords])
        return notesKeyChords

    def compareSpectrograms(self):
    # Create spectrogram of both audio files and compare them
        spectrogram1 = self.ear.melScaleSpec()
        self.ear.setAudio(self.audio2)
        spectrogram2 = self.ear.melScaleSpec()
        self.ear.setAudio(self.audio1)
        layeredSpectrogram = spectrogram1 - spectrogram2
        return layeredSpectrogram

