#!/usr/bin/env python3
"""
Free STT using Vosk - Offline, supports Gujarati
Uses vosk-model-small-gu-0.42 (Gujarati model)
"""

import argparse
import json
import os
import sys
import subprocess
import tempfile
from pathlib import Path

from vosk import Model, KaldiRecognizer
import wave

VOSK_MODEL_PATH = "/home/ubuntu/.openclaw/workspace/vosk_models/vosk-model-small-gu-0.42"


def convert_to_wav(input_path: str) -> str:
    """Convert any audio to 16kHz mono WAV for Vosk"""
    input_path = Path(input_path)
    
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_wav.close()
    
    try:
        subprocess.run(
            ['ffmpeg', '-i', str(input_path), '-ar', '16000', '-ac', '1', 
             '-acodec', 'pcm_s16le', '-y', temp_wav.name],
            check=True, capture_output=True, timeout=30
        )
        return temp_wav.name
    except Exception as e:
        if os.path.exists(temp_wav.name):
            os.unlink(temp_wav.name)
        raise RuntimeError(f"FFmpeg conversion failed: {e}")


def transcribe_vosk(audio_path: str) -> dict:
    """Transcribe using Vosk Gujarati model"""
    
    if not os.path.exists(VOSK_MODEL_PATH):
        raise FileNotFoundError(f"Vosk model not found at {VOSK_MODEL_PATH}")
    
    # Convert to proper WAV
    wav_path = convert_to_wav(audio_path)
    
    try:
        # Load model
        model = Model(VOSK_MODEL_PATH)
        
        # Open audio file
        wf = wave.open(wav_path, "rb")
        
        if wf.getframerate() != 16000:
            raise ValueError(f"Audio must be 16kHz, got {wf.getframerate()}")
        if wf.getnchannels() != 1:
            raise ValueError(f"Audio must be mono, got {wf.getnchannels()} channels")
        
        recognizer = KaldiRecognizer(model, 16000)
        
        # Process audio
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result.get("text"):
                    results.append(result["text"])
        
        # Get final result
        final_result = json.loads(recognizer.FinalResult())
        if final_result.get("text"):
            results.append(final_result["text"])
        
        transcript = " ".join(results).strip()
        
        return {
            "text": transcript,
            "source": "vosk-gujarati",
            "model": "vosk-model-small-gu-0.42"
        }
        
    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)


def main():
    parser = argparse.ArgumentParser(description="Free Gujarati STT via Vosk (offline)")
    parser.add_argument('audio', help='Audio file (OGG, WAV, MP3, etc)')
    parser.add_argument('--json', '-j', action='store_true', help='JSON output')
    
    args = parser.parse_args()
    
    if not Path(args.audio).exists():
        print(f"Error: File not found: {args.audio}", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = transcribe_vosk(args.audio)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result["text"])
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
