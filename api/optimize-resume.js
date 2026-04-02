// Vercel Serverless Function - Resume Optimizer API
// Rewrites resume content specifically for a job description

const fetch = require('node-fetch');

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Parse body if it's a string
    let body = req.body;
    if (typeof req.body === 'string') {
      body = JSON.parse(req.body);
    }
    
    const { resumeText, jobDescription, rewriteType } = body;
    
    if (!resumeText || !jobDescription) {
      return res.status(400).json({ 
        error: 'Missing resume text or job description' 
      });
    }

    // Ensure jobDescription is a string
    const jd = String(jobDescription);

    // Extract key requirements from job description
    const requirements = extractRequirements(jd);
    
    // Generate optimized content
    const optimized = await generateOptimizedContent(resumeText, jd, requirements, rewriteType);
    
    res.status(200).json({
      success: true,
      optimized,
      requirements,
      changes: optimized.changes
    });
    
  } catch (error) {
    console.error('Resume optimization error:', error);
    res.status(500).json({ error: 'Failed to optimize resume', details: error.message });
  }
}

function extractRequirements(jobText) {
  const requirements = {
    skills: [],
    experience: [],
    keywords: []
  };
  
  // Extract skills
  const skillPatterns = [
    'python', 'javascript', 'java', 'typescript', 'go', 'rust', 'c++', 'c#', 'ruby', 'php',
    'react', 'vue', 'angular', 'node', 'express', 'django', 'flask', 'spring',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
    'machine learning', 'deep learning', 'tensorflow', 'pytorch',
    'agile', 'scrum', 'ci/cd', 'devops'
  ];
  
  const lowerText = String(jobText).toLowerCase();
  skillPatterns.forEach(skill => {
    if (lowerText.includes(skill)) {
      requirements.skills.push(skill);
    }
  });
  
  // Extract keywords (words appearing multiple times)
  const words = String(jobText).toLowerCase().replace(/[^\w\s]/g, '').split(/\s+/);
  const wordCount = {};
  words.forEach(word => {
    if (word.length > 3) {
      wordCount[word] = (wordCount[word] || 0) + 1;
    }
  });
  
  requirements.keywords = Object.entries(wordCount)
    .filter(([_, count]) => count >= 2)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([word]) => word);
  
  // Extract experience requirements
  const expMatch = String(jobText).match(/(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?experience/i);
  if (expMatch) {
    requirements.experience.push(`${expMatch[1]} years experience required`);
  }
  
  return requirements;
}

async function generateOptimizedContent(resumeText, jobDescription, requirements, rewriteType) {
  const changes = [];
  let optimized = resumeText;
  
  // Parse existing resume sections
  const sections = parseResumeSections(resumeText);
  
  // Rewrite based on type
  if (rewriteType === 'full' || rewriteType === 'summary') {
    const newSummary = generateSummary(sections.summary, jobDescription, requirements);
    if (sections.summary && newSummary !== sections.summary) {
      changes.push('Updated professional summary with job-specific language');
      optimized = optimized.replace(sections.summary, newSummary);
    }
  }
  
  if (rewriteType === 'full' || rewriteType === 'bullets') {
    // Improve bullet points with job language
    const improvedBullets = improveBulletPoints(sections.bullets, requirements);
    if (improvedBullets.length > 0) {
      changes.push(`Improved ${improvedBullets.length} bullet points with job-specific keywords`);
    }
  }
  
  // Add missing keywords naturally into skills section
  if (requirements.skills.length > 0) {
    const existingSkills = sections.skills || '';
    const missingSkills = requirements.skills.filter(s => 
      !existingSkills.toLowerCase().includes(s)
    );
    
    if (missingSkills.length > 0) {
      const skillsAddition = `\n• ${missingSkills.slice(0, 5).join('\n• ')}`;
      changes.push(`Added ${missingSkills.slice(0, 5).length} missing keywords: ${missingSkills.slice(0, 3).join(', ')}`);
      optimized += skillsAddition;
    }
  }
  
  return {
    text: optimized,
    changes,
    requirements
  };
}

function parseResumeSections(text) {
  const sections = {
    summary: '',
    bullets: [],
    skills: ''
  };
  
  // Find summary
  const summaryMatch = text.match(/(?:professional summary|summary|profile)[\s:]*([^\n]+(?:\n(?!experience|education|skills|work)[^\n]+)*)/i);
  if (summaryMatch) {
    sections.summary = summaryMatch[0];
  }
  
  // Find bullets
  const bulletRegex = /(?:^|\n)(?:[-•*]|\d+\.)\s*([^\n]+)/g;
  let match;
  while ((match = bulletRegex.exec(text)) !== null) {
    sections.bullets.push(match[1]);
  }
  
  // Find skills
  const skillsMatch = text.match(/(?:skills|technical skills|technologies)[\s:]*([^\n]+(?:\n[^\n]+)*)/i);
  if (skillsMatch) {
    sections.skills = skillsMatch[0];
  }
  
  return sections;
}

function generateSummary(existingSummary, jobDescription, requirements) {
  // Extract key phrases from job description
  const keyPhrases = [];
  const phrases = [
    'responsible for', 'manage', 'lead', 'develop', 'create', 'implement',
    'optimize', 'improve', 'analyze', 'design', 'build', 'deliver'
  ];
  
  phrases.forEach(phrase => {
    if (String(jobDescription).toLowerCase().includes(phrase)) {
      keyPhrases.push(phrase);
    }
  });
  
  // Build a new summary using job language
  const summary = existingSummary || 'Professional with relevant experience.';
  const updated = `[Optimized for this role: ${requirements.keywords.slice(0, 3).join(', ')}]\n\n${summary}`;
  
  return updated;
}

function improveBulletPoints(bullets, requirements) {
  const improved = [];
  const jobKeywords = requirements.skills.map(s => s.toLowerCase());
  
  bullets.forEach(bullet => {
    let improvedBullet = bullet;
    let changed = false;
    
    // Add keywords if missing
    jobKeywords.forEach(keyword => {
      if (!bullet.toLowerCase().includes(keyword)) {
        improvedBullet += `, ${keyword}`;
        changed = true;
      }
    });
    
    // Add quantification hints if not present
    if (!/\d+%|\$\d+|\d+%|increased|improved|decreased|reduced/i.test(bullet)) {
      improvedBullet += ' [Consider adding metrics]';
      changed = true;
    }
    
    if (changed) {
      improved.push(improvedBullet);
    }
  });
  
  return improved;
}