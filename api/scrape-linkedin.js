// Vercel Serverless Function - Scrape LinkedIn Job
const fetch = require('node-fetch');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { url } = req.body;
    if (!url || !url.includes('linkedin.com')) {
      return res.status(400).json({ error: 'Valid LinkedIn URL required' });
    }

    const fetchWithHeaders = async (headers) => {
      return fetch(url, { headers, redirect: 'follow' });
    };

    // Try multiple User-Agent strategies
    const strategies = [
      { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36', 'Accept': 'text/html,*/*', 'Accept-Language': 'en-US,en;q=0.9', 'Referer': 'https://www.linkedin.com/jobs/' },
      { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 'Accept': 'text/html', 'Accept-Language': 'en-US,en;q=0.9' },
      { 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 Safari/604.1', 'Accept': 'text/html' }
    ];

    let html = null;

    for (const headers of strategies) {
      try {
        const response = await fetchWithHeaders(headers);
        if (response.ok) {
          const text = await response.text();
          if (!text.includes('authwall') && text.length > 5000) {
            html = text;
            break;
          }
        }
      } catch (e) {}
    }

    if (!html) {
      const cleanUrl = url.split('?')[0];
      return res.status(200).json({
        success: true,
        title: 'LinkedIn Job',
        company: 'LinkedIn',
        location: '',
        description: 'Visit: ' + cleanUrl
      });
    }

    // Extract with regex
    const titleMatch = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
    const companyMatch = html.match(/<a[^>]*href="[^"]*\/company\/[^"]*"[^>]*>([^<]+)<\/a>/);
    const descMatch = html.match(/<div[^>]*class="[^"]*description[^"]*"[^>]*>([\s\S]*?)<\/div>/i);

    const title = titleMatch ? titleMatch[1].trim() : 'Job Title';
    const company = companyMatch ? companyMatch[1].trim() : 'Company';
    const description = descMatch ? descMatch[1].replace(/<[^>]+>/g, ' ').trim() : html.substring(0, 1000);

    return res.status(200).json({
      success: true,
      title,
      company,
      location: '',
      description: `${title}\n${company}\n\n${description}`
    });

  } catch (error) {
    res.status(200).json({
      success: true,
      title: 'LinkedIn Job',
      company: 'LinkedIn',
      location: '',
      description: 'Job URL: ' + (req.body.url || 'Unknown')
    });
  }
};
