"""Integrity checks for the active peer-V2 real-engine intake."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/derived/common/"
    / "E18_PEER_V2_REAL_ENGINE_INTAKE_V1.json"
)
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_intake_is_complete_real_engine_development_matrix() -> None:
    artifact = _load(ARTIFACT)
    manifest = _load(MANIFEST)
    development = set(manifest["seed_policy"]["development"])
    reserved = {
        *manifest["seed_policy"]["holdout"]["seeds"],
        *manifest["seed_policy"]["final_confirmation"]["seeds"],
    }
    assert artifact["match_count"] == 84
    assert artifact["engine"] == "kaggle_environments/kaggriculture"
    assert set(artifact["seeds"]) == development
    assert development.isdisjoint(reserved)
    assert artifact["holdout_consumed"] is False
    assert artifact["final_confirmation_consumed"] is False
    assert all("ANTIGRAVITY" not in name for name in artifact["participants"])


def test_only_v4d_passes_and_peer_money_is_engine_observed() -> None:
    artifact = _load(ARTIFACT)
    standings = artifact["standings"]
    gates = artifact["gates"]
    assert gates["CODEX_E17_V4D_CONTROL"]["passed"] is True
    assert gates["CODEX_E18_1_ABLATION"]["passed"] is False
    assert gates["CLAUDE_E18_2"]["passed"] is False
    assert gates["COPILOT_E18_2"]["passed"] is False
    assert standings["CODEX_E17_V4D_CONTROL"]["wins"] == 42
    assert standings["CLAUDE_E18_2"]["money_mean"] == 9756.285714285714
    assert standings["COPILOT_E18_2"]["money_mean"] == 260.0
    assert standings["CLAUDE_E18_2"]["verified_livestock_losses"] == 44
