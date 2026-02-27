// Simple Express server for testing ResumeCraft locally
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 8080;

app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// ATS Score API
app.post('/api/ats-score', async (req, res) => {
  try {
    const { resume, job_description } = req.body;
    
    if (!resume || !job_description) {
      return res.status(400).json({ error: 'Missing resume or job_description' });
    }

    const resumeText = typeof resume === 'string' ? resume : JSON.stringify(resume);
    const resumeLower = resumeText.toLowerCase();
    const jobLower = job_description.toLowerCase();
    
    // Comprehensive keyword list
    const keywords = [
      'python', 'javascript', 'java', 'typescript', 'go', 'rust', 'c++', 'c#', 'ruby', 'php',
      'react', 'vue', 'angular', 'svelte', 'next.js', 'node.js', 'express', 'django', 'flask',
      'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github',
      'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
      'machine learning', 'tensorflow', 'pytorch', 'ai', 'data science',
      'leadership', 'communication', 'teamwork', 'problem-solving',
      'agile', 'scrum', 'devops', 'ci/cd',
      'software engineer', 'developer', 'full-stack', 'backend', 'frontend'
    ];
    
    const found = [];
    const missing = [];
    
    keywords.forEach(keyword => {
      if (jobLower.includes(keyword.toLowerCase())) {
        const regex = new RegExp(`\\b${keyword}\\b`, 'i');
        if (regex.test(resumeLower)) {
          found.push(keyword);
        } else {
          missing.push(keyword);
        }
      }
    });
    
    const totalJobKeywords = found.length + missing.length;
    const keywordMatch = totalJobKeywords > 0 
      ? Math.round((found.length / totalJobKeywords) * 100)
      : 50;
    
    const hasBulletPoints = /[•\-]/.test(resumeText);
    const hasContactInfo = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/.test(resumeText);
    const wordCount = resumeText.split(/\s+/).filter(w => w.length > 0).length;
    
    const formatScore = Math.min(100, 
      (hasBulletPoints ? 40 : 0) + 
      (hasContactInfo ? 30 : 0) + 
      (wordCount >= 300 && wordCount <= 700 ? 30 : 15)
    );
    
    const hasActionVerbs = /\b(achieved|improved|increased|led|managed|developed|created|built)\b/gi.test(resumeText);
    const hasMetrics = /\d+%|\$\d+|\d+\s*(years?|months?)/gi.test(resumeText);
    
    const contentScore = (hasActionVerbs ? 50 : 25) + (hasMetrics ? 50 : 25);
    
    const totalScore = Math.round((keywordMatch * 0.5) + (formatScore * 0.25) + (contentScore * 0.25));
    
    const suggestions = [];
    if (missing.length > 0) {
      suggestions.push(`Add these keywords: ${missing.slice(0, 5).join(', ')}`);
    }
    if (!hasBulletPoints) suggestions.push('Use bullet points (• or -) for achievements');
    if (!hasMetrics) suggestions.push('Add metrics (e.g., "Improved performance by 50%")');
    if (!hasActionVerbs) suggestions.push('Start bullets with action verbs');
    
    res.json({
      success: true,
      score: totalScore,
      found_keywords: found.slice(0, 15),
      missing_keywords: missing.slice(0, 10),
      suggestions: suggestions.slice(0, 5)
    });
    
  } catch (error) {
    console.error('ATS Score error:', error);
    res.status(500).json({ error: 'Failed to analyze resume' });
  }
});

// LinkedIn Scraper API (mock for local testing)
app.post('/api/scrape-linkedin', async (req, res) => {
  try {
    const { url } = req.body;
    
    if (!url || !url.includes('linkedin.com')) {
      return res.status(400).json({ error: 'Valid LinkedIn URL required' });
    }

    // For local testing, return a mock job description
    res.json({
      success: true,
      title: 'Software Engineer',
      company: 'Tech Company',
      location: 'Remote',
      description: `Software Engineer position at Tech Company.

Requirements:
- 3+ years of experience with Python and JavaScript
- Experience with React, Node.js, and AWS
- Knowledge of Docker and Kubernetes
- Strong problem-solving skills
- Excellent communication and teamwork abilities

Responsibilities:
- Build scalable web applications
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews`
    });
    
  } catch (error) {
    console.error('LinkedIn scrape error:', error);
    res.status(500).json({ error: 'Failed to scrape LinkedIn job' });
  }
});

// Resume Generation API
app.post('/api/generate-resume', async (req, res) => {
  try {
    const { name, title, email, phone, experience, education, skills } = req.body;
    
    if (!name || !title) {
      return res.status(400).json({ error: 'Name and title are required' });
    }

    // Generate a professional resume template
    const skillList = skills ? skills.split(/[,\n]/).map(s => s.trim()).filter(s => s) : [];
    
    const resume = `
<div style="font-family: Georgia, serif; max-width: 800px; margin: 0 auto; padding: 40px; line-height: 1.6;">
  <div style="text-align: center; border-bottom: 2px solid #6366f1; padding-bottom: 20px; margin-bottom: 30px;">
    <h1 style="color: #1a1a1a; margin: 0; font-size: 2.5rem;">${name}</h1>
    <p style="font-size: 1.2rem; color: #555; margin: 10px 0;">${title}</p>
    <p style="color: #666;">${email}${phone ? ' | ' + phone : ''}</p>
  </div>
  
  <div style="margin-bottom: 25px;">
    <h2 style="color: #4f46e5; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">Professional Summary</h2>
    <p>Results-driven ${title} with proven expertise in ${skillList.slice(0, 3).join(', ') || 'relevant technologies'}. Demonstrated ability to deliver high-quality solutions and collaborate effectively in fast-paced environments.</p>
  </div>
  
  <div style="margin-bottom: 25px;">
    <h2 style="color: #4f46e5; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">Experience</h2>
    ${experience ? experience.split('\n').map(line => `<p style="margin: 8px 0;">• ${line}</p>`).join('') : '<p>Experience details to be added</p>'}
  </div>
  
  <div style="margin-bottom: 25px;">
    <h2 style="color: #4f46e5; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">Education</h2>
    ${education ? education.split('\n').map(line => `<p style="margin: 8px 0;">${line}</p>`).join('') : '<p>Education details to be added</p>'}
  </div>
  
  <div>
    <h2 style="color: #4f46e5; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">Skills</h2>
    <p>${skillList.join(' • ') || 'Skills to be added'}</p>
  </div>
</div>`;
    
    res.json({ success: true, resume });
    
  } catch (error) {
    console.error('Generation error:', error);
    res.status(500).json({ error: 'Resume generation failed' });
  }
});

app.listen(PORT, () => {
  console.log(`ResumeCraft server running at http://localhost:${PORT}`);
  console.log('Press Ctrl+C to stop');
});
