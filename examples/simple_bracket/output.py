"""
Simple Bracket — Expected FreeCAD Python Script
Generated manually as ground truth
"""

import FreeCAD as App
import Part

doc = App.newDocument("Bracket")

# Step 1: Base sketch
sketch1 = doc.addObject("Sketcher::SketchObject", "BaseSketch")
sketch1.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation())
sketch1.addGeometry(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(80, 0, 0)))
sketch1.addGeometry(Part.LineSegment(App.Vector(80, 0, 0), App.Vector(80, 60, 0)))
sketch1.addGeometry(Part.LineSegment(App.Vector(80, 60, 0), App.Vector(0, 60, 0)))
sketch1.addGeometry(Part.LineSegment(App.Vector(0, 60, 0), App.Vector(0, 0, 0)))

# Step 2: Pad
pad1 = doc.addObject("PartDesign::Pad", "BasePad")
pad1.Profile = sketch1
pad1.Length = 10.0
pad1.Length2 = 0.0

doc.recompute()
