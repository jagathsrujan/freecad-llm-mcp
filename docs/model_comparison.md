# Model Comparison for FreeCAD CAD Execution

## Evaluation Criteria

- Schema adherence (does output match required JSON schema)
- Script validity (does generated FreeCAD Python run without errors)
- Geometric accuracy (does result match intent)
- Cost per operation
- Latency

## Models Tested

### Claude Sonnet 4.6
- Best geometric reasoning
- Highest schema adherence
- Most expensive
- Recommended: prompt design, complex debugging, one-off templates

### Claude Haiku 4.5
- Good schema adherence with strong system prompt
- 10x cheaper than Sonnet
- Recommended: simple geometry execution, high-volume runs

### DeepSeek V3 (low temp)
- Competitive with Haiku at low temperature
- Degrades significantly above temp 0.3
- Recommended: execution layer when cost is primary concern

## Recommendation by Use Case

| Use Case | Recommended Model | Temp |
|---|---|---|
| Template/prompt design | Sonnet 4.6 | 0.4 |
| Simple geometry execution | Haiku 4.5 | 0.2 |
| Complex geometry execution | Sonnet 4.6 or DeepSeek @ 0.1 | 0.1 |
| Debugging | Sonnet 4.6 | 0.3 |
| High-volume batch | DeepSeek V3 | 0.15 |
