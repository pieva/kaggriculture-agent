"""Configuration contract only: not tests of an implemented E18.33 agent."""
import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

CONFIG = Path(__file__).resolve().parents[1] / "configs"
NAME = "CODEX_E18_33_COMMON_RESOURCE_POLICY_V1"
PROFILE = json.loads((CONFIG / f"{NAME}.json").read_text())
SCHEMA = json.loads((CONFIG / f"{NAME}.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)


def test_schema_and_current_profile():
    Draft202012Validator.check_schema(SCHEMA)
    VALIDATOR.validate(PROFILE)
    assert PROFILE["pastures"] == {"target": 14, "uniform_capacity_per_quadrant": 7}
    assert PROFILE["maximum_hands"] == 12
    bootstrap_schema = json.loads((CONFIG / "CODEX_E18_33_COMMON_RESOURCE_POLICY_V2.schema.json").read_text())
    Draft202012Validator.check_schema(bootstrap_schema)
    bootstrap_validator = Draft202012Validator(bootstrap_schema)
    for suffix in ("V2_BOOTSTRAP", "V3_AUTONOMY"):
        profile = json.loads((CONFIG / f"CODEX_E18_33_COMMON_RESOURCE_POLICY_{suffix}.json").read_text())
        bootstrap_validator.validate(profile)
        for key in ("activation_day", "Q0", "coordinates", "calendar"):
            contaminated = deepcopy(profile)
            contaminated["bootstrap"][key] = 1
            with pytest.raises(ValidationError):
                bootstrap_validator.validate(contaminated)


def test_target_fifteen_changes_only_one_setting():
    alternate = deepcopy(PROFILE)
    alternate["pastures"]["target"] = 15
    VALIDATOR.validate(alternate)
    # Schema acceptance is not proof that an engine agent builds the pasture.
    assert set(alternate) == set(PROFILE)


@pytest.mark.parametrize("key", [
    "trajectory", "calendar", "reference_plan", "parent_config", "treatment_config",
    "pasture_targets", "late_q0_pasture", "late_q0_pasture_day", "q2_plant_day",
    "minimum_hands_by_day", "animal_care_blackout_days", "skip_water_cells_by_day",
    "jesse_d10_action_targets", "crop_checkpoints", "animal_checkpoints", "seed",
    "opponent", "quadrant_policies", "livestock_resource_cap", "Q0", "Q1", "Q2",
])
def test_legacy_or_duplicated_configuration_is_rejected(key):
    contaminated = deepcopy(PROFILE)
    contaminated[key] = {}
    with pytest.raises(ValidationError):
        VALIDATOR.validate(contaminated)


@pytest.mark.parametrize("key,value", [
    ("coordinates", [[3, 4]]), ("activation_day", 14), ("Q0", 7), ("Q1", 7),
    ("Q2", 0), ("target", -1), ("target", True), ("uniform_capacity_per_quadrant", 0),
])
def test_nested_pasture_policy_has_no_calendar_or_overrides(key, value):
    contaminated = deepcopy(PROFILE)
    contaminated["pastures"][key] = value
    with pytest.raises(ValidationError):
        VALIDATOR.validate(contaminated)


def test_full_frozen_plan_is_not_a_valid_policy_profile():
    path = CONFIG.parent / "artifacts/derived/E18_28_FULL_SEASON_C_PLAN_V1.json"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(json.loads(path.read_text()))


def test_no_per_quadrant_crop_override():
    contaminated = deepcopy(PROFILE)
    contaminated["allowed_crops"] = {"Q0": ["MELON"], "Q1": ["STRAWBERRY"]}
    with pytest.raises(ValidationError):
        VALIDATOR.validate(contaminated)
