from __future__ import annotations

from agricola.strategy.codex.codex_e18_770_extra_q2_water_hand import (
    CodexE18770ExtraQ2WaterHandAgent,
    load_e18_770_extra_q2_water_hand_config,
)


def _observation(*, hands: list[list[int]], money: float = 10000.0) -> dict:
    tiles = [[None for _ in range(10)] for _ in range(10)]
    tiles[6][3] = {
        "kind": "PLANT",
        "crop": "STRAWBERRY",
        "yield_units": 0,
        "watered_today": False,
        "consecutive_unwatered": 1,
    }
    return {
        "day": 14,
        "hour": 4,
        "player": 0,
        "farms": [
            {
                "farmer": [4, 4],
                "hands": hands,
                "tiles": tiles,
                "money": money,
                "unlocked_quadrants": [0, 1, 2],
            }
        ],
        "private": {
            "inventories": [{} for _ in range(1 + len(hands))],
            "shed": {},
        },
    }


def test_config_keeps_provider_workers_authoritative() -> None:
    config = load_e18_770_extra_q2_water_hand_config()
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}
    assert config["target_hands"] == 13
    assert config["provider_workers_authoritative"] is True
    assert config["service_opcode"] == "WATER"


def test_appends_at_most_one_hire_for_the_day() -> None:
    agent = CodexE18770ExtraQ2WaterHandAgent()
    observation = _observation(hands=[[4, 4] for _ in range(12)])
    action = {"farmer": ["PASS"], "hands": [], "market": []}
    agent._append_extra_hire(action, observation, {"maxMarketOrdersPerTurn": 10})
    agent._append_extra_hire(action, observation, {"maxMarketOrdersPerTurn": 10})
    assert action["market"] == [["HIRE"]]
    assert agent.extra_hire_orders == 1


def test_only_extra_worker_is_dispatched_to_q2_water() -> None:
    agent = CodexE18770ExtraQ2WaterHandAgent()
    hands = [[4, 4] for _ in range(12)] + [[3, 6]]
    observation = _observation(hands=hands)
    provider_hands = [["PASS"] for _ in range(12)]
    action = {
        "farmer": ["PASS"],
        "hands": provider_hands.copy(),
        "market": [],
    }
    agent._dispatch_extra_worker(action, observation)
    assert action["farmer"] == ["PASS"]
    assert action["hands"][:12] == provider_hands
    assert action["hands"][12] == ["WATER"]
    assert agent.extra_worker_water_actions == 1
    assert agent.provider_worker_overrides == 0
