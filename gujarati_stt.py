#!/usr/bin/env python3
"""
Gujarati STT: Whisper + Romanized→Gujarati converter
Handles WhatsApp voice notes (OGG Opus) → Gujarati text
"""

import argparse
import os
import sys
import tempfile
import subprocess
import whisper
from pathlib import Path

# Gujarati romanized word dictionary
GUJARATI_WORDS = {
    # Greetings
    'shubh': 'શુભ', 'sava': 'સવા', 'savar': 'સવાર', 'ratri': 'રાત્રિ',
    'prabhat': 'પ્રભાત', 'namaste': 'નમસ્તે', 'kem': 'કેમ', 'cho': 'છો',
    'che': 'છે', 'chu': 'છું', 'aap': 'આપ', 'tame': 'તમે', 'tamne': 'તમને',
    'hu': 'હું', 'na': 'ના',
    
    # Common words
    'tamaro': 'તમારો', 'tamara': 'તમારા', 'tamari': 'તમારી', 'naam': 'નામ',
    'shunu': 'શું', 'su': 'શું', 'shu': 'શુ', 'kya': 'ક્યાં',
    'maja': 'મજા', 'ma': 'માં', 'ha': 'હા', 'bhai': 'ભાઈ', 'ben': 'બેન',
    'papa': 'પપા', 'mummy': 'મમ્મી', 'maa': 'મા', 'biju': 'બીજુ',
    'badhu': 'બધું', 'badha': 'બધા', 'game': 'ગમે', 'gam': 'ગમ',
    
    # Pronouns
    'aapne': 'આપને', 'me': 'મે', 'aapno': 'આપનો',
    'taro': 'તારો', 'tara': 'તારા', 'tari': 'તારી',
    'maro': 'મારો', 'mara': 'મારા', 'mari': 'મારી',
    'tenu': 'તેનું', 'menu': 'મેનું',
    
    # Verbs
    'jau': 'જાઉં', 'java': 'જવા', 'avu': 'આવું', 'aava': 'આવા',
    'karo': 'કરો', 'khavu': 'ખાવું', 'pisu': 'પીશ',
    'khabar': 'ખબર', 'bolo': 'બોલો', 'samaju': 'સમજું',
    
    # Time
    'ek': 'એક', 'be': 'બે', 'tran': 'ત્રણ', 'char': 'ચાર', 'panch': 'પાંચ',
    'vaje': 'વાગ્યે', 'divas': 'દિવસ', 'din': 'દિન', 'raat': 'રાત',
    
    # Emotions
    'khushi': 'ખુશી', 'prem': 'પ્રેમ', 'sath': 'સાથ', 'dosti': 'દોસ્તી',
    
    # Family
    'parivar': 'પરિવાર', 'patni': 'પત્ની', 'pati': 'પતિ',
    'dikra': 'દીકરા', 'dikri': 'દીકરી', 'baalak': 'બાળક',
    
    # Objects
    'rotli': 'રોટલી', 'shak': 'શાક', 'dudh': 'દૂધ', 'pani': 'પાણી',
    'cha': 'ચા', 'kapda': 'કપડા', 'ghar': 'ઘર',
    
    # Adjectives
    'saru': 'સારું', 'sari': 'સારી', 'nanu': 'નાનું', 'bar': 'બહાર',
    
    # Question words
    'shub': 'શુભ','ke': 'કે', 'kem': 'કેમ', 'kevi': 'કેવી', 'kevu': 'કેવું',
    'shu': 'શું', 'kai': 'કઈ',
    
    # Particles
    'ne': 'ને', 'thi': 'થી', 'chhe': 'છે', 'karta': 'કરતા',
    'jee': 'જી', 'jo': 'જો', 'kar': 'કર', 'la': 'લા', 'de': 'દે',
    'le': 'લે', 'mari': 'મારી', 'sa': 'સા', 'vas': 'વાસ', 
    'man': 'મન', 'gam': 'ગમ', 'tama': 'તમા', 
}


def romanized_to_gujarati(text: str) -> str:
    """Convert romanized Gujarati to Gujarati script."""
    text = text.lower().strip()
    words = text.split()
    result = []
    
    for word in words:
        word_clean = word.rstrip('.,!?')
        suffix = word[len(word_clean):]
        
        if word_clean in GUJARATI_WORDS:
            result.append(GUJARATI_WORDS[word_clean] + suffix)
        else:
            # Try dropping common endings
            for ending in ['o', 'a', 'i', 'u', 'e']:
                if word_clean.endswith(ending) and word_clean[:-1] in GUJARATI_WORDS:
                    base = GUJARATI_WORDS[word_clean[:-1]]
                    result.append(base + GUJARATI_WORDS.get(ending, ending) + suffix)
                    break
            else:
                result.append(word)
    
    return ' '.join(result)


def transcribe_audio(audio_path: str, model_size: str = "tiny") -> dict:
    """Transcribe audio using Whisper."""
    model = whisper.load_model(model_size)
    result = model.transcribe(
        str(audio_path),
        language="gu",
        task="transcribe",
        fp16=False
    )
    return result


def process_whatsapp_voice(input_path: str, output_text: bool = True):
    """Process WhatsApp voice note (OGG Opus)."""
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    wav_path = input_path
    temp_wav = None
    
    if input_path.suffix.lower() in ['.ogg', '.opus', '.oga']:
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        wav_path = temp_wav.name
        temp_wav.close()
        
        try:
            subprocess.run(
                ['ffmpeg', '-i', str(input_path), '-ar', '16000', '-ac', '1', 
                 '-y', wav_path],
                check=True, capture_output=True, timeout=30
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"FFmpeg error: {e}", file=sys.stderr)
            if os.path.exists(wav_path):
                os.unlink(wav_path)
            sys.exit(1)
    
    try:
        print("Loading Whisper model (small)...", file=sys.stderr)
        result = transcribe_audio(wav_path, model_size="small")
        romanized = result['text'].strip()
        
        if output_text:
            print(f"Romanized: {romanized}")
        
        gujarati = romanized_to_gujarati(romanized)
        print(f"Gujarati: {gujarati}")
        
        return {'romanized': romanized, 'gujarati': gujarati}
        
    finally:
        if temp_wav and os.path.exists(wav_path):
            os.unlink(wav_path)


def main():
    parser = argparse.ArgumentParser(description='Gujarati STT: Whisper + Gujarati')
    parser.add_argument('audio', help='Audio file path (WAV, OGG, Opus)')
    parser.add_argument('--model', default='small', 
                       choices=['tiny', 'base', 'small', 'medium'],
                       help='Whisper model size')
    parser.add_argument('--rom', action='store_true', 
                       help='Output romanized text too')
    
    args = parser.parse_args()
    process_whatsapp_voice(args.audio, output_text=args.rom)


if __name__ == '__main__':
    main()
