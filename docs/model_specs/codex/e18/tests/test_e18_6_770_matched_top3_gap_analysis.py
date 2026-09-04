"""Integrity tests for the E18.6 exact-7-7-0 Top-3 gap analysis."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
ARTIFACT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_6_770_MATCHED_TOP3_GAP_ANALYSIS_2026_09_04.json"
)
TOP3 = (
    ROOT
    / "experiments/e18/artifacts/discovery/"
    / "E18_CURRENT_TOP3_STRATEGY_BENCHMARK_2026_09_04.json"
)


def _payload() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_selection_contains_only_exact_770_profiles() -> None:
    payload = _payload()
    source = json.loads(TOP3.read_text(encoding="utf-8"))
    exact = [
        profile
        for profile in source["profiles"]
        if profile["final_pasture_topology"] == "7-7-0"
    ]
    selection = payload["selection"]
    assert len(exact) == selection["top3_exact_profiles"] == 6
    assert selection["giulio_profiles"] == 2
    assert selection["jesse_profiles"] == 4
    assert selection["crop_dusta_profiles"] == 0
    assert selection["episode_ids"] == [
        105366473,
        105384058,
        105391568,
        105398563,
        105405557,
    ]
    head_to_head = [
        row
        for row in payload["leader_exact_770_rows"]
        if row["episode_id"] == selection["matched_head_to_head_episode"]
    ]
    assert {row["player"] for row in head_to_head} == {
        "Giulio Ravasio",
        "Jesse Bullard",
    }


def test_normalized_action_taxonomy_is_applied_to_every_codex_row() -> None:
    payload = _payload()
    assert payload["normalization"]["money_and_score_compared"] is False
    assert len(payload["codex_rows"]) == 14
    for row in payload["codex_rows"]:
        assert row["productive_normalized"] == (
            row["unit_actions"] - row["move"] - row["pass"]
        )
        assert row["crop_service"] + row["other_productive"] == row[
            "productive_normalized"
        ]
        assert row["move_per_productive_normalized"] == pytest.approx(
            row["move"] / row["productive_normalized"]
        )


def test_matched_gap_metrics_are_frozen() -> None:
    payload = _payload()
    codex = payload["cohorts"]["CODEX_E18_6_770"]
    leaders = payload["cohorts"]["TOP3_EXACT_770_POOL"]
    gaps = payload["codex_vs_top3_exact_770_gaps"]
    assert codex["unit_actions_mean"] == pytest.approx(7519.0)
    assert leaders["unit_actions_mean"] == pytest.approx(7305.0)
    assert codex["productive_normalized_mean"] == pytest.approx(
        3065.0714285714284
    )
    assert leaders["productive_normalized_mean"] == pytest.approx(3315.0)
    assert gaps["productive_normalized"]["percent"] == pytest.approx(
        -7.539323421676367
    )
    assert gaps["crop_service"]["percent"] == pytest.approx(
        -18.12139515310543
    )
    assert gaps["pass"]["percent"] == pytest.approx(60.505259372471464)
    assert gaps["harvest_events"]["percent"] == pytest.approx(
        -31.68337510442774
    )
    assert gaps["harvested_units"]["percent"] == pytest.approx(
        -36.65895144794918
    )


def test_hypotheses_are_ordered_and_keep_worker_count_separate() -> None:
    hypotheses = _payload()["hypotheses"]
    assert [row["priority"] for row in hypotheses] == list(range(6))
    assert [row["id"] for row in hypotheses] == [
        "NORMALIZE_ACTION_TAXONOMY",
        "CONVERT_PASS_TO_LOCAL_CROP_SERVICE",
        "PERSISTENT_CROP_LIFECYCLE",
        "LOCAL_ROUTE_COMPLETION",
        "EXACT_LIVESTOCK_CAP_14",
        "WORKER_13_ONLY_AFTER_SCHEDULER",
    ]


def test_input_artifacts_match_recorded_provenance() -> None:
    provenance = _payload()["provenance"]
    for path_key, hash_key in (
        ("top3_artifact", "top3_artifact_sha256"),
        ("codex_artifact", "codex_artifact_sha256"),
    ):
        path = ROOT / provenance[path_key]
        assert path.is_file()
        assert _sha256(path) == provenance[hash_key]
