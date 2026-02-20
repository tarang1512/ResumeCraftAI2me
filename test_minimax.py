#!/usr/bin/env python3
"""Test MiniMax M2.1 via NVIDIA NIM API (non-streaming)"""
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

print("Testing MiniMax M2.1...")
print("-" * 40)

try:
    completion = client.chat.completions.create(
        model="minimaxai/minimax-m2.1",
        messages=[{"role": "user", "content": "Say hello and confirm you're MiniMax M2.1"}],
        temperature=1,
        top_p=0.95,
        max_tokens=512,
        stream=False
    )
    
    print("✅ Success!")
    print(f"Model: {completion.model}")
    print(f"Response: {completion.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
