"""Unit and integration tests for E10-01 Q1 Expansion Capital Protection Agent."""

import pytest
from agricola.core.state import GameState
from agricola.core.actions import ActionBuilder
from agricola.strategy.hybrid_livestock_cluster_roi import CompetitiveConfig
from agricola.strategy.q1_capital_protected_roi import Q1CapitalProtectedROIAgent


def test_e10_initialization_invariants():
    """Verify E10 inherits all structural invariants from E09 (40 tiles, Livestock OFF)."""
    agent = Q1CapitalProtectedROIAgent()
    
    assert agent.config.target_cows == 0
    assert agent.config.target_sheep == 0
    assert agent.config.feed_safety_buffer == 0
    assert len(agent.q0_crop_tiles) == 20
    assert len(agent.q1_crop_tiles) == 20
    assert len(agent.q0_crop_tiles) + len(agent.q1_crop_tiles) == 40
    assert agent.owned_quadrants == 1


def test_e10_seed_buying_capital_protection():
    """Verify seed buying on Days 8-11 protects $1,000 capital floor when Q1 unowned."""
    agent = Q1CapitalProtectedROIAgent()
    builder = ActionBuilder()
    
    # State mock on Day 10 with $1,040 cash (Q1 unowned)
    # Wheat cost = $60. $1,040 - $60 = $980 < $1,000 floor. Seed buying should be blocked.
    class DummyState:
        day = 10
        hires_today = 0
        def get_seed_count(self, crop):
            return 0
            
    dummy = DummyState()
    
    agent._buy_seeds_if_needed(dummy, builder, cash=1040.0, reserve=300.0)
    actions = builder.build()
    
    # Market actions should be empty (no seed purchases allowed)
    assert actions["market"] == []


def test_e10_buy_land_execution_on_day_12():
    """Verify BUY_LAND Q1 executes on Day 12 when cash >= $1,000."""
    agent = Q1CapitalProtectedROIAgent()
    builder = ActionBuilder()
    
    class DummyState:
        day = 12
        hour = 0
        money = 1050.0
        hires_today = 3  # All 3 hands already hired
        step = 288
        def get_seed_count(self, crop):
            return 10
            
    dummy = DummyState()
    agent._process_market_decisions(dummy, builder, current_workers=4)
    actions = builder.build()
    
    assert actions["market"] == [["BUY_LAND"]]
    assert agent.owned_quadrants == 2


def test_e10_post_expansion_reserve_release():
    """Verify after Q1 is owned, seed buying uses standard $300 reserve floor."""
    agent = Q1CapitalProtectedROIAgent()
    agent.owned_quadrants = 2  # Q1 already owned
    builder = ActionBuilder()
    
    class DummyState:
        day = 13
        hires_today = 0
        def get_seed_count(self, crop):
            return 0
            
    dummy = DummyState()
    
    # Cash is $500. $500 - 60 = 440 >= 300 reserve. Wheat seeds should be purchased.
    agent._buy_seeds_if_needed(dummy, builder, cash=500.0, reserve=300.0)
    actions = builder.build()
    
    assert len(actions["market"]) > 0
    assert actions["market"][0] == ["BUY_SEED", "WHEAT", 6]
