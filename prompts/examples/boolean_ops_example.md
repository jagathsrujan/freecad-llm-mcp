# Boolean Operations Example — Worked Prompt

## Goal
Create a housing with a subtractive cavity using boolean operations.

## Execution Plan

### Step 1: Outer Shell
Create box: 100mm x 80mm x 60mm

### Step 2: Inner Cavity
Create box: 90mm x 70mm x 50mm, centered inside outer shell

### Step 3: Boolean Cut
Subtract inner box from outer shell to create hollowed cavity

### Step 4: Opening
Create sketch on top face: 60mm x 40mm rectangle, centered

### Step 5: Pocket
Pocket through wall (5mm depth) to create access opening

## Validation
- Wall thickness: 5mm all around (OK > 1mm)
- No open shells (cavity is enclosed except opening)
- Boolean cut applied correctly
- Opening dimensions match specification
