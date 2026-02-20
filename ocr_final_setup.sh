#!/bin/bash
set -e
cd /home/ubuntu/.openclaw/ocr_env && source bin/activate

echo "Installing minimal OCR tools..."
pip install --no-cache-dir paddleocr pytesseract easyocr 2>&1 | tail -5

echo "Installing system Tesseract with Gujarati/Hindi..."
sudo apt-get update -qq && sudo apt-get install -y -qq tesseract-ocr tesseract-ocr-guj tesseract-ocr-hin

echo "OCR setup COMPLETE!"
