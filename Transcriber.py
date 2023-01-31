# Class Transcribe: Holds the logic for predicting the musicial notation given audio

import AudioProcessor as ap

class Transcriber:

    # Holds predicted chords
    chords = None
    network = None #Import Network
    ap = ap()

    def __init__(self):
        pass

    def __init__(self, audio):
    # This constructor sets the audio for processing.
        self.audio = audio

    def findChords(self, audio):
    # Predict the chord of a song based on the notes and key
        ap.setAudio(audio)
        spectrogram, mfcc = ap.getSpectrograms()
        chords = self.network.run(spectrogram, mfcc)
        return self.chords