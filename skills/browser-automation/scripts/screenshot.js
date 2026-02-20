const { chromium } = require('playwright');

(async () => {
    const url = process.argv[2] || 'https://example.com';
    const output = process.argv[3] || 'screenshot.png';
    
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.screenshot({ path: output, fullPage: true });
    await browser.close();
    
    console.log(`✅ Screenshot saved: ${output}`);
})();
