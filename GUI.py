import tkinter as tk
from tkinter import filedialog
from GUI_Interface import GUI_Interface
from librosa import display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import numpy as np
from IPython.display import Audio

class GUI(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.master.title("Audio Processing GUI")
        self.gui_interface = GUI_Interface()
        self.active_radio_button = ""
        self.mouse_event_connection = 0
        self.create_widgets()
        self.master.configure(background='light blue')
        
        


    def create_widgets(self):

        # Create left frame
        left_frame = tk.Frame(self.master)

        # Transcribe label and button
        self.transcribe_label = tk.Label(left_frame, text="Transcribed Chords:", bg="light blue")
        self.transcribe_button = tk.Button(left_frame, text="Transcribe", command=self.get_transcribed_audio, fg="white", bg="blue")

        self.transcribe_label.pack(side="top", pady=10, ipadx=5)
        self.transcribe_button.pack(side="top", pady=5, ipadx=5)

        # Transcribe output text
        self.transcribe_output_text = tk.Text(left_frame, state="disabled")
        self.transcribe_output_text.pack(side='top', fill='y', expand=True, pady=20)


        # Create center frame
        center_frame = tk.Frame(self.master)

        # Compare label and button
        self.compare_label = tk.Label(center_frame, text="Layered Spectrogram:", bg="light blue")
        self.compare_button = tk.Button(center_frame, text="Compare", command=self.get_compared_spectrograms, fg="white", bg="blue")

        self.compare_label.pack(side="top", pady=10, ipadx=5, padx=0)
        self.compare_button.pack(side="top", pady=5, ipadx=5, padx=0)

        # Comparison output text
        self.output_text = tk.Text(center_frame, state="disabled")
        self.output_text.pack(side='top', fill='y', expand=True, pady=20)


        # Create right frame
        right_frame = tk.Frame(self.master)
        
        # Create radio buttons
        self.transcribe_radio = tk.Radiobutton(right_frame, variable=self.active_radio_button, value='transcribe', )
        self.first_compare_radio = tk.Radiobutton(right_frame, variable=self.active_radio_button, value='firstCompare')
        self.second_compare_radio = tk.Radiobutton(right_frame, variable=self.active_radio_button, value='secondCompare')

        self.transcribe_radio.pack(side="left", pady=10, ipadx=5, padx=5)
        self.first_compare_radio.pack(side="left", pady=10, ipadx=5, padx=5)
        self.second_compare_radio.pack(side="left", pady=10, ipadx=5, padx=5)

        # Matplotlib canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)

        # Link mouse event to canvas for scrubbing
        self.mouse_event_connection = self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

        # Navigation toolbar for canvas
        self.toolbar = NavigationToolbar2Tk(self.canvas, right_frame)
        self.toolbar.update()


        # Add left, center and right frames to master frame
        left_frame.pack(side='left', fill="both", expand=True, padx=10, pady=5)
        center_frame.pack(side='left', fill="both", expand=True,  padx=10, pady=5)
        right_frame.pack(side='left', fill="both", expand=True,  padx=10, pady=5)

    def get_transcribed_audio(self):

        # Prompt user to select audio file
        self.file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])

        if self.file_path:

            # Display loading message
            self.transcribe_output_text.config(state="normal") # set state to normal
            self.transcribe_output_text.delete("1.0", tk.END)
            self.transcribe_output_text.insert(tk.END, "Loading...\n")
            self.transcribe_output_text.update()
            self.transcribe_output_text.config(state="disabled") # set state back to disabled

            # Set audio1 in GUI_Interface
            self.gui_interface.setAudio1(self.file_path)

            # Get transcribed chords and display them
            chords = self.gui_interface.getTranscribedAudio()
            self.transcribe_output_text.config(state="normal") # set state to normal
            self.transcribe_output_text.delete("1.0", tk.END)
            self.transcribe_output_text.insert(tk.END, " ".join(chords))
            self.transcribe_output_text.config(state="disabled") # set state back to disabled

            # Get spectrograms and display 
            print(self.gui_interface.getAudio1)
            self.gui_interface.ap.setAudio(self.gui_interface.getAudio1)
            spectrogram, _ = self.gui_interface.ap.melScaleSpec()
                
            # Plot the spectrogram using Matplotlib
            display.specshow(spectrogram, ax=self.ax, x_axis='time', y_axis='linear')
            self.ax.set(title='Compared Spectrograms')

            # Draw the canvas object with the updated plot
            self.canvas.draw()

    def get_compared_spectrograms(self):
        # Prompt user to select two audio files
        self.file_path1 = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if self.file_path1:
            self.file_path2 = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
            if self.file_path2:

                # Display loading message
                self.output_text.config(state="normal") # set state to normal
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Loading...\n")
                self.output_text.update()
                self.output_text.config(state="disabled") # set state back to disabled

                # Set audio1 and audio2 in GUI_Interface
                self.gui_interface.setAudio1(self.file_path1)
                self.gui_interface.setAudio2(self.file_path2)

                # Get compared spectrograms, the score of similarity, and display them
                spectrogram, score = self.gui_interface.getComparedSpectrogramsAndScore()
                
                # Plot the spectrogram using Matplotlib
                display.specshow(spectrogram, ax=self.ax, x_axis='time', y_axis='linear')
                self.ax.set(title='Compared Spectrograms')

                # Draw the canvas object with the updated plot
                self.canvas.draw()
                
                
                # Update output text
                self.output_text.config(state="normal") # set state to normal
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Done")
                self.output_text.config(state="disabled") # set state back to disabled

    def getAudioSegment(self, current_time, audio_segments):

        segment_length = len(audio_segments[0])

        # Calculate the index of the audio segment corresponding to the current time
        segment_index = int(current_time / segment_length)

        # Get the audio segment corresponding to the index
        audio_segment = audio_segments[segment_index * segment_length:
                                (segment_index + 1) * segment_length]

        return audio_segment

    def on_mouse_move(self, event):
        # Check if the mouse is over the spectrogram
        if event.inaxes == self.ax:
            # Calculate the current time based on the mouse position
            current_time = event.xdata
            if self.gui_interface.getAudioSegments1 != None:
                try:
                    if self.active_radio_button == "transcribe":
                        # Get the audio segment of transcribed file corresponding to the current time
                        audio_segment = self.getAudioSegment(current_time, self.gui_interface.getAudioSegments1)
                    elif self.active_radio_button == "firstCompare":
                        # Get the audio segment of first compared file corresponding to the current time
                        audio_segment = self.getAudioSegment(current_time, self.gui_interface.getAudioSegments1)
                    elif self.active_radio_button == "secondCompare":
                        # Get the audio segment of second compared file corresponding to the current time
                        audio_segment = self.getAudioSegment(current_time, self.gui_interface.getAudioSegments2)

                    # Update the audio player to play the current audio segment
                    Audio(data=audio_segment, rate=22050)

                except:
                    print('There was an error in audio playback')

if __name__ == "__main__":
    
    # Main loop for running GUI
    root = tk.Tk()
    root.title("Audio Processing GUI")
    gui = GUI(root)
    gui.pack()
    root.mainloop()
