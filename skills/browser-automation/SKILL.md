---
name: browser-automation
description: Control headless Chromium browser on AWS for web scraping, screenshots, PDFs, and automation.
---

# Browser Automation Skill

Run headless browser (Chromium) on AWS for web tasks.

## Installed Browsers

- **Chromium** (v145.0.7632.6) — Full browser
- **Chromium Headless Shell** — Lightweight headless
- **FFmpeg** — Video recording

## Usage

```bash
# Basic page automation
node scripts/test.js

# Screenshot of website
npx playwright screenshot --browser=chromium "https://google.com" output.png

# PDF generation
npx playwright pdf --browser=chromium "https://example.com" output.pdf
```

## Examples

### Screenshot
```javascript
const { chromium } = require('playwright');
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('https://example.com');
await page.screenshot({ path: 'screenshot.png' });
await browser.close();
```

### PDF Export
```javascript
await page.pdf({ path: 'page.pdf', format: 'A4' });
```

## Features

- ✅ **Headless** — No GUI needed on AWS
- ✅ **Fast** — Local on same instance as OpenClaw
- ✅ **Screenshots** — Full page or elements
- ✅ **PDFs** — Generate from any webpage
- ✅ **Mobile emulation** — Test responsive designs
- ✅ **Video recording** — Capture sessions

## Location

Browsers installed at: `~/.cache/ms-playwright/`
