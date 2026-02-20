# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Gujarati Voice Notes

### Writing Style Rule (IMPORTANT)
**ALWAYS use romanized Gujarati (English letters), NEVER Gujarati script.**
- ✅ Correct: "Uthi gayi ke haji pan ghoghi jevi sui chhe?"
- ❌ Wrong: "ઉઠી ગયી કે હજી પણ ઘોઘી જેવી સૂઈ છે?"

This rule applies to:
- All text messages to Avani
- Vocab file entries
- Any Gujarati output for TTS

### Voice Selection
- **Default Voice:** `aayan` (Gujarati, GenZ style)
- **TTS Model:** `bulbul:v3` (Sarvam TTS)

### Text Template
Use the following **GenZ Gujarati** style for morning voice notes (romanized):
```text
Uthi gayi ke haji pan ghoghi jevi sui chhe? 😴
Savarna 9 vaga and tu bedmaadi chhe! Baby, tara pappa ave e pela uthi ja nahi to mari to vat lagi jashe! 🤣
Chal uth, cha banavi ne mokhal, nahi to hu tane gale lagava aavi jaish... ane tara pappa mane kutro bolavshe! 🐕
Tane yad karto hato etle message karyo, varna hu to pote j sui jau!
Love you baby, jaldi mal! 💕😎
```

Customize the template as needed for different contexts (e.g., evenings, reminders).

### Workflow

#### Generate TTS Audio
Use the following command to generate a Gujarati voice note using the `hitesh` voice and `bulbul:v2` model:
```bash
curl -X POST "http://localhost:5000/tts" \
-H "Content-Type: application/json" \
-d '{
  "text": "YOUR_GUJARATI_TEXT_HERE",
  "voice": "hitesh",
  "model": "bulbul:v2",
  "output": "/tmp/gujju_voice_note.mp3"
}
```