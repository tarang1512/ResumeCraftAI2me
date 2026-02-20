# Sarvam TTS Skill

Text-to-Speech powered by Sarvam AI for Indian languages including Gujarati, Hindi, Tamil, Telugu, and more.

## Configuration

Set `SARVAM_API_KEY` in your environment or `.env` file.

## Usage

```bash
# Using the tts tool
tts text="Tame kemi cho?" voice="hitesh" model="bulbul:v2"
```

## Supported Voices

- `hitesh` - Gujarati male (default)
- `aayan` - Gujarati GenZ style
- `neha` - Hindi female
- See Sarvam docs for more voices

## Models

- `bulbul:v2` - Stable (default)
- `bulbul:v3` - Latest

## Endpoints

If running local TTS service:
```
POST http://localhost:5000/tts
Content-Type: application/json

{
  "text": "Your text here",
  "voice": "hitesh",
  "model": "bulbul:v2",
  "output": "/tmp/output.mp3"
}
```
