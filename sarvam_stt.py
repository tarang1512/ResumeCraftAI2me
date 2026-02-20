#!/usr/bin/env python3
"""
Sarvam AI Saras v3 STT for Gujarati
Test voice note transcription
"""

import os
import sys
import requests
import json
from pathlib import Path

API_KEY_FILE = Path.home() / ".sarvam_api_key"

def get_api_key():
    """Get Sarvam API key"""
    if API_KEY_FILE.exists():
        return API_KEY_FILE.read_text().strip()
    return None

def transcribe_sarvam(audio_path: str, language_code: str = "gu-IN"):
    """
    Transcribe audio using Sarvam Saras v3 STT
    
    Args:
        audio_path: Path to audio file (wav/ogg/mp3)
        language_code: Language (gu-IN for Gujarati)
    
    Returns:
        JSON with transcript
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError("API key not found")
    
    url = "https://api.sarvam.ai/speech-to-text"
    
    # Read audio file
    with open(audio_path, 'rb') as f:
        audio_data = f.read()
    
    files = {
        'file': (Path(audio_path).name, audio_data, 'audio/ogg')
    }
    
    data = {
        'model': 'saaras:v3',
        'language_code': language_code,
        'mode': 'transcribe'  # Options: transcribe, translate
    }
    
    headers = {
        'api-subscription-key': api_key
    }
    
    print(f"🎙️ Transcribing {audio_path}...")
    response = requests.post(url, files=files, data=data, headers=headers, timeout=60)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"STT failed: {response.status_code} - {response.text}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Sarvam STT')
    parser.add_argument('audio', help='Audio file')
    parser.add_argument('--lang', default='gu-IN', help='Language code')
    args = parser.parse_args()
    
    try:
        result = transcribe_sarvam(args.audio, args.lang)
        print(f"\n✅ Transcript: {result.get('transcript', result)}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
