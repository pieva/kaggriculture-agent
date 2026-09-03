"""Integrity tests for the E18 four-agent reactive development tournament."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/derived/common/"
    / "E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2.json"
)
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"


def _payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_round_robin_is_complete_and_uses_only_development_seeds() -> None:
    tournament = _payload(ARTIFACT)
    manifest = _payload(MANIFEST)
    development = set(manifest["seed_policy"]["development"])
    reserved = {
        *manifest["seed_policy"]["holdout"]["seeds"],
        *manifest["seed_policy"]["final_confirmation"]["seeds"],
    }

    assert tournament["match_count"] == 84
    assert len(tournament["pairs"]) == 6
    assert tournament["seats"] == [0, 1]
    assert set(tournament["seeds"]) == development
    assert development.isdisjoint(reserved)
    assert tournament["holdout_consumed"] is False
    assert tournament["final_confirmation_consumed"] is False


def test_antigravity_rounds_are_present_for_every_opponent_and_seat() -> None:
    matches = _payload(ARTIFACT)["matches"]
    antigravity = [
        row
        for row in matches
        if row["p0"] == "ANTIGRAVITY_E17_OBSOLETE"
        or row["p1"] == "ANTIGRAVITY_E17_OBSOLETE"
    ]

    assert len(antigravity) == 42
    assert sum(row["p0"] == "ANTIGRAVITY_E17_OBSOLETE" for row in antigravity) == 21
    assert sum(row["p1"] == "ANTIGRAVITY_E17_OBSOLETE" for row in antigravity) == 21
    for opponent in ("CODEX_E18_1", "CLAUDE_E18_1", "COPILOT_E18_1"):
        direct = [
            row
            for row in antigravity
            if opponent in {row["p0"], row["p1"]}
        ]
        assert len(direct) == 14


def test_no_candidate_passes_all_reactive_promotion_gates() -> None:
    tournament = _payload(ARTIFACT)
    assert tournament["gates"]["CODEX_E18_1"]["passed"] is False
    assert tournament["gates"]["CLAUDE_E18_1"]["passed"] is False
    assert tournament["gates"]["COPILOT_E18_1"]["passed"] is False
    assert tournament["gates"]["ANTIGRAVITY_E17_OBSOLETE"]["passed"] is False

    codex = tournament["standings"]["CODEX_E18_1"]
    claude = tournament["standings"]["CLAUDE_E18_1"]
    copilot = tournament["standings"]["COPILOT_E18_1"]
    antigravity = tournament["standings"]["ANTIGRAVITY_E17_OBSOLETE"]
    assert codex["wins"] == 42 and codex["money_mean"] > 100_000
    assert codex["activated_regimes"] == ["6-6-2"]
    assert claude["verified_livestock_losses"] == 31
    assert copilot["money_min"] == copilot["money_max"] == 2840.0
    assert antigravity["wins"] == 0 and antigravity["money_mean"] == 0.0
