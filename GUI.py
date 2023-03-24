import tkinter as tk
from tkinter import filedialog
from GUI_Interface import GUI_Interface
from librosa import display
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


class GUI(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.master.title("Audio Processing GUI")
        self.gui_interface = GUI_Interface()
        self.create_widgets()

    def create_widgets(self):

        # Transcribe button and label
        self.transcribe_label = tk.Label(self.master, text="Transcribed Chords:")
        self.transcribe_button = tk.Button(self.master, text="Transcribe", command=self.get_transcribed_audio)
        self.transcribe_label.pack(side="top", pady=10)
        self.transcribe_button.pack(side="top", pady=5)

        # Compare button and label
        self.compare_label = tk.Label(self.master, text="Layered Spectrogram:")
        self.compare_button = tk.Button(self.master, text="Compare", command=self.get_compared_spectrograms)
        self.compare_label.pack(side="top", pady=10)
        self.compare_button.pack(side="top", pady=5)

        # Output text
        self.output_text = tk.Text(self.master, height=10, state="disabled")
        self.output_text.pack(side="top", pady=5)

        # Matplotlib canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        self.toolbar.update()

    def get_transcribed_audio(self):

        # Prompt user to select audio file
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])

        if file_path:

            # Display loading message
            self.output_text.config(state="normal") # set state to normal
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Loading...\n")
            self.output_text.update()
            self.output_text.config(state="disabled") # set state back to disabled

            # Set audio1 in GUI_Interface
            self.gui_interface.setAudio1(file_path)

            # Get transcribed chords and display them
            chords = self.gui_interface.getTranscribedAudio()
            self.output_text.config(state="normal") # set state to normal
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "\n".join(chords))
            self.output_text.config(state="disabled") # set state back to disabled
            
            

    def get_compared_spectrograms(self):
        # Prompt user to select two audio files
        file_path1 = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path1:
            file_path2 = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
            if file_path2:

                # Display loading message
                self.output_text.config(state="normal") # set state to normal
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Loading...\n")
                self.output_text.update()
                self.output_text.config(state="disabled") # set state back to disabled

                # Set audio1 and audio2 in GUI_Interface
                self.gui_interface.setAudio1(file_path1)
                self.gui_interface.setAudio2(file_path2)

                # Get compared spectrograms and display them
                spectrogram = self.gui_interface.getComparedSpectrograms()

                # Plot the spectrogram using Matplotlib
                display.specshow(spectrogram, ax=self.ax, x_axis='time', y_axis='linear')
                self.ax.set(title='Compared Spectrograms')

                # Draw the canvas
                self.canvas.draw()
                

                # Update output text
                self.output_text.config(state="normal") # set state to normal
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Done")
                self.output_text.config(state="disabled") # set state back to disabled
                

if __name__ == "__main__":
    
    # Main loop for running GUI
    root = tk.Tk()
    root.title("Audio Processing GUI")
    gui = GUI(root)
    gui.pack()
    root.mainloop()
