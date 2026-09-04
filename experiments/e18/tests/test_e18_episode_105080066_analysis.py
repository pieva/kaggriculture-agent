import json
from pathlib import Path

from experiments.e18.tools.common.analyze_episode_105080066 import _unit_commands

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = (
    ROOT
    / "experiments"
    / "e18"
    / "artifacts"
    / "discovery"
    / "E18_EPISODE_105080066_LIFECYCLE_ANALYSIS_V1.json"
)


def _artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_missing_engine_action_is_treated_as_pass() -> None:
    assert list(_unit_commands(None)) == [(0, ["PASS"])]


def test_episode_identity_and_evidence_boundary() -> None:
    artifact = _artifact()
    identity = artifact["identity"]
    assert artifact["epistemic_role"] == "E18_TRAINING_EVIDENCE"
    assert identity["episode_id"] == 105080066
    assert identity["steps"] == 720
    assert identity["statuses"] == ["DONE", "DONE"]
    assert identity["raw_sha256"] == (
        "7AAEE0B4F43FFA5187C37FE8AEFF3FB9892D482CA20506C69B0C905552513F2C"
    )


def test_topology_is_comparable_but_lifecycle_is_not() -> None:
    codex, yusuf = _artifact()["players"]
    assert codex["final_topology"]["pasture_by_quadrant"] == {
        "Q0": 6,
        "Q1": 6,
        "Q2": 2,
    }
    assert yusuf["final_topology"]["pasture_by_quadrant"] == {
        "Q0": 7,
        "Q1": 6,
        "Q2": 1,
    }
    assert codex["crop_tile_days_d21_d30"] > yusuf["crop_tile_days_d21_d30"]
    assert (
        codex["crop_action_execution"]["harvested_units_total"]
        < yusuf["crop_action_execution"]["harvested_units_total"]
    )


def test_rotation_and_service_diagnosis_is_frozen() -> None:
    codex, yusuf = _artifact()["players"]
    codex_exits = codex["transition_metrics"]["counts"]
    yusuf_exits = yusuf["transition_metrics"]["counts"]
    assert codex_exits["expired_to_weed"] == 35
    assert codex_exits["starved_to_weed"] == 14
    assert yusuf_exits["dug_up_crop"] == 27
    assert yusuf_exits.get("starved_to_weed", 0) == 0
    assert codex["unwatered_tile_days_d21_d30"] == 224
    assert yusuf["unwatered_tile_days_d21_d30"] == 161
    assert codex["crop_action_execution"]["harvested_units"]["WHEAT"] == 286
    assert yusuf["crop_action_execution"]["harvested_units"]["WHEAT"] == 504
