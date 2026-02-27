// Vercel Serverless Function - ATS Score Calculator
module.exports = async (req, res) => {
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
    const { resume, job_description } = req.body;
    
    if (!resume || !job_description) {
      return res.status(400).json({ 
        error: 'Missing resume or job_description' 
      });
    }

    const resumeText = typeof resume === 'string' ? resume : JSON.stringify(resume);
    const resumeLower = resumeText.toLowerCase();
    const jobLower = job_description.toLowerCase();
    
    // Comprehensive keyword list
    const keywords = [
      // Programming
      'python', 'javascript', 'java', 'typescript', 'go', 'rust', 'c++', 'c#', 'ruby', 'php',
      'swift', 'kotlin', 'scala', 'r', 'matlab',
      // Frontend
      'react', 'vue', 'angular', 'svelte', 'next.js', 'nuxt', 'gatsby',
      'html', 'css', 'sass', 'less', 'tailwind', 'bootstrap', 'jquery',
      // Backend
      'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'laravel', 'rails',
      'asp.net', 'graphql', 'rest api', 'soap', 'grpc',
      // Database
      'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 
      'dynamodb', 'sqlite', 'cassandra', 'neo4j', 'firebase',
      // Cloud & DevOps
      'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
      'git', 'github', 'gitlab', 'bitbucket', 'terraform', 'ansible', 'puppet',
      'circleci', 'travis ci', 'github actions', 'gitlab ci',
      // AI/ML
      'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
      'scikit-learn', 'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn',
      'nlp', 'computer vision', 'ai', 'llm', 'openai', 'huggingface',
      // Mobile
      'react native', 'flutter', 'ios', 'android', 'xamarin', 'ionic',
      // Data
      'data science', 'data analysis', 'data engineering', 'etl', 'data pipeline',
      'tableau', 'power bi', 'looker', 'spark', 'hadoop', 'kafka',
      // Security
      'cybersecurity', 'penetration testing', 'owasp', 'encryption', 'oauth',
      'jwt', 'ssl', 'firewall', 'vulnerability assessment',
      // Methodologies
      'agile', 'scrum', 'kanban', 'ci/cd', 'devops', 'sre', 'tdd', 'bdd',
      'microservices', 'serverless', 'event-driven', 'domain-driven design',
      // Soft Skills
      'leadership', 'communication', 'teamwork', 'problem-solving', 'analytical',
      'organized', 'detail-oriented', 'self-motivated', 'collaboration',
      // Tools
      'jira', 'confluence', 'slack', 'teams', 'zoom', 'notion', 'linear',
      'figma', 'sketch', 'adobe xd', 'invision', 'miro', 'trello',
      // Roles
      'software engineer', 'developer', 'full-stack', 'backend', 'frontend',
      'senior', 'lead', 'manager', 'architect', 'analyst', 'designer',
      'product manager', 'tech lead', 'engineering manager', 'cto', 'vp'
    ];
    
    const found = [];
    const missing = [];
    
    keywords.forEach(keyword => {
      // Escape regex special characters: + . * ? ^ $ ( ) [ ] { } | \
      const cleanKeyword = keyword.toLowerCase()
        .replace(/[.+*?^$()[\]{}|\\]/g, '\\$&')
        .replace(/\s+/g, '\\s+');
      const regex = new RegExp(`\\b${cleanKeyword}\\b`, 'i');
      
      if (jobLower.includes(keyword.toLowerCase())) {
        if (regex.test(resumeLower)) {
          found.push(keyword);
        } else {
          missing.push(keyword);
        }
      }
    });
    
    // Calculate scores
    const totalJobKeywords = found.length + missing.length;
    const keywordMatch = totalJobKeywords > 0 
      ? Math.round((found.length / totalJobKeywords) * 100)
      : 50;
    
    // Format checks
    const hasBulletPoints = /[•\-]/.test(resumeText);
    const hasContactInfo = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/.test(resumeText);
    const hasPhone = /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/.test(resumeText);
    const hasLinkedIn = /linkedin\.com/.test(resumeLower);
    const wordCount = resumeText.split(/\s+/).filter(w => w.length > 0).length;
    
    const formatScore = Math.min(100, 
      (hasBulletPoints ? 25 : 0) + 
      (hasContactInfo ? 25 : 0) + 
      (hasPhone ? 15 : 0) + 
      (hasLinkedIn ? 15 : 0) +
      (wordCount >= 300 && wordCount <= 700 ? 20 : 10)
    );
    
    // Content quality
    const hasActionVerbs = /\b(achieved|improved|increased|decreased|saved|led|managed|developed|created|built|designed|implemented|launched|delivered|optimized|reduced|accelerated|spearheaded|transformed|engineered|architected)\b/gi.test(resumeText);
    const hasMetrics = /\d+%|\$\d+|\d+\s*(million|thousand|k|m|years?|months?)/gi.test(resumeText);
    
    const contentScore = (hasActionVerbs ? 50 : 25) + (hasMetrics ? 50 : 25);
    
    // Overall score
    const totalScore = Math.round((keywordMatch * 0.5) + (formatScore * 0.25) + (contentScore * 0.25));
    
    // Generate suggestions
    const suggestions = [];
    if (missing.length > 0) {
      suggestions.push(`Add these keywords: ${missing.slice(0, 5).join(', ')}`);
    }
    if (!hasBulletPoints) suggestions.push('Use bullet points (• or -) for achievements');
    if (!hasMetrics) suggestions.push('Add metrics (e.g., "Improved performance by 50%")');
    if (!hasActionVerbs) suggestions.push('Start bullets with action verbs (Led, Built, Created)');
    if (wordCount < 300) suggestions.push('Expand with more details');
    if (wordCount > 700) suggestions.push('Consider condensing for ATS readability');
    
    res.status(200).json({
      success: true,
      score: totalScore,
      breakdown: {
        keyword_match: keywordMatch,
        format_score: formatScore,
        content_score: contentScore
      },
      found_keywords: found.slice(0, 15),
      missing_keywords: missing.slice(0, 10),
      suggestions: suggestions.slice(0, 5),
      stats: {
        word_count: wordCount,
        has_contact: hasContactInfo,
        has_phone: hasPhone,
        has_linkedin: hasLinkedIn
      }
    });
    
  } catch (error) {
    console.error('ATS Score error:', error);
    res.status(500).json({ 
      error: 'Failed to analyze resume',
      details: error.message
    });
  }
};