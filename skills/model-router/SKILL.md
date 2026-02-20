---
name: model-router
description: Intelligently route user requests between free models (Qwen, Kimi, Mistral) based on task complexity. Use when user wants optimal model selection for speed vs quality. Routes to nvidia-nim/qwen/qwen3.5-397b-a17b (256k ctx) for complex reasoning, nvidia-nim/moonshotai/kimi-k2.5 (256k ctx) for coding/analysis, or nvidia-nim/mistralai/mistral-large-3-675b-instruct-2512 (128k ctx) for quick tasks. NEVER uses paid models.
---

# Model Router

Intelligently routes requests between free models based on task characteristics.

## Available Models

1. **nvidia-nim/qwen/qwen3.5-397b-a17b** (Qwen 3.5 - Premium Free)
   - 256k context window
   - Best for complex reasoning, multi-step analysis, deep thinking
   - MoE architecture (397B total, 17B active)
   - Use for: complex problem-solving, deep analysis, nuanced reasoning, long-context understanding

2. **nvidia-nim/moonshotai/kimi-k2.5** (Kimi Free)
   - 256k context window
   - Better at coding, technical tasks, structured analysis
   - Use for: coding tasks, debugging, technical documentation, multi-step workflows

3. **nvidia-nim/mistralai/mistral-large-3-675b-instruct-2512** (Mistral Free)
   - 128k context window
   - Fastest response times
   - Use for: quick Q&A, simple summaries, one-step tasks, speed-critical responses

## Routing Logic

Analyze user request and route accordingly:

### Route to Qwen 3.5 if:
- Complex multi-step reasoning required
- Deep analysis or nuanced explanations
- Abstract problem-solving
- Tasks requiring "thinking" or deliberation
- Long-context understanding with complex relationships
- Strategic planning or decision-making

### Route to Kimi (Free) if:
- Coding tasks (analysis, debugging, writing, refactoring)
- Technical documentation
- Multi-step workflows (but not deeply complex)
- Data analysis or structured tasks
- Tasks requiring precision over speed

### Route to Mistral (Free) if:
- Quick factual questions
- Simple summaries or paraphrasing
- One-step tasks
- Speed is priority over depth
- Short responses expected (<200 words)
- Casual conversation or greetings

## Execution

Spawn sub-agent with appropriate model:

```json
{
  "agentId": "main",
  "model": "nvidia-nim/qwen/qwen3.5-397b-a17b",
  "task": "<original_user_request>"
}
```

Or for Kimi:

```json
{
  "agentId": "main",
  "model": "nvidia-nim/moonshotai/kimi-k2.5",
  "task": "<original_user_request>"
}
```

Or for Mistral:

```json
{
  "agentId": "main",
  "model": "nvidia-nim/mistralai/mistral-large-3-675b-instruct-2512",
  "task": "<original_user_request>"
}
```

## IMPORTANT
- NEVER spawn with kimi-coding/k2p5 (paid)
- NEVER spawn with kimi-coding/kimi-k2-thinking (paid)
- Only use free tier models
- Always preserve conversation context when spawning
- Default to Qwen 3.5 for ambiguous complex tasks
- Default to Mistral for ambiguous simple tasks
