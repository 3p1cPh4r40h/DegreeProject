import tkinter as tk
from tkinter import filedialog
from GUI_Interface import GUI_Interface
import numpy as np
from PIL import Image, ImageTk
import librosa

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
                self.output_text.image_create(tk.END, image=self.convert_to_image(spectrogram))

    def convert_to_image(self, spectrogram):
        # Convert spectrogram to tkinter image
        # Normalize the spectrogram to a range of 0-255
        spectrogram -= np.min(spectrogram)
        spectrogram /= np.max(spectrogram)
        spectrogram *= 255

        # Convert the spectrogram to a PIL image
        image = Image.fromarray(spectrogram.astype(np.uint8)).convert("RGB")

        # Convert the PIL image to a Tkinter image and return it
        return ImageTk.PhotoImage(image)

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    gui.pack()
    root.mainloop()
