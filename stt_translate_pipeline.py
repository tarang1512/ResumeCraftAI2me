#!/usr/bin/env python3
"""
Simple STT + Translation Pipeline for Gujarati Voice Notes
Sarvam STT (API) → Gujarati text → Google Translate → English
"""

import argparse
import json
import os
import sys
import subprocess
import tempfile
import requests
from pathlib import Path
from googletrans import Translator
import base64

# Suppress logs
os.environ['VOSK_LOG_LEVEL'] = '-1'
os.environ['HOME'] = '/home/ubuntu'

API_KEY_FILE = Path.home() / ".sarvam_api_key"

def get_sarvam_api_key():
    """Get Sarvam API key"""
    if API_KEY_FILE.exists():
        return API_KEY_FILE.read_text().strip()
    return None

def transcribe_sarvam(audio_path: str, language_code: str = "gu-IN") -> str:
    """
    Transcribe using Sarvam Saras v3 STT
    Much better for desi Gujarati!
    """
    api_key = get_sarvam_api_key()
    if not api_key:
        raise ValueError("Sarvam API key not found")
    
    url = "https://api.sarvam.ai/speech-to-text"
    
    with open(audio_path, 'rb') as f:
        audio_data = f.read()
    
    files = {
        'file': (Path(audio_path).name, audio_data, 'audio/ogg')
    }
    
    data = {
        'model': 'saaras:v3',
        'language_code': language_code,
        'mode': 'transcribe'
    }
    
    headers = {
        'api-subscription-key': api_key
    }
    
    response = requests.post(url, files=files, data=data, headers=headers, timeout=60)
    
    if response.status_code == 200:
        result = response.json()
        return result.get('transcript', '')
    else:
        raise Exception(f"STT failed: {response.status_code} - {response.text}")

def translate_to_english(gujarati_text: str) -> str:
    """Translate Gujarati to English"""
    if not gujarati_text.strip():
        return ""
    try:
        translator = Translator()
        result = translator.translate(gujarati_text, src='gu', dest='en')
        return result.text
    except Exception as e:
        return f"[Translation error: {e}]"

def process_voice_note(audio_path: str):
    """Full pipeline: Audio → Gujarati (Sarvam) → English"""
    try:
        gujarati = transcribe_sarvam(audio_path)
        english = translate_to_english(gujarati)
        return {
            "gujarati": gujarati,
            "english": english,
            "source": "sarvam-saaras:v3 + google-translate"
        }
    except Exception as e:
        return {
            "gujarati": f"[STT Error: {e}]",
            "english": "",
            "source": "error"
        }

def main():
    parser = argparse.ArgumentParser(description="Gujarati STT (Sarvam)")
    parser.add_argument('audio', help='Audio file')
    parser.add_argument('--gu', action='store_true', help='Gujarati only')
    parser.add_argument('--json', '-j', action='store_true')
    args = parser.parse_args()
    
    if not Path(args.audio).exists():
        print(f"Error: File not found: {args.audio}", file=sys.stderr)
        sys.exit(1)
    
    result = process_voice_note(args.audio)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.gu:
        print(result["gujarati"])
    else:
        print(f"Gujarati: {result['gujarati']}")
        print(f"English: {result['english']}")

if __name__ == '__main__':
    main()
