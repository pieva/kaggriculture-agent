"""Tests for Antigravity C2 Model Specification and Policy Implementation."""

import pytest
from typing import Any, Dict

from agricola.strategy.antigravity.c2_config import AntigravityC2Config
from agricola.strategy.antigravity.c2_policy import AntigravityC2Policy
from agricola.strategy.antigravity.agent_c2 import AntigravityC2Agent


def test_antigravity_c2_harvest_readiness_rejection_and_acceptance():
    """Verify CRP-10 harvest_ready rejects premature harvest and accepts mature harvest."""
    policy = AntigravityC2Policy()

    # Wheat: first_yield_day = 3
    premature_wheat = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 0,
        "yield_units": 5,
        "watered_today": True,
    }
    # On day 0, 1, 2: premature! Must reject
    assert not policy.is_harvest_ready(premature_wheat, current_day=0)
    assert not policy.is_harvest_ready(premature_wheat, current_day=1)
    assert not policy.is_harvest_ready(premature_wheat, current_day=2)

    # On day 3: mature! Must accept
    assert policy.is_harvest_ready(premature_wheat, current_day=3)
    assert policy.is_harvest_ready(premature_wheat, current_day=4)

    # Melon: first_yield_day = 8
    premature_melon = {
        "kind": "PLANT",
        "crop": "MELON",
        "planted_day": 1,
        "yield_units": 10,
    }
    assert not policy.is_harvest_ready(premature_melon, current_day=8)  # 8 - 1 = 7 < 8
    assert policy.is_harvest_ready(premature_melon, current_day=9)   # 9 - 1 = 8 >= 8

    # Zero yield units is never harvest ready even if age is sufficient
    zero_yield_plant = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 0,
        "yield_units": 0,
    }
    assert not policy.is_harvest_ready(zero_yield_plant, current_day=5)


def test_antigravity_c2_tile_lifecycle_classification():
    """Verify CRP-09 classification into canonical 6 states."""
    policy = AntigravityC2Policy()
    pos = (0, 0)  # In crop plan

    # 1. EMPTY_ASSIGNED
    assert policy.classify_tile_lifecycle(pos, None, current_day=1, engine_step=24) == "EMPTY_ASSIGNED"

    # 2. LOST_WEED
    weed_tile = {"kind": "WEED"}
    assert policy.classify_tile_lifecycle(pos, weed_tile, current_day=1, engine_step=24) == "LOST_WEED"

    # 3. GROWING (premature wheat)
    growing_wheat = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "yield_units": 5}
    assert policy.classify_tile_lifecycle(pos, growing_wheat, current_day=2, engine_step=48) == "GROWING"

    # 4. HARVEST_READY (mature wheat)
    mature_wheat = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "yield_units": 5}
    assert policy.classify_tile_lifecycle(pos, mature_wheat, current_day=4, engine_step=96) == "HARVEST_READY"

    # 5. RETIREMENT_DUE (exhausted strawberry after max lifespan step)
    retired_strawberry = {
        "kind": "PLANT",
        "crop": "STRAWBERRY",
        "planted_day": 1,
        "yield_units": 0,
        "max_lifespan_step": 300,
    }
    assert policy.classify_tile_lifecycle(pos, retired_strawberry, current_day=15, engine_step=350) == "RETIREMENT_DUE"

    # 6. OUT_OF_SCOPE (position outside working set)
    out_pos = (9, 9)
    assert policy.classify_tile_lifecycle(out_pos, None, current_day=1, engine_step=24) == "OUT_OF_SCOPE"


def test_antigravity_c2_recovery_and_preventive_dig_dispatch():
    """Verify recovery DIG on WEED and preventive DIG on retired crop."""
    policy = AntigravityC2Policy()

    # Create dummy observation where (0,0) is WEED and (1,0) is RETIREMENT_DUE
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
        "farms": [
            {
                "money": 1000.0,
                "farmer": [0, 0],
                "hands": [[1, 0]],
                "tiles": tiles,
                "unlocked_quadrants": ["NW", "NE"],
                "hires_today": 0,
            }
        ],
        "private": [
            {
                "shed": {},
                "seeds": {"WHEAT": 5, "STRAWBERRY": 5, "MELON": 5},
                "inventories": [{}, {}],
            }
        ],
    }

    actions = policy.decide_actions(obs, player_index=0)
    assert len(actions) == 2
    # Farmer at (0,0) on WEED should execute DIG (recovery)
    assert actions[0] == ["DIG"]
    # Hand at (1,0) on RETIREMENT_DUE should execute DIG (preventive)
    assert actions[1] == ["DIG"]


def test_antigravity_c2_no_premature_harvest_dispatch():
    """Verify that under no circumstances is HARVEST dispatched to an immature crop."""
    policy = AntigravityC2Policy()

    # (0,0) is WHEAT on Day 0 with yield_units=5 (standard starting state)
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
        "farms": [
            {
                "money": 1000.0,
                "farmer": [0, 0],
                "hands": [],
                "tiles": tiles,
                "unlocked_quadrants": ["NW"],
                "hires_today": 0,
            }
        ],
        "private": [
            {
                "shed": {},
                "seeds": {"WHEAT": 5},
                "inventories": [{}],
            }
        ],
    }

    actions = policy.decide_actions(obs, player_index=0)
    # Action MUST be WATER (because it's Day 0 unwatered) and MUST NOT be HARVEST!
    assert actions[0] == ["WATER"]


def test_antigravity_c2_agent_callable_interface():
    """Verify AntigravityC2Agent acts as a compliant Kaggle callable entrypoint."""
    agent = AntigravityC2Agent()

    tiles = [["LOCKED" for _ in range(10)] for _ in range(10)]
    tiles[0][0] = None

    obs = {
        "step": 0,
        "day": 0,
        "hour": 0,
        "turnsPerDay": 24,
        "max_steps": 720,
        "farms": [
            {
                "money": 1500.0,
                "farmer": [4, 4],
                "hands": [],
                "tiles": tiles,
                "unlocked_quadrants": ["NW"],
                "hires_today": 0,
            }
        ],
        "private": [
            {
                "shed": {},
                "seeds": {"WHEAT": 10},
                "inventories": [{}],
            }
        ],
    }

    result = agent(obs)
    assert isinstance(result, dict)
    assert "farmer" in result
    assert "hands" in result
    assert "market" in result
    assert isinstance(result["farmer"], list)
    assert isinstance(result["hands"], list)
    assert isinstance(result["market"], list)

    # Test error containment fallback on invalid state
    fallback_result = agent({"invalid": "state"})
    assert fallback_result == {"farmer": ["PASS"], "hands": [], "market": []}
