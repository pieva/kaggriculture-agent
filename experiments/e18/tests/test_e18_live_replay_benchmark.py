"""Integrity tests for the E18 live Top-3 and Codex replay benchmark."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/discovery/"
    / "E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_V1.json"
)
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"


def _load() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_live_replay_corpus_is_complete_training_evidence() -> None:
    data = _load()
    assert data["schema_version"] == 1
    assert data["epistemic_role"] == "E18_TRAINING_EVIDENCE"
    assert len(data["corpus"]) == 11
    assert {row["episode_id"] for row in data["corpus"]} == {
        105075696,
        105080066,
        105084394,
        105088610,
        105089826,
        105090557,
        105100853,
        105101421,
        105102327,
        105107425,
        105107748,
    }
    assert len({row["raw_sha256"] for row in data["corpus"]}) == 11


def test_codex_is_lifecycle_invariant_but_not_byte_identical() -> None:
    cohort = _load()["cohort_aggregates"]["CODEX_662_EXTERNAL"]
    assert cohort["profiles"] == 3
    assert cohort["unique_lifecycle_profiles"] == 1
    assert cohort["unique_action_streams"] == 3
    assert cohort["mean_harvested_units_total"] == 586
    assert cohort["mean_unwatered_tile_days_d21_d30"] == 224


def test_top3_signal_is_output_and_service_not_one_rotation_recipe() -> None:
    data = _load()
    codex = data["cohort_aggregates"]["CODEX_662_EXTERNAL"]
    top3 = data["cohort_aggregates"]["LIVE_TOP3_TARGET"]
    assert top3["unique_lifecycle_profiles"] == 8
    assert top3["unique_pasture_topologies"] == 5
    assert top3["all_q2_zero"] is False
    assert top3["q2_zero_profiles"] == 7
    assert top3["mean_harvested_units_total"] > codex["mean_harvested_units_total"]
    assert top3["mean_harvested_wheat_units"] > codex["mean_harvested_wheat_units"]
    assert (
        top3["mean_unwatered_tile_days_d21_d30"]
        < codex["mean_unwatered_tile_days_d21_d30"]
    )
    assert top3["mean_live_crop_rotations"] < 7


def test_top3_targets_and_topologies_are_frozen() -> None:
    rows = [
        row
        for row in _load()["target_profiles"]
        if row["cohort"] == "LIVE_TOP3_TARGET"
    ]
    assert {row["player"] for row in rows} == {"Crop Dusta", "3정훈", "sbol ball"}
    assert {
        player: {
            row["final_pasture_topology"] for row in rows if row["player"] == player
        }
        for player in {row["player"] for row in rows}
    } == {
        "Crop Dusta": {"7-0-0", "8-4-3"},
        "3정훈": {"7-7-0", "10-7-0"},
        "sbol ball": {"6-7-0", "7-7-0", "10-7-0"},
    }


def test_online_opponent_signal_excludes_identity_and_rating() -> None:
    observability = _load()["online_observability"]
    assert observability["opponent_public_farm"] is True
    assert observability["opponent_private_inventory"] is False
    assert observability["submission_rating"] is False
    assert observability["opponent_rating"] is False
    assert observability["agent_identity"] is False
    assert observability["cross_episode_state_contract"] is False


def test_live_benchmark_manifest_hashes_are_frozen() -> None:
    section = json.loads(MANIFEST.read_text(encoding="utf-8"))[
        "live_replay_benchmark"
    ]
    for path_key, hash_key in (
        ("artifact", "artifact_sha256"),
        ("profiles_csv", "profiles_csv_sha256"),
        ("report", "report_sha256"),
        ("builder", "builder_sha256"),
    ):
        assert _sha256(ROOT / section[path_key]) == section[hash_key]
    assert section["holdout_consumed"] is False
