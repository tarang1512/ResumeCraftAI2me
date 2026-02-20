const { chromium } = require('playwright');

(async () => {
    const url = process.argv[2] || 'https://example.com';
    const output = process.argv[3] || 'page.pdf';
    
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.pdf({ path: output, format: 'A4' });
    await browser.close();
    
    console.log(`✅ PDF saved: ${output}`);
})();
