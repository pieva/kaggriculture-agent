"""Integrity checks for the completed E18.4 V2 development gate artifact."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ARTIFACT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_4_STATE_DRIVEN_772_V2_DEV_GATE.json"
)


def test_v2_gate_is_development_only_and_sequentially_rejected() -> None:
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["match_count"] == 14
    assert payload["holdout_consumed"] is False
    assert payload["final_confirmation_consumed"] is False
    assert payload["kaggle_upload_authorized"] is False
    assert payload["gate_a"]["passed"] is False
    assert payload["gate_b"]["evaluated"] is False


def test_v2_integrity_passes_while_work_kpis_fail() -> None:
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    checks = payload["gate_a"]["checks"]
    for name in (
        "zero_pass_on_actionable",
        "zero_route_thrashing",
        "exact_772_topology_all_matches",
        "all_16_target_pastures_filled",
        "zero_technical_errors",
        "zero_fallbacks",
        "zero_verified_livestock_losses",
    ):
        assert checks[name] is True
    for name in (
        "move_actions_lte_e18_2",
        "productive_actions_gte_95pct_e18_2",
        "move_per_productive_lte_1_28",
        "harvested_units_gte_95pct_e18_2",
        "late_weed_tile_days_lte_110pct_e18_2",
    ):
        assert checks[name] is False
