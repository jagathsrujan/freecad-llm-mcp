# Contributing to freecad-llm-mcp

## What We Need

- Benchmark results from real FreeCAD operations
- Prompt templates that work reliably across models
- Geometry validation rules
- Example CAD tasks with ground truth

## How to Contribute

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit with clear messages
4. Open a PR with context on what you tested

## Adding Prompt Templates

Add to `prompts/templates/`. Include:
- Target operation type
- Which models it was tested on
- Success rate if known

## Reporting Failures

Open an issue with:
- Operation attempted
- Model and temperature used
- LLM output (redact API keys)
- FreeCAD error if any
