"""Tests for Copilot C2 model specification and policy implementation."""

from agricola.strategy.copilot.c2_config import CopilotC2Config
from agricola.strategy.copilot.c2_policy import CopilotC2Policy
from agricola.strategy.copilot.agent_c2 import CopilotC2Agent


def test_copilot_c2_harvest_readiness_rejection_and_acceptance():
    """Verify strict harvest_ready gate rejects premature harvest and accepts mature crops."""
    policy = CopilotC2Policy()

    premature_wheat = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 0,
        "yield_units": 5,
        "watered_today": True,
    }
    assert not policy.is_harvest_ready(premature_wheat, current_day=0)
    assert not policy.is_harvest_ready(premature_wheat, current_day=1)
    assert policy.is_harvest_ready(premature_wheat, current_day=2)
    assert policy.is_harvest_ready(premature_wheat, current_day=3)
    assert policy.is_harvest_ready(premature_wheat, current_day=4)

    premature_melon = {
        "kind": "PLANT",
        "crop": "MELON",
        "planted_day": 1,
        "yield_units": 10,
    }
    assert not policy.is_harvest_ready(premature_melon, current_day=8)
    assert not policy.is_harvest_ready(premature_melon, current_day=9)
    assert policy.is_harvest_ready(premature_melon, current_day=11)

    zero_yield_plant = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 0,
        "yield_units": 0,
    }
    assert not policy.is_harvest_ready(zero_yield_plant, current_day=5)


def test_copilot_c2_tile_lifecycle_classification():
    """Verify canonical lifecycle states are classified consistently."""
    policy = CopilotC2Policy()
    pos = (0, 0)

    assert policy.classify_tile_lifecycle(pos, None, current_day=1, engine_step=24) == "EMPTY_ASSIGNED"

    weed_tile = {"kind": "WEED"}
    assert policy.classify_tile_lifecycle(pos, weed_tile, current_day=1, engine_step=24) == "LOST_WEED"

    growing_wheat = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "yield_units": 5}
    assert policy.classify_tile_lifecycle(pos, growing_wheat, current_day=2, engine_step=48) == "GROWING"

    mature_wheat = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "yield_units": 5}
    assert policy.classify_tile_lifecycle(pos, mature_wheat, current_day=4, engine_step=96) == "HARVEST_READY"

    retired_strawberry = {
        "kind": "PLANT",
        "crop": "STRAWBERRY",
        "planted_day": 1,
        "yield_units": 0,
        "max_lifespan_step": 300,
    }
    assert policy.classify_tile_lifecycle(pos, retired_strawberry, current_day=15, engine_step=350) == "RETIREMENT_DUE"

    out_pos = (9, 9)
    assert policy.classify_tile_lifecycle(out_pos, "LOCKED", current_day=1, engine_step=24) == "OUT_OF_SCOPE"


def test_copilot_c2_recovery_and_preventive_dig_dispatch():
    """Verify recovery DIG on WEED and preventive DIG on retired crop."""
    policy = CopilotC2Policy()

    tiles = [["LOCKED" for _ in range(10)] for _ in range(10)]
    tiles[0][0] = {"kind": "WEED"}
    tiles[0][1] = {
        "kind": "PLANT",
        "crop": "STRAWBERRY",
        "planted_day": 1,
        "yield_units": 0,
        "max_lifespan_step": 100,
    }

    obs = {
        "step": 150,
        "day": 6,
        "hour": 6,
        "turnsPerDay": 24,
        "max_steps": 720,
        "farms": [{
            "money": 1000.0,
            "farmer": [0, 0],
            "hands": [[1, 0]],
            "tiles": tiles,
            "unlocked_quadrants": ["NW", "NE"],
            "hires_today": 0,
        }],
        "private": [{
            "shed": {},
            "seeds": {"WHEAT": 5, "STRAWBERRY": 5, "MELON": 5},
            "inventories": [{}, {}],
        }],
    }

    actions = policy.decide_actions(obs, player_index=0)
    assert len(actions) == 2
    assert actions[0] == ["DIG"]
    assert actions[1] == ["DIG"]


def test_copilot_c2_no_premature_harvest_dispatch():
    """Verify the policy must not dispatch HARVEST on immature crop."""
    policy = CopilotC2Policy()

    tiles = [["LOCKED" for _ in range(10)] for _ in range(10)]
    tiles[0][0] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 0,
        "yield_units": 5,
        "watered_today": False,
        "consecutive_unwatered": 1,
    }

    obs = {
        "step": 5,
        "day": 0,
        "hour": 5,
        "turnsPerDay": 24,
        "max_steps": 720,
        "farms": [{
            "money": 1000.0,
            "farmer": [0, 0],
            "hands": [],
            "tiles": tiles,
            "unlocked_quadrants": ["NW"],
            "hires_today": 0,
        }],
        "private": [{
            "shed": {},
            "seeds": {"WHEAT": 5},
            "inventories": [{}],
        }],
    }

    actions = policy.decide_actions(obs, player_index=0)
    assert actions[0] == ["WATER"]


def test_copilot_c2_agent_callable_interface():
    """Verify the Kaggle callable entrypoint exposes the expected contract."""
    agent = CopilotC2Agent()

    tiles = [["LOCKED" for _ in range(10)] for _ in range(10)]
    tiles[0][0] = None

    obs = {
        "step": 0,
        "day": 0,
        "hour": 0,
        "turnsPerDay": 24,
        "max_steps": 720,
        "farms": [{
            "money": 1500.0,
            "farmer": [4, 4],
            "hands": [],
            "tiles": tiles,
            "unlocked_quadrants": ["NW"],
            "hires_today": 0,
        }],
        "private": [{
            "shed": {},
            "seeds": {"WHEAT": 10},
            "inventories": [{}],
        }],
    }

    result = agent(obs)
    assert isinstance(result, dict)
    assert "farmer" in result
    assert "hands" in result
    assert "market" in result
    assert isinstance(result["farmer"], list)
    assert isinstance(result["hands"], list)
    assert isinstance(result["market"], list)
