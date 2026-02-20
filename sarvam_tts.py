#!/usr/bin/env python3
"""
Sarvam AI Bulbul V3 TTS for Gujarati
Free until Feb 2026
Corrected API format
"""

import os
import sys
import requests
import json
import base64
from pathlib import Path

API_KEY_FILE = Path.home() / ".sarvam_api_key"

def get_api_key():
    """Get Sarvam API key from file or prompt"""
    if API_KEY_FILE.exists():
        return API_KEY_FILE.read_text().strip()
    return None

def save_api_key(key: str):
    """Save API key securely"""
    API_KEY_FILE.write_text(key)
    os.chmod(API_KEY_FILE, 0o600)
    print(f"✅ API key saved to {API_KEY_FILE}")

def text_to_speech(text: str, voice: str = "aayan"):
    """
    Convert text to speech using Sarvam Bulbul V3
    Correct API format
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError("API key not set. Call save_api_key() first.")
    
    url = "https://api.sarvam.ai/text-to-speech"
    
    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": api_key
    }
    
    # Correct format: bulbul:v3 with inputs array
    payload = {
        "text": text,
        "source_language_code": "gu-IN",
        "speaker": voice,
        "model": "bulbul:v3",
        "target_language_code": "gu-IN"
    }
    
    print(f"🎙️ Generating voice for: {text}")
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        # Debug
        print(f"audios type: {type(data['audios'])}, len: {len(data['audios'])}")
        print(f"audios[0] type: {type(data['audios'][0])}")
        # Response has 'audios' array - could be direct string or object
        if isinstance(data['audios'][0], dict):
            audio_b64 = data['audios'][0]['data']
        else:
            audio_b64 = data['audios'][0]
        audio_data = base64.b64decode(audio_b64)
        
        # Save as OGG
        output_path = "/tmp/sarvam_voice_note.ogg"
        with open(output_path, 'wb') as f:
            f.write(audio_data)
        
        print(f"✅ Voice saved: {output_path}")
        return output_path
    else:
        raise Exception(f"TTS failed: {response.status_code} - {response.text}")

def main():
    """CLI usage"""
    import argparse
    parser = argparse.ArgumentParser(description='Sarvam TTS')
    parser.add_argument('--text', help='Gujarati text')
    parser.add_argument('--voice', default='aayan', help='Voice name')
    parser.add_argument('--setup', help='Save API key')
    args = parser.parse_args()
    
    if args.setup:
        save_api_key(args.setup)
        return
    
    if not args.text:
        print("Usage: python3 sarvam_tts.py --text 'નમસ્તે' --voice meera")
        return
    
    try:
        output = text_to_speech(args.text, voice=args.voice)
        print(f"Saved: {output}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
