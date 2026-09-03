"""Integrity tests for the frozen E18 dynamic-architecture tournament."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/derived/common/"
    / "E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1.json"
)
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
CANDIDATE = "CODEX_E18_REACTIVE_662_770"


def _payload(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_tournament_uses_only_preregistered_development_seeds() -> None:
    artifact = _payload(ARTIFACT)
    manifest = _payload(MANIFEST)
    development = set(manifest["seed_policy"]["development"])
    reserved = {
        *manifest["seed_policy"]["holdout"]["seeds"],
        *manifest["seed_policy"]["final_confirmation"]["seeds"],
    }
    assert set(artifact["seeds"]) == development
    assert development.isdisjoint(reserved)
    assert artifact["holdout_consumed"] is False
    assert artifact["final_confirmation_consumed"] is False
    assert artifact["match_count"] == 56


def test_dynamic_gate_requires_behavior_and_safety_not_only_money() -> None:
    artifact = _payload(ARTIFACT)
    gate = artifact["architecture_gate"]
    assert gate["passed"] is True
    assert all(gate["checks"].values())
    assert set(gate["checks"]) == {
        "both_topology_modes_activated",
        "fourteen_pastures_built_mean",
        "fourteen_pastures_filled_mean",
        "one_decision_per_run",
        "opponent_conditioned_action_divergence",
        "opponent_conditioned_topology_divergence",
        "zero_fallbacks",
        "zero_technical_errors",
        "zero_topology_breaches",
        "zero_verified_livestock_losses",
    }


def test_candidate_activates_both_modes_and_preserves_fourteen() -> None:
    candidate = _payload(ARTIFACT)["standings"][CANDIDATE]
    assert candidate["topology_modes"] == {"6-6-2": 28, "7-7-0": 14}
    assert candidate["mode_by_opponent"] == {
        "CLAUDE_V3": {"6-6-2": 14},
        "CODEX_662_CONTROL": {"6-6-2": 14},
        "COPILOT_NATIVE": {"7-7-0": 14},
    }
    assert candidate["mode_decision_rate"] == 1.0
    assert candidate["target_pastures_built_mean"] == 14.0
    assert candidate["target_pastures_filled_mean"] == 14.0
    assert candidate["empty_target_pastures_mean"] == 0.0
    assert candidate["verified_livestock_losses"] == 0
    assert candidate["technical_errors"] == 0
    assert candidate["fallbacks"] == 0


def test_reported_economic_tradeoff_is_preserved() -> None:
    artifact = _payload(ARTIFACT)
    candidate = artifact["standings"][CANDIDATE]
    direct = artifact["head_to_head"][
        "CODEX_E18_REACTIVE_662_770_vs_CODEX_662_CONTROL"
    ]
    assert candidate["money_mean"] > artifact["target_money"]
    assert direct["CODEX_E18_REACTIVE_662_770_money_mean"] < artifact[
        "target_money"
    ]
    assert direct["CODEX_E18_REACTIVE_662_770_mean_money_delta"] < 0
