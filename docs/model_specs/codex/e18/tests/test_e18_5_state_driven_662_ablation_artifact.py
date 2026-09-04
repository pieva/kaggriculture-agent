"""Integrity checks for the completed E18.5 6-6-2 ablation artifact."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ARTIFACT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1.json"
)
CANDIDATE = "CODEX_E18_5_STATE_DRIVEN_662"


def _payload() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def _candidate_rows(payload: dict) -> list[dict]:
    return [
        match[f"p{seat}_metrics"]
        for match in payload["matches"]
        for seat in (0, 1)
        if match[f"p{seat}"] == CANDIDATE
    ]


def test_ablation_uses_the_frozen_comparable_development_sample() -> None:
    payload = _payload()
    reference = payload["frozen_772_reference"]
    assert payload["match_count"] == 14
    assert len(payload["seeds"]) == 7
    assert payload["seats"] == [0, 1]
    assert reference["same_development_seeds"] is True
    assert reference["same_seats"] is True
    assert reference["common_opponent"] == "CODEX_E18_2_CONTROL"
    assert payload["holdout_consumed"] is False
    assert payload["final_confirmation_consumed"] is False
    assert payload["kaggle_upload_authorized"] is False


def test_candidate_reaches_exact_filled_662_without_integrity_violations() -> None:
    payload = _payload()
    rows = _candidate_rows(payload)
    assert len(rows) == 14
    assert all(
        row["final_pastures_by_quadrant"] == {"Q0": 6, "Q1": 6, "Q2": 2}
        for row in rows
    )
    assert all(row["final_empty_target_pastures"] == 0 for row in rows)
    assert sum(row["pass_on_actionable_violations"] for row in rows) == 0
    assert sum(row["route_thrashing_violations"] for row in rows) == 0
    assert sum(row["technical_errors"] for row in rows) == 0
    assert sum(row["fallbacks"] for row in rows) == 0
    assert sum(row["verified_livestock_losses"] for row in rows) == 0


def test_efficiency_gate_is_internally_consistent() -> None:
    payload = _payload()
    gate = payload["efficiency_gate"]
    candidate = payload["standings"][CANDIDATE]
    reference = payload["frozen_772_reference"]["standings"]
    candidate_ratio = (
        candidate["move_actions_mean"] / candidate["productive_actions_mean"]
    )
    reference_ratio = (
        reference["move_actions_mean"] / reference["productive_actions_mean"]
    )
    assert gate["candidate_move_per_productive"] == candidate_ratio
    assert gate["control_move_per_productive"] == reference_ratio
    assert gate["checks"]["move_actions_at_least_5pct_lower"] == (
        candidate["move_actions_mean"] <= reference["move_actions_mean"] * 0.95
    )
    assert gate["checks"]["move_per_productive_at_least_5pct_lower"] == (
        candidate_ratio <= reference_ratio * 0.95
    )
    assert gate["checks"]["productive_actions_at_least_90pct_control"] == (
        candidate["productive_actions_mean"]
        >= reference["productive_actions_mean"] * 0.90
    )
    assert gate["passed"] == all(gate["checks"].values())


def test_only_the_preregistered_five_percent_efficiency_checks_fail() -> None:
    gate = _payload()["efficiency_gate"]
    assert gate["passed"] is False
    assert {
        name for name, passed in gate["checks"].items() if not passed
    } == {
        "move_actions_at_least_5pct_lower",
        "move_per_productive_at_least_5pct_lower",
    }
