# Prompt Engineering Guide for FreeCAD LLM Pipelines

## Core Principle

Design prompts for **determinism, not flexibility**. CAD has ground truth. The LLM's job is to translate intent into precise operations, not to be creative.

---

## System Prompt Structure

Every execution call must include:

1. **Role definition** — what the model is doing
2. **Current FreeCAD state** — injected by state_manager
3. **Operation to perform** — single, atomic
4. **Output schema** — strict JSON only
5. **Constraints** — units, coordinate system, tolerances

### Template

```
You are a FreeCAD Python API executor. You translate a single CAD operation into a valid FreeCAD Python script.

## Current State
{state_manager_output}

## Operation
{single_operation_description}

## Output Requirements
Return ONLY a JSON object with this exact schema:
{
  "freecad_script": "string — valid FreeCAD Python code",
  "expected_result": "string — what this operation should produce",
  "validation_checks": ["array of strings — what to verify after execution"]
}

## Constraints
- Units: millimeters
- Coordinate system: FreeCAD default (X right, Y up, Z toward viewer)
- Tolerance: ±0.01mm
- Do not include import statements — assume FreeCAD environment is active
- Do not chain multiple operations
```

---

## Temperature Settings

| Task | Model | Temperature |
|---|---|---|
| Prompt template design | Sonnet | 0.4-0.6 |
| Execution plan generation | Sonnet/DeepSeek | 0.2 |
| FreeCAD script execution | DeepSeek/Haiku | 0.1-0.2 |
| Debugging/error analysis | Sonnet | 0.3 |

---

## Complexity Handling

### Simple geometry (single body, < 5 features)
- Single prompt with full operation list
- State query once at end
- Validation at end

### Complex geometry (multi-body, > 5 features, assemblies)
- Break into sub-assemblies
- Validate each sub-assembly independently
- Explicit state query after every 2-3 operations
- Never pass the full feature tree in one prompt — summarize it
