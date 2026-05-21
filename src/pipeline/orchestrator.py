import yaml
import json
from pathlib import Path
from .state_manager import StateManager
from .step_executor import StepExecutor
from ..validation.geometry_validator import GeometryValidator
from ..validation.schema_validator import SchemaValidator
from ..mcp.freecad_client import FreeCADClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


class Orchestrator:
    def __init__(self, config_path: str = "configs/pipeline.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.state_manager = StateManager()
        self.executor = StepExecutor()
        self.geometry_validator = GeometryValidator()
        self.schema_validator = SchemaValidator()
        self.mcp_client = FreeCADClient()
        self.consecutive_failures = 0

    def run(self, execution_plan: list[dict]) -> dict:
        results = []

        for i, step in enumerate(execution_plan):
            logger.info(f"Executing step {i+1}/{len(execution_plan)}: {step.get('operation_type')}")

            result = self._execute_step(step, step_index=i)
            results.append(result)

            if not result["success"]:
                self.consecutive_failures += 1
                if self.consecutive_failures >= self.config["pipeline"]["max_consecutive_failures"]:
                    logger.error("Max consecutive failures reached. Halting pipeline.")
                    self._dump_state(step_index=i)
                    break
            else:
                self.consecutive_failures = 0

            if i % self.config["pipeline"]["state_query_interval"] == 0:
                self.state_manager.refresh(self.mcp_client)

        return {"steps_executed": len(results), "results": results}

    def _execute_step(self, step: dict, step_index: int) -> dict:
        current_state = self.state_manager.get_current_state()

        for attempt in range(self.config["pipeline"].get("max_retries", 2) + 1):
            llm_output = self.executor.execute(step, current_state)

            if not self.schema_validator.validate(llm_output):
                logger.warning(f"Schema validation failed on attempt {attempt+1}")
                continue

            mcp_result = self.mcp_client.execute_script(llm_output["freecad_script"])

            if not mcp_result["success"]:
                logger.warning(f"MCP execution failed on attempt {attempt+1}: {mcp_result.get('error')}")
                continue

            self.state_manager.refresh(self.mcp_client)

            geo_valid, geo_errors = self.geometry_validator.validate(self.state_manager.get_current_state())
            if not geo_valid:
                logger.warning(f"Geometry validation failed: {geo_errors}")
                continue

            return {"success": True, "step": step, "mcp_result": mcp_result}

        return {"success": False, "step": step, "error": "Max retries exceeded"}

    def _dump_state(self, step_index: int):
        dump_path = Path(self.config["output"]["snapshot_dir"]) / f"failure_dump_step_{step_index}.json"
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dump_path, "w") as f:
            json.dump(self.state_manager.get_current_state(), f, indent=2)
        logger.info(f"State dumped to {dump_path}")
