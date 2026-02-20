---
name: perplexity-search
description: Search the web using Perplexity API (Sonar model). Use when user wants web search results, current information, flight prices, news, or any query requiring real-time data. Falls back to Brave Search if Perplexity key unavailable.
---

# Perplexity Search

Search the web using Perplexity AI's Sonar model for real-time information.

## Usage

Tool: `perplexity-search.search`

```json
{
  "query": "your search query here",
  "model": "sonar" // optional: sonar (default), sonar-pro, sonar-reasoning
}
```

## When to Use

- Flight prices and travel info
- Current news and events
- Product research
- Weather forecasts
- Any "what's the latest on..." questions
- Fact-checking with sources

## Models

- `sonar` — Fast, accurate, good for most searches (default)
- `sonar-pro` — More detailed responses
- `sonar-reasoning` — Complex reasoning tasks

## Response Format

Returns structured data with:
- Answer text
- Citations (URLs)
- Source snippets
- Token usage info

## API Key

Reads from `PERPLEXITY_API_KEY` environment variable.

## Example

```json
{
  "query": "cheapest flights JFK to Cancun July 2025",
  "model": "sonar"
}
```