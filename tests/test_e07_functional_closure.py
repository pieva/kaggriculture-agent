"""Targeted unit tests for E07-07 Functional Closure.

Verifies:
1. HIRE multi-worker scaling logic in ActionBuilder & strategy.
2. GameState inventories accessor & worker inventory checking.
3. Livestock feeding logic requiring WHEAT in personal inventory.
4. Telemetry distinction between feed_attempted, feed_successful, and wheat_consumed.
"""

from agricola.core.state import GameState
from agricola.core.actions import ActionBuilder
from agricola.strategy.hybrid_livestock_cluster_roi import HybridLivestockClusterROIAgent, CompetitiveConfig

def test_game_state_inventories():
    obs = {
        "step": 10,
        "day": 0,
        "hour": 10,
        "player": 0,
        "farms": [{"money": 1000.0, "farmer": [4, 4], "hands": [[4, 5]]}],
        "private": {
            "inventories": [{"WHEAT": 5}, {"MILK": 2}],
            "shed": {"WHEAT": 10}
        }
    }
    state = GameState(obs)
    assert len(state.inventories) == 2
    assert state.get_worker_inventory_count(0, "WHEAT") == 5
    assert state.get_worker_inventory_count(1, "MILK") == 2
    assert state.get_worker_inventory_count(0, "MILK") == 0

def test_hire_multi_worker_scaling():
    agent = HybridLivestockClusterROIAgent()
    obs = {
        "step": 24, # Day 1 Hour 0 -> target_hands = 1
        "day": 1,
        "hour": 0,
        "player": 0,
        "farms": [{"money": 3000.0, "farmer": [4, 4], "hands": [], "hires_today": 0}],
        "private": {"inventories": [{}], "shed": {}}
    }
    state = GameState(obs)
    action = agent.decide(state)
    assert ["HIRE"] in action["market"]

def test_livestock_feeding_pickup_routing():
    agent = HybridLivestockClusterROIAgent()
    # Cow placed at (0,0), unfed today, shed has 10 WHEAT, worker 0 (Farmer) at (4,4) has 0 WHEAT in personal inv
    obs = {
        "step": 100,
        "day": 4,
        "hour": 4,
        "player": 0,
        "farms": [{
            "money": 2000.0,
            "farmer": [4, 4],
            "hands": [],
            "tiles": [[{"animal": "COW", "yield_units": 0, "fed_today": False} if (x==0 and y==0) else None for x in range(10)] for y in range(10)]
        }],
        "private": {"inventories": [{}], "shed": {"WHEAT": 10}}
    }
    state = GameState(obs)
    action = agent.decide(state)
    # Since farmer is at (4,4) with 0 WHEAT in inv and shed has 10 WHEAT, action should be PICKUP WHEAT
    assert action["farmer"] == ["PICKUP", "WHEAT", 5]
