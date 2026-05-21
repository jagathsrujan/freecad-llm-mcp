from typing import Optional
from .freecad_client import FreeCADClient


class ToolWrappers:
    def __init__(self, client: FreeCADClient):
        self._client = client

    def create_sketch(self, plane: str = "XY") -> dict:
        script = f"""
import FreeCAD as App
import Sketcher
doc = App.ActiveDocument
body = doc.addObject("PartDesign::Body", "Body")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
sketch.Support = (doc.getObject("XY_Plane"), [""])
sketch.MapMode = "FlatFace"
doc.recompute()
"""
        return self._client.execute_script(script)

    def create_pad(self, sketch_name: str, length_mm: float) -> dict:
        script = f"""
doc = App.ActiveDocument
sketch = doc.getObject("{sketch_name}")
pad = doc.addObject("PartDesign::Pad", "Pad")
pad.Profile = sketch
pad.Length = {length_mm}
pad.Length2 = 0.0
doc.recompute()
"""
        return self._client.execute_script(script)

    def create_pocket(self, sketch_name: str, depth_mm: Optional[float] = None, through_all: bool = False) -> dict:
        if through_all:
            depth_param = "ThroughAll"
        else:
            depth_param = str(depth_mm)

        script = f"""
doc = App.ActiveDocument
sketch = doc.getObject("{sketch_name}")
pocket = doc.addObject("PartDesign::Pocket", "Pocket")
pocket.Profile = sketch
pocket.Length = {depth_param}
doc.recompute()
"""
        return self._client.execute_script(script)

    def create_fillet(self, edge_selection: list[str], radius_mm: float) -> dict:
        script = f"""
doc = App.ActiveDocument
fillet = doc.addObject("PartDesign::Fillet", "Fillet")
fillet.Base = (doc.ActiveObject, ["Edge1"])
fillet.Radius = {radius_mm}
doc.recompute()
"""
        return self._client.execute_script(script)

    def boolean_cut(self, base_name: str, tool_name: str) -> dict:
        script = f"""
doc = App.ActiveDocument
base = doc.getObject("{base_name}")
tool = doc.getObject("{tool_name}")
cut = doc.addObject("Part::Cut", "Cut")
cut.Base = base
cut.Tool = tool
doc.recompute()
"""
        return self._client.execute_script(script)
