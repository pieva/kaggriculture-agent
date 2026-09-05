from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "docs/model_specs/codex/e18/tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from e18_18_capacity_trajectory_planner import CapacityTrajectoryPlanner
from e18_25_d10_labor_step_controller import (
    D10LaborStepController,
    load_candidate_config,
)

PARENT_HASH = "844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1"
PARENT_PLAN = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_V1.json"
)
CANDIDATE_PLAN = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_25_770_D10_LABOR_STEP_PLAN_V1.json"
)
RESULT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_25_770_D10_LABOR_STEP_PRE_GATE_V1.json"
)


@pytest.fixture(scope="module")
def plans():
    return (
        json.loads(PARENT_PLAN.read_text(encoding="utf-8")),
        json.loads(CANDIDATE_PLAN.read_text(encoding="utf-8")),
    )


def _productive_counts(day):
    excluded = {"NORTH", "SOUTH", "EAST", "WEST", "PASS"}
    return {
        opcode: count
        for opcode, count in day["action_counts"].items()
        if opcode not in excluded
    }


def test_d10_labor_step_is_the_only_daily_action_change(plans):
    parent, candidate = plans
    assert parent["plan_sha256"] == PARENT_HASH
    assert candidate["plan_sha256"] != PARENT_HASH
    assert parent["daily"][9]["planned_hands"] == 6
    assert candidate["daily"][9]["planned_hands"] == 11
    assert candidate["daily"][9]["active_units"] == 12
    assert _productive_counts(candidate["daily"][9]) == _productive_counts(
        parent["daily"][9]
    )
    assert candidate["snapshots"] == parent["snapshots"]
    assert candidate["gate_0a_passed"] is True


def test_candidate_controller_reuses_e18_22_policy(plans):
    _, candidate = plans
    controller = D10LaborStepController(candidate, seat=1)
    assert controller.seat == 1
    assert controller.daily_hands[10] == 11


def test_matched_parent_delta_passes_both_seats():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["causal_delta_passed"] is True
    assert result["matched_parent_baseline"]["delta_by_seat"] == {
        "0": 184.0,
        "1": 184.0,
    }
    assert result["incumbent_gate_passed"] is False


def test_invalid_minimum_hands_is_rejected():
    config = load_candidate_config()
    config["minimum_hands_by_day"] = {"1": 13}
    with pytest.raises(ValueError, match="minimum_hands_by_day"):
        CapacityTrajectoryPlanner(config).build()
