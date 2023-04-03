# DegreeProject
Using artificial neural networks to transcribe chords over time and find the key from an audio recording.

Current goals for the project:
- Using our categorization neural network on audio to find chords
- Creation of an intuitive and fast GUI

Breaking this down we start with chords, or combinations of notes. Musicians often use multiple notes at once when writing music, this concept is known as polyphany,
and these combinations of notes are called chords. The chords over the course of a song will typically define a progression through a scale (a set of notes which are
known to sound good together). *Important to note*, is that scales are subjective in nature, and often when multiple scales can be chosen the choice is based on 
readability for the musician. Scales and notes are denoted by the letters A to G, and the set of notes represent a set of pitches defined by a logarithmic equation.

Our goal is to use fast fourier transforms to generate a spectrogram (an amplitude of pitch over time graph), then find the mel scale cepstral coefficients which correspond to the tambre of audio, use a classification AI that can recognize which chords are being played, and then display the chord over time data.

# Scope
At the moment we have limited our training to guitar; however, adding in new instruments is more a question of data curation than processing. Depending on time alloted our group might record and label chords on piano and guitar to expand the dataset.

# TODO and Questions
- Colorbar for spectrograms
- Set radio buttons to prevent confusing behaviour from compare 1 and transcribe radio buttons
- Make buttons rounded
- Consider better ways of displaying chords