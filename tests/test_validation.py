import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from validation.schema_validator import SchemaValidator
from validation.geometry_validator import GeometryValidator
from validation.constraint_checker import ConstraintChecker


class TestSchemaValidator:
    def setup_method(self):
        self.validator = SchemaValidator()

    def test_valid_output_passes(self):
        output = {
            "freecad_script": "doc = App.ActiveDocument",
            "operation_type": "sketch",
            "expected_result": "A new sketch on XY plane",
            "validation_checks": ["check sketch exists"],
        }
        assert self.validator.validate(output) is True

    def test_missing_field_fails(self):
        output = {
            "freecad_script": "doc = App.ActiveDocument",
            "operation_type": "sketch",
        }
        assert self.validator.validate(output) is False

    def test_invalid_operation_type_fails(self):
        output = {
            "freecad_script": "doc = App.ActiveDocument",
            "operation_type": "invalid_op",
            "expected_result": "test",
            "validation_checks": [],
        }
        assert self.validator.validate(output) is False

    def test_empty_script_fails(self):
        output = {
            "freecad_script": "",
            "operation_type": "sketch",
            "expected_result": "test",
            "validation_checks": [],
        }
        assert self.validator.validate(output) is False

    def test_json_string_input(self):
        json_str = json.dumps({
            "freecad_script": "doc = App.ActiveDocument",
            "operation_type": "pad",
            "expected_result": "extruded solid",
            "validation_checks": ["check body"],
        })
        assert self.validator.validate(json_str) is True


class TestGeometryValidator:
    def setup_method(self):
        self.validator = GeometryValidator()

    def test_valid_state_passes(self):
        state = {
            "feature_tree": ["Feature1", "Feature2"],
            "committed_dimensions": {"width": 100, "height": 50},
        }
        valid, errors = self.validator.validate(state)
        assert valid is True
        assert errors == []

    def test_excessive_dimension_fails(self):
        state = {
            "feature_tree": ["Feature1"],
            "committed_dimensions": {"length": 10000},
        }
        valid, errors = self.validator.validate(state)
        assert valid is False
        assert any("exceeds max" in e for e in errors)

    def test_negative_dimension_fails(self):
        state = {
            "feature_tree": ["Feature1"],
            "committed_dimensions": {"depth": -5},
        }
        valid, errors = self.validator.validate(state)
        assert valid is False
        assert any("negative" in e for e in errors)


class TestConstraintChecker:
    def setup_method(self):
        self.checker = ConstraintChecker()

    def test_empty_sketch_fails(self):
        sketch = {"geometry": [], "constraints": []}
        valid, errors = self.checker.check_sketch_constraints(sketch)
        assert valid is False

    def test_fully_constrained_sketch(self):
        sketch = {
            "geometry": [{"type": "line"}, {"type": "line"}],
            "constraints": ["c1", "c2", "c3", "c4"],
        }
        valid, errors = self.checker.check_sketch_constraints(sketch)
        assert valid is True
