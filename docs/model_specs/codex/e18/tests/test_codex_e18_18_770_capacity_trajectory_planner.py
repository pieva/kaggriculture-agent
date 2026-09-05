from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "docs/model_specs/codex/e18/tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from e18_18_capacity_trajectory_planner import build_plan, load_config

GATE_0B_ARTIFACT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0B_V1.json"
)


@pytest.fixture(scope="module")
def plan():
    return build_plan()


def test_frozen_invariants_and_gate_0a(plan):
    config = load_config()
    assert config["topology"] == "7-7-0"
    assert config["livestock_mix"] == {"COW": 9, "SHEEP": 5}
    assert plan["gate_0a_passed"] is True
    assert all(plan["gate_0a_checks"].values())
    assert plan["executor_authorized"] is False
    assert plan["gate_0b_passed"] is False


def test_composition_output_and_terminal_cutoff(plan):
    assert plan["snapshots"]["D10"]["crop_total"] == 37
    assert plan["snapshots"]["D15"]["crop_total"] == 61
    assert plan["snapshots"]["D25"]["crops"] == {
        "STRAWBERRY": 22,
        "WHEAT": 39,
    }
    assert plan["snapshots"]["D30"]["crop_total"] <= 2
    assert plan["totals"]["shadow_crop_output"] >= 885
    assert plan["totals"]["minimum_daily_slack_ratio"] >= 0.01
    assert plan["totals"]["action_counts"]["DROP"] > 0


def test_plan_hash_is_deterministic(plan):
    repeated = build_plan()
    assert repeated["plan_sha256"] == plan["plan_sha256"]
    assert repeated["snapshots"] == plan["snapshots"]
    assert repeated["totals"] == plan["totals"]


def test_d7_wool_sale_precedes_northeast_planting(plan):
    day_seven = [row for row in plan["trajectory"] if row["day"] == 7]
    wool_drop_turns = [
        row["turn"]
        for row in day_seven
        if row["opcode"] == "DROP"
        and row["arguments"].get("expected_items", {}).get("SHEEP", 0) > 0
    ]
    northeast_plant_turns = [
        row["turn"]
        for row in day_seven
        if row["opcode"] == "PLANT" and row["position"][0] >= 5
    ]
    daily = next(row for row in plan["daily"] if row["day"] == 7)
    assert len(wool_drop_turns) == 2
    assert northeast_plant_turns
    assert max(wool_drop_turns) < min(northeast_plant_turns)
    assert daily["planned_hands"] == 12


def test_gate_0b_exact_engine_artifact_is_reproducible():
    payload = json.loads(GATE_0B_ARTIFACT.read_text(encoding="utf-8"))
    assert payload["gate_0b_passed"] is True
    assert payload["policy_build_authorized"] is True
    assert payload["executor_authorized"] is False
    assert all(payload["gate_0b_checks"].values())
    assert payload["determinism"]["passed"] is True
    assert payload["final"]["topology"] == {"Q0": 7, "Q1": 7}
    assert payload["final"]["animals"] == {"COW": 9, "SHEEP": 5}
    assert payload["final"]["shed_units"] == 0
