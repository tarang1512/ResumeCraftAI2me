#!/bin/bash
set -e
export PATH="/home/ubuntu/.openclaw/conda/bin:$PATH"
cd /home/ubuntu/.openclaw/workspace/Fastspeech2_HS

# Step 1: Check gcc is installed
echo "Waiting for gcc..."
until command -v gcc &> /dev/null; do
  sleep 5
done
echo "gcc available!"

# Step 2: Create conda environment
echo "Creating conda env..."
conda env create -f environment.yml -y || true
conda env update -f environment.yml -y || conda create -n tts-hs-hifigan python=3.10 -y

# Step 3: Activate and install PyTorch
echo "Installing PyTorch..."
source /home/ubuntu/.openclaw/conda/bin/activate tts-hs-hifigan
pip install torch torchaudio

# Step 4: Install remaining deps
echo "Installing dependencies..."
pip install -r requirements.txt || true

# Step 5: Setup HiFi-GAN vocoder
echo "Setting up HiFi-GAN..."
cd /home/ubuntu/.openclaw/workspace
git clone https://github.com/jik876/hifi-gan.git || true

# Step 6: Create wrapper script
echo "Creating wrapper..."
cat > /home/ubuntu/.openclaw/workspace/gujarati_tts_wrapper.py << 'EOF'
#!/usr/bin/env python3
import sys
import os
import argparse
import json

# Add Fastspeech2_HS to path
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace/Fastspeech2_HS')

def synthesize_tts(text, output_path, speaker='female', language='gujarati'):
    """Simple wrapper for Gujarati TTS"""
    import torch
    import yaml
    from inference import inference
    
    model_path = f'/home/ubuntu/.openclaw/workspace/Fastspeech2_HS/{language}/{speaker}/model'
    config_path = os.path.join(model_path, 'config.yaml')
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Run inference
    result = inference(
        text=text,
        config=config,
        model_path=os.path.join(model_path, 'model.pth'),
        output_path=output_path
    )
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--speaker', default='female')
    parser.add_argument('--language', default='gujarati')
    args = parser.parse_args()
    
    result = synthesize_tts(args.text, args.output, args.speaker, args.language)
    print(json.dumps({"success": True, "output": args.output}))
EOF

chmod +x /home/ubuntu/.openclaw/workspace/gujarati_tts_wrapper.py

echo "Setup complete! Gujarati TTS is ready."
