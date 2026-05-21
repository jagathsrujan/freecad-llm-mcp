import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipeline.state_manager import StateManager
from pipeline.step_executor import StepExecutor
from pipeline.orchestrator import Orchestrator


class TestStateManager:
    def setup_method(self):
        self.manager = StateManager()

    def test_initial_state(self):
        state = self.manager.get_current_state()
        assert state["feature_tree"] == []
        assert state["active_body"] is None

    def test_get_state_as_prompt_context(self):
        context = self.manager.get_state_as_prompt_context()
        assert "active_body" in context
        assert "feature_count" in context

    def test_refresh_handles_failure_gracefully(self):
        class FailingClient:
            def query_state(self):
                raise ConnectionError("MCP not available")

        self.manager.refresh(FailingClient())
        state = self.manager.get_current_state()
        assert state["feature_tree"] == []


class TestStepExecutor:
    def setup_method(self):
        self.executor = StepExecutor()

    def test_execute_without_llm_client(self):
        step = {
            "operation_type": "sketch",
            "freecad_script": "doc = App.ActiveDocument",
            "description": "Create a sketch",
        }
        result = self.executor.execute(step)
        assert result["operation_type"] == "sketch"
        assert result["freecad_script"] == "doc = App.ActiveDocument"
