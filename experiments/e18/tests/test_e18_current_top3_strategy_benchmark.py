"""Integrity tests for the current Top-3 strategy reconstruction benchmark."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/discovery/"
    / "E18_CURRENT_TOP3_STRATEGY_BENCHMARK_2026_09_04.json"
)


def _load() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_current_top3_snapshot_and_balanced_corpus_are_frozen() -> None:
    data = _load()
    assert data["schema_version"] == 1
    assert data["epistemic_role"] == "E18_EXTERNAL_DISCOVERY_EVIDENCE"
    assert data["sampling_design"]["episodes"] == 11
    assert data["sampling_design"]["profiles"] == 22
    assert data["sampling_design"]["pair_counts"] == {
        "CROP_GIULIO": 4,
        "CROP_JESSE": 4,
        "GIULIO_JESSE": 3,
    }
    assert data["sampling_design"]["raw_replays_retained_in_repository"] is False
    assert data["leaderboard_snapshot"]["entries"] == [
        {
            "rank": 1,
            "player": "Crop Dusta",
            "owner": "Rishi Gottumukkala",
            "rating": 3032.3,
        },
        {
            "rank": 2,
            "player": "Giulio Ravasio",
            "owner": "Giulio Ravasio",
            "rating": 2967.3,
        },
        {
            "rank": 3,
            "player": "Jesse Bullard",
            "owner": "Jesse Bullard",
            "rating": 2960.4,
        },
    ]


def test_replay_integrity_and_profile_coverage() -> None:
    data = _load()
    corpus = data["corpus"]
    profiles = data["profiles"]
    assert len({row["episode_id"] for row in corpus}) == 11
    assert len({row["raw_sha256"] for row in corpus}) == 11
    assert all(row["steps"] == 720 for row in corpus)
    assert all(row["statuses"] == ["DONE", "DONE"] for row in corpus)
    counts = {
        player: sum(row["player"] == player for row in profiles)
        for player in ("Crop Dusta", "Giulio Ravasio", "Jesse Bullard")
    }
    assert counts == {"Crop Dusta": 8, "Giulio Ravasio": 7, "Jesse Bullard": 7}
    assert all(
        {row["player_index"] for row in profiles if row["player"] == player}
        == {0, 1}
        for player in counts
    )


def test_crop_dusta_is_variable_and_wins_the_direct_sample() -> None:
    crop = _load()["agent_aggregates"]["Crop Dusta"]
    assert crop["wins"] == 6
    assert crop["losses"] == 2
    assert crop["unique_action_shapes"] == 8
    assert crop["largest_action_shape_cluster"] == 1
    assert len(crop["topology_counts"]) == 7
    assert crop["mean_harvested_units_total"] == 917.375
    assert crop["mean_move_per_productive"] == 1.256907
    assert crop["mean_requested_crop_sell_share_pct"] == 71.25825


def test_giulio_reconstruction_is_compact_q2_zero_and_logistically_efficient() -> None:
    giulio = _load()["agent_aggregates"]["Giulio Ravasio"]
    assert giulio["profiles"] == 7
    assert giulio["topology_counts"] == {
        "10-7-0": 1,
        "7-2-0": 1,
        "7-5-0": 3,
        "7-7-0": 2,
    }
    assert giulio["topology_mode"] == ["7-5-0"]
    assert giulio["unique_action_shapes"] == 3
    assert giulio["largest_action_shape_cluster"] == 5
    assert giulio["mean_move_per_productive"] == 1.011762
    assert giulio["phase_action_means"]["D21_D30"]["move_per_productive"] < 1
    assert giulio["mean_harvested_units_per_1000_moves"] == 265.106594


def test_top3_comparison_falsifies_geometry_only_explanation() -> None:
    data = _load()
    comparison = data["e18_5_662_comparison"]
    codex = comparison["codex_e18_5_662"]
    assert codex["topology"] == "6-6-2"
    assert codex["mean_move_per_productive"] == 2.0025706878106537
    assert codex["mean_harvested_units_per_1000_moves"] == 115.264897
    for player in ("Crop Dusta", "Giulio Ravasio", "Jesse Bullard"):
        aggregate = data["agent_aggregates"][player]
        assert aggregate["mean_move"] < codex["mean_move"]
        assert aggregate["mean_productive"] > codex["mean_productive"]
        assert aggregate["mean_move_per_productive"] < codex[
            "mean_move_per_productive"
        ]
        assert aggregate["mean_harvested_units_per_1000_moves"] > codex[
            "mean_harvested_units_per_1000_moves"
        ]
    assert any("cannot" in line for line in comparison["comparability_boundary"])


def test_evidence_boundary_blocks_causal_and_online_identity_claims() -> None:
    data = _load()
    assert data["observability"] == {
        "public_farms": True,
        "private_inventory": False,
        "cross_episode_state": False,
        "strategy_source_code": False,
    }
    assert any("not causal" in line for line in data["limitations"])
