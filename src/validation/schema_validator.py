import json
from ..utils.logger import get_logger

logger = get_logger(__name__)

REQUIRED_FIELDS = ["freecad_script", "operation_type", "expected_result", "validation_checks"]
VALID_OPERATION_TYPES = ["sketch", "pad", "pocket", "fillet", "chamfer", "boolean", "constraint", "other"]


class SchemaValidator:
    def validate(self, llm_output) -> bool:
        if isinstance(llm_output, str):
            try:
                llm_output = json.loads(llm_output.strip().removeprefix("```json").removesuffix("```"))
            except json.JSONDecodeError:
                logger.error("LLM output is not valid JSON")
                return False

        for field in REQUIRED_FIELDS:
            if field not in llm_output:
                logger.error(f"Missing required field: {field}")
                return False

        if llm_output.get("operation_type") not in VALID_OPERATION_TYPES:
            logger.error(f"Invalid operation_type: {llm_output.get('operation_type')}")
            return False

        if not isinstance(llm_output.get("freecad_script"), str) or len(llm_output["freecad_script"]) < 5:
            logger.error("freecad_script is empty or invalid")
            return False

        return True
