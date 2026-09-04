"""Unit and smoke tests for the Copilot E18 opponent-reactive V2 controller."""

from __future__ import annotations

from pathlib import Path

from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
    create_copilot_e18_opponent_reactive_v2,
    load_copilot_e18_opponent_reactive_v2_config,
)

ROOT = Path(__file__).resolve().parents[5]


def _make_observation(*, day: int = 5, pressure: str = "low") -> dict:
    board = [[None for _ in range(10)] for _ in range(10)]
    if pressure == "low":
        board[4][4] = {
            "kind": "PLANT",
            "crop": "WHEAT",
            "planted_day": max(1, day - 1),
            "watered_today": True,
            "yield_units": 1,
        }
    else:
        board[4][4] = None
    for x in range(2, 7):
        if x == 4:
            continue
        board[4][x] = {
            "kind": "PLANT",
            "crop": "WHEAT",
            "planted_day": max(1, day - 1),
            "watered_today": x % 2 == 0,
            "yield_units": 1 if x % 3 == 0 else 0,
        }
    board[4][7] = {"kind": "WEED"}
    board[5][5] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": day - 2, "watered_today": False, "yield_units": 1}
    board[3][5] = None
    opponent_tiles = [[None for _ in range(10)] for _ in range(10)]
    if pressure == "high":
        for y in range(1, 5):
            for x in range(1, 7):
                opponent_tiles[y][x] = {
                    "kind": "PLANT",
                    "crop": "WHEAT",
                    "planted_day": max(1, day - 1),
                    "watered_today": False,
                    "yield_units": 1,
                }
        opponent_tiles[4][7] = {"kind": "WEED"}
        opponent_tiles[5][4] = {"kind": "PASTURE"}
        hands = [[1, 2], [2, 1], [2, 2], [1, 3]]
        money = 2600.0
        quadrants = ["NW", "NE", "SW"]
    else:
        opponent_tiles[1][1] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": day - 1, "watered_today": True, "yield_units": 1}
        opponent_tiles[1][2] = {"kind": "WEED"}
        hands = [[1, 2]]
        money = 1500.0
        quadrants = ["NW", "NE"]
    own = {
        "farmer": [4, 4],
        "hands": [[5, 4], [4, 5]],
        "tiles": board,
        "money": 3200.0 + (day * 18),
        "unlocked_quadrants": ["NW", "NE"],
    }
    opponent = {
        "farmer": [1, 1],
        "hands": hands,
        "tiles": opponent_tiles,
        "money": money,
        "unlocked_quadrants": quadrants,
    }
    private = {
        "seeds": {"WHEAT": 12 + day, "CARROT": 5, "STRAWBERRY": 2},
        "inventory": {"WHEAT": 2 + (day % 5), "CARROT": 1},
    }
    return {
        "step": day * 24 + 12,
        "day": day,
        "hour": 12,
        "player": 0,
        "farms": [own, opponent],
        "private": private,
        "market": {},
    }


def test_config_loads_and_validates() -> None:
    config_path = ROOT / "docs/model_specs/copilot/e18/configs/COPILOT_E18_2_OPPONENT_REACTIVE_V2.json"
    config = load_copilot_e18_opponent_reactive_v2_config(config_path)
    assert config.candidate_id == "COPILOT_E18_2_OPPONENT_REACTIVE_V2"
    assert config.model_spec_version == "COPILOT-E18.2-OPPONENT-REACTIVE-V2"
    assert config.family == "ADAPTIVE_CROP"
    assert config.snapshot_day_start == 4
    assert config.snapshot_day_end == 8


def test_regime_changes_and_action_divergence_is_causal() -> None:
    low_policy = create_copilot_e18_opponent_reactive_v2()
    high_policy = create_copilot_e18_opponent_reactive_v2()
    low = _make_observation(day=5, pressure="low")
    high = _make_observation(day=5, pressure="high")
    low_regime, low_snapshot = low_policy._decide_regime(low, day=5)
    high_regime, high_snapshot = high_policy._decide_regime(high, day=5)
    assert low_regime == "BALANCED"
    assert high_regime == "EXPANSION"
    assert low_snapshot["pressure_score"] != high_snapshot["pressure_score"]
    low_action = low_policy(low, {"turnsPerDay": 24, "episodeSteps": 720, "boardSize": 10})
    high_action = high_policy(high, {"turnsPerDay": 24, "episodeSteps": 720, "boardSize": 10})
    assert low_action["hands"] != high_action["hands"] or low_action["market"] != high_action["market"]
    assert isinstance(low_policy.telemetry_snapshot()["current_regime"], str)


def test_smoke_cycle_runs_for_720_turns_and_stays_profitable() -> None:
    policy = create_copilot_e18_opponent_reactive_v2()
    productive = 0
    cash = 2840.0
    terminal_backlog = 0
    for day in range(1, 721):
        board = [[None for _ in range(10)] for _ in range(10)]
        if day <= 2:
            board[4][4] = None
            inventory = {"WHEAT": 0}
        elif day <= 5:
            board[4][4] = {
                "kind": "PLANT",
                "crop": "WHEAT",
                "planted_day": 1,
                "watered_today": False,
                "yield_units": 0,
            }
            inventory = {"WHEAT": 0}
        elif day <= 7:
            board[4][4] = {
                "kind": "PLANT",
                "crop": "WHEAT",
                "planted_day": 1,
                "watered_today": True,
                "yield_units": 1,
            }
            inventory = {"WHEAT": 2}
        else:
            board[4][4] = {
                "kind": "PLANT",
                "crop": "WHEAT",
                "planted_day": 1,
                "watered_today": True,
                "yield_units": 1,
            }
            inventory = {"WHEAT": 5}
        farm = {
            "farmer": [4, 4],
            "hands": [[5, 4]],
            "tiles": board,
            "money": 3200.0 + day * 27,
            "unlocked_quadrants": ["NW", "NE"],
        }
        opponent = {
            "farmer": [1, 1],
            "hands": [[1, 2]],
            "tiles": [[None for _ in range(10)] for _ in range(10)],
            "money": 1500.0,
            "unlocked_quadrants": ["NW", "NE"],
        }
        observation = {
            "step": day * 24 + 12,
            "day": day,
            "hour": 12,
            "player": 0,
            "farms": [farm, opponent],
            "private": {"seeds": {"WHEAT": 12}, "inventory": inventory},
            "market": {},
        }
        action = policy(observation, {"turnsPerDay": 24, "episodeSteps": 720, "boardSize": 10})
        tokens = set(action["farmer"]) | {token for hand in action["hands"] for token in hand}
        if tokens & {"DIG", "PLANT", "WATER", "HARVEST"}:
            productive += 1
        if action["market"]:
            for order in action["market"]:
                if order and order[0] == "SELL":
                    cash += max(40, int(order[2]) * 12)
        terminal_backlog = max(terminal_backlog, policy.telemetry_snapshot().get("terminal_backlog", 0))
    assert productive > 0
    assert cash != 2840.0
    assert terminal_backlog <= 25
