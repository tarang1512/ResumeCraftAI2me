#!/usr/bin/env python3
"""
Sarvam Speech-to-Text Transcription
Supports Indian languages including Gujarati
"""

import argparse
import json
import sys
import os
import requests
import subprocess

SARVAM_API_KEY = "sk_yusxarti_8XHAnwUjSKU9LUPLvFArVJOZ"

def transcribe_audio(audio_file, language="gu"):
    """Transcribe audio using Sarvam API via curl"""
    
    lang_map = {
        "gu": "gu-IN", "hi": "hi-IN", "ta": "ta-IN", "te": "te-IN",
        "kn": "kn-IN", "ml": "ml-IN", "bn": "bn-IN", "mr": "mr-IN",
        "pa": "pa-IN", "as": "as-IN", "en": "en-IN"
    }
    sarvam_lang = lang_map.get(language, "gu-IN")
    
    try:
        result = subprocess.run([
            'curl', '-s', '-X', 'POST',
            'https://api.sarvam.ai/speech-to-text',
            '-H', f'api-subscription-key: {SARVAM_API_KEY}',
            '-F', f'file=@{audio_file}',
            '-F', f'language_code={sarvam_lang}'
        ], capture_output=True, text=True, timeout=60)
        
        result_data = json.loads(result.stdout)
        return result_data.get('transcript')
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Transcribe audio using Sarvam STT')
    parser.add_argument('--file', required=True, help='Path to audio file')
    parser.add_argument('--language', default='gu', help='Language code (gu/hi/ta/etc)')
    
    args = parser.parse_args()
    transcript = transcribe_audio(args.file, args.language)
    
    if transcript:
        print(transcript)
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
