#!/usr/bin/env python3
"""
STT via OpenRouter Gemini Flash
Uses OpenRouter API key with Base64 audio format
"""

import argparse
import os
import sys
import requests
import base64
import json
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def transcribe_openrouter(audio_path: str, api_key: str) -> dict:
    """OpenRouter Gemini Flash with audio input"""
    
    # Read audio file
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    
    # Encode as base64
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    
    # Detect mime type
    ext = Path(audio_path).suffix.lower()
    mime_types = {
        ".ogg": "audio/ogg",
        ".opus": "audio/opus", 
        ".oga": "audio/ogg",
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg"
    }
    mime = mime_types.get(ext, "audio/wav")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://gujarati-stt.local",
        "X-Title": "Gujarati STT"
    }
    
    payload = {
        "model": "google/gemini-flash-1.5-8b",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Transcribe this audio to English text. If the speech is Gujarati, translate it. If it's English, transcribe it. Only return the text, nothing else."
                    },
                    {
                        "type": "image_url",  # OpenRouter uses this for audio too
                        "image_url": {
                            "url": f"data:{mime};base64,{audio_b64}"
                        }
                    }
                ]
            }
        ]
    }
    
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}", file=sys.stderr)
        response.raise_for_status()
    
    data = response.json()
    return {
        "text": data["choices"][0]["message"]["content"].strip(),
        "source": "openrouter-gemini-flash",
        "raw": data
    }


def main():
    parser = argparse.ArgumentParser(description="STT via OpenRouter Gemini Flash")
    parser.add_argument('audio', help='Audio file path')
    parser.add_argument('--key', '-k', default=os.getenv('OPENROUTER_API_KEY'), help='API key')
    parser.add_argument('--json', '-j', action='store_true')
    
    args = parser.parse_args()
    
    if not args.key:
        print("Error: OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    result = transcribe_openrouter(args.audio, args.key)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result["text"])


if __name__ == '__main__':
    main()
