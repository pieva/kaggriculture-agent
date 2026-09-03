"""Integrity checks for the Codex E18.2 development gate artifact."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/derived/codex/"
    / "E18_2_CAPACITY_GOVERNED_V4D_DEV_GATE_V1.json"
)
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_gate_uses_only_development_seeds_and_excludes_antigravity() -> None:
    artifact = _load(ARTIFACT)
    manifest = _load(MANIFEST)
    development = set(manifest["seed_policy"]["development"])
    reserved = {
        *manifest["seed_policy"]["holdout"]["seeds"],
        *manifest["seed_policy"]["final_confirmation"]["seeds"],
    }
    assert artifact["match_count"] == 56
    assert set(artifact["seeds"]) == development
    assert development.isdisjoint(reserved)
    assert artifact["holdout_consumed"] is False
    assert artifact["final_confirmation_consumed"] is False
    assert artifact["antigravity_excluded"] is True
    assert all("ANTIGRAVITY" not in name for name in artifact["participants"])


def test_candidate_has_four_matched_opponents() -> None:
    artifact = _load(ARTIFACT)
    assert len(artifact["pairs"]) == 4
    assert all(pair[0] == "CODEX_E18_2_CAPACITY_GOVERNED_V4D" for pair in artifact["pairs"])
    candidate = artifact["standings"]["CODEX_E18_2_CAPACITY_GOVERNED_V4D"]
    assert candidate["matches"] == 56
    assert set(candidate["mode_by_opponent"]) == set(artifact["participants"][1:])


def test_gate_reports_architecture_and_safety_checks() -> None:
    gate = _load(ARTIFACT)["candidate_gate"]
    assert set(gate["checks"]) == {
        "zero_technical_errors",
        "zero_fallbacks",
        "zero_verified_livestock_losses",
        "overall_economic_100k",
        "direct_money_not_below_v4d_minus_5pct",
        "direct_pass_not_above_v4d_plus_5pct",
        "direct_weed_tile_days_not_above_v4d_plus_10pct",
        "at_least_two_action_effect_modes",
        "no_freed_work_to_pass",
    }
