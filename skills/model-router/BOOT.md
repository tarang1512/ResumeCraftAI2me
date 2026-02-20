# Model Router - Auto-Activation

This skill is configured to auto-activate on gateway startup.

## Configuration

- **enabled**: `true` - Skill is active
- **autoActivate**: `true` - Loads automatically on boot
- **defaultModel**: `nvidia-nim/qwen/qwen3.5-397b-a17b` - Fallback model

## Routing Logic

The `model-router.route` tool analyzes each request and routes to:

1. **Qwen 3.5** - Complex reasoning, strategy, deep analysis
2. **Kimi K2.5** - Coding, technical tasks, debugging
3. **Mistral Large 3** - Quick questions, simple tasks

## Usage

The router runs automatically. No manual activation needed.

For manual routing:
```bash
python3 scripts/route.py "your request here"
```

## Status

✅ Active on boot
✅ Auto-routes all requests
✅ Never uses paid models
