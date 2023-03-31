# Class Transcribe: Holds the logic for predicting the musicial notation given audio

from AudioProcessor import AudioProcessor as ap
import keras
import numpy as np

class Transcriber:

    def __init__(self, audio=None):

    # Transcriber has a palceholder for one variable,
    # an audio file to be transcribed.
        self.audio = audio
        self.network = keras.models.load_model('network_files/model90proof.h5') #Import Network
        self.ap = ap() # AudioProcessor object used to find spectrograms
        self.chords = []
        self.audio = []

    def setAudio(self, audio):

    # Set audio for transcribing
        self.audio = audio

    def chop_audio(self, audio):
    
    # Internal function to chop audio into 1 second segments

        # Sample rate used to chop audio for AI (chopping to length of shortest training clip)
        sr = 24775

        # Load audio file using librosa
        # Compute the number of 1-second segments in the audio
        num_segments = int(np.ceil(len(audio) / sr))

        # Pad the audio with silence if necessary to make it an exact number of seconds
        audio = np.pad(audio, (0, num_segments * sr - len(audio)), 'constant')

        # Split the audio into 1-second segments
        segments = np.split(audio, num_segments)

        return segments

    def findChords(self):

    # Predict the chord of a song based on the notes and key

        choppedAudio = self.chop_audio(self.audio) # List for holding audio cut into pieces
        chords = []
        for clip in choppedAudio:
            self.ap.setAudio(clip)
            x = self.ap.getSpectrograms()
            chords.append(self.network.predict(x, batch_size=48))
            
        label_set = ['Am', 'Bb', 'Bdim', 'C', 'Dm', 'Em', 'F', 'G']
        self.chords = [label_set[np.argmax(label)] for label in chords]
        
        return self.chords, choppedAudio