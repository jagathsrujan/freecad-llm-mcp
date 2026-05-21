import json
from ..utils.logger import get_logger

logger = get_logger(__name__)


class StateManager:
    def __init__(self):
        self._state = {
            "feature_tree": [],
            "active_body": None,
            "active_sketch": None,
            "last_operation": None,
            "committed_dimensions": {}
        }

    def refresh(self, mcp_client):
        try:
            result = mcp_client.query_state()
            if result and result.get("success"):
                self._state.update(result.get("state", {}))
                logger.info("State refreshed from FreeCAD")
            else:
                logger.warning("State refresh returned no data")
        except Exception as e:
            logger.error(f"State refresh failed: {e}")

    def get_current_state(self) -> dict:
        return self._state.copy()

    def get_state_as_prompt_context(self) -> str:
        return json.dumps({
            "active_body": self._state.get("active_body"),
            "feature_count": len(self._state.get("feature_tree", [])),
            "last_features": self._state.get("feature_tree", [])[-3:],
            "last_operation": self._state.get("last_operation")
        }, indent=2)
