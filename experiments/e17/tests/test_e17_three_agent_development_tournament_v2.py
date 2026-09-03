"""Integrity checks for the E17.3 three-agent development tournament."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
RESULTS = (
    ROOT
    / "experiments/e17/artifacts/derived/common/"
    / "E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2.json"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_tournament_matrix_and_reserved_seed_boundary() -> None:
    results = _load(RESULTS)
    manifest = _load(MANIFEST)
    assert results["match_count"] == 42
    assert len(results["matches"]) == 42
    assert results["participants"] == [
        "CODEX_662",
        "CLAUDE_V3",
        "COPILOT_NATIVE",
    ]
    assert results["excluded_participants"] == {
        "ANTIGRAVITY": "OWNER_UNAVAILABLE_UNTIL_2026-09-04"
    }
    assert results["holdout_consumed"] is False
    assert results["final_confirmation_consumed"] is False
    assert results["seeds"] == manifest["seed_policy"]["development"]
    reserved = {
        *manifest["seed_policy"]["holdout"]["seeds"],
        *manifest["seed_policy"]["final_confirmation"]["seeds"],
    }
    assert not set(results["seeds"]).intersection(reserved)


def test_tournament_standings_and_safety_are_complete() -> None:
    standings = _load(RESULTS)["standings"]
    assert (standings["CODEX_662"]["wins"], standings["CODEX_662"]["losses"]) == (
        28,
        0,
    )
    assert (standings["CLAUDE_V3"]["wins"], standings["CLAUDE_V3"]["losses"]) == (
        14,
        14,
    )
    assert (
        standings["COPILOT_NATIVE"]["wins"],
        standings["COPILOT_NATIVE"]["losses"],
    ) == (0, 28)
    assert all(row["matches"] == 28 for row in standings.values())
    assert all(row["technical_errors"] == 0 for row in standings.values())
    assert all(row["fallbacks"] == 0 for row in standings.values())
    codex = standings["CODEX_662"]
    assert codex["target_pastures_built"] == 14
    assert codex["target_pastures_filled"] == 14
    assert codex["empty_target_pastures"] == 0
    assert codex["max_reclaimed_crops"] == 5
    assert codex["max_q2_pastures"] == 2
    assert codex["topology_cap_breaches"] == 0
    assert codex["animal_escapes"] == 0


def test_tournament_provenance_matches_current_frozen_inputs() -> None:
    results = _load(RESULTS)
    for participant, provenance in results["provenance"].items():
        del participant
        assert _sha256(ROOT / provenance["source"]) == provenance["source_sha256"]
        assert _sha256(ROOT / provenance["config"]) == provenance["config_sha256"]
