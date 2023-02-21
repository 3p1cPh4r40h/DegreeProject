# Class Transcribe: Holds the logic for predicting the musicial notation given audio

import AudioProcessor as ap
import tensorflow as tf

class Transcriber:

    chords = [] # List for holding the transcribed chords over time
    network = tf.keras.models.load_model('network_files/model.h5') #Import Network
    ap = ap() # AudioProcessor object used to find spectrograms

    def __init__(self):
        pass

    def __init__(self, audio):
    # This constructor sets the audio for processing.
        self.audio = audio

    def findChords(self, audio):
    # Predict the chord of a song based on the notes and key
        cutAudio = [] # List for holding audio cut into pieces
        for clip in cutAudio:
            ap.setAudio(clip)
            spectrogram, mfcc = ap.getSpectrograms()
            self.chords.append(self.network.run(spectrogram, mfcc))
        
        return self.chords