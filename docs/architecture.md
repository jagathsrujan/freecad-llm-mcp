# System Architecture

## Overview

```
User Prompt
    │
    ▼
[Prompt Engineer — Sonnet / Human]
    │  Generates structured execution plan (JSON)
    ▼
[Orchestrator — orchestrator.py]
    │  Splits plan into atomic steps
    ▼
[Step Executor — step_executor.py]
    │  Sends one step to Execution LLM (low temp)
    ▼
[Schema Validator — schema_validator.py]
    │  Rejects malformed output before MCP call
    ▼
[FreeCAD MCP Client — freecad_client.py]
    │  Executes tool call
    ▼
[State Manager — state_manager.py]
    │  Queries FreeCAD state post-operation
    ▼
[Geometry Validator — geometry_validator.py]
    │  Checks physical validity
    ▼
[Next Step or Error Recovery]
```

## Why Atomic Steps

Complex geometry fails because errors compound. Step 3's bad dimension breaks steps 4-10. Atomic execution with state validation between steps catches errors early and cheaply.

## State Management

FreeCAD MCP is stateless per call. The `state_manager.py` maintains a local representation of:
- Current feature tree
- Active sketch constraints
- Body/Part hierarchy
- Last committed dimensions

This is injected into every LLM call as context.

## Error Recovery Strategy

1. Geometry validator fails -> retry step with corrected constraints
2. Schema validator fails -> re-prompt execution model with error context
3. MCP call fails -> log, skip, flag for human review
4. 3 consecutive failures -> halt pipeline, dump state for debugging
