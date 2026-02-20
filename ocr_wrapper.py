#!/usr/bin/env python3
"""
OCR Wrapper for OpenClaw
Supports: PaddleOCR (primary), EasyOCR (fallback), Tesseract (legacy)
Optimized for Indic languages (Gujarati, Hindi, etc.)
"""

import sys
import os
import argparse
import json
from pathlib import Path

def ocr_paddle(image_path, lang='en'):
    """Primary OCR using PaddleOCR - best for Indic languages"""
    try:
        from paddleocr import PaddleOCR
        
        # Map language codes
        lang_map = {
            'gu': 'gu',      # Gujarati
            'hi': 'hi',      # Hindi
            'mr': 'mr',      # Marathi
            'bn': 'bn',      # Bengali
            'ta': 'ta',      # Tamil
            'te': 'te',      # Telugu
            'kn': 'kn',      # Kannada
            'ml': 'ml',      # Malayalam
            'pa': 'pa',      # Punjabi
            'ur': 'ur',      # Urdu
            'en': 'en',      # English
            'gujarati': 'gu',
            'hindi': 'hi'
        }
        
        paddle_lang = lang_map.get(lang, 'en')
        
        # Initialize PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang=paddle_lang, show_log=False)
        
        # Run OCR
        result = ocr.ocr(image_path, cls=True)
        
        # Extract text
        texts = []
        for line in result[0]:
            if line:
                texts.append(line[1][0])
        
        return {
            "success": True,
            "text": "\n".join(texts),
            "engine": "paddleocr",
            "language": paddle_lang
        }
    except Exception as e:
        return {"success": False, "error": str(e), "engine": "paddleocr"}

def ocr_tesseract(image_path, lang='eng'):
    """Fallback OCR using Tesseract"""
    try:
        import pytesseract
        from PIL import Image
        
        # Map language codes
        lang_map = {
            'gu': 'guj',
            'hi': 'hin',
            'mr': 'mar',
            'bn': 'ben',
            'ta': 'tam',
            'te': 'tel',
            'kn': 'kan',
            'ml': 'mal',
            'pa': 'pan',
            'ur': 'urd',
            'en': 'eng',
            'gujarati': 'guj',
            'hindi': 'hin'
        }
        
        tess_lang = lang_map.get(lang, 'eng')
        
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=tess_lang)
        
        return {
            "success": True,
            "text": text.strip(),
            "engine": "tesseract",
            "language": tess_lang
        }
    except Exception as e:
        return {"success": False, "error": str(e), "engine": "tesseract"}

def main():
    parser = argparse.ArgumentParser(description='OCR wrapper for OpenClaw')
    parser.add_argument('image', help='Path to image file')
    parser.add_argument('--lang', default='en', help='Language code (gu/hi/en/etc)')
    parser.add_argument('--engine', default='paddle', choices=['paddle', 'tesseract', 'auto'],
                       help='OCR engine to use')
    args = parser.parse_args()
    
    # Validate image exists
    if not os.path.exists(args.image):
        print(json.dumps({"success": False, "error": f"Image not found: {args.image}"}))
        sys.exit(1)
    
    # Try primary engine
    if args.engine in ['paddle', 'auto']:
        result = ocr_paddle(args.image, args.lang)
        if result.get('success'):
            print(json.dumps(result))
            return
        
        # Fallback to tesseract
        if args.engine == 'auto':
            result = ocr_tesseract(args.image, args.lang)
    
    elif args.engine == 'tesseract':
        result = ocr_tesseract(args.image, args.lang)
    
    print(json.dumps(result))

if __name__ == '__main__':
    main()
