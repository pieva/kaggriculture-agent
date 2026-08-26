"""Unit and behavioral tests for E08 HybridLivestockClusterROIAgent."""

import pytest
from agricola.strategy.hybrid_livestock_cluster_roi import (
    HybridLivestockClusterROIAgent, CompetitiveConfig, TelemetryLogger
)
from agricola.core.state import GameState


def mock_observation(step=0, money=3000.0, shed=None, seeds=None, farmer_pos=None, hands=None):
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
                "hires_today": 0,
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


def test_config_defaults_e08():
    config = CompetitiveConfig()
    assert config.target_quadrants == 2
    assert config.target_workers == 4
    assert config.target_productive_tiles == 40
    assert config.wheat_tiles == 6
    assert config.melon_tiles == 22
    assert config.carrot_tiles == 12
    assert config.target_cows == 4
    assert config.target_sheep == 2
    assert config.cash_reserve == 300.0
    assert config.spatial_partitioning is True
    assert config.cross_boundary_water_assist is True


def test_40_tile_layout_validity():
    agent = HybridLivestockClusterROIAgent()
    
    total_crop_tiles = agent.q0_crop_tiles + agent.q1_crop_tiles
    assert len(total_crop_tiles) == 40
    assert len(set(total_crop_tiles)) == 40, "All 40 crop tile coordinates must be unique"
    
    pastures = set(agent.pasture_tiles_cow + agent.pasture_tiles_sheep)
    for tile in total_crop_tiles:
        assert tile not in pastures, f"Crop tile {tile} collides with pastures"
        assert 0 <= tile[0] <= 9 and 0 <= tile[1] <= 9, f"Crop tile {tile} out of grid bounds"


def test_phase_transitions():
    agent = HybridLivestockClusterROIAgent()
    
    # Day 0 -> OPENING
    obs_d0 = mock_observation(step=0)
    agent.decide(GameState(obs_d0))
    assert agent.current_phase == "OPENING"
    
    # Day 6 -> SCALE
    obs_d6 = mock_observation(step=6 * 24)
    agent.decide(GameState(obs_d6))
    assert agent.current_phase == "SCALE"
    
    # Day 16 -> PRODUCE
    obs_d16 = mock_observation(step=16 * 24)
    agent.decide(GameState(obs_d16))
    assert agent.current_phase == "PRODUCE"
    
    # Day 28 -> LIQUIDATE
    obs_d28 = mock_observation(step=28 * 24)
    agent.decide(GameState(obs_d28))
    assert agent.current_phase == "LIQUIDATE"


def test_capital_reserve_enforcement():
    config = CompetitiveConfig(cash_reserve=500.0)
    agent = HybridLivestockClusterROIAgent(config)
    
    # Money is 400 (below 500 reserve) -> should not buy land or animals
    obs = mock_observation(step=12 * 24, money=400.0)
    action = agent.decide(GameState(obs))
    
    market_orders = action.get("market", [])
    assert not any(o[0] == "BUY_LAND" for o in market_orders)
    assert not any(o[0] == "BUY_ANIMAL" for o in market_orders)


def test_land_expansion_execution():
    agent = HybridLivestockClusterROIAgent()
    
    # Day 12 turn 0 with $3000 cash -> should issue BUY_LAND
    obs = mock_observation(step=12 * 24, money=3000.0)
    action = agent.decide(GameState(obs))
    
    market_orders = action.get("market", [])
    assert any(o[0] == "BUY_LAND" for o in market_orders)
    assert agent.owned_quadrants == 2


def test_workforce_burst_hiring_turn_zero():
    agent = HybridLivestockClusterROIAgent()
    
    # Day 1 hour 0 -> should issue HIRE
    obs_h0 = mock_observation(step=1 * 24, money=3000.0)
    action_h0 = agent.decide(GameState(obs_h0))
    assert any(o[0] == "HIRE" for o in action_h0.get("market", []))
    
    # Day 1 hour 1 -> should NOT issue HIRE
    obs_h1 = mock_observation(step=1 * 24 + 1, money=3000.0)
    action_h1 = agent.decide(GameState(obs_h1))
    assert not any(o[0] == "HIRE" for o in action_h1.get("market", []))


def test_staggered_seed_purchasing_cash_floor():
    agent = HybridLivestockClusterROIAgent()
    
    # Money = $310 (only $10 above $300 floor) -> should not buy expensive Melon seed ($80)
    obs = mock_observation(step=13 * 24, money=310.0, seeds={"WHEAT": 5, "CARROT": 5, "MELON": 0})
    action = agent.decide(GameState(obs))
    
    market_orders = action.get("market", [])
    assert not any(o[0] == "BUY_SEED" and o[1] == "MELON" for o in market_orders)


def test_spatial_partitioning_and_cross_boundary_assist():
    agent = HybridLivestockClusterROIAgent()
    agent.owned_quadrants = 2
    
    obs_data = mock_observation(
        step=14 * 24,
        money=3000.0,
        farmer_pos=[4, 4],
        hands=[[4, 4], [7, 2], [7, 3]]
    )
    
    # Place a unwatered plant tile in Q0 at (1,2)
    obs_data["farms"][0]["tiles"][2][1] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 10,
        "watered_today": False
    }
    
    gs = GameState(obs_data)
    action = agent.decide(gs)
    
    # Hand 2 (at 7,2 in Q1) has no water tasks in Q1, so Cross-Boundary Assist allows assisting Q0 water task at (1,2)
    assert "hands" in action
    assert len(action["hands"]) >= 2


def test_telemetry_emission_and_backlog():
    agent = HybridLivestockClusterROIAgent()
    obs = mock_observation(step=0, money=3000.0)
    agent.decide(GameState(obs))
    
    t_dict = agent.telemetry.to_dict()
    assert t_dict["starting_money"] == 3000.0
    assert "backlog" in t_dict
    assert "land_breakdown" in t_dict
    assert t_dict["land_breakdown"]["configured_crop_tiles"] == 40
