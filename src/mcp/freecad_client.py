from typing import Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FreeCADClient:
    def __init__(self, server_url: Optional[str] = None, timeout: int = 30):
        self.server_url = server_url or "localhost:PORT"
        self.timeout = timeout

    def execute_script(self, script: str) -> dict:
        logger.info(f"Executing FreeCAD script ({len(script)} chars)")
        try:
            result = self._send_command("execute", {"script": script})
            return result
        except Exception as e:
            logger.error(f"MCP execute failed: {e}")
            return {"success": False, "error": str(e)}

    def query_state(self) -> dict:
        try:
            result = self._send_command("get_state", {})
            return result
        except Exception as e:
            logger.error(f"MCP state query failed: {e}")
            return {"success": False, "error": str(e)}

    def _send_command(self, method: str, params: dict) -> dict:
        import requests

        url = f"http://{self.server_url}/{method}"
        response = requests.post(url, json=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
