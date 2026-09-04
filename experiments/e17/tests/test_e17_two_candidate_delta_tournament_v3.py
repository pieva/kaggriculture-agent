"""Integrity checks for the two-candidate E17 development tournament."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from agricola.core.repository_paths import (
    canonical_repository_path,
    expected_current_sha256,
)

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
RESULTS = (
    ROOT
    / "experiments/e17/artifacts/derived/common/"
    / "E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3.json"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_delta_tournament_matrix_and_seed_boundary() -> None:
    results = _load(RESULTS)
    manifest = _load(MANIFEST)
    assert results["match_count"] == 84
    assert len(results["matches"]) == 84
    assert results["participants"] == [
        "CLAUDE_V5",
        "CLAUDE_V3_CONTROL",
        "COPILOT_662_V3",
        "CODEX_662_V2_CONTROL",
    ]
    assert results["seeds"] == manifest["seed_policy"]["development"]
    assert results["holdout_consumed"] is False
    assert results["final_confirmation_consumed"] is False
    reserved = {
        *manifest["seed_policy"]["holdout"]["seeds"],
        *manifest["seed_policy"]["final_confirmation"]["seeds"],
    }
    assert not set(results["seeds"]).intersection(reserved)


def test_delta_tournament_outputs_are_complete_and_safe() -> None:
    results = _load(RESULTS)
    assert all(row["matches"] == 42 for row in results["standings"].values())
    assert all(row["technical_errors"] == 0 for row in results["standings"].values())
    assert all(row["fallbacks"] == 0 for row in results["standings"].values())
    assert set(results["candidate_deltas"]) == {"CLAUDE_V5", "COPILOT_662_V3"}
    for delta in results["candidate_deltas"].values():
        assert delta["shared_opponent_samples_per_agent"] == 28
        assert delta["direct_samples_per_agent"] == 14
        assert set(delta["shared_opponent_metrics"]) == {
            "money",
            "peak_hands",
            "peak_crops",
            "peak_animals",
            "peak_weeds",
            "animal_escapes",
            "final_crops",
            "final_animals",
            "final_empty_livestock_tiles",
            "move_actions",
            "productive_actions",
            "pass_actions",
            "move_per_productive",
        }
    for name in ("COPILOT_662_V3", "CODEX_662_V2_CONTROL"):
        row = results["standings"][name]
        assert row["max_q2_pastures_mean"] <= 2
        assert row["topology_cap_breaches"] == 0


def test_delta_tournament_provenance_matches_inputs() -> None:
    results = _load(RESULTS)
    for provenance in results["provenance"].values():
        expected_source_hash = provenance.get(
            "source_sha256_at_closeout", provenance["source_sha256"]
        )
        source = canonical_repository_path(ROOT, provenance["source"])
        config = canonical_repository_path(ROOT, provenance["config"])
        expected_source_hash = expected_current_sha256(
            provenance["source"], expected_source_hash
        )
        assert _sha256(source) == expected_source_hash
        assert _sha256(config) == provenance["config_sha256"]
