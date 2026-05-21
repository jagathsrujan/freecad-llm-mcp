"""
Complex Housing — Expected FreeCAD Python Script
Generated manually as ground truth
"""

import FreeCAD as App
import Part

doc = App.newDocument("Housing")

# Step 1: Base sketch
sketch1 = doc.addObject("Sketcher::SketchObject", "BaseSketch")
sketch1.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation())
sketch1.addGeometry(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(100, 0, 0)))
sketch1.addGeometry(Part.LineSegment(App.Vector(100, 0, 0), App.Vector(100, 80, 0)))
sketch1.addGeometry(Part.LineSegment(App.Vector(100, 80, 0), App.Vector(0, 80, 0)))
sketch1.addGeometry(Part.LineSegment(App.Vector(0, 80, 0), App.Vector(0, 0, 0)))

# Step 2: Pad outer shell
pad1 = doc.addObject("PartDesign::Pad", "OuterShell")
pad1.Profile = sketch1
pad1.Length = 60.0

doc.recompute()
