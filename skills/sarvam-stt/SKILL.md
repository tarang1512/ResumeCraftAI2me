---
name: sarvam-stt
description: Transcribe audio messages and voice notes using Sarvam AI Speech-to-Text API. Supports Indian languages including Gujarati, Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Punjabi, and Assamese. Use when user sends voice messages or audio files that need transcription.
---

# Sarvam STT Skill

Transcribe audio using Sarvam AI's Speech-to-Text API.

## Supported Languages

- Gujarati (gu) - **Default for this user**
- Hindi (hi)
- Tamil (ta)
- Telugu (te)
- Kannada (kn)
- Malayalam (ml)
- Bengali (bn)
- Marathi (mr)
- Punjabi (pa)
- Assamese (as)

## Usage

When user sends an audio file or voice message:

1. Read the audio file path from the media attachment
2. Call the STT script with the audio file
3. Return the transcription

## Script

```bash
scripts/sarvam_stt.py --file <audio_file> [--language gu]
```

## Example

User sends voice message in Gujarati:
- Extract audio path: `/home/ubuntu/.openclaw/media/inbound/xxx.ogg`
- Run: `python3 scripts/sarvam_stt.py --file /path/to/audio.ogg --language gu`
- Return transcription

## API Key

Sarvam API key is stored in gateway config: `auth.sarvam.apiKey`

## Notes

- Default language: Gujarati (gu) for user Tarang
- Supported formats: ogg, mp3, wav, m4a
- Maximum file size: 10MB
