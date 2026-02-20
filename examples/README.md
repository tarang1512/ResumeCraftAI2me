# Multi-Agent Demo

This example demonstrates spawning sub-agents with different names, models, and specializations.

## Files

- `multi-agent-demo.js` - Main demonstration script

## What It Demonstrates

1. **Named Agents**: Each agent gets a unique identity (e.g., "code-reviewer", "creative-writer")
2. **Model Selection**: Different tasks can use different AI models
3. **Specialized Tasks**: Each agent is configured for a specific purpose
4. **Concurrent Spawning**: Multiple agents can be spawned and managed

## Usage

```bash
node examples/multi-agent-demo.js
```

## Agent Types in This Demo

| Name | Model | Purpose |
|------|-------|---------|
| code-reviewer | kimi-k2.5 | Code review and bug detection |
| creative-writer | kimi-k2.5 | Creative writing with poetic style |
| data-analyzer | kimi-k2.5 | Data analysis and insights |

## Key Concepts

- **spawnAgent()**: Function to create new agent instances
- **Configuration**: Each agent has name, model, task, and metadata
- **Timeout**: Agents can have custom timeout limits
- **Results**: Track success/failure of each spawned agent
