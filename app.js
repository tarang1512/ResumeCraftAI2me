// ResumeCraft AI - Main Application
// Calls backend API securely (API key hidden server-side)

const API_URL = '/api/generate-resume';

// DOM Elements
const form = document.getElementById('resumeForm');
const generateBtn = document.getElementById('generateBtn');
const btnText = generateBtn.querySelector('.btn-text');
const btnLoading = generateBtn.querySelector('.btn-loading');
const outputSection = document.getElementById('outputSection');
const resumePreview = document.getElementById('resumePreview');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');

// Event Listeners
form.addEventListener('submit', handleGenerate);
copyBtn.addEventListener('click', copyToClipboard);
downloadBtn.addEventListener('click', downloadResume);

async function handleGenerate(e) {
    e.preventDefault();
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    setLoading(true);
    
    try {
        const resume = await generateResume(data);
        displayResume(resume);
    } catch (error) {
        console.error('Generation failed:', error);
        // Fallback to template-based generation
        const resume = generateTemplateResume(data);
        displayResume(resume);
    } finally {
        setLoading(false);
    }
}

async function generateResume(data) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (!response.ok) throw new Error("API request failed");
    
    const result = await response.json();
    
    if (!result.success) throw new Error(result.error || "Generation failed");
    
    return result.resume;
    
  } catch (error) {
    throw error;
  }
}

function buildPrompt(data) {
    return `Create a professional resume for:

Name: ${data.name}
Target Role: ${data.title}
Email: ${data.email}
Phone: ${data.phone || 'N/A'}

Work Experience:
${data.experience}

Education:
${data.education}

Skills:
${data.skills}

Format as clean HTML with these sections:
1. Header with name (large, bold) and contact info
2. Professional Summary (2-3 sentences highlighting key strengths)
3. Experience (formatted with company, role, dates, bullet points for achievements)
4. Education (formatted nicely)
5. Skills (as a clean list)

Use professional formatting. Make achievements sound impactful with action verbs.`;
}

function generateTemplateResume(data) {
    // Parse experience into structured format
    const expLines = data.experience.split('\n').filter(line => line.trim());
    const eduLines = data.education.split('\n').filter(line => line.trim());
    const skillList = data.skills.split(/[,\n]/).map(s => s.trim()).filter(s => s);
    
    // Generate professional summary based on role
    const summary = generateSummary(data.title, expLines.length, skillList);
    
    let html = `
        <div class="resume-header">
            <h1>${escapeHtml(data.name)}</h1>
            <p class="job-title">${escapeHtml(data.title)}</p>
            <p class="contact-info">
                ${escapeHtml(data.email)}${data.phone ? ' | ' + escapeHtml(data.phone) : ''}
            </p>
        </div>
        
        <h2>Professional Summary</h2>
        <p>${escapeHtml(summary)}</p>
        
        <h2>Experience</h2>
    `;
    
    // Format experience
    expLines.forEach(line => {
        if (line.includes('-') || line.includes('|') || line.includes('at')) {
            html += `<p><strong>${escapeHtml(line)}</strong></p>`;
        } else {
            html += `<p>• ${escapeHtml(line)}</p>`;
        }
    });
    
    html += `<h2>Education</h2>`;
    eduLines.forEach(line => {
        html += `<p>${escapeHtml(line)}</p>`;
    });
    
    html += `<h2>Skills</h2>`;
    html += `<p>${escapeHtml(skillList.join(' • '))}</p>`;
    
    return html;
}

