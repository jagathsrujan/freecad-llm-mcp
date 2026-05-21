# Bracket Example — Worked Prompt

## Goal
Create a simple L-bracket with two mounting holes.

## Execution Plan

### Step 1: Base Sketch
Create a rectangle on XY plane: 80mm x 60mm

### Step 2: Pad
Extrude 10mm in Z direction

### Step 3: Vertical Leg Sketch
Sketch on top face: 60mm x 50mm rectangle, offset from edge by 10mm

### Step 4: Pad
Extrude vertical leg 40mm in Z direction

### Step 5: Hole Sketch
Sketch on top of vertical leg: two circles, 6mm diameter, 20mm apart

### Step 6: Pocket
Through-all pocket for mounting holes

## State Queries
- After Step 2: verify body exists, check dimensions
- After Step 4: verify L-shape formed
- After Step 6: verify holes present

## Validation
- Minimum wall thickness: 10mm (OK if > 1mm)
- No interference (single body)
- Holes fully through
