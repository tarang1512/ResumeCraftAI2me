#!/bin/bash
set -e
export PATH="/home/ubuntu/.openclaw/conda/bin:$PATH"
source /home/ubuntu/.openclaw/conda/bin/activate tts-hs-hifigan

echo "Installing TTS deps without cache..."
pip install --no-cache-dir -r /home/ubuntu/.openclaw/workspace/Fastspeech2_HS/requirements.txt 2>&1 | tail -5

echo "Installing HiFi-GAN vocoder..."
cd /home/ubuntu/.openclaw/workspace
[ -d hifi-gan ] || git clone https://github.com/jik876/hifi-gan.git
cd hifi-gan && pip install --no-cache-dir -e . 2>&1 | tail -3

echo "TTS setup COMPLETE!"
