# OCR Skill

Extract text from images using state-of-the-art OCR engines.

## Tools

- `ocr.extract` - Extract text from an image file

## Usage

```
ocr.extract({"image": "path/to/image.png", "lang": "gu"})
```

## Parameters

- `image` (string, required) - Path to the image file
- `lang` (string, optional) - Language code:
  - `gu`/`gujarati` - Gujarati 🇮🇳
  - `hi`/`hindi` - Hindi 🇮🇳
  - `mr` - Marathi
  - `bn` - Bengali
  - `ta` - Tamil
  - `te` - Telugu
  - `kn` - Kannada
  - `ml` - Malayalam
  - `pa` - Punjabi
  - `ur` - Urdu
  - `en` - English (default)
- `engine` (string, optional) - OCR engine:
  - `paddle` - PaddleOCR (default, best for Indic)
  - `tesseract` - Tesseract OCR
  - `auto` - Try Paddle first, fallback to Tesseract

## Examples

```bash
# Extract Gujarati text
ocr.extract({"image": "/path/to/gujarati_sign.png", "lang": "gu"})

# Extract Hindi text
ocr.extract({"image": "/path/to/hindi_document.jpg", "lang": "hi"})

# Extract English text
ocr.extract({"image": "/path/to/english_receipt.png"})
```

## Supported Formats

- PNG
- JPG/JPEG
- BMP
- TIFF
- WebP

## Notes

- PaddleOCR is optimized for Indic languages
- For best results with Gujarati/Hindi, use `lang: "gu"` or `lang: "hi"`
- Large images are automatically resized for faster processing

## Setup Status

OCR tools installation is running in background.
Check progress: `cat /tmp/ocr_setup.log`
