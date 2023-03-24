import tkinter as tk
from tkinter import filedialog
from GUI_Interface import GUI_Interface
import numpy as np
from PIL import Image, ImageTk
import winsound
class GUI(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.master.title("Audio Processing GUI")
        self.gui_interface = GUI_Interface()
        self.image = None
        self.file_path = ""
        self.master.configure(background='light blue')

        self.create_widgets()
    def create_widgets(self):

        # Transcribe button and label
        self.transcribe_label = tk.Label(self.master, text="Transcribed Chords:",bg = "light blue")
        self.transcribe_button = tk.Button(self.master, text="Transcribe", command=self.get_transcribed_audio,fg="white",bg = "blue")
        self.play_button = tk.Button(self.master, text="Play Song", command=self.playMusic,fg="white",bg = "lime green")
      
        self.transcribe_label.pack(side="top", pady=10,ipadx=5)
        self.transcribe_button.pack(side="top", pady=5,ipadx=5)
        self.play_button.pack(side="top", pady=5,ipadx=5)
        # Output text
        self.transcribe_output_text = tk.Text(self.master, height=3, state="disabled")
        self.transcribe_output_text.pack(side="top", pady=5)

        # Compare button and label
        self.compare_label = tk.Label(self.master, text="Layered Spectrogram:",bg = "light blue")
        self.compare_button = tk.Button(self.master, text="Compare", command=self.get_compared_spectrograms,fg="white",bg = "blue")
        self.compare_label.pack(side="top", pady=10,ipadx=5,padx = 0)
        self.compare_button.pack(side="top", pady=5,ipadx=5,padx = 0)

        # Output Image
        self.output_text = tk.Text(self.master, height=2, state="disabled")
        self.output_text.pack(side="top", pady=5)


    def get_transcribed_audio(self):

        # Prompt user to select audio file
        self.file_path  = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        
        if self.file_path :

            # Display loading message
            self.transcribe_output_text.config(state="normal") # set state to normal
            self.transcribe_output_text.delete("1.0", tk.END)
            self.transcribe_output_text.insert(tk.END, "Loading...\n")
            self.transcribe_output_text.update()
            self.transcribe_output_text.config(state="disabled") # set state back to disabled

            # Set audio1 in GUI_Interface
            self.gui_interface.setAudio1(self.file_path )

            # Get transcribed chords and display them
            chords = self.gui_interface.getTranscribedAudio()
            self.transcribe_output_text.config(state="normal") # set state to normal
            self.transcribe_output_text.delete("1.0", tk.END)
            self.transcribe_output_text.insert(tk.END, " ".join(chords))
            self.transcribe_output_text.config(state="disabled") # set state back to disabled

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
                self.output_text.config(state="normal") # set state to normal
                self.output_text.delete("1.0", tk.END)
                self.convert_to_image(spectrogram)
                self.output_text.image_create(tk.END, image=self.image)
                self.output_text.config(state="disabled") # set state back to disabled
        

    def convert_to_image(self, spectrogram):

        # Convert spectrogram to tkinter image
        spectrogram *= 255
        spectrogram = np.abs(255 - spectrogram)

        # Convert the spectrogram to a PIL image
        image = Image.fromarray(np.uint8(spectrogram)).convert("RGB")

        # Convert the PIL image to a Tkinter image and return it
        self.image = ImageTk.PhotoImage(image)


    def playMusic(self):
        # check if the user has entered in some music
        if self.file_path:
            winsound.PlaySound(self.file_path, winsound.SND_FILENAME)




if __name__ == "__main__":
    
    # Main loop for running GUI
    root = tk.Tk()
    root.title("Audio Processing GUI")
    gui = GUI(root)
    gui.pack()
    root.mainloop()
