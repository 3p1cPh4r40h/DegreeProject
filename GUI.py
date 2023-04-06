import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from GUI_Interface import GUI_Interface
from librosa import display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import numpy as np
from sounddevice import play
import winsound

class GUI(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.master.title("Audio Processing GUI")
        self.gui_interface = GUI_Interface()
        self.active_radio_button = tk.StringVar()
        self.mouse_event_connection = 0
        self.create_widgets()
        self.master.configure(background='light blue')
        self.file_path = ""
        self.file_path2 = ""
        self.file_path1 = ""
        
        


    def create_widgets(self):

        # Create left frame
        left_frame = tk.Frame(self.master,bg='light blue')
        s = Style()
        s.configure('left_frame', background='light blue')
        left_frame.master.configure(background='light blue')
        

        # Transcribe label and button
        self.transcribe_label = tk.Label(left_frame, text="Transcribed Chords:", bg="light blue")
        self.transcribe_button = tk.Button(left_frame, text="Transcribe", command=self.get_transcribed_audio, fg="white", bg="blue")

        # Pack the transcribe button
        self.transcribe_label.pack(side="top", pady=10, ipadx=5)
        self.transcribe_button.pack(side="top", pady=5, ipadx=5)
        self.transcribe_output_text = tk.Text(left_frame, height=10,state="disabled")
        self.transcribe_output_text.pack(side='top', expand=False, pady=30)

        # Compare label and button
        self.compare_label = tk.Label(left_frame, text="Layered Spectrogram:", bg="light blue")
        self.compare_button = tk.Button(left_frame, text="Compare", command=self.get_compared_spectrograms, fg="white", bg="blue")
        self.compare_label.pack(side="top", pady=10, ipadx=5, padx=10)
        self.compare_button.pack(side="top", pady=5, ipadx=5, padx=10)

        # Comparison output text
        self.output_text = tk.Text(left_frame,  height=5,state="disabled")
        self.output_text.pack(side='top', expand=False, pady=20)

        # Create center frame
        center_frame = tk.Frame(self.master)



        # Create right frame
        right_frame = tk.Frame(self.master)
        
        # Create top of the right frame to hold the radio buttons
        top_right_frame = tk.Frame(right_frame)
        top_right_frame.pack(side='top', fill='x', padx=10, pady=5)
        # Create radio buttons
        self.play_button = tk.Button(top_right_frame, text="Play Song", command=self.playMusic,fg="white",bg = "lime green")


        self.audio_selection_label = tk.Label(top_right_frame, text="Choose Audio to Play:", bg="light blue")
        self.transcribe_radio = tk.Radiobutton(top_right_frame, text='Transcribe Audio', variable=self.active_radio_button, value='transcribe', state="disabled")
        self.first_compare_radio = tk.Radiobutton(top_right_frame, text='Compare Audio 1', variable=self.active_radio_button, value='firstCompare', state="disabled")
        self.second_compare_radio = tk.Radiobutton(top_right_frame, text='Compare Audio 2', variable=self.active_radio_button, value='secondCompare', state="disabled")
        self.audio_selection_label.pack(side="top", pady=10, ipadx=5, padx=0)
        self.transcribe_radio.pack(side="left", pady=10, ipadx=5, padx=5)
        self.first_compare_radio.pack(side="left", pady=10, ipadx=5, padx=5)
        self.second_compare_radio.pack(side="left", pady=10, ipadx=5, padx=5)
        
        self.play_button.pack(side="top", pady=5,ipadx=5)
        # Create bottom of right frame to hold canvas and toolbar
        bottom_right_frame = tk.Frame(right_frame)
        bottom_right_frame.pack(side='top', fill='both', expand=True, padx=10, pady=5)

        # Matplotlib canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=bottom_right_frame)
        self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)

        # Link mouse event to canvas for scrubbing
        self.mouse_event_connection = self.canvas.mpl_connect('button_press_event', self.on_mouse_click)

        # Navigation toolbar for canvas
        self.toolbar = NavigationToolbar2Tk(self.canvas, bottom_right_frame)
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

            # Clear the canvas
            plt.cla()

            # Get spectrograms and display 
            self.gui_interface.ap.setAudio(self.gui_interface.getAudio1())
            spectrogram = self.gui_interface.ap.melScaleSpec()
            
            # Plot the spectrogram using Matplotlib
            display.specshow(spectrogram, ax=self.ax, x_axis='time', y_axis='linear')
            self.ax.set(title='Transcribed Audio')
            
            # Draw the canvas object with the updated plot
            self.canvas.draw()

            # Enable selection of transcribe radio button and disable other radio buttons
            self.transcribe_radio.config(state='normal')
           # self.first_compare_radio.config(state="disabled")
           # self.second_compare_radio.config(state="disabled")
            self.transcribe_radio.select()

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

                # Clear the canvas
                plt.cla()

                # Get compared spectrograms and and display them
                spectrogram, score = self.gui_interface.getComparedSpectrogramsAndScore()

                # Plot the spectrogram using Matplotlib
                display.specshow(spectrogram, ax=self.ax, x_axis='time', y_axis='linear')
                self.ax.set(title='Compared Spectrograms')


                # Draw the canvas object with the updated plot

                self.canvas.draw()
                
                
                # Update output text
                self.output_text.config(state="normal") # set state to normal
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, score)
                self.output_text.config(state="disabled") # set state back to disabled

                # Enable selection of compare radio buttons and disable other radio button
               # self.transcribe_radio.config(state="disabled")
                self.first_compare_radio.config(state='normal')
                self.second_compare_radio.config(state='normal')
                self.first_compare_radio.select()

    def getAudioSegment(self, current_time, audio_segments):
        # Current time is given in seconds (decimal value)
        # Audio segments are 24775 samples long at a sample rate of 22050
        
        # Convert current_time to an integer
        current_time = round(current_time)
        # Number of samples to get to the clicked time
        number_of_samples = current_time * 22050
        # Calculate the index of the audio segment corresponding to the current time
        segment_index = round(number_of_samples / 24775)

        # Get the audio segment corresponding to the index
        audio_segment = audio_segments[segment_index]

        return audio_segment

    def on_mouse_click(self, event):
        # Check if the mouse is over the spectrogram
        if event.inaxes == self.ax:
            # Calculate the current time based on the mouse position
            current_time = event.xdata
            if self.gui_interface.getAudioSegments1 != None and event.button == 1:
 
                if self.active_radio_button.get() == "transcribe":
                    # Get the audio segment of transcribed file corresponding to the current time
                    audio_segment = self.getAudioSegment(current_time, self.gui_interface.getAudioSegments1())
                elif self.active_radio_button.get() == "firstCompare":
                    # Get the audio segment of first compared file corresponding to the current time
                    audio_segment = self.getAudioSegment(current_time, self.gui_interface.getAudioSegments1())
                elif self.active_radio_button.get() == "secondCompare":
                    # Get the audio segment of second compared file corresponding to the current time
                    audio_segment = self.getAudioSegment(current_time, self.gui_interface.getAudioSegments2())
                # Update the audio player to play the current audio segment

                
                try:
                    audio_segment = np.asarray(audio_segment)
                    audio_segment = audio_segment.T
                    play(audio_segment, 22050)
                except UnboundLocalError as e:
                    print(e)
                    print('Please wait for audio to process before trying to play an audio file.')
    
    def playMusic(self):
        # check if the user has entered in some music
                if self.active_radio_button.get() == "transcribe":
                    # Get the audio segment of transcribed file corresponding to the current time
                            if self.file_path:
                                winsound.PlaySound(self.file_path, winsound.SND_FILENAME) 
                elif self.active_radio_button.get() == "firstCompare":
                    # Get the audio segment of first compared file corresponding to the current time
                            if self.file_path1:
                                winsound.PlaySound(self.file_path1, winsound.SND_FILENAME) 
                elif self.active_radio_button.get() == "secondCompare":
                            if self.file_path2:
                                winsound.PlaySound(self.file_path2, winsound.SND_FILENAME) 

if __name__ == "__main__":
    
    # Main loop for running GUI
    root = tk.Tk()
    root.title("Audio Processing GUI")
    gui = GUI(root)
    gui.pack()
    root.mainloop()
