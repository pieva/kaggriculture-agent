"""Focused tests for the Copilot E18 adaptive-crop opponent-reactive controller."""

from __future__ import annotations

from pathlib import Path

from agricola.strategy.copilot.e18_opponent_reactive_v1 import (
    create_copilot_e18_opponent_reactive_v1,
    load_copilot_e18_opponent_reactive_v1_config,
)

ROOT = Path(__file__).resolve().parents[3]


def _make_observation(*, opponent_pressure: str = "low") -> dict:
    board = [[None for _ in range(10)] for _ in range(10)]
    for x in range(2, 6):
        board[3][x] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "watered_today": False, "yield_units": 1}
    board[4][4] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "watered_today": True, "yield_units": 0}
    board[5][4] = {"kind": "WEED"}

    opponent = {
        "farmer": [1, 1],
        "hands": [[2, 1], [1, 2], [2, 2]] if opponent_pressure == "high" else [[2, 1]],
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "money": 2000.0 if opponent_pressure == "high" else 1200.0,
        "unlocked_quadrants": ["NW", "NE"] if opponent_pressure == "low" else ["NW", "NE", "SW"],
    }
    if opponent_pressure == "low":
        opponent["tiles"][1][1] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "watered_today": True, "yield_units": 1}
        opponent["tiles"][1][2] = {"kind": "WEED"}
    else:
        for y in range(1, 4):
            for x in range(1, 5):
                opponent["tiles"][y][x] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "watered_today": False, "yield_units": 1}
        opponent["tiles"][4][4] = {"kind": "WEED"}
        opponent["tiles"][4][5] = {"kind": "WEED"}
        opponent["tiles"][5][4] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 1, "watered_today": False, "yield_units": 1}
        opponent["tiles"][5][5] = {"kind": "PASTURE"}

    own = {
        "farmer": [4, 4],
        "hands": [[5, 4], [4, 5]],
        "tiles": board,
        "money": 2800.0,
        "unlocked_quadrants": ["NW", "NE"],
    }
    return {
        "step": 24 * 2 + 12,
        "day": 2,
        "hour": 12,
        "player": 0,
        "farms": [own, opponent],
        "private": {"seeds": {"WHEAT": 12, "CARROT": 3, "STRAWBERRY": 2}},
        "market": {},
    }


def test_config_loads_and_validates() -> None:
    config_path = ROOT / "experiments/e18/configs/copilot/COPILOT_E18_1_OPPONENT_REACTIVE_V1.json"
    config = load_copilot_e18_opponent_reactive_v1_config(config_path)
    assert config.candidate_id == "COPILOT_E18_1_OPPONENT_REACTIVE_V1"
    assert config.family == "ADAPTIVE_CROP"
    assert config.snapshot_day_start == 4
    assert config.snapshot_day_end == 8


def test_regime_changes_with_opponent_pressure() -> None:
    policy = create_copilot_e18_opponent_reactive_v1()
    low = _make_observation(opponent_pressure="low")
    high = _make_observation(opponent_pressure="high")
    low_regime = policy._public_snapshot_to_regime(low)["regime"]
    high_regime = policy._public_snapshot_to_regime(high)["regime"]
    assert low_regime == "BALANCED"
    assert high_regime == "EXPANSION"


def test_action_stream_is_well_formed_and_independent() -> None:
    policy = create_copilot_e18_opponent_reactive_v1()
    low = _make_observation(opponent_pressure="low")
    high = _make_observation(opponent_pressure="high")
    low_regime = policy._public_snapshot_to_regime(low)["regime"]
    high_regime = policy._public_snapshot_to_regime(high)["regime"]
    low_action = policy(low, {"turnsPerDay": 24, "episodeSteps": 720, "boardSize": 10})
    high_action = policy(high, {"turnsPerDay": 24, "episodeSteps": 720, "boardSize": 10})
    assert set(low_action) == {"farmer", "hands", "market"}
    assert set(high_action) == {"farmer", "hands", "market"}
    assert low_regime != high_regime
    assert isinstance(low_action["farmer"], list)
    assert isinstance(high_action["hands"], list)
    assert isinstance(policy.telemetry_snapshot()["current_regime"], str)
