from ..utils.logger import get_logger

logger = get_logger(__name__)


class ConstraintChecker:
    def __init__(self):
        self._constraints = []

    def check_sketch_constraints(self, sketch_data: dict) -> tuple[bool, list[str]]:
        issues = []
        constraints = sketch_data.get("constraints", [])
        geometry = sketch_data.get("geometry", [])

        if not geometry:
            issues.append("Sketch has no geometry elements")

        if len(constraints) < self._min_constraints_needed(geometry):
            issues.append("Sketch is not fully constrained")

        if issues:
            logger.warning(f"Constraint check failed: {issues}")
            return False, issues

        return True, []

    def check_body_validity(self, body_data: dict) -> tuple[bool, list[str]]:
        issues = []
        features = body_data.get("features", [])

        if not features:
            issues.append("Body has no features")

        for feature in features:
            if feature.get("type") in ("pad", "pocket"):
                sketch = feature.get("sketch")
                if sketch and not sketch.get("fully_constrained", True):
                    issues.append(f"Feature '{feature.get('name')}' uses unconstrained sketch")

        return (len(issues) == 0, issues)

    @staticmethod
    def _min_constraints_needed(geometry: list) -> int:
        count = 0
        for element in geometry:
            if element.get("type") == "line":
                count += 2
            elif element.get("type") == "circle":
                count += 3
            elif element.get("type") == "arc":
                count += 5
            elif element.get("type") == "rectangle":
                count += 4
        return count
