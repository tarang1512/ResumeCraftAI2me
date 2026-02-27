#!/usr/bin/env node
// Simple test script for ResumeCraft website

const http = require('http');
const fs = require('fs');
const path = require('path');

// Test the file upload endpoint
async function testAPIs() {
  console.log('Testing ResumeCraft APIs...\n');
  
  // Test 1: Check if server is running
  console.log('1. Testing server connection...');
  try {
    const response = await fetch('http://localhost:8080/');
    console.log('   ✓ Server is running (status:', response.status + ')');
  } catch (e) {
    console.log('   ✗ Server not accessible:', e.message);
    return;
  }
  
  // Test 2: Test ATS Score API
  console.log('\n2. Testing ATS Score API...');
  try {
    const response = await fetch('http://localhost:8080/api/ats-score', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resume: 'Software Engineer with 5 years experience in Python, React, and AWS. Built scalable web applications.',
        job_description: 'Looking for Software Engineer with Python, React, AWS, and Kubernetes experience.'
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('   ✓ ATS Score API working');
      console.log('   Score:', data.score);
      console.log('   Found keywords:', data.found_keywords?.length || 0);
    } else {
      console.log('   ✗ ATS Score API failed (status:', response.status + ')');
    }
  } catch (e) {
    console.log('   ✗ ATS Score API error:', e.message);
  }
  
  // Test 3: Test LinkedIn Scraper API
  console.log('\n3. Testing LinkedIn Scraper API...');
  try {
    const response = await fetch('http://localhost:8080/api/scrape-linkedin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url: 'https://www.linkedin.com/jobs/view/12345'
      })
    });
    
    console.log('   Status:', response.status);
    const data = await response.json();
    if (data.success) {
      console.log('   ✓ LinkedIn API working');
    } else {
      console.log('   ⚠ LinkedIn API returned error (expected for invalid URL):', data.error || 'Unknown error');
    }
  } catch (e) {
    console.log('   ✗ LinkedIn API error:', e.message);
  }
  
  // Test 4: Test Resume Generation API
  console.log('\n4. Testing Resume Generation API...');
  try {
    const response = await fetch('http://localhost:8080/api/generate-resume', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'John Doe',
        title: 'Software Engineer',
        email: 'john@example.com',
        experience: '5 years at Tech Corp',
        education: 'BS Computer Science',
        skills: 'Python, React, AWS'
      })
    });
    
    console.log('   Status:', response.status);
    if (response.ok) {
      const data = await response.json();
      console.log('   ✓ Resume Generation API working');
      console.log('   Has resume content:', !!data.resume);
    } else {
      console.log('   ⚠ Resume Generation API returned error');
    }
  } catch (e) {
    console.log('   ✗ Resume Generation API error:', e.message);
  }
  
  console.log('\n--- Test Complete ---');
}

testAPIs();
