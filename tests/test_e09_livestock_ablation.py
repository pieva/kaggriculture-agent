"""Unit and behavioral tests for E09-01 LivestockAblationROIAgent."""

import pytest
from agricola.strategy.livestock_ablation_roi import LivestockAblationROIAgent
from agricola.strategy.hybrid_livestock_cluster_roi import CompetitiveConfig
from agricola.core.state import GameState


def mock_observation(step=0, money=3000.0, shed=None, seeds=None, farmer_pos=None, hands=None, hires_today=0):
    if shed is None:
        shed = {"WHEAT": 0, "CARROT": 0, "TOMATO": 0, "STRAWBERRY": 0, "MELON": 0, "EGG": 0, "MILK": 0, "WOOL": 0, "FERTILIZER": 0}
    if seeds is None:
        seeds = {"WHEAT": 5, "CARROT": 5, "MELON": 5}
    if farmer_pos is None:
        farmer_pos = [4, 4]
    if hands is None:
        hands = []
        
    return {
        "step": step,
        "day": step // 24,
        "hour": step % 24,
        "player": 0,
        "farms": [
            {
                "money": money,
                "farmer": farmer_pos,
                "hands": hands,
                "hires_today": hires_today,
                "tiles": [[None for _ in range(10)] for _ in range(10)]
            }
        ],
        "private": {
            "shed": shed,
            "seeds": seeds
        },
        "market": {
            "prices": {"WHEAT": 25.0, "CARROT": 35.0, "MELON": 250.0, "MILK": 160.0, "WOOL": 200.0},
            "inventory": {}
        }
    }


def test_e09_configuration_ablation():
    agent = LivestockAblationROIAgent()
    assert agent.config.target_cows == 0
    assert agent.config.target_sheep == 0
    assert agent.config.feed_safety_buffer == 0
    assert agent.config.target_productive_tiles == 40
    assert len(agent.q0_crop_tiles) == 20
    assert len(agent.q1_crop_tiles) == 20
    assert len(agent.pasture_tiles_cow) == 0
    assert len(agent.pasture_tiles_sheep) == 0


def test_e09_no_livestock_actions_emitted():
    agent = LivestockAblationROIAgent()
    
    # Test across simulation step with cash float and shed items
    obs = mock_observation(
        step=8 * 24, money=2500.0, hires_today=0,
        hands=[[4, 3], [5, 2]],
        shed={"WHEAT": 20, "MILK": 10, "WOOL": 5, "COW": 2, "SHEEP": 2}
    )
    state = GameState(obs)
    action = agent.act(state)
    
    # Verify no BUY_ANIMAL, BUILD_PASTURE, PLACE, FEED, or MILK/WOOL sales
    market_cmds = [m[0] for m in action.get("market", [])]
    farmer_cmds = [f[0] for f in action.get("farmer", [])]
    
    assert "BUY_ANIMAL" not in market_cmds
    assert "BUILD_PASTURE" not in farmer_cmds
    assert "PLACE" not in farmer_cmds
    assert "FEED" not in farmer_cmds
    
    # Confirm Milk/Wool sales are not issued
    sell_items = [m[1] for m in action.get("market", []) if m[0] == "SELL"]
    assert "MILK" not in sell_items
    assert "WOOL" not in sell_items


def test_e09_hiring_and_expansion_preserved():
    agent = LivestockAblationROIAgent()
    
    # Day 12 Hour 0: should issue HIRE and BUY_LAND
    obs = mock_observation(step=12 * 24, money=3000.0, hires_today=0, hands=[[4, 3], [5, 2]])
    state = GameState(obs)
    action = agent.act(state)
    
    market_cmds = [m[0] for m in action.get("market", [])]
    assert "HIRE" in market_cmds
    assert "BUY_LAND" in market_cmds


def test_e09_water_first_priority_preserved():
    agent = LivestockAblationROIAgent()
    
    obs_data = mock_observation(
        step=8 * 24 + 1,
        money=1000.0,
        farmer_pos=[2, 3]
    )
    # Place unwatered plant tile in Q0 at (2,3)
    obs_data["farms"][0]["tiles"][3][2] = {
        "kind": "PLANT",
        "crop": "MELON",
        "planted_day": 5,
        "watered_today": False
    }
    
    state = GameState(obs_data)
    action = agent.act(state)
    
    # Farmer at (2,3) should execute WATER
    farmer_action = action.get("farmer", [])
    assert farmer_action == ["WATER"]

