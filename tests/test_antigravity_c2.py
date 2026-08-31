"""Tests for Antigravity C2 Model Specification and Policy Implementation."""

import pytest
import kaggle_environments
from typing import Any, Dict

from agricola.strategy.antigravity.c2_config import AntigravityC2Config
from agricola.strategy.antigravity.c2_policy import AntigravityC2Policy
from agricola.strategy.antigravity.agent_c2 import AntigravityC2Agent


def test_antigravity_c2_harvest_readiness_rejection_and_acceptance():
    """Verify CRP-10 harvest_ready rejects premature harvest and accepts mature harvest."""
    policy = AntigravityC2Policy()

    # Wheat: first_yield_day = 2
    premature_wheat = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 0,
        "yield_units": 5,
        "watered_today": True,
    }
    # On day 0, 1: premature! Must reject
    assert not policy.is_harvest_ready(premature_wheat, current_day=0)
    assert not policy.is_harvest_ready(premature_wheat, current_day=1)

    # On day 2: premature for non-ongoing wheat when yield_units=5 < 6 and age=2 < 4
    assert not policy.is_harvest_ready(premature_wheat, current_day=2)
    # On day 4: max yield day reached! Must accept
    assert policy.is_harvest_ready(premature_wheat, current_day=4)
    # Or if yield_units == 6 (max yield): Must accept even at day 2
    max_wheat = dict(premature_wheat, yield_units=6)
    assert policy.is_harvest_ready(max_wheat, current_day=2)

    # Melon: first_yield_day = 10, max_yield_day = 12, max_yield = 6
    premature_melon = {
        "kind": "PLANT",
        "crop": "MELON",
        "planted_day": 1,
        "yield_units": 4,
    }
    assert not policy.is_harvest_ready(premature_melon, current_day=9)   # 9 - 1 = 8 < 10
    assert not policy.is_harvest_ready(premature_melon, current_day=10)  # 10 - 1 = 9 < 10
    assert not policy.is_harvest_ready(premature_melon, current_day=11)  # age 10 < 12 and yield 4 < 6
    assert policy.is_harvest_ready(premature_melon, current_day=13)      # 13 - 1 = 12 >= 12 (max yield day)

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
    pos = (3, 4)  # In crop plan (Distance 1 from shed)

    # 1. EMPTY_ASSIGNED
    assert policy.classify_tile_lifecycle(pos, None, current_day=1, engine_step=24) == "EMPTY_ASSIGNED"

    # 2. LOST_WEED
    weed_tile = {"kind": "WEED"}
    assert policy.classify_tile_lifecycle(pos, weed_tile, current_day=1, engine_step=24) == "LOST_WEED"

    # 3. GROWING (premature wheat, day 1, planted day 1 -> age 0 < 2)
    growing_wheat = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "yield_units": 5}
    assert policy.classify_tile_lifecycle(pos, growing_wheat, current_day=1, engine_step=24) == "GROWING"

    # 4. HARVEST_READY (mature wheat at max yield, day 4, planted day 1 -> age 3 >= 2 and yield 6 >= 6)
    mature_wheat = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "yield_units": 6}
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

    # Create dummy observation where (3,4) is WEED and (4,3) is RETIREMENT_DUE
    tiles = [["LOCKED" for _ in range(10)] for _ in range(10)]
    tiles[4][3] = {"kind": "WEED"}
    tiles[3][4] = {
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
                "farmer": [3, 4],
                "hands": [[4, 3]],
                "tiles": tiles,
                "unlocked_quadrants": ["NW", "NE"],
                "hires_today": 0,
            }
        ],
        "private": {
            "shed": {},
            "seeds": {"WHEAT": 5, "STRAWBERRY": 5, "MELON": 5},
            "inventories": [{}, {}],
        },
    }

    actions = policy.decide_actions(obs, player_index=0)
    assert len(actions) == 2
    # Farmer at (3,4) on WEED should execute DIG (recovery)
    assert actions[0] == ["DIG"]
    # Hand at (4,3) on RETIREMENT_DUE should execute DIG (preventive)
    assert actions[1] == ["DIG"]


def test_antigravity_c2_no_premature_harvest_dispatch():
    """Verify that under no circumstances is HARVEST dispatched to an immature crop."""
    policy = AntigravityC2Policy()

    # (3,4) is WHEAT on Day 0 with yield_units=5 (standard starting state)
    tiles = [["LOCKED" for _ in range(10)] for _ in range(10)]
    tiles[4][3] = {
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
                "farmer": [3, 4],
                "hands": [],
                "tiles": tiles,
                "unlocked_quadrants": ["NW", "NE"],
                "hires_today": 0,
            }
        ],
        "private": {
            "shed": {},
            "seeds": {"WHEAT": 5},
            "inventories": [{}],
        },
    }

    actions = policy.decide_actions(obs, player_index=0)
    # Action MUST be WATER (because it's Day 0 unwatered) and MUST NOT be HARVEST!
    assert actions[0] == ["WATER"]


