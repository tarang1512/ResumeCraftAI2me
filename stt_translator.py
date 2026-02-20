#!/usr/bin/env python3
"""
STT Translator: Voice note → English text
Auto-detects language (Gujarati/English) and transcribes/translates
Fast local mode (Whisper tiny) or cloud mode (Groq Whisper API) - $0.004/min
"""

import argparse
import os
import sys
import tempfile
import subprocess
import json

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

from pathlib import Path

GROQ_MODEL = "whisper-large-v3-turbo"  # Fast, cheap, great at multilingual


def transcribe_local(audio_path: str, translate: bool = True) -> dict:
    """Local Whisper tiny - fast, free, offline"""
    if not WHISPER_AVAILABLE:
        raise ImportError("Whisper not installed. Run: pip install openai-whisper")
    
    model = whisper.load_model("tiny")
    task = "translate" if translate else "transcribe"
    
    result = model.transcribe(audio_path, task=task, fp16=False)
    
    return {
        "text": result["text"].strip(),
        "language": result.get("language", "unknown"),
        "source": "local-whisper-tiny"
    }


def transcribe_groq(audio_path: str, api_key: str = None) -> dict:
    """Groq Whisper API - $0.004/min, fast, supports 99 languages"""
    from groq import Groq
    
    api_key = api_key or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API key required. Set GROQ_API_KEY env var or pass --key")
    
    client = Groq(api_key=api_key)
    
    with open(audio_path, "rb") as file:
        # Use translate endpoint for auto-English output
        translation = client.audio.translations.create(
            file=(Path(audio_path).name, file.read()),
            model=GROQ_MODEL,
            prompt="Transcribe this audio. If Gujarati, translate to English. If English, transcribe as-is."
        )
    
    return {
        "text": translation.text.strip(),
        "language": "auto-detected",
        "source": "groq-whisper-turbo"
    }


def convert_audio(input_path: Path) -> str:
    """Convert OGG/Opus to MP4 for Groq compatibility"""
    if input_path.suffix.lower() in ['.wav', '.mp3', '.mp4', '.m4a']:
        return str(input_path)
    
    # OGG/Opus needs conversion
    temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp.close()
    
    try:
        subprocess.run(
            ['ffmpeg', '-i', str(input_path), '-ar', '16000', '-ac', '1', '-y', temp.name],
            check=True, capture_output=True, timeout=30
        )
        return temp.name
    except Exception as e:
        os.unlink(temp.name)
        raise RuntimeError(f"FFmpeg conversion failed: {e}")


def process_voice_note(input_path: str, mode: str = "groq", api_key: str = None) -> dict:
    """Main entry point"""
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    wav_path = None
    try:
        wav_path = convert_audio(input_path)
        
        if mode == "groq":
            result = transcribe_groq(wav_path, api_key)
        else:
            result = transcribe_local(wav_path, translate=True)
        
        return result
        
    finally:
        if wav_path and wav_path != str(input_path) and os.path.exists(wav_path):
            os.unlink(wav_path)


def main():
    parser = argparse.ArgumentParser(
        description="Voice note → English text (Gujarati/English auto-detect)"
    )
    parser.add_argument('audio', help='Audio file path')
    parser.add_argument('--mode', '-m', choices=['local', 'groq'], default='groq',
                       help='Transcription mode: groq (default, $0.004/min) or local (free, slow/poor quality)')
    parser.add_argument('--key', '-k', help='API key (or set GROQ_API_KEY env var)')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    try:
        result = process_voice_note(args.audio, mode=args.mode, api_key=args.key)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result["text"])
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
