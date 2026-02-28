// ResumeCraft AI - Main Application
// Calls backend API securely (API key hidden server-side)

const API_URL = '/api/generate-resume';

// PDF Rendering Function
async function renderPdfToCanvas(elementId, arrayBuffer, scale = 1.0) {
  try {
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    const canvas = document.getElementById(elementId);
    if (!canvas) return null;
    
    const firstPage = await pdf.getPage(1);
    const viewport = firstPage.getViewport({ scale });
    
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    
    const ctx = canvas.getContext('2d');
    await firstPage.render({ canvasContext: ctx, viewport }).promise;
    
    // Store PDF data for later
    window.pdfData = arrayBuffer;
    
    return { pageCount: pdf.numPages, width: viewport.width, height: viewport.height };
  } catch (e) {
    console.error('PDF render error:', e);
    return null;
  }
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
    // Read PDF
    const arrayBuffer = await file.arrayBuffer();
    window.pdfData = arrayBuffer;
    
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    
    // Extract text
    let fullText = '';
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const pageText = textContent.items.map(item => item.str).join(' ');
      fullText += pageText + ' ';
    }

    window.extractedResumeText = fullText.trim();

    // RENDER FULL PDF PREVIEW (ALL PAGES)
    const pdfCanvasContainer = document.getElementById('pdfCanvasContainer');
    const pdfPreview = document.getElementById('pdfPreview');
    
    if (pdfCanvasContainer && pdf) {
      // Clear previous content
      pdfCanvasContainer.innerHTML = '';
      pdfCanvasContainer.style.display = 'block';
      pdfCanvasContainer.style.overflow = 'auto';
      pdfCanvasContainer.style.background = '#1a1a2e';
      
      // Render ALL pages
      const scale = 1.3; // Good balance of quality vs size
      const numPages = pdf.numPages;
      
      for (let pageNum = 1; pageNum <= numPages && pageNum <= 3; pageNum++) { // Limit to first 3 pages for performance
        try {
          const page = await pdf.getPage(pageNum);
          const viewport = page.getViewport({ scale });
          
          // Create canvas for this page
          const canvas = document.createElement('canvas');
          canvas.style.display = 'block';
          canvas.style.margin = '10px auto';
          canvas.style.boxShadow = '0 4px 20px rgba(0,0,0,0.5)';
          canvas.style.background = 'white';
          canvas.style.maxWidth = '100%';
          canvas.width = viewport.width;
          canvas.height = viewport.height;
          
          const ctx = canvas.getContext('2d');
          await page.render({ canvasContext: ctx, viewport }).promise;
          
          pdfCanvasContainer.appendChild(canvas);
          
          // Add page separator
          if (pageNum < numPages && pageNum < 3) {
            const separator = document.createElement('div');
            separator.style.textAlign = 'center';
            separator.style.color = '#6366f1';
            separator.style.padding = '10px';
            separator.innerHTML = '<i class="fas fa-ellipsis-h"></i> Page ' + pageNum;
            pdfCanvasContainer.appendChild(separator);
          }
        } catch (pageErr) {
          console.error('Error rendering page', pageNum, pageErr);
        }
      }
      
      // Show preview container
      if (pdfPreview) {
        pdfPreview.classList.add('active');
      }
      
      // Store PDF for analysis section
      window.pdfData = arrayBuffer;
    }
    
    // Also show text content
    const pdfContent = document.getElementById('pdfContent');
    if (pdfContent) {
      const displayText = fullText.trim().substring(0, 3000)
        .replace(/\s+/g, ' ')
        .replace(/\n\s*\n/g, '\n\n')
        .trim();
      pdfContent.textContent = displayText + (fullText.length > 3000 ? "\n\n..." : "");
    }

    // Update UI to success state
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

    // Auto-fill resume form
    const resumeForm = document.getElementById('resumeForm');
    if (resumeForm && fullText) {
      extractAndFillResumeData(fullText);
    }
    
  } catch (error) {
    console.error('PDF parsing error:', error);
    alert('Error reading PDF: ' + error.message);
  } finally {
    if (spinner) spinner.style.display = 'none';
  }
}

function resetUpload() {
  // Hide previews
  const pdfPreview = document.getElementById('pdfPreview');
  const pdfCanvasContainer = document.getElementById('pdfCanvasContainer');
  const pdfCanvas = document.getElementById('pdfCanvas');
  const pdfContent = document.getElementById('pdfContent');
  
  if (pdfPreview) pdfPreview.classList.remove('active');
  if (pdfCanvasContainer) pdfCanvasContainer.style.display = 'none';
  if (pdfCanvas) {
    const ctx = pdfCanvas.getContext('2d');
    ctx.clearRect(0, 0, pdfCanvas.width, pdfCanvas.height);
  }
  if (pdfContent) pdfContent.textContent = '';
  
  // Clear data
  if (fileInput) fileInput.value = '';
  window.extractedResumeText = '';
  window.pdfData = null;
  
  // Reset preview in analysis section
  const analysisPreviewSection = document.getElementById('resumePreviewSection');
  if (analysisPreviewSection) analysisPreviewSection.style.display = 'none';
  
  if (uploadArea) {
    uploadArea.innerHTML = `
      <div class="upload-icon">
        <i class="fas fa-cloud-upload-alt"></i>
      </div>
      <h3>Drag & Drop Your Resume</h3>
      <p>Supports PDF files up to 10MB</p>
      <label for="fileInput" class="btn btn-primary" style="cursor:pointer;pointer-events:auto;display:inline-flex;align-items:center;gap:8px;position:relative;z-index:100">
        <i class="fas fa-folder-open"></i> Browse Files
      </label>
      <input type="file" id="fileInput" class="file-input" accept=".pdf" onchange="handleFileUpload(this)" style="display:none">
    `;
  }
}

