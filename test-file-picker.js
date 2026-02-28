const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log('Testing https://resume.ai2me.us...');
  await page.goto('https://resume.ai2me.us', { waitUntil: 'networkidle' });
  
  // Check if label or button exists
  const label = await page.$('label[for="fileInput"]');
  const button = await page.$('button:has-text("Browse Files")');
  
  console.log('Label found:', !!label);
  console.log('Button found:', !!button);
  
  if (label) {
    console.log('✅ File picker uses LABEL (correct)');
    // Try clicking
    await label.click();
    console.log('✅ Click succeeded');
  } else if (button) {
    console.log('❌ File picker uses BUTTON (broken)');
  } else {
    console.log('❌ Neither label nor button found');
  }
  
  await browser.close();
})();