def test_antigravity_c2_agent_callable_interface():
    """Verify AntigravityC2Agent acts as a compliant Kaggle callable entrypoint with dict private."""
    agent = AntigravityC2Agent()

    tiles = [["LOCKED" for _ in range(10)] for _ in range(10)]
    tiles[0][0] = None

    obs = {
        "step": 0,
        "day": 0,
        "hour": 0,
        "turnsPerDay": 24,
        "max_steps": 720,
        "player": 0,
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
        "private": {
            "shed": {},
            "seeds": {"WHEAT": 10},
            "inventories": [{}],
        },
    }

    result = agent(obs)
    assert isinstance(result, dict)
    assert "farmer" in result
    assert "hands" in result
    assert "market" in result
    assert isinstance(result["farmer"], list)
    assert isinstance(result["hands"], list)
    assert isinstance(result["market"], list)
    assert agent.error_count == 0
    assert agent.last_exception is None

    # Test error containment fallback on non-dict / invalid input
    fallback_result = agent(None)
    assert fallback_result == {"farmer": ["PASS"], "hands": [], "market": []}
    assert agent.error_count == 1
    assert agent.last_exception is not None


def test_antigravity_c2_player1_support():
    """Verify AntigravityC2Agent correctly reads player 1 state when player == 1."""
    agent = AntigravityC2Agent()

    tiles_p0 = [["LOCKED" for _ in range(10)] for _ in range(10)]
    tiles_p1 = [["LOCKED" for _ in range(10)] for _ in range(10)]
    tiles_p1[0][0] = None

    obs = {
        "step": 0,
        "day": 0,
        "hour": 0,
        "turnsPerDay": 24,
        "max_steps": 720,
        "player": 1,
        "farms": [
            {
                "money": 500.0,
                "farmer": [0, 0],
                "hands": [],
                "tiles": tiles_p0,
                "unlocked_quadrants": ["NW"],
                "hires_today": 0,
            },
            {
                "money": 3000.0,
                "farmer": [4, 4],
                "hands": [],
                "tiles": tiles_p1,
                "unlocked_quadrants": ["NW"],
                "hires_today": 0,
            },
        ],
        "private": {
            "shed": {},
            "seeds": {"WHEAT": 10},
            "inventories": [{}],
        },
    }

    result = agent(obs)
    assert agent.error_count == 0
    assert agent.last_exception is None
    assert isinstance(result, dict)
    # Market orders should be generated based on P1's money ($3000.0)
    assert len(result["market"]) > 0


def test_antigravity_c2_real_engine_smoke_48_steps():
    """Run real 48-step smoke test in kaggle_environments in both P0 and P1 positions."""
    agent_p0 = AntigravityC2Agent()
    agent_p1 = AntigravityC2Agent()

    env = kaggle_environments.make("kaggriculture", configuration={"episodeSteps": 48})
    env.run([agent_p0, agent_p1])

    # 1. Verify zero internal exceptions / fallbacks in agent
    assert agent_p0.error_count == 0, f"P0 raised exception: {agent_p0.last_exception}"
    assert agent_p1.error_count == 0, f"P1 raised exception: {agent_p1.last_exception}"

    # 2. Verify game status completed cleanly
    assert env.state[0].status == "DONE"
    assert env.state[1].status == "DONE"

    # 3. Verify observable state transitions (money modified, farm active, not 720 PASS)
    final_money_p0 = float(env.state[0].observation.farms[0].money)
    final_money_p1 = float(env.state[1].observation.farms[1].money)
    assert final_money_p0 != 3000.0, "P0 remained completely inactive"
    assert final_money_p1 != 3000.0, "P1 remained completely inactive"


def test_antigravity_c2_expanded_footprint_and_crop_plan():
    """Verify expanded 40-tile footprint and balanced crop allocation across Q0+Q1."""
    config = AntigravityC2Config(crop_working_set_target=40)
    policy = AntigravityC2Policy(config=config)

    # 1. Verify working set size is 40
    assert len(policy.crop_plan) == 40
    # 2. Verify all positions are unique and within Q0 (NW) or Q1 (NE)
    positions = list(policy.crop_plan.keys())
    assert len(set(positions)) == 40
    for x, y in positions:
        assert 0 <= x < 10
        assert 0 <= y < 5
        assert (x, y) not in {(4, 4), (5, 4)}

    # 3. Verify crop allocation quotas
    crop_counts = {}
    for crop in policy.crop_plan.values():
        crop_counts[crop] = crop_counts.get(crop, 0) + 1

    assert crop_counts.get("WHEAT", 0) == 8
    assert crop_counts.get("STRAWBERRY", 0) == 18
    assert crop_counts.get("MELON", 0) == 14


def test_antigravity_c2_late_planting_biological_cutoff():
    """Verify that late planting cutoffs prevent planting slow crops near endgame."""
    policy = AntigravityC2Policy()

    # On day 22, Melon (12-day cycle) and Strawberry (10-day cycle) must be replaced with Wheat
    tiles = [["LOCKED" for _ in range(10)] for _ in range(10)]
    # (3, 4) is a Melon tile in crop plan
    pos_melon = (3, 4)
    tiles[4][3] = None

    obs = {
        "step": 22 * 24 + 2,
        "day": 22,
        "hour": 2,
        "turnsPerDay": 24,
        "max_steps": 720,
        "farms": [
            {
                "money": 10000.0,
                "farmer": [3, 4],
                "hands": [],
                "tiles": tiles,
                "unlocked_quadrants": ["NW", "NE"],
                "hires_today": 0,
            }
        ],
        "private": {
            "shed": {},
            "seeds": {"WHEAT": 5, "MELON": 5, "STRAWBERRY": 5},
            "inventories": [{}],
        },
    }

    actions = policy.decide_actions(obs, player_index=0)
    # Even though (3,4) was planned for MELON, at Day 22 it MUST plant WHEAT
    assert actions[0] == ["PLANT", "WHEAT"]
