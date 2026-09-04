"""Integrity tests for the E18 6-6-2 / Top-3 entry benchmark."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from agricola.core.repository_paths import canonical_repository_path

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/baseline/"
    / "E18_662_TOP3_BASELINE_BENCHMARK_V1.json"
)
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"


def _load() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_e18_baseline_sources_and_evidence_boundary() -> None:
    data = _load()
    assert data["schema_version"] == "E18_662_TOP3_BASELINE_BENCHMARK_V1"
    assert data["epistemic_role"] == "E18_TRAINING_BASELINE_FROM_E17_CONSUMED_EVIDENCE"
    assert data["holdout_consumed"] is False
    assert data["final_confirmation_consumed"] is False
    assert set(data["top3_profiles"]) == {"tetsuya", "OceanMix", "Crop Dusta"}
    assert all(
        canonical_repository_path(ROOT, path).is_file()
        for path in data["sources"].values()
    )


def test_e18_baseline_preserves_662_safety_and_exposes_reactivity_gap() -> None:
    data = _load()
    baseline = data["baseline_662"]
    assert baseline["topology"] == {"Q0": 6, "Q1": 6, "Q2": 2}
    assert baseline["target_pastures_built_mean"] == 14
    assert baseline["target_pastures_filled_mean"] == 14
    assert baseline["max_q2_pastures_mean"] == 2
    assert baseline["topology_cap_breaches"] == 0
    assert baseline["animal_escapes"] == 0
    equivalence = data["v3_vs_v2_behavioral_equivalence"]
    assert equivalence["comparable_runs"] == 28
    assert equivalence["exact_complete_metric_profiles"] == 28
    assert equivalence["exact_action_count_profiles"] == 28
    assert data["e18_entry_gates"]["reactive_action_stream_divergence"]["status"] == "FAIL"
    assert data["e18_entry_gates"]["causal_activation_telemetry"]["status"] == "MISSING"


def test_e18_target_vector_has_both_passes_and_open_gaps() -> None:
    gates = _load()["e18_entry_gates"]
    assert gates["money_vs_claude_at_least_100k"]["status"] == "PASS"
    assert gates["symmetric_662_money_at_least_100k"]["status"] == "FAIL"
    assert gates["top3_q1_timing_window"]["status"] == "PASS"
    assert gates["top3_q2_timing_window"]["status"] == "PASS"
    assert gates["top3_peak_crop_floor"]["status"] == "PASS"
    assert gates["zero_escapes"]["status"] == "PASS"
    assert gates["pasture_fill_14_of_14"]["status"] == "PASS"


def test_e18_manifest_hashes_and_seed_partitions_are_frozen() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    predecessor = manifest["predecessor"]
    benchmark = manifest["benchmark"]
    hashed_paths = (
        (predecessor["baseline_source"], predecessor["baseline_source_sha256"]),
        (predecessor["baseline_config"], predecessor["baseline_config_sha256"]),
        (
            predecessor["baseline_submission"],
            predecessor["baseline_submission_sha256"],
        ),
        (benchmark["plan"], benchmark["plan_sha256"]),
        (benchmark["artifact"], benchmark["artifact_sha256"]),
        (benchmark["top3_source"], benchmark["top3_source_sha256"]),
        (
            benchmark["tournament_source"],
            benchmark["tournament_source_sha256"],
        ),
    )
    for relative_path, expected in hashed_paths:
        assert _sha256(ROOT / relative_path) == expected
    seed_policy = manifest["seed_policy"]
    development = set(seed_policy["development"])
    reserved = {
        *seed_policy["holdout"]["seeds"],
        *seed_policy["final_confirmation"]["seeds"],
        *seed_policy["e17_training_seeds_must_not_be_presented_as_e18_validation"],
    }
    assert len(development) == 7
    assert not development.intersection(reserved)
    assert manifest["holdout_consumed"] is False
    assert manifest["final_confirmation_consumed"] is False
