# Class Transcribe: Holds the logic for predicting the musicial notation given audio

import pandas as pd
import numpy as np

class Transcribe:

    noteFrequencyTable = pd.DataFrame()
    # Holds predicted notes
    notes = None
    # Holds predicted key
    key = None
    # Holds predicted chords
    chords = None

    def __init__(self, ear):
    # Takes ear object that has listened to audio
        ear = self.ear
    
    def findNotes(self):
    # Predict the notes that would be picked out by a human
        self.notes = self.ear.getSpectrograms()
        return self.notes

    def findKey(self):
    # Predict the key that would be chosen by a human
        self.key = self.notes
        return self.key

    def findChords(self):
    # Predict the chord of a song based on the notes and key
        self.chords = self.notes + self.key
        return self.chords