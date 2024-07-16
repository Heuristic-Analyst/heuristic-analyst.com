import os
import sys
import torch
from faster_whisper import WhisperModel
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    video.close()

def transcribe_audio(audio_path, output_path):
    # Load the model

    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, 'WhisperModels')
    model = WhisperModel("base", device="cuda", download_root=models_dir)

    # Transcribe the audio
    segments, info = model.transcribe(audio_path, beam_size=5)

    # Calculate total duration for progress bar
    total_duration = info.duration

    with open(output_path, 'w', encoding='utf-8') as f:
        with tqdm(total=total_duration, unit='sec', desc="Transcribing") as pbar:
            for segment in segments:
                f.write(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n")
                pbar.update(segment.end - segment.start)

def main():
    # Create a root window and hide it
    root = tk.Tk()
    root.withdraw()

    # Open file dialog to select the video file
    video_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])

    if not video_path:
        print("No file selected. Exiting.")
        sys.exit()

    # Generate paths for intermediate audio and output text files
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = f"{base_name}_audio.wav"
    output_path = f"{base_name}_transcription.txt"

    print("Extracting audio from video...")
    extract_audio(video_path, audio_path)

    print("Transcribing audio...")
    transcribe_audio(audio_path, output_path)

    print(f"Transcription complete. Output saved to {output_path}")

    # Clean up the temporary audio file
    os.remove(audio_path)

if __name__ == "__main__":
    main()
