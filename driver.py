import tkinter as tk
from tkinter import filedialog
from GUI_Interface import GUI_Interface
import numpy as np
from PIL import Image, ImageTk

import librosa
from librosa import display
import matplotlib.pyplot as plt

class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Audio Processing GUI")
        self.gui_interface = GUI_Interface()
        self.create_widgets()
        self.image = None

    def create_widgets(self):
        # Transcribe button and label
        self.transcribe_label = tk.Label(self.master, text="Transcribed Chords:")
        self.transcribe_label.pack(side="top", pady=10)

        self.transcribe_button = tk.Button(self.master, text="Transcribe", command=self.get_transcribed_audio)
        self.transcribe_button.pack(side="top", pady=5)

        # Compare button and label
        self.compare_label = tk.Label(self.master, text="Layered Spectrogram:")
        self.compare_label.pack(side="top", pady=10)

        self.compare_button = tk.Button(self.master, text="Compare", command=self.get_compared_spectrograms)
        self.compare_button.pack(side="top", pady=5)

        # Output text
        self.output_text = tk.Text(self.master, height=10)
        self.output_text.config(state="normal")
        self.output_text.pack(side="top", pady=5)


    def get_transcribed_audio(self):
        # Prompt user to select audio file
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            # Set audio1 in GUI_Interface
            self.gui_interface.setAudio1(file_path)
            # Get transcribed chords and display them
            chords = self.gui_interface.getTranscribedAudio()
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "\n".join(chords))

    def get_compared_spectrograms(self):
        # Prompt user to select two audio files
        file_path1 = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path1:
            file_path2 = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
            if file_path2:
                # Set audio1 and audio2 in GUI_Interface
                self.gui_interface.setAudio1(file_path1)
                self.gui_interface.setAudio2(file_path2)
                # Get compared spectrograms and display them
                spectrogram = self.gui_interface.getComparedSpectrograms()
                self.output_text.delete("1.0", tk.END)
                self.convert_to_image(spectrogram)
                self.output_text.image_create(tk.END, image=self.image)

    def convert_to_image(self, spectrogram):
        # Convert spectrogram to tkinter image
        spectrogram *= 255
        spectrogram = np.abs(255 - spectrogram)
        # Convert the spectrogram to a PIL image
        image = Image.fromarray(np.uint8(spectrogram)).convert("RGB")
        image.show()
        # Convert the PIL image to a Tkinter image and return it
        self.image = ImageTk.PhotoImage(image)

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    gui.pack()
    root.mainloop()
