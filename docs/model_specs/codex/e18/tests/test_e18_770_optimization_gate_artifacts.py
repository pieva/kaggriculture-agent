"""Integrity and decision tests for topology-matched E18.7-E18.13 gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
ARTIFACTS = ROOT / "docs/model_specs/codex/e18/artifacts/derived"


def _load(name: str) -> dict:
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize(
    "name",
    [
        "E18_7_770_IN_PLACE_CROP_SERVICE_DEV_GATE_V1.json",
        "E18_8_770_ADJACENT_CROP_QUEUE_DEV_GATE_V1.json",
        "E18_9_770_LIVE_CROP_ROTATION_GUARD_DEV_GATE_V1.json",
        "E18_10_V2_770_WATER_BEFORE_DIG_GUARD_DEV_GATE_V1.json",
        "E18_11_770_INVALID_COMMAND_WATER_RECOVERY_DEV_GATE_V1.json",
        "E18_13_770_D20_CRITICAL_FEED_DEADLINE_DEV_GATE_V1.json",
        "E18_16_770_EXACT_CAP_CRITICAL_FEED_DEV_GATE_V1.json",
    ],
)
def test_gate_matrix_is_development_only_exact_770(name: str) -> None:
    payload = _load(name)
    assert payload["match_count"] == 14
    assert len(payload["seeds"]) == 7
    assert payload["seats"] == [0, 1]
    assert payload["holdout_consumed"] is False
    assert payload["final_confirmation_consumed"] is False
    assert payload["kaggle_upload_authorized"] is False
    assert payload["mutation_freeze"]["pasture_topology"] == {
        "Q0": 7,
        "Q1": 7,
        "Q2": 0,
    }
    assert payload["gates"]["exact_candidate_matches"] == 14
    assert payload["gates"]["exact_control_matches"] == 14
    assert payload["gates"]["gate_b_top3_convergence"]["passed"] is False


@pytest.mark.parametrize(
    "name",
    [
        "E18_7_770_IN_PLACE_CROP_SERVICE_DEV_GATE_V1.json",
        "E18_8_770_ADJACENT_CROP_QUEUE_DEV_GATE_V1.json",
        "E18_9_770_LIVE_CROP_ROTATION_GUARD_DEV_GATE_V1.json",
        "E18_10_770_WATER_BEFORE_DIG_GUARD_DEV_GATE_V1.json",
        "E18_10_V2_770_WATER_BEFORE_DIG_GUARD_DEV_GATE_V1.json",
        "E18_11_770_INVALID_COMMAND_WATER_RECOVERY_DEV_GATE_V1.json",
        "E18_13_770_D20_CRITICAL_FEED_DEADLINE_DEV_GATE_V1.json",
        "E18_16_770_EXACT_CAP_CRITICAL_FEED_DEV_GATE_V1.json",
    ],
)
def test_recorded_source_and_config_hashes_are_current(name: str) -> None:
    provenance = _load(name)["provenance"]
    for prefix in ("candidate", "control"):
        for kind in ("source", "config"):
            relative = provenance[f"{prefix}_{kind}"]
            assert provenance[f"{prefix}_{kind}_sha256"].lower() == _sha256(
                ROOT / relative
            )


def test_e18_7_proves_in_place_only_is_mechanically_safe_but_inert() -> None:
    payload = _load("E18_7_770_IN_PLACE_CROP_SERVICE_DEV_GATE_V1.json")
    candidate = payload["standings"]["CODEX_E18_7_770_IN_PLACE_SERVICE"]
    control = payload["standings"]["CODEX_E18_6_770_CONTROL"]
    assert payload["gates"]["gate_a_causal"]["passed"] is False
    assert candidate["pass_actions_mean"] == pytest.approx(
        control["pass_actions_mean"] - 2
    )
    assert candidate["crop_service_actions_mean"] == pytest.approx(
        control["crop_service_actions_mean"] + 2
    )
    assert candidate["harvest_events_total_mean"] == pytest.approx(
        control["harvest_events_total_mean"]
    )
    assert candidate["money_mean"] == pytest.approx(control["money_mean"])


def test_e18_8_rejects_adjacent_overlay_despite_lower_pass() -> None:
    payload = _load("E18_8_770_ADJACENT_CROP_QUEUE_DEV_GATE_V1.json")
    candidate = payload["standings"]["CODEX_E18_8_770_ADJACENT_CROP_QUEUE"]
    control = payload["standings"]["CODEX_E18_6_770_CONTROL"]
    assert payload["gates"]["gate_a_causal"]["passed"] is False
    assert candidate["wins"] == 0
    assert control["wins"] == 14
    assert candidate["pass_actions_mean"] < control["pass_actions_mean"]
    assert candidate["harvest_events_total_mean"] < (
        control["harvest_events_total_mean"] * 0.70
    )
    assert payload["gates"]["mean_matched_money_delta_percent"] < -15


def test_e18_9_is_positive_but_below_preregistered_promotion_gate() -> None:
    payload = _load("E18_9_770_LIVE_CROP_ROTATION_GUARD_DEV_GATE_V1.json")
    candidate = payload["standings"][
        "CODEX_E18_9_770_LIVE_CROP_ROTATION_GUARD"
    ]
    control = payload["standings"]["CODEX_E18_6_770_CONTROL"]
    assert payload["gates"]["gate_a_causal"]["passed"] is False
    assert candidate["wins"] == 10
    assert control["wins"] == 4
    assert candidate["money_mean"] > control["money_mean"]
    assert candidate["crop_tile_days_d21_d30_mean"] > (
        control["crop_tile_days_d21_d30_mean"]
    )
    assert candidate["harvest_events_total_mean"] > (
        control["harvest_events_total_mean"]
    )
    assert candidate["harvested_units_total_mean"] > (
        control["harvested_units_total_mean"]
    )
    assert payload["gates"]["worst_matched_money_delta_percent"] > -1


def test_e18_10_v1_is_invalidated_by_fill_and_livestock_safety() -> None:
    payload = _load("E18_10_770_WATER_BEFORE_DIG_GUARD_DEV_GATE_V1.json")
    candidate = payload["standings"]["CODEX_E18_10_770_WATER_BEFORE_DIG_GUARD"]
    control = payload["standings"][
        "CODEX_E18_9_770_LIVE_CROP_ROTATION_GUARD_CONTROL"
    ]
    assert payload["gates"]["gate_a_causal"]["passed"] is False
    assert payload["gates"]["exact_candidate_matches"] == 0
    assert candidate["verified_livestock_losses"] == 42
    assert control["verified_livestock_losses"] == 14


def test_e18_10_v2_is_safe_positive_but_below_three_volume_thresholds() -> None:
    payload = _load("E18_10_V2_770_WATER_BEFORE_DIG_GUARD_DEV_GATE_V1.json")
    candidate = payload["standings"]["CODEX_E18_10_770_WATER_BEFORE_DIG_GUARD"]
    control = payload["standings"][
        "CODEX_E18_9_770_LIVE_CROP_ROTATION_GUARD_CONTROL"
    ]
    assert payload["gates"]["gate_a_causal"]["passed"] is False
    assert payload["gates"]["exact_candidate_matches"] == 14
    assert candidate["wins"] == 12
    assert control["wins"] == 2
    assert candidate["verified_livestock_losses"] == (
        control["verified_livestock_losses"]
    )
    assert candidate["money_mean"] > control["money_mean"]
    assert candidate["water_actions_mean"] > control["water_actions_mean"]
    assert candidate["dig_actions_mean"] < control["dig_actions_mean"]
    assert candidate["late_unwatered_per_crop_tile_mean"] < (
        control["late_unwatered_per_crop_tile_mean"]
    )
    assert candidate["crop_tile_days_d21_d30_mean"] > (
        control["crop_tile_days_d21_d30_mean"]
    )
    assert candidate["harvest_events_total_mean"] > (
        control["harvest_events_total_mean"]
    )
    failed = {
        key
        for key, value in payload["gates"]["gate_a_causal"]["checks"].items()
        if not value
    }
    assert failed == {
        "crop_service_at_least_1pct_higher",
        "harvested_units_at_least_1pct_higher",
        "pass_at_least_1pct_lower",
    }


def test_e18_11_is_safe_but_only_changes_action_accounting() -> None:
    payload = _load(
        "E18_11_770_INVALID_COMMAND_WATER_RECOVERY_DEV_GATE_V1.json"
    )
    candidate = payload["standings"][
        "CODEX_E18_11_770_INVALID_COMMAND_WATER_RECOVERY"
    ]
    control = payload["standings"]["CODEX_E18_10_V2_770_CONTROL"]
    assert payload["gates"]["gate_a_causal"]["passed"] is False
    assert candidate["water_actions_mean"] > control["water_actions_mean"]
    assert candidate["money_mean"] == pytest.approx(control["money_mean"])
    assert candidate["late_unwatered_per_crop_tile_mean"] == pytest.approx(
        control["late_unwatered_per_crop_tile_mean"]
    )
    assert candidate["harvest_events_total_mean"] == pytest.approx(
        control["harvest_events_total_mean"]
    )
    assert candidate["harvested_units_total_mean"] == pytest.approx(
        control["harvested_units_total_mean"]
    )


def test_e18_13_removes_losses_but_fails_worst_tail_gate() -> None:
    payload = _load(
        "E18_13_770_D20_CRITICAL_FEED_DEADLINE_DEV_GATE_V1.json"
    )
    candidate = payload["standings"][
        "CODEX_E18_13_770_D20_CRITICAL_FEED_DEADLINE"
    ]
    control = payload["standings"]["CODEX_E18_10_V2_770_CONTROL"]
    assert payload["gates"]["gate_a_causal"]["passed"] is False
    assert candidate["verified_livestock_losses"] == 0
    assert control["verified_livestock_losses"] == 14
    assert candidate["money_mean"] > control["money_mean"]
    assert candidate["move_actions_mean"] < (
        control["move_actions_mean"] * 1.005
    )
    failed = {
        key
        for key, value in payload["gates"]["gate_a_causal"]["checks"].items()
        if not value
    }
    assert failed == {"worst_matched_money_delta_at_least_minus_2pct"}
    assert all(
        match[f"{slot}_metrics"]["move_to_critical_feed_overrides"] == 1
        for match in payload["matches"]
        for slot in ("p0", "p1")
        if match[slot]
        == "CODEX_E18_13_770_D20_CRITICAL_FEED_DEADLINE"
    )


def test_e18_16_cap_and_feed_pass_causal_gate_without_top3_convergence() -> None:
    payload = _load(
        "E18_16_770_EXACT_CAP_CRITICAL_FEED_DEV_GATE_V1.json"
    )
    candidate_name = "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED"
    candidate = payload["standings"][candidate_name]
    control = payload["standings"]["CODEX_E18_10_V2_770_CONTROL"]
    assert payload["gates"]["gate_a_causal"]["passed"] is True
    assert payload["gates"]["gate_b_top3_convergence"]["passed"] is False
    assert candidate["wins"] == 8
    assert control["wins"] == 6
    assert candidate["verified_livestock_losses"] == 0
    assert control["verified_livestock_losses"] == 14
    assert candidate["money_mean"] > control["money_mean"]
    assert payload["gates"]["worst_matched_money_delta_percent"] > -1
    rows = [
        match[f"p{seat}_metrics"]
        for match in payload["matches"]
        for seat in (0, 1)
        if match[f"p{seat}"] == candidate_name
    ]
    assert all(row["max_observed_livestock_resources"] == 14 for row in rows)
    assert all(row["clamped_animal_units"] >= 1 for row in rows)
    assert all(row["move_to_critical_feed_overrides"] == 1 for row in rows)
