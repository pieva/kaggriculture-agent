"""Integrity checks for the exact E18.1 versus E17 V4D benchmark."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/derived/codex/"
    / "E18_CODEX_LATEST_VS_E17_V4D_BENCHMARK_V1.json"
)
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"


def _payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_matrix_uses_only_e18_development_seeds() -> None:
    artifact = _payload(ARTIFACT)
    manifest = _payload(MANIFEST)
    development = set(manifest["seed_policy"]["development"])
    reserved = {
        *manifest["seed_policy"]["holdout"]["seeds"],
        *manifest["seed_policy"]["final_confirmation"]["seeds"],
    }
    assert artifact["new_match_count"] == 56
    assert set(artifact["seeds"]) == development
    assert development.isdisjoint(reserved)
    assert artifact["holdout_consumed"] is False
    assert artifact["final_confirmation_consumed"] is False


def test_v4d_wins_every_direct_match_and_both_comparisons() -> None:
    artifact = _payload(ARTIFACT)
    direct = artifact["direct_head_to_head"]
    assert direct["latest"]["wins"] == 0
    assert direct["v4d"]["wins"] == 14
    assert direct["latest"]["money_mean"] == 71831.0
    assert direct["v4d"]["money_mean"] == 89760.57142857143
    assert direct["delta_latest_minus_v4d"]["money_mean"]["percent_vs_v4d"] < -19.9

    common = artifact["common_opponent_pool"]
    assert common["latest_reused_from_frozen_v2"]["money_mean"] == 125983.73809523809
    assert common["v4d_new"]["money_mean"] == 143486.45238095237
    assert common["money_delta_latest_minus_v4d"]["percent_vs_v4d"] < -12.1


def test_reclaimed_crop_surface_does_not_compensate_for_lost_capacity() -> None:
    direct = _payload(ARTIFACT)["direct_head_to_head"]
    latest = direct["latest"]
    v4d = direct["v4d"]
    assert latest["crop_tile_days_total_mean"] > v4d["crop_tile_days_total_mean"]
    assert latest["final_crops_mean"] < v4d["final_crops_mean"]
    assert latest["final_animals_mean"] == 15.0
    assert v4d["final_animals_mean"] == 19.0
    assert latest["weed_tile_days_total_mean"] == 63.0
    assert v4d["weed_tile_days_total_mean"] == 15.0
    assert latest["productive_actions_mean"] < v4d["productive_actions_mean"]
    assert latest["pass_actions_mean"] > v4d["pass_actions_mean"]
    assert latest["regimes"] == {"6-6-2": 14}


def test_both_exact_bundles_remain_technically_safe() -> None:
    direct = _payload(ARTIFACT)["direct_head_to_head"]
    for candidate in ("latest", "v4d"):
        assert direct[candidate]["technical_errors"] == 0
        assert direct[candidate]["fallbacks"] == 0
        assert direct[candidate]["verified_livestock_losses"] == 0
