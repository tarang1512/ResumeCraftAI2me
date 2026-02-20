#!/usr/bin/env python3
"""
Perplexity Search - Web search via Perplexity API
Uses Sonar model for real-time web search results.
"""

import os
import sys
import json
import urllib.request
import urllib.error

def search(query, model="sonar"):
    """Search using Perplexity API."""
    api_key = os.environ.get('PERPLEXITY_API_KEY')
    
    if not api_key:
        return {
            "error": "PERPLEXITY_API_KEY not set",
            "message": "Export PERPLEXITY_API_KEY environment variable"
        }
    
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Be concise and accurate. Include sources."},
            {"role": "user", "content": query}
        ]
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # Extract useful info
            answer = result['choices'][0]['message']['content']
            citations = result.get('citations', [])
            usage = result.get('usage', {})
            
            return {
                "success": True,
                "answer": answer,
                "citations": citations,
                "model": model,
                "tokens": usage.get('total_tokens', 0)
            }
            
    except urllib.error.HTTPError as e:
        return {
            "error": f"HTTP {e.code}",
            "message": e.read().decode('utf-8')
        }
    except Exception as e:
        return {
            "error": "Request failed",
            "message": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided"}))
        sys.exit(1)
    
    query = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "sonar"
    
    result = search(query, model)
    print(json.dumps(result, indent=2))