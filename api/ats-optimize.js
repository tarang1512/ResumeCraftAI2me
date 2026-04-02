// Vercel Serverless Function - ATS Optimizer API
// Handles: LinkedIn scraping, PDF parsing, ATS scoring

const fetch = require('node-fetch');
const cheerio = require('cheerio');
const pdfParse = require('pdf-parse');

export default async function handler(req, res) {
  // CORS
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
    const { resumeText, jobUrl, jobDescription } = req.body;
    
    let jobText = jobDescription || '';
    
    // Scrape LinkedIn if URL provided
    if (jobUrl && jobUrl.includes('linkedin.com')) {
      jobText = await scrapeLinkedIn(jobUrl);
    }
    
    if (!resumeText || !jobText) {
      return res.status(400).json({ 
        error: 'Missing resume text or job description' 
      });
    }
    
    // Calculate ATS Score
    const analysis = await analyzeATS(resumeText, jobText);
    
    // Generate optimization suggestions
    const suggestions = generateSuggestions(resumeText, jobText, analysis);
    
    res.status(200).json({
      success: true,
      score: analysis.score,
      breakdown: analysis.breakdown,
      foundKeywords: analysis.found,
      missingKeywords: analysis.missing,
      suggestions: suggestions,
      optimizedText: analysis.optimizedText
    });
    
  } catch (error) {
    console.error('ATS Optimization error:', error);
    res.status(500).json({ 
      error: 'Failed to analyze resume',
      details: error.message 
    });
  }
}

async function scrapeLinkedIn(url) {
  try {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
      }
    });
    
    if (!response.ok) throw new Error('Failed to fetch LinkedIn job');
    
    const html = await response.text();
    const $ = cheerio.load(html);
    
    // Extract job description
    const description = 
      $('.description__text').text() ||
      $('.show-more-less-html__markup').text() ||
      $('[data-test-id="job-description"]').text() ||
      $('meta[name="description"]').attr('content') ||
      $('.job-description').text();
    
    const title = 
      $('h1').first().text() ||
      $('.top-card__title').text() ||
      $('[data-test-id="job-title"]').text() ||
      $('title').text().replace(' | LinkedIn', '');
    
    const company = 
      $('.top-card__company-name').text() ||
      $('[data-test-id="company-name"]').text() ||
      $('a[href*="/company/"]').first().text();
    
    return `${title}\n${company}\n\n${description}`.trim();
    
  } catch (error) {
    throw new Error(`LinkedIn scraping failed: ${error.message}`);
  }
}

async function analyzeATS(resumeText, jobText) {
  // Extract keywords
  const jobKeywords = extractKeywords(jobText);
  const resumeKeywords = extractKeywords(resumeText);
  
  // Find matches
  const found = [];
  const missing = [];
  
  jobKeywords.forEach(keyword => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
    if (regex.test(resumeText)) {
      found.push(keyword);
    } else {
      missing.push(keyword);
    }
  });
  
  // Calculate scores
  const keywordMatch = jobKeywords.length > 0 
    ? Math.round((found.length / jobKeywords.length) * 100)
    : 0;
  
  // Check format
  const hasBulletPoints = resumeText.includes('•') || /\n- /.test(resumeText);
  const hasContactInfo = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/.test(resumeText);
  const hasPhone = /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/.test(resumeText);
  
  const formatScore = (hasBulletPoints ? 30 : 0) + (hasContactInfo ? 20 : 0) + (hasPhone ? 10 : 0);
  
  // Calculate overall score
  const score = Math.min(100, Math.round((keywordMatch * 0.7) + (formatScore * 0.3)));
  
  // Generate optimized text
  const optimizedText = generateOptimizedResume(resumeText, missing, found);
  
  return {
    score,
    breakdown: {
      keywordMatch,
      formatScore: Math.min(60, formatScore),
      length: resumeText.length > 500 ? 90 : 60
    },
    found: found.slice(0, 15),
    missing: missing.slice(0, 10),
    optimizedText
  };
}

function extractKeywords(text) {
  // Common tech and professional keywords
  const keywordPatterns = [
    // Programming Languages
    'python', 'javascript', 'java', 'typescript', 'go', 'rust', 'c\\+\\+', 'c#', 'ruby', 'php',
    // Frameworks
    'react', 'vue', 'angular', 'node', 'express', 'django', 'flask', 'spring', 'laravel',
    'fastapi', 'nextjs', 'tailwind', 'bootstrap', 'jquery',
    // Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
    'terraform', 'ansible', 'circleci', 'travis', 'github actions',
    // Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'dynamodb', 'sqlite',
    // AI/ML
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas',
    'numpy', 'data science', 'nlp', 'computer vision', 'ai', 'llm',
    // Soft Skills
    'leadership', 'communication', 'teamwork', 'problem-solving', 'analytical', 'organized',
    // Methodologies
    'agile', 'scrum', 'kanban', 'ci/cd', 'devops', 'sre', 'tdd', 'microservices',
    // Tools
    'jira', 'confluence', 'slack', 'figma', 'notion', 'linear',
    // Roles
    'software engineer', 'developer', 'full-stack', 'backend', 'frontend', 'senior',
    'manager', 'architect', 'analyst', 'designer', 'product', 'lead'
  ];
  
  const keywords = new Set();
  const lowerText = text.toLowerCase();
  
  keywordPatterns.forEach(pattern => {
    const regex = new RegExp(`\\b${pattern}\\b`, 'gi');
    if (regex.test(lowerText)) {
      keywords.add(pattern.replace(/\\/g, ''));
    }
  });
  
  // Extract capitalized words (likely proper nouns/technologies)
  const properNouns = text.match(/\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b/g) || [];
  properNouns.forEach(word => {
    if (word.length > 2 && !['The', 'And', 'For', 'With'].includes(word)) {
      keywords.add(word.toLowerCase());
    }
  });
  
  return Array.from(keywords);
}

function generateSuggestions(resumeText, jobText, analysis) {
  const suggestions = [];
  
  if (analysis.missing.length > 0) {
    suggestions.push(`Add these keywords: ${analysis.missing.slice(0, 5).join(', ')}`);
  }
  
  if (!resumeText.includes('•') && !/\n- /.test(resumeText)) {
    suggestions.push('Use bullet points (• or -) for better readability');
  }
  
  if (resumeText.length < 500) {
    suggestions.push('Expand your resume with more details about achievements');
  }
  
  if (resumeText.length > 1500) {
    suggestions.push('Consider condensing - ATS may truncate long resumes');
  }
  
  if (!/\b(achieved|improved|increased|decreased|saved|led|managed)\b/gi.test(resumeText)) {
    suggestions.push('Add action verbs and quantify achievements (e.g., "Improved X by 50%")');
  }
  
  return suggestions;
}

function generateOptimizedResume(resumeText, missingKeywords, foundKeywords) {
  // Simple optimization: suggest where to add keywords
  let optimized = resumeText;
  
  if (missingKeywords.length > 0) {
    const skillsSection = `\n\nTechnical Skills: ${foundKeywords.join(', ')}, ${missingKeywords.slice(0, 5).join(', ')}`;
    optimized += skillsSection;
  }
  
  return optimized;
}