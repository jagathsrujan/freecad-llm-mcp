import json
from typing import Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


class StepExecutor:
    def __init__(self, llm_client=None):
        self._llm_client = llm_client

    def execute(self, step: dict, state: Optional[dict] = None) -> dict:
        prompt = self._build_prompt(step, state)

        if self._llm_client:
            response = self._llm_client.complete(prompt)
            return self._parse_response(response)
        else:
            logger.warning("No LLM client configured, returning step as-is")
            return {
                "freecad_script": step.get("freecad_script", ""),
                "operation_type": step.get("operation_type", "unknown"),
                "expected_result": step.get("description", ""),
                "validation_checks": [],
            }

    def _build_prompt(self, step: dict, state: Optional[dict] = None) -> str:
        state_context = json.dumps(state, indent=2) if state else "No state available"
        return f"""
You are a FreeCAD Python API executor.

Current State:
{state_context}

Operation:
{step.get('description', step.get('operation_type', 'unknown operation'))}

Output ONLY valid JSON with: freecad_script, operation_type, expected_result, validation_checks
"""

    def _parse_response(self, response: str) -> dict:
        try:
            cleaned = response.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(cleaned)
        except (json.JSONDecodeError, AttributeError):
            logger.error("Failed to parse LLM response as JSON")
            return {}
