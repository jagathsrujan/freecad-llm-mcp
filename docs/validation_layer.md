# Validation Layer Design

## Purpose

Catch physically invalid geometry before it propagates through the pipeline.

## Validation Checks (Implemented)

- [ ] Minimum wall thickness (default: 1.0mm)
- [ ] Body interference detection
- [ ] Open shell detection (non-watertight bodies)
- [ ] Dimension range sanity (catches unit errors — e.g., 1000mm when 10mm intended)
- [ ] Sketch constraint completeness (fully constrained before pad/pocket)

## Validation Checks (Planned)

- [ ] FDM printability (overhang angle > 45 deg)
- [ ] Stress concentration indicators (sharp internal corners)
- [ ] Assembly mate feasibility
- [ ] GD&T tolerance stack analysis

## Integration Point

Validator runs after every MCP tool call returns success. Pipeline does not proceed to next step until validation passes.

## Error Response

On validation failure:
1. Log failure with current state snapshot
2. Retry step with corrected constraints (max 2 retries)
3. On 3rd failure: halt, dump state, flag for human review
