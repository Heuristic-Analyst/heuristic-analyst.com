import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import threading
import tempfile
import os
from faster_whisper import WhisperModel

class AudioRecorderApp:
    def __init__(self, master, model):
        self.master = master
        self.model = model
        master.title("Transcribe and Translate")
        master.configure(padx=20, pady=20)

        self.is_recording = False
        self.frames = []

        # Create a frame for buttons and dropdown
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.RIGHT, padx=(20, 0))

        self.start_button = tk.Button(self.control_frame, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.control_frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Language dropdown with label
        tk.Label(self.control_frame, text="Recording Language:").pack(pady=(10, 0))
        self.languages = [
            ("Automatic", None),
            ("English", "en"),
            ("French", "fr"),
            ("German", "de"),
            ("Italian", "it"),
            ("Mandarin", "zh"),
            ("Russian", "ru"),
            ("Spanish", "es"),
            ("Turkish", "tr"),
            ("Ukrainian", "uk"),
            ("Arabic", "ar"),
            ("Czech", "cs"),
            ("Danish", "da"),
            ("Dutch", "nl"),
            ("Finnish", "fi"),
            ("Greek", "el"),
            ("Hebrew", "he"),
            ("Hindi", "hi"),
            ("Hungarian", "hu"),
            ("Japanese", "ja"),
            ("Korean", "ko"),
            ("Persian", "fa"),
            ("Polish", "pl"),
            ("Portuguese", "pt"),
            ("Romanian", "ro"),
            ("Slovak", "sk"),
            ("Swedish", "sv"),
            ("Thai", "th"),
            ("Vietnamese", "vi")
        ]
        self.language_var = tk.StringVar(value=self.languages[0][0])
        self.language_dropdown = ttk.Combobox(self.control_frame, textvariable=self.language_var,
                                              values=[lang[0] for lang in self.languages], state="readonly")
        self.language_dropdown.pack(pady=5)

        # Add translation checkbox
        self.translate_var = tk.BooleanVar()
        self.translate_check = tk.Checkbutton(self.control_frame, text="Translate to English", variable=self.translate_var)
        self.translate_check.pack(pady=5)

        # Frame for status, copy button, and text box
        self.content_frame = tk.Frame(master)
        self.content_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Create a frame for the status label and copy button
        self.status_copy_frame = tk.Frame(self.content_frame)
        self.status_copy_frame.pack(fill=tk.X, pady=(0, 5))

        # Add status label aligned to the left
        self.status_label = tk.Label(self.status_copy_frame, text="Ready to record")
        self.status_label.pack(side=tk.LEFT, anchor=tk.W)

        # Add copy text button aligned to the right
        self.copy_button = tk.Button(self.status_copy_frame, text="Copy Text", command=self.copy_text)
        self.copy_button.pack(side=tk.RIGHT)

        self.text_box = tk.Text(self.content_frame, height=10, width=50, wrap=tk.WORD)
        self.text_box.pack(expand=True, fill=tk.BOTH)

        self.p = pyaudio.PyAudio()
        self.stream = None

        self.dot_count = 0
        self.dot_animation = None

    def get_language_name(self, code):
        return next((lang[0] for lang in self.languages if lang[1] == code), code)

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        threading.Thread(target=self.record_audio).start()
        self.animate_dots("Recording")

    def animate_dots(self, prefix):
        if self.dot_animation:
            self.master.after_cancel(self.dot_animation)
        self.dot_count = (self.dot_count % 3) + 1
        self.status_label.config(text=f"{prefix}{'.' * self.dot_count}")
        self.dot_animation = self.master.after(500, lambda: self.animate_dots(prefix))

    def record_audio(self):
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        if self.dot_animation:
            self.master.after_cancel(self.dot_animation)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            wf = wave.open(temp_wav.name, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()

        threading.Thread(target=self.transcribe_audio, args=(temp_wav.name,)).start()

    def transcribe_audio(self, audio_file):
        self.animate_dots("Processing")

        selected_language = self.language_var.get()
        language_code = next((lang[1] for lang in self.languages if lang[0] == selected_language), None)

        task = "transcribe"
        if self.translate_var.get():
            task = "translate"

        segments, info = self.model.transcribe(audio_file, task=task, language=language_code)

        transcription = " ".join([segment.text for segment in segments])
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, transcription)

        if self.dot_animation:
            self.master.after_cancel(self.dot_animation)

        detected_language_code = info.language
        detected_language = self.get_language_name(detected_language_code)

        if language_code is None and task == "transcribe":
            self.status_label.config(text=f"Transcription complete (Detected: {detected_language})")
        elif task == "translate":
            source_language = detected_language if language_code is None else selected_language
            self.status_label.config(text=f"Translation complete (From {source_language} to English)")
        else:
            self.status_label.config(text=f"Transcription complete ({selected_language})")

    def copy_text(self):
        text = self.text_box.get(1.0, tk.END).strip()
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        self.status_label.config(text="Text copied to clipboard")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, 'WhisperModels')
    model = WhisperModel("medium", device="cpu", compute_type="int8", download_root=models_dir)

    root = tk.Tk()
    app = AudioRecorderApp(root, model)
    root.mainloop()

if __name__ == "__main__":
    main()
