#!/usr/bin/env python3
"""
ATS Resume Optimizer for ResumeCraftAI2me
- Scrapes LinkedIn job descriptions
- Parses resumes (PDF/DOCX)
- Scores and optimizes resumes for ATS
"""

import requests
from bs4 import BeautifulSoup
import PyPDF2
import spacy
from docx import Document
from collections import Counter
import re
import os

# Load NLP model
nlp = spacy.load("en_core_web_sm")


def scrape_linkedin_job(url: str) -> dict:
    """Scrape LinkedIn job description from URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }