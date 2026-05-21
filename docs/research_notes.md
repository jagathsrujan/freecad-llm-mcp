# Research Notes — LLM + FreeCAD MCP Inconsistency Analysis

## Problem Statement

LLM-driven CAD automation via MCP produces inconsistent results. Inconsistency is significantly higher for complex geometry than simple geometry. This document records findings, hypotheses, and tested solutions.

---

## Root Cause Analysis

### 1. Statelessness
**Problem**: MCP servers are stateless per call. LLMs don't receive geometry state unless explicitly queried.
**Impact**: LLM makes next operation based on assumed state -> wrong feature tree -> cascading failures.
**Fix**: Explicit state query after every MCP tool call. Inject into next prompt.

### 2. Temperature Sensitivity
**Problem**: Execution models running at high temperature introduce variation in parameter values.
**Impact**: Dimensional inconsistency (e.g., 10.0mm vs 10.3mm) — acceptable in text, catastrophic in CAD.
**Fix**: Temperature <= 0.2 for all execution calls. Reserve higher temp for brainstorming/planning only.

### 3. Two-Model Behavioral Mismatch
**Problem**: Prompt written for Sonnet's reasoning style sent to DeepSeek for execution.
**Impact**: DeepSeek interprets instructions differently, especially for conditional geometry logic.
**Fix**: Use Sonnet for template generation only. Templates must be model-agnostic (schema-driven, not prose-driven).

### 4. Compound Operation Failure
**Problem**: Prompts asking for multiple FreeCAD operations in one call.
**Impact**: Partial execution with no clear failure point. Hard to debug.
**Fix**: One operation per LLM call. Orchestrator handles sequencing.

### 5. No Physical Validation
**Problem**: LLM has no awareness of physical constraints (min wall thickness, interference, printability).
**Impact**: Geometrically valid but physically invalid models committed silently.
**Fix**: Rule-based validator after every MCP commit.

---

## Model Comparison (Execution Task)

| Model | Temp | Simple Geo Success | Complex Geo Success | Notes |
|---|---|---|---|---|
| Sonnet 4.6 | 0.2 | ~95% | ~78% | Best overall, expensive |
| DeepSeek V3 | 0.5 | ~88% | ~52% | Degrades sharply with complexity |
| DeepSeek V3 | 0.2 | ~90% | ~70% | Much better at low temp |
| Haiku 4.5 | 0.2 | ~85% | ~60% | Good cost/performance for simple |

*Results based on informal testing, not rigorous benchmarks. Contributions welcome.*

---

## Prompt Engineering Findings

### What works:
- JSON schema output constraints (massive improvement)
- Explicit coordinate system specification in every prompt
- "Confirm current state before proceeding" instruction
- Numbered step plans over prose instructions

### What doesn't work:
- Long prose prompts for complex geometry
- Asking model to "figure out the best approach"
- Compound operations ("create a box and then fillet all edges")
- Omitting units (model assumes, often wrong)

---

## Open Questions

- Can a small model be fine-tuned on FreeCAD Python scripts to outperform general LLMs?
- What's the minimum state representation needed for reliable complex geometry?
- Can a planner-executor-validator multi-agent setup reduce human intervention to near zero?
