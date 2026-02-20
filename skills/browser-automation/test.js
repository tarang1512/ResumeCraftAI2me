const { chromium } = require('playwright');

(async () => {
    console.log('🚀 Launching headless browser...');
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    
    console.log('🌐 Opening example.com...');
    await page.goto('https://example.com');
    
    const title = await page.title();
    console.log(`✅ Page title: ${title}`);
    
    await page.screenshot({ path: 'test-screenshot.png' });
    console.log('📸 Screenshot saved: test-screenshot.png');
    
    await browser.close();
    console.log('🎉 Browser test SUCCESSFUL!');
})();
