#!/usr/bin/env python3
"""
Model Router - Intelligently routes requests between free models (Qwen, Kimi, Mistral).
Analyzes task complexity and routes accordingly.
NEVER uses paid models.
"""
import sys
import json

def analyze_request(text):
    """Analyze request and return appropriate model."""
    text_lower = text.lower()
    
    # Qwen 3.5 indicators (complex reasoning, deep analysis)
    qwen_keywords = [
        'reason', 'think', 'analyze deeply', 'complex', 'strategy', 'plan',
        'evaluate', 'compare', 'contrast', 'pros and cons', 'trade-off',
        'nuance', 'sophisticated', 'abstract', 'conceptual', 'theoretical',
        'philosophical', 'ethical', 'implications', 'consequences', 'predict',
        'forecast', 'scenario', 'hypothesis', 'synthesis', 'integrate'
    ]
    
    # Kimi indicators (coding, technical, structured tasks)
    kimi_keywords = [
        'code', 'debug', 'program', 'script', 'function', 'class', 'api',
        'library', 'framework', 'implement', 'build', 'create', 'write code',
        'refactor', 'optimize', 'error', 'bug', 'fix', 'test', 'unit test',
        'documentation', 'technical', 'data', 'parse', 'json', 'xml', 'sql',
        'database', 'algorithm', 'data structure', 'regex', 'shell', 'bash'
    ]
    
    # Mistral indicators (quick, simple, factual)
    mistral_keywords = [
        'what', 'when', 'where', 'who', 'is', 'are', 'was', 'were',
        'quick', 'fast', 'brief', 'short', 'summary', 'simple', 'basic',
        'hello', 'hi', 'hey', 'thanks', 'thank you', 'goodbye', 'bye',
        'yes', 'no', 'maybe', 'list', 'define', 'meaning', 'translate'
    ]
    
    # Score each model
    qwen_score = sum(1 for kw in qwen_keywords if kw in text_lower)
    kimi_score = sum(1 for kw in kimi_keywords if kw in text_lower)
    mistral_score = sum(1 for kw in mistral_keywords if kw in text_lower)
    
    # Find highest score
    scores = {
        'qwen': qwen_score,
        'kimi': kimi_score,
        'mistral': mistral_score
    }
    
    max_score = max(scores.values())
    
    # If all scores are 0, use heuristics based on length and question type
    if max_score == 0:
        # Long requests tend to be complex
        if len(text) > 200:
            return {
                "model": "nvidia-nim/qwen/qwen3.5-397b-a17b",
                "reason": "Long request - using Qwen 3.5 for deep analysis"
            }
        # Questions starting with how/why tend to need reasoning
        elif text_lower.startswith(('how', 'why')):
            return {
                "model": "nvidia-nim/moonshotai/kimi-k2.5",
                "reason": "How/why question - using Kimi for structured explanation"
            }
        else:
            return {
                "model": "nvidia-nim/mistralai/mistral-large-3-675b-instruct-2512",
                "reason": "Simple request - using Mistral for fast response"
            }
    
    # Route to highest scoring model
    if qwen_score == max_score:
        return {
            "model": "nvidia-nim/qwen/qwen3.5-397b-a17b",
            "reason": "Complex reasoning task - using Qwen 3.5 (256k ctx, deep thinking)"
        }
    elif kimi_score == max_score:
        return {
            "model": "nvidia-nim/moonshotai/kimi-k2.5",
            "reason": "Technical/coding task - using Kimi K2.5 (256k ctx, precise)"
        }
    else:
        return {
            "model": "nvidia-nim/mistralai/mistral-large-3-675b-instruct-2512",
            "reason": "Quick/simple task - using Mistral Large 3 (fast, 128k ctx)"
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No request text provided"}))
        sys.exit(1)
    
    request_text = sys.argv[1]
    result = analyze_request(request_text)
    print(json.dumps(result))