function generateSummary(title, expYears, skills) {
    const actionVerbs = ['Results-driven', 'Innovative', 'Detail-oriented', 'Strategic', 'Dynamic'];
    const verb = actionVerbs[Math.floor(Math.random() * actionVerbs.length)];
    
    let summary = `${verb} ${title} with ${expYears > 0 ? 'proven experience' : 'strong foundation'} in `;
    
    if (skills.length >= 3) {
        summary += `${skills[0].toLowerCase()}, ${skills[1].toLowerCase()}, and ${skills[2].toLowerCase()}. `;
    } else if (skills.length > 0) {
        summary += `${skills[0].toLowerCase()}. `;
    } else {
        summary += `the field. `;
    }
    
    summary += `Demonstrated ability to deliver high-quality results and collaborate effectively in fast-paced environments. Seeking to leverage expertise to drive success and contribute to organizational goals.`;
    
    return summary;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function displayResume(html) {
    resumePreview.innerHTML = html;
    outputSection.style.display = 'block';
    outputSection.scrollIntoView({ behavior: 'smooth' });
}

function setLoading(loading) {
    generateBtn.disabled = loading;
    btnText.style.display = loading ? 'none' : 'inline';
    btnLoading.style.display = loading ? 'flex' : 'none';
}

function copyToClipboard() {
    const text = resumePreview.innerText;
    navigator.clipboard.writeText(text).then(() => {
        showMessage('Copied to clipboard!', 'success');
        copyBtn.textContent = '✅ Copied!';
        setTimeout(() => copyBtn.textContent = '📋 Copy', 2000);
    });
}

function downloadResume() {
    const name = document.getElementById('name').value.replace(/\s+/g, '_');
    const html = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>${document.getElementById('name').value} - Resume</title>
    <style>
        body { font-family: Georgia, serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }
        h1 { color: #1a1a1a; border-bottom: 2px solid #6366f1; padding-bottom: 10px; }
        h2 { color: #4f46e5; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #e2e8f0; margin-top: 1.5rem; }
        .job-title { font-size: 1.1rem; color: #555; font-weight: 500; }
        .contact-info { color: #666; margin-bottom: 1rem; }
        p { margin: 0.5rem 0; }
        @media print { body { margin: 0; } }
    </style>
</head>
<body>
    ${resumePreview.innerHTML}
</body>
</html>`;
    
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${name}_Resume.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showMessage('Resume downloaded!', 'success');
}

function showMessage(text, type) {
    const existing = document.querySelector('.message');
    if (existing) existing.remove();
    
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    msg.textContent = text;
    outputSection.insertBefore(msg, outputSection.firstChild);
    
    setTimeout(() => msg.remove(), 3000);
}

// File Upload Handling
async function handleFileUpload(input) {
  const file = input.files[0];
  if (!file) return;

  if (file.type !== 'application/pdf') {
    alert('Please upload a PDF file');
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    alert('File size must be less than 10MB');
    return;
  }

  const spinner = document.getElementById('uploadSpinner');
  const uploadArea = document.getElementById('uploadArea');
  
  if (spinner) spinner.style.display = 'block';
  
  try {
    // Read PDF using PDF.js
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    
    let fullText = '';
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const pageText = textContent.items.map(item => item.str).join(' ');
      fullText += pageText + ' ';
    }

    // Store extracted text and show success
    window.extractedResumeText = fullText.trim();
    
    // Update UI
    if (uploadArea) {
      uploadArea.innerHTML = `
        <div class="upload-icon" style="color: var(--success);">
          <i class="fas fa-check-circle"></i>
        </div>
        <h3>✅ Resume Uploaded Successfully</h3>
        <p>${file.name} (${(file.size / 1024).toFixed(1)} KB)</p>
        <button class="btn btn-primary" onclick="resetUpload()">
          <i class="fas fa-redo"></i> Upload Different File
        </button>
      `;
    }
    
    // Auto-fill form if resume form exists
    const resumeForm = document.getElementById('resumeForm');
    if (resumeForm && fullText) {
      // Try to extract basic info and fill form
      extractAndFillResumeData(fullText);
    }
    
  } catch (error) {
    console.error('PDF parsing error:', error);
    alert('Error reading PDF. Please try again.');
  } finally {
    if (spinner) spinner.style.display = 'none';
  }
}

function resetUpload() {
  const uploadArea = document.getElementById('uploadArea');
  const fileInput = document.getElementById('fileInput');
  
  if (fileInput) fileInput.value = '';
  window.extractedResumeText = '';
  
  if (uploadArea) {
    uploadArea.innerHTML = `
      <div class="upload-icon">
        <i class="fas fa-cloud-upload-alt"></i>
      </div>
      <h3>Drag & Drop Your Resume</h3>
      <p>Supports PDF files up to 10MB</p>
      <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
        <i class="fas fa-folder-open"></i> Browse Files
      </button>
      <input type="file" id="fileInput" class="file-input" accept=".pdf" onchange="handleFileUpload(this)">
    `;
  }
}

function extractAndFillResumeData(text) {
  // Simple extraction logic - can be enhanced
  const lines = text.split(/\n|\.\s+/).filter(l => l.trim());
  
  // Try to find name (first line with 2-3 words, capitalized)
  for (const line of lines.slice(0, 10)) {
    const words = line.trim().split(/\s+/);
    if (words.length >= 2 && words.length <= 4 && /^[A-Z]/.test(line)) {
      const nameInput = document.querySelector('input[name="name"]');
      if (nameInput && !nameInput.value) {
        nameInput.value = line.trim();
        break;
      }
    }
  }
  
  // Try to find email
  const emailMatch = text.match(/[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}/);
  if (emailMatch) {
    const emailInput = document.querySelector('input[name="email"]');
    if (emailInput) emailInput.value = emailMatch[0];
  }
  
  // Try to find phone
  const phoneMatch = text.match(/[\+]?[\d\s\-\(\)]{10,}/);
  if (phoneMatch) {
    const phoneInput = document.querySelector('input[name="phone"]');
    if (phoneInput) phoneInput.value = phoneMatch[0];
  }
}
