from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller import (
    JesseBoostD10Controller,
    load_candidate_config,
)

PLAN = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/E18_26_770_JESSE_BOOST_D10_PLAN_V1.json"
)
RESULT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/E18_26_770_JESSE_BOOST_D10_GATE_V1.json"
)
PLAN_HASH = "3a733b29e137a64092087394883f0ef7fa1d4c81c17ba5bfb8e47139a9ba9de7"


def _phase_counts(plan: dict) -> Counter[str]:
    counts = Counter(
        str(row["opcode"]) for row in plan["trajectory"] if int(row["day"]) <= 10
    )
    counts["MOVE"] = sum(
        counts.pop(direction, 0) for direction in ("NORTH", "SOUTH", "EAST", "WEST")
    )
    return counts


def test_candidate_locks_topology_and_boost_treatment():
    config = load_candidate_config()
    assert config["topology"] == "7-7-0"
    assert config["livestock_resource_cap"] == 14
    assert config["livestock_mix"] == {"COW": 9, "SHEEP": 5}
    assert config["d10_wheat_fast_cycle_days"] == [3, 5, 7, 9]
    assert config["d7_reuse_unlock_workers"] is True
    assert config["d13_fertilizer_payroll_bridge"] is True


def test_plan_matches_the_identified_jesse_d10_core():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    counts = _phase_counts(plan)
    assert plan["plan_sha256"] == PLAN_HASH
    assert plan["gate_0a_passed"] is True
    assert counts["PLANT"] == 63
    assert counts["WATER"] == 254
    assert counts["HARVEST"] == 30
    assert counts["MOVE"] == 529
    assert plan["snapshots"]["D10"]["crops"] == {
        "MELON": 12,
        "STRAWBERRY": 20,
        "WHEAT": 5,
    }
    assert plan["daily"][6]["active_units"] == 10
    assert plan["daily"][9]["active_units"] == 12
    assert plan["daily"][11]["planned_hands"] == 8
    assert plan["daily"][12]["planned_hands"] == 11
    assert plan["totals"]["shadow_crop_output"] == 885


def test_controller_binds_the_generated_plan():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    controller = JesseBoostD10Controller(plan, seat=1)
    assert controller.seat == 1
    assert controller.daily_hands[10] == 11
    assert controller.daily_hands[13] == 11


def test_internal_gate_records_gain_and_remaining_blockers():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["matched_parent_baseline"]["delta_by_seat"] == {
        "0": 2198.0,
        "1": 2080.0,
    }
    assert result["checks"]["jesse_plant_exact"] is True
    assert result["checks"]["jesse_water_exact"] is True
    assert result["checks"]["d10_actual_hands_11"] is True
    assert result["checks"]["actual_crop_checkpoints_match_jesse"] is False
    assert result["checks"]["candidate_exact_9_cow_5_sheep"] is False
    assert result["causal_delta_passed"] is False
    assert result["full_gate_1_authorized"] is False
    assert result["kaggle_upload_authorized"] is False
