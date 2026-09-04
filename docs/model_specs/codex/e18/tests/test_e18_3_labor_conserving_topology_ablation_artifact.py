"""Integrity checks for the frozen E18.3 topology-ablation artifact."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from agricola.core.repository_paths import (
    canonical_repository_path,
    expected_current_sha256,
)

ROOT = Path(__file__).resolve().parents[5]
ARTIFACT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1.json"
)
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_ablation_uses_only_development_seeds_and_codex_agents() -> None:
    artifact = _load(ARTIFACT)
    manifest = _load(MANIFEST)
    development = set(manifest["seed_policy"]["development"])
    reserved = {
        *manifest["seed_policy"]["holdout"]["seeds"],
        *manifest["seed_policy"]["final_confirmation"]["seeds"],
    }
    assert artifact["match_count"] == 70
    assert set(artifact["seeds"]) == development
    assert development.isdisjoint(reserved)
    assert artifact["peer_agents_excluded"] is True
    assert artifact["antigravity_excluded"] is True
    assert all(name.startswith("CODEX_") for name in artifact["participants"])


def test_every_arm_has_both_seats_and_exact_topology() -> None:
    artifact = _load(ARTIFACT)
    arms = [name for name in artifact["participants"] if name != "CODEX_E18_2_CONTROL"]
    assert len(arms) == 5
    for arm in arms:
        assert artifact["standings"][arm]["matches"] == 14
        gate = artifact["arm_gates"][arm]
        assert gate["exact_topology_matches"] == 14
        assert gate["checks"]["exact_target_topology_all_matches"] is True


def test_no_reduced_topology_is_promoted() -> None:
    artifact = _load(ARTIFACT)
    assert artifact["selected_candidate"] is None
    assert artifact["submission_authorized"] is False
    assert not any(gate["passed"] for gate in artifact["arm_gates"].values())
    assert artifact["arm_gates"]["CODEX_E18_3_775"][
        "checks"
    ]["mean_money_not_below_control_minus_5pct"] is True
    for arm in ("CODEX_E18_3_772", "CODEX_E18_3_662", "CODEX_E18_3_770", "CODEX_E18_3_670"):
        assert artifact["arm_gates"][arm][
            "checks"
        ]["mean_money_not_below_control_minus_5pct"] is False


def test_candidate_provenance_matches_current_source_and_config() -> None:
    artifact = _load(ARTIFACT)
    provenance = artifact["provenance"]
    source = canonical_repository_path(ROOT, provenance["candidate_source"])
    config = canonical_repository_path(ROOT, provenance["candidate_config"])
    expected_source = expected_current_sha256(
        provenance["candidate_source"], provenance["candidate_source_sha256"]
    )
    assert _sha256(source) == expected_source
    assert _sha256(config) == provenance["candidate_config_sha256"]