function extractAndFillResumeData(text) {
  const lines = text.split(/\n|\.\s+/).filter(l => l.trim());
  
  // Find name
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
  
  // Find email
  const emailMatch = text.match(/[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}/);
  if (emailMatch) {
    const emailInput = document.querySelector('input[name="email"]');
    if (emailInput) emailInput.value = emailMatch[0];
  }
  
  // Find phone
  const phoneMatch = text.match(/[\+]?[\d\s\-\(\)]{10,}/);
  if (phoneMatch) {
    const phoneInput = document.querySelector('input[name="phone"]');
    if (phoneInput) phoneInput.value = phoneMatch[0];
  }
}

// Toast notification
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  toast.style.cssText = 'position:fixed;bottom:20px;right:20px;padding:12px 20px;border-radius:8px;z-index:1000;font-weight:500;';
  
  if (type === 'success') toast.style.background = '#10b981';
  else if (type === 'error') toast.style.background = '#ef4444';
  else toast.style.background = '#6366f1';
  
  toast.style.color = 'white';
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

// LinkedIn Scrape
async function scrapeLinkedIn() {
  const url = document.getElementById('linkedinUrl').value.trim();
  if (!url) {
    showToast('Please enter a LinkedIn job URL', 'error');
    return;
  }

  showToast('Fetching job description...', 'info');

  try {
    const response = await fetch('/api/scrape-linkedin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    const contentType = response.headers.get('content-type');
    let data
    // Handle response
    const contentType = response.headers.get('content-type');
    let data;
    
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      const text = await response.text();
      throw new Error(text.substring(0, 100) || 'Invalid response');
    }

    if (data.success) {
      document.getElementById('jobDescription').value = data.description;
      showToast(`Loaded: ${data.title} at ${data.company}`, 'success');
    } else {
      showToast(data.error || 'Failed to fetch job', 'warning');
    }
  } catch (error) {
    showToast('Error: ' + error.message, 'error');
  }
}

// Resume Analysis
async function analyzeResume() {
  if (!window.extractedResumeText) {
    showToast('Please upload a resume first', 'error');
    return;
  }

  const jobDescription = document.getElementById('jobDescription').value.trim();
  if (!jobDescription) {
    showToast('Please enter a job description', 'error');
    return;
  }

  // SHOW PDF PREVIEW FIRST IN ANALYSIS SECTION
  const previewSection = document.getElementById('resumePreviewSection');
  const analysisCanvas = document.getElementById('analysisPdfCanvas');
  
  if (previewSection && analysisCanvas && window.pdfData) {
    try {
      const pdf = await pdfjsLib.getDocument({ data: window.pdfData }).promise;
      const firstPage = await pdf.getPage(1);
      const viewport = firstPage.getViewport({ scale: 1.0 });
      
      analysisCanvas.width = viewport.width;
      analysisCanvas.height = viewport.height;
      
      const ctx = analysisCanvas.getContext('2d');
      await firstPage.render({ canvasContext: ctx, viewport }).promise;
      
      previewSection.style.display = 'block';
      
      // Scroll to resume preview
      previewSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (e) {
      console.error('PDF render error:', e);
    }
  }

  const spinner = document.getElementById('analysisSpinner');
  const result = document.getElementById('atsResult');

  if (spinner) spinner.style.display = 'block';
  if (result) result.classList.remove('active');

  try {
    const response = await fetch('/api/ats-score', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        resume: window.extractedResumeText, 
        job_description: jobDescription 
      })
    });

    const data = await response.json();

    if (data.success) {
      // Update score
      const scoreValue = document.getElementById('scoreValue');
      const scoreCircle = document.getElementById('scoreCircle');
      if (scoreValue) scoreValue.textContent = data.score;
      if (scoreCircle) scoreCircle.style.setProperty('--score', data.score);

      // Update keywords
      const foundContainer = document.getElementById('foundKeywords');
      const missingContainer = document.getElementById('missingKeywords');
      
      if (foundContainer) {
        foundContainer.innerHTML = (data.found_keywords || [])
          .map(k => `<span class="keyword-tag keyword-found"><i class="fas fa-check"></i> ${k}</span>`)
          .join('');
      }
      
      if (missingContainer) {
        missingContainer.innerHTML = (data.missing_keywords || [])
          .map(k => `<span class="keyword-tag keyword-missing"><i class="fas fa-times"></i> ${k}</span>`)
          .join('');
      }

      // Update suggestions
      const suggestionsList = document.getElementById('suggestionsList');
      if (suggestionsList) {
        suggestionsList.innerHTML = (data.suggestions || [])
          .map(s => `<li style="margin-bottom: 0.5rem;">${s}</li>`)
          .join('');
      }

      if (result) {
        result.classList.add('active');
        // Scroll to results
        result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
      
      showToast(`Analysis complete! Score: ${data.score}/100`, 'success');
    } else {
      showToast(data.error || 'Analysis failed', 'error');
    }
  } catch (error) {
    showToast('Error: ' + error.message, 'error');
  } finally {
    if (spinner) spinner.style.display = 'none';
  }
}

// DOM Elements and Event Listeners
document.addEventListener('DOMContentLoaded', function() {
  // Initialize any necessary elements
  const fileInput = document.getElementById('fileInput');
  if (fileInput) {
    fileInput.addEventListener('change', function() {
      handleFileUpload(this);
    });
  }
});
