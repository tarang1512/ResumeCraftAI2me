// ResumeCraft AI - Resume Generation Backend
// Calls NVIDIA NIM API securely (key hidden server-side)
const API_URL = 'https://integrate.api.nvidia.com/v1/chat/completions';
const API_KEY = process.env.NVIDIA_API_KEY || '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';

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
    const { name, title, email, phone, experience, education, skills } = req.body;
    
    if (!name || !title) {
      return res.status(400).json({ error: 'Name and title are required' });
    }

    const prompt = buildPrompt({ name, title, email, phone, experience, education, skills });
    
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        model: 'nvidia-nim/mistralai/mistral-large-3-675b-instruct-2512',
        messages: [
          {
            role: 'system',
            content: 'You are a professional resume writer. Create polished, ATS-friendly resumes. Return only the resume content in clean HTML format with proper sections. Use h1 for name, h2 for section headers, and p/div for content.'
          },
          { role: 'user', content: prompt }
        ],
        temperature: 0.7,
        max_tokens: 2000
      })
    });

    if (!response.ok) {
      throw new Error(`NVIDIA API error: ${response.status}`);
    }

    const result = await response.json();
    const resume = result.choices[0].message.content;
    
    return res.status(200).json({ success: true, resume });
    
  } catch (error) {
    console.error('Generation error:', error);
    return res.status(500).json({ 
      error: 'Resume generation failed', 
      fallback: true 
    });
  }
};

function buildPrompt(data) {
  return `Create a professional resume for:
Name: ${data.name}
Target Role: ${data.title}
Email: ${data.email || 'N/A'}
Phone: ${data.phone || 'N/A'}
Work Experience: ${data.experience || 'Not provided'}
Education: ${data.education || 'Not provided'}
Skills: ${data.skills || 'Not provided'}

Format as clean HTML with these sections:
1. Header with name (large, bold) and contact info
2. Professional Summary (2-3 sentences)
3. Experience (company, role, dates, bullet points)
4. Education
5. Skills

Use professional styling inline. Return ONLY the HTML, no markdown.`;
}
