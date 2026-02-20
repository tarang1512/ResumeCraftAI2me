#!/bin/bash
set -e

echo "Setting up OCR tools..."

# Create virtual environment
python3 -m venv /home/ubuntu/.openclaw/ocr_env
source /home/ubuntu/.openclaw/ocr_env/bin/activate

# Install PaddleOCR (best for Indic languages)
pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install paddleocr

# Install EasyOCR as fallback
pip install easyocr

# Install Tesseract OCR (system package)
sudo apt-get update -qq
sudo apt-get install -y -qq tesseract-ocr tesseract-ocr-guj tesseract-ocr-hin tesseract-ocr-san

# Install pytesseract Python wrapper
pip install pytesseract pillow

echo "OCR Setup Complete!"
