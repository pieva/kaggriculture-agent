"""Integrity checks for the completed E18.6 concentrated 7-7-0 gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
ARTIFACT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_6_CONCENTRATED_770_THROUGHPUT_DEV_GATE_V1.json"
)
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
CANDIDATE = "CODEX_E18_6_CONCENTRATED_770"
CONTROL = "CODEX_E18_2_CONTROL"


def _payload() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def _candidate_rows(payload: dict) -> list[dict]:
    return [
        match[f"p{seat}_metrics"]
        for match in payload["matches"]
        for seat in (0, 1)
        if match[f"p{seat}"] == CANDIDATE
    ]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_gate_uses_only_the_preregistered_development_matrix() -> None:
    payload = _payload()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
    }
    assert payload["match_count"] == 14
    assert payload["seeds"] == manifest["seed_policy"]["development"]
    assert payload["seats"] == [0, 1]
    assert not set(payload["seeds"]).intersection(reserved)
    assert payload["holdout_consumed"] is False
    assert payload["final_confirmation_consumed"] is False
    assert payload["kaggle_upload_authorized"] is False


def test_valid_run_reaches_exact_filled_770() -> None:
    payload = _payload()
    rows = _candidate_rows(payload)
    assert len(rows) == 14
    assert all(
        row["final_pastures_by_quadrant"] == {"Q0": 7, "Q1": 7, "Q2": 0}
        for row in rows
    )
    assert all(row["final_filled_pastures_total"] == 14 for row in rows)
    assert all(row["max_observed_q2_pastures"] == 0 for row in rows)
    assert sum(row["technical_errors"] for row in rows) == 0
    assert sum(row["fallbacks"] for row in rows) == 0
    assert sum(row["topology_cap_breaches"] for row in rows) == 0
    assert sum(row["verified_livestock_losses"] for row in rows) == 14


def test_pre_gate_integrity_correction_is_transparent_and_non_promotional() -> None:
    correction = _payload()["pre_gate_correction"]
    assert correction["invalid_attempt_completed"] is True
    assert correction["invalid_final_topology"] == "6-5-0"
    assert correction["invalid_match_count"] == 14
    assert correction["kpi_thresholds_changed"] is False
    assert correction["invalid_attempt_used_for_promotion"] is False


def test_frozen_gate_result_matches_the_reported_kpis() -> None:
    payload = _payload()
    candidate = payload["standings"][CANDIDATE]
    control = payload["standings"][CONTROL]
    gate = payload["candidate_gate"]
    assert candidate["wins"] == 0
    assert control["wins"] == 14
    assert candidate["money_mean"] == pytest.approx(58957.0)
    assert control["money_mean"] == pytest.approx(71104.42857142857)
    assert candidate["move_actions_mean"] == pytest.approx(3603.785714285714)
    assert control["move_actions_mean"] == pytest.approx(3592.4285714285716)
    assert candidate["productive_actions_mean"] == pytest.approx(
        2643.0714285714284
    )
    assert candidate["move_per_productive_mean"] == pytest.approx(
        1.3634840934713346
    )
    assert candidate["harvested_units_total_mean"] == pytest.approx(
        560.3571428571429
    )
    assert gate["passed"] is False
    assert gate["exact_topology_matches"] == 14
    assert gate["fully_filled_matches"] == 14
    assert gate["mean_matched_money_delta_percent"] == pytest.approx(
        -16.69434868824743
    )
    assert gate["worst_matched_money_delta_percent"] == pytest.approx(
        -31.676262051688674
    )
    assert gate["passed"] == all(gate["checks"].values())


def test_candidate_source_and_config_are_the_frozen_inputs() -> None:
    provenance = _payload()["provenance"]
    for path_key, hash_key in (
        ("candidate_source", "candidate_source_sha256"),
        ("candidate_config", "candidate_config_sha256"),
        ("control_source", "control_source_sha256"),
        ("control_config", "control_config_sha256"),
    ):
        path = ROOT / provenance[path_key]
        assert path.is_file()
        assert _sha256(path) == provenance[hash_key].lower()
