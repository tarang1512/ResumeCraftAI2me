#!/usr/bin/env python3
"""
Sarvam Text-to-Speech for Gujarati Voice Replies
"""

import argparse
import json
import sys
import os
import requests

SARVAM_API_URL = "https://api.sarvam.ai/text-to-speech"
API_KEY = "sk_yusxarti_8XHAnwUjSKU9LUPLvFArVJOZ"

def text_to_speech(text, language="gu-IN", speaker="hitesh"):
    """Convert text to speech using Sarvam TTS"""
    
    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": [text],
        "target_language_code": language,
        "speaker": speaker,
        "model": "bulbul:v3",
        "pitch": 0,
        "pace": 1.0,
        "loudness": 1.0
    }
    
    try:
        response = requests.post(
            SARVAM_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        if 'audios' in result and len(result['audios']) > 0:
            import base64
            import tempfile
            audio_data = base64.b64decode(result['audios'][0])
            temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3', delete=False)
            temp_file.write(audio_data)
            temp_file.close()
            return temp_file.name
        else:
            return None
            
    except Exception as e:
        print(f"TTS Error: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Sarvam TTS')
    parser.add_argument('--text', required=True, help='Text to convert')
    parser.add_argument('--language', default='gu-IN', help='Language code')
    parser.add_argument('--speaker', default='hitesh', help='Voice')
    
    args = parser.parse_args()
    
    audio_path = text_to_speech(args.text, args.language, args.speaker)
    
    if audio_path:
        print(audio_path)
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
