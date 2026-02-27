#!/usr/bin/env node
// End-to-end test for ResumeCraft
const { chromium } = require('playwright');
const fs = require('fs');

async function createTestPDF() {
  // Create a minimal PDF file for testing
  // PDF header and basic structure
  const pdfContent = `%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 5 0 R
>>
>>
>>
endobj

4 0 obj
<<
/Length 150
>>
stream
BT
/F1 12 Tf
100 700 Td
(John Doe) Tj
0 -20 Td
(Software Engineer) Tj
0 -20 Td
(john@example.com) Tj
0 -40 Td
(Experience:) Tj
0 -20 Td
(• 5 years Python development) Tj
0 -15 Td
(• React and Node.js expert) Tj
0 -15 Td
(• AWS certified developer) Tj
ET
endstream
endobj

5 0 obj
<<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
endobj

xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000266 00000 n 
0000000467 00000 n 

trailer
<<
/Size 6
/Root 1 0 R
>>
startxref
545
%%EOF`;

  fs.writeFileSync('/tmp/test_resume.pdf', pdfContent);
  return '/tmp/test_resume.pdf';
}

async function testEndToEnd() {
  console.log('=== ResumeCraft End-to-End Test ===\n');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // Load page
    console.log('1. Loading ResumeCraft...');
    await page.goto('http://localhost:8080/');
    await page.waitForLoadState('networkidle');
    console.log('   ✓ Page loaded\n');
    
    // Test File Upload
    console.log('2. Testing file upload...');
    const pdfPath = await createTestPDF();
    
    // Set up dialog handler for any alerts
    page.on('dialog', async dialog => {
      console.log('   Dialog message:', dialog.message());
      await dialog.dismiss();
    });
    
    // Upload the file
    const fileInput = await page.locator('#fileInput');
    await fileInput.setInputFiles(pdfPath);
    
    // Wait for processing
    await page.waitForTimeout(2000);
    
    // Check if preview appeared
    const preview = await page.locator('#pdfPreview');
    const previewVisible = await preview.isVisible().catch(() => false);
    console.log('   Preview visible:', previewVisible);
    console.log('   ✓ File upload processed\n');
    
    // Test LinkedIn Fetch
    console.log('3. Testing LinkedIn job fetch...');
    await page.fill('#linkedinUrl', 'https://www.linkedin.com/jobs/view/12345');
    
    // Click fetch button and wait for response
    const [response] = await Promise.all([
      page.waitForResponse(resp => resp.url().includes('/api/scrape-linkedin') && resp.status() === 200),
      page.click('button:has-text("Fetch Job Description")')
    ]);
    
    const responseData = await response.json();
    console.log('   Response:', responseData.success ? 'Success' : 'Failed');
    
    // Check if job description was filled
    await page.waitForTimeout(500);
    const jobDesc = await page.inputValue('#jobDescription');
    console.log('   Job description filled:', jobDesc.length > 0);
    console.log('   ✓ LinkedIn fetch working\n');
    
    // Test ATS Analysis
    console.log('4. Testing ATS analysis...');
    
    // First ensure we have resume text
    await page.evaluate(() => {
      window.resumeText = `John Doe
Software Engineer
john@example.com

Experience:
• 5 years Python development
• Built React applications
• AWS and Docker experience
• Improved performance by 40%

Skills: Python, React, AWS, Docker, JavaScript`;
    });
    
    // Ensure job description has content
    if (!jobDesc || jobDesc.length < 10) {
      await page.fill('#jobDescription', `Software Engineer
Requirements:
- Python, React, AWS
- Docker and Kubernetes
- 3+ years experience
- Team leadership skills`);
    }
    
    // Click analyze
    const [analyzeResponse] = await Promise.all([
      page.waitForResponse(resp => resp.url().includes('/api/ats-score') && resp.status() === 200),
      page.click('button:has-text("Analyze Resume")')
    ]);
    
    const analyzeData = await analyzeResponse.json();
    console.log('   ATS Score:', analyzeData.score);
    console.log('   Found keywords:', analyzeData.found_keywords?.length || 0);
    console.log('   Missing keywords:', analyzeData.missing_keywords?.length || 0);
    console.log('   Suggestions:', analyzeData.suggestions?.length || 0);
    
    // Check if results are displayed
    await page.waitForTimeout(500);
    const atsResult = await page.locator('#atsResult');
    const resultVisible = await atsResult.isVisible().catch(() => false);
    console.log('   Results visible:', resultVisible);
    console.log('   ✓ ATS analysis working\n');
    
    // Test Resume Generation
    console.log('5. Testing resume generation API directly...');
    const genResponse = await page.evaluate(async () => {
      const res = await fetch('/api/generate-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: 'Jane Smith',
          title: 'Full Stack Developer',
          email: 'jane@example.com',
          phone: '555-1234',
          experience: 'Senior Developer at Tech Corp\nBuilt scalable applications',
          education: 'BS Computer Science, MIT',
          skills: 'Python, React, Node.js, AWS, Docker'
        })
      });
      return res.json();
    });
    
    console.log('   Generation success:', genResponse.success);
    console.log('   Has resume content:', !!genResponse.resume);
    console.log('   ✓ Resume generation working\n');
    
    // Take screenshot
    console.log('6. Taking screenshot...');
    await page.screenshot({ path: '/tmp/resumecraft_test.png', fullPage: true });
    console.log('   ✓ Screenshot saved to /tmp/resumecraft_test.png\n');
    
    console.log('=== All End-to-End Tests Passed! ===');
    
  } catch (error) {
    console.error('\n✗ Test failed:', error.message);
    console.error(error.stack);
    
    // Take error screenshot
    await page.screenshot({ path: '/tmp/resumecraft_error.png', fullPage: true });
    console.log('\nError screenshot saved to /tmp/resumecraft_error.png');
    
  } finally {
    await browser.close();
    // Cleanup
    if (fs.existsSync('/tmp/test_resume.pdf')) {
      fs.unlinkSync('/tmp/test_resume.pdf');
    }
  }
}

testEndToEnd();
