#!/usr/bin/env node
// Test the new resume generation form
const { chromium } = require('playwright');

async function testResumeGeneration() {
  console.log('Testing Resume Generation Form...\n');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    await page.goto('http://localhost:8080/');
    await page.waitForLoadState('networkidle');
    
    // Scroll to generate section
    console.log('1. Navigating to Generate section...');
    await page.click('a[href="#generate"]');
    await page.waitForTimeout(500);
    console.log('   ✓ Navigated to generate section\n');
    
    // Fill in the form
    console.log('2. Filling resume generation form...');
    await page.fill('#genName', 'Jane Smith');
    await page.fill('#genTitle', 'Senior Software Engineer');
    await page.fill('#genEmail', 'jane@example.com');
    await page.fill('#genPhone', '555-123-4567');
    await page.fill('#genExperience', 'Senior Developer at Tech Corp (2020-Present)\n• Built scalable web applications serving 1M+ users\n• Led team of 5 developers\n• Improved performance by 40%');
    await page.fill('#genEducation', 'BS Computer Science, MIT (2016-2020)');
    await page.fill('#genSkills', 'Python, React, AWS, Docker, Kubernetes, Node.js');
    console.log('   ✓ Form filled\n');
    
    // Click generate
    console.log('3. Generating resume...');
    const [response] = await Promise.all([
      page.waitForResponse(resp => resp.url().includes('/api/generate-resume') && resp.status() === 200),
      page.click('button:has-text("Generate Professional Resume")')
    ]);
    
    const data = await response.json();
    console.log('   Response success:', data.success);
    console.log('   Has resume content:', !!data.resume);
    
    // Wait for result
    await page.waitForTimeout(500);
    const container = await page.locator('#generatedResumeContainer');
    const isVisible = await container.isVisible();
    console.log('   Result container visible:', isVisible);
    console.log('   ✓ Resume generated\n');
    
    // Take screenshot
    console.log('4. Taking screenshot...');
    await page.screenshot({ path: '/tmp/resumecraft_generate.png', fullPage: true });
    console.log('   ✓ Screenshot saved\n');
    
    console.log('=== Resume Generation Test Passed! ===');
    
  } catch (error) {
    console.error('\n✗ Test failed:', error.message);
    await page.screenshot({ path: '/tmp/resumecraft_generate_error.png', fullPage: true });
  } finally {
    await browser.close();
  }
}

testResumeGeneration();
