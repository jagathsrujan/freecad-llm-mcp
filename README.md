# freecad-llm-mcp

> Intelligent CAD automation using LLMs + FreeCAD via Model Context Protocol

A framework for reliable, reproducible AI-assisted CAD modeling in FreeCAD — addressing the core failure modes of LLM-MCP pipelines for both simple and complex geometry.

---

## Why This Exists

LLMs integrated with FreeCAD via MCP produce inconsistent results — especially for complex geometry. The root causes are:

- **Stateless execution**: LLMs don't know the current geometry state between tool calls
- **Model switching drift**: Prompt-writing model ≠ execution model → behavioral mismatch
- **High temperature chaos**: CAD needs determinism, not creativity
- **No validation layer**: Bad geometry commits silently

This repo is a research-backed framework to fix all of that.

---

## Stack

| Layer | Tool |
|---|---|
| Prompt Engineering | Claude Sonnet (template generation, one-time) |
| Execution | DeepSeek / Haiku 4.5 (low temp, structured output) |
| CAD Backend | FreeCAD via MCP Server |
| Orchestration | OpenCode Agent |
| Validation | Rule-based Python layer |

---

## Core Concepts

### 1. Two-Phase Prompt Architecture
Separate prompt *design* from prompt *execution*. Use an expensive model (Sonnet) once to build robust templates. Use a cheap model to run them repeatedly.

### 2. Stateful Execution Pipeline
After every MCP tool call, query FreeCAD state before proceeding. Never let the LLM assume what the geometry looks like.

### 3. Atomic Operations
One feature per LLM call. No compound operations for complex geometry. Validate between each step.

### 4. Schema-Constrained Output
All LLM outputs must conform to a strict JSON schema before hitting the MCP server. Freeform text responses are rejected.

### 5. Validation Layer
Rule-based checks (wall thickness, interference, dimensional tolerance) run after each geometry commit — before the next LLM call.

---

## Quickstart

```bash
git clone https://github.com/yourusername/freecad-llm-mcp
cd freecad-llm-mcp
pip install -r requirements.txt

# Configure your models and MCP server
cp configs/models.yaml.example configs/models.yaml
# Edit configs/models.yaml with your API keys and endpoints

# Run an example
python src/pipeline/orchestrator.py --input examples/simple_bracket/prompt.md
```

---

## Project Structure

```
freecad-llm-mcp/
├── docs/           # Architecture, research notes, model comparisons
├── prompts/        # System prompts, templates, worked examples
├── src/            # Core pipeline, validation, MCP client
├── configs/        # Model and server configuration
├── examples/       # End-to-end worked examples
└── tests/          # Unit tests
```

---

## Key Findings (from real usage)

- Temperature > 0.3 on execution models causes ~40% more failures on complex geometry
- Compound MCP calls (multiple operations in one prompt) fail 2-3x more than atomic calls
- Explicit state queries between steps reduce cascading errors significantly
- DeepSeek performs comparably to Sonnet for execution when given schema-constrained prompts

Full research notes: [`docs/research_notes.md`](docs/research_notes.md)

---

## Roadmap

- [ ] Geometry validation layer (v0.2)
- [ ] Fine-tuning dataset — FreeCAD Python scripts corpus
- [ ] Multi-agent setup: planner + executor + validator
- [ ] Web UI for prompt-to-CAD pipeline
- [ ] Benchmarking suite for model comparison

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs welcome.

---

## License

MIT
