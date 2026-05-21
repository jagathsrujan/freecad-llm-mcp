import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp.freecad_client import FreeCADClient
from mcp.tool_wrappers import ToolWrappers


class TestFreeCADClient:
    def setup_method(self):
        self.client = FreeCADClient(server_url="localhost:9999", timeout=1)

    def test_execute_script_handles_connection_error(self):
        result = self.client.execute_script("doc = App.ActiveDocument")
        assert result["success"] is False
        assert "error" in result

    def test_query_state_handles_connection_error(self):
        result = self.client.query_state()
        assert result["success"] is False


class TestToolWrappers:
    def setup_method(self):
        self.client = FreeCADClient(server_url="localhost:9999", timeout=1)
        self.wrappers = ToolWrappers(self.client)

    def test_create_sketch_produces_script(self):
        result = self.wrappers.create_sketch()
        assert result["success"] is False
