// Vercel Serverless Function - Scrape LinkedIn Job
const fetch = require('node-fetch');
const cheerio = require('cheerio');

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
    const { url } = req.body;
    
    if (!url || !url.includes('linkedin.com')) {
      return res.status(400).json({ error: 'Valid LinkedIn URL required' });
    }

    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const html = await response.text();
    const $ = cheerio.load(html);
    
    // Extract job details
    const title = $('h1').first().text().trim() ||
                  $('.top-card-layout__title').text().trim() ||
                  $('meta[property="og:title"]').attr('content')?.replace(' | LinkedIn', '') ||
                  'Job Title Not Found';
    
    const company = $('.top-card-layout__company-name').text().trim() ||
                    $('.top-card-layout__card-subline').text().trim() ||
                    $('a[href*="/company/"]').first().text().trim() ||
                    'Company Not Found';
    
    // Extract job description - prioritize main content areas
    let description = $(".show-more-less-html__markup").text().trim() || 
                      $(".description__text").text().trim() || 
                      $("[data-test-id="job-description"]").text().trim() || 
                      $(".job-description").text().trim() || 
                      "";

    // Clean up: remove empty lines, excess whitespace, special chars
    if (description) {
        description = description
            .replace(/^\s*[\n\r]+/gm, "")
            .replace(/[\n\r]{3,}/g, "\n\n")
            .replace(/\s+$/gm, "")
            .replace(/^\s+/gm, "")
            .replace(/[\x00-\x08\x0B-\x0C\x0E-\x1F]/g, "")
            .trim();
    }

    // Fallback if still empty
    if (!description || description.length < 50) {
        description = "Job description could not be extracted. The posting may require login or use dynamic loading.";
    }
    
    const location = $('.top-card-layout__location').text().trim() ||
                    $('.top-card-layout__bullet').text().trim() ||
                    '';

    res.status(200).json({
      success: true,
      title,
      company,
      location,
      description: `${title}\n${company}${location ? "\n" + location : ""}\n\n${description}`
    });
    
  } catch (error) {
    console.error('LinkedIn scrape error:', error);
    res.status(500).json({ 
      error: 'Failed to scrape LinkedIn job',
      details: error.message,
      fallback: 'Please paste the job description manually'
    });
  }
};