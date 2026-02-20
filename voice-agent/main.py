#!/usr/bin/env python3
"""
Test Sarvam STT/TTS and wake-word detection (no LangChain).
"""

import os
import sounddevice as sd
import numpy as np
import requests
import pygame
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

# STT: Record audio and convert to text using Sarvam
def record_audio(duration=5, sample_rate=16000):
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    return audio

def stt(audio):
    url = "https://api.sarvam.ai/stt"
    headers = {"Authorization": f"Bearer {SARVAM_API_KEY}"}
    files = {"audio": ("audio.wav", audio.tobytes(), "audio/wav")}
    response = requests.post(url, headers=headers, files=files)
    return response.json().get("text", "")

# TTS: Convert text to speech using Sarvam
def tts(text, voice="hitesh"):
    url = "https://api.sarvam.ai/tts"
    headers = {"Authorization": f"Bearer {SARVAM_API_KEY}"}
    data = {"text": text, "voice": voice, "model": "bulbul:v3"}
    response = requests.post(url, headers=headers, json=data)
    with open("output.mp3", "wb") as f:
        f.write(response.content)
    return "output.mp3"

# Wake-Word Detection
def wake_word_detection():
    import pvporcupine
    import pyaudio
    porcupine = pvporcupine.create(keywords=["hey sarvam"])
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    print("Listening for wake word... (Press Ctrl+C to stop)")
    try:
        while True:
            keyword_index = porcupine.process(stream.read(porcupine.frame_length))
            if keyword_index >= 0:
                print("Wake word detected!")
                return True
    except KeyboardInterrupt:
        print("Stopping wake-word detection...")
    finally:
        stream.close()
        pa.terminate()
        porcupine.delete()

# Main Loop
if __name__ == "__main__":
    print("Starting voice agent... (Press Ctrl+C to stop)")

    while True:
        if wake_word_detection():
            audio = record_audio(duration=5)
            user_input = stt(audio)
            print(f"You said: {user_input}")
            if user_input.strip():
                # Static response for testing (no LangChain)
                response = f"I heard you say: {user_input}"
                print(f"Agent: {response}")
                audio_file = tts(response)
                pygame.mixer.init()
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.delay(100)
                os.remove(audio_file)  # Clean up
