#!/usr/bin/env node
// Final comprehensive test
const { chromium } = require('playwright');

async function finalTest() {
  console.log('=== FINAL COMPREHENSIVE TEST ===\n');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  const results = {
    filePicker: false,
    fileUpload: false,
    linkedInFetch: false,
    atsAnalysis: false,
    resumeGeneration: false
  };
  
  try {
    // Load page
    await page.goto('http://localhost:8080/');
    await page.waitForLoadState('networkidle');
    
    // Test 1: File Picker
    console.log('1. Testing File Picker...');
    const browseBtn = await page.locator('#browseBtn');
    const fileInput = await page.locator('#fileInput');
    results.filePicker = await browseBtn.isVisible() && await fileInput.count() > 0;
    console.log('   File picker working:', results.filePicker);
    
    // Test 2: File Upload
    console.log('2. Testing File Upload...');
    const pdfContent = `%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 100 >>
stream
BT /F1 12 Tf 100 700 Td (John Doe - Software Engineer) Tj ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000214 00000 n 
trailer
<< /Size 5 /Root 1 0 R >>
startxref
365
%%EOF`;
    require('fs').writeFileSync('/tmp/test.pdf', pdfContent);
    await fileInput.setInputFiles('/tmp/test.pdf');
    await page.waitForTimeout(1500);
    const preview = await page.locator('#pdfPreview');
    results.fileUpload = await preview.isVisible().catch(() => false);
    console.log('   File upload working:', results.fileUpload);
    
    // Test 3: LinkedIn Fetch
    console.log('3. Testing LinkedIn Fetch...');
    await page.fill('#linkedinUrl', 'https://www.linkedin.com/jobs/view/12345');
    const [response] = await Promise.all([
      page.waitForResponse(r => r.url().includes('/api/scrape-linkedin')),
      page.click('button:has-text("Fetch Job Description")')
    ]);
    results.linkedInFetch = response.status() === 200;
    console.log('   LinkedIn fetch working:', results.linkedInFetch);
    
    // Test 4: ATS Analysis
    console.log('4. Testing ATS Analysis...');
    await page.evaluate(() => {
      window.resumeText = 'Software Engineer with Python, React, AWS experience. 5 years building scalable apps.';
    });
    await page.fill('#jobDescription', 'Need Software Engineer with Python, React, AWS, Docker. 3+ years experience.');
    const [atsResponse] = await Promise.all([
      page.waitForResponse(r => r.url().includes('/api/ats-score')),
      page.click('button:has-text("Analyze Resume")')
    ]);
    const atsData = await atsResponse.json();
    results.atsAnalysis = atsData.success && atsData.score >= 0;
    console.log('   ATS analysis working:', results.atsAnalysis, '(Score:', atsData.score + ')');
    
    // Test 5: Resume Generation
    console.log('5. Testing Resume Generation...');
    await page.evaluate(() => {
      document.getElementById('generate').scrollIntoView({ behavior: 'instant' });
    });
    await page.waitForTimeout(300);
    await page.fill('#genName', 'Test User');
    await page.fill('#genTitle', 'Developer');
    await page.fill('#genEmail', 'test@example.com');
    await page.fill('#genSkills', 'Python, React');
    const [genResponse] = await Promise.all([
      page.waitForResponse(r => r.url().includes('/api/generate-resume')),
      page.click('button:has-text("Generate Professional Resume")')
    ]);
    const genData = await genResponse.json();
    results.resumeGeneration = genData.success && genData.resume;
    console.log('   Resume generation working:', results.resumeGeneration);
    
    // Take final screenshot
    console.log('\n6. Taking final screenshot...');
    await page.screenshot({ path: '/tmp/resumecraft_final.png', fullPage: true });
    console.log('   Screenshot saved');
    
    // Summary
    console.log('\n=== TEST RESULTS ===');
    const allPassed = Object.values(results).every(r => r);
    for (const [test, passed] of Object.entries(results)) {
      console.log(`   ${passed ? '✓' : '✗'} ${test}: ${passed ? 'PASS' : 'FAIL'}`);
    }
    console.log('\n' + (allPassed ? '✅ ALL TESTS PASSED!' : '❌ SOME TESTS FAILED'));
    
  } catch (error) {
    console.error('Test error:', error.message);
    await page.screenshot({ path: '/tmp/resumecraft_error.png', fullPage: true });
  } finally {
    await browser.close();
    try { require('fs').unlinkSync('/tmp/test.pdf'); } catch(e) {}
  }
}

finalTest();
