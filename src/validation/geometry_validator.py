from ..utils.logger import get_logger

logger = get_logger(__name__)


class GeometryValidator:
    def __init__(self, min_wall_thickness: float = 1.0, dimension_sanity_max: float = 5000.0):
        self.min_wall_thickness = min_wall_thickness
        self.dimension_sanity_max = dimension_sanity_max

    def validate(self, state: dict) -> tuple[bool, list[str]]:
        errors = []

        errors.extend(self._check_dimension_sanity(state))
        errors.extend(self._check_feature_tree(state))

        if errors:
            logger.warning(f"Geometry validation failed: {errors}")
            return False, errors

        return True, []

    def _check_dimension_sanity(self, state: dict) -> list[str]:
        errors = []
        dims = state.get("committed_dimensions", {})
        for key, value in dims.items():
            if isinstance(value, (int, float)):
                if value > self.dimension_sanity_max:
                    errors.append(f"Dimension {key}={value}mm exceeds max {self.dimension_sanity_max}mm")
                if value < 0:
                    errors.append(f"Dimension {key}={value}mm is negative")
        return errors

    def _check_feature_tree(self, state: dict) -> list[str]:
        errors = []
        tree = state.get("feature_tree", [])
        if not isinstance(tree, list):
            errors.append("Feature tree is not a list")
        return errors
