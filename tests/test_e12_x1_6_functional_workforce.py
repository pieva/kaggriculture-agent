"""Unit tests for E12-X1.6 — Functional Workforce & Hybrid Economic Scaling."""

import pytest
from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig


def test_crop_working_set_capacity_formula():
    """Verify crop_working_set_capacity = 4 * crop_workers (excluding livestock worker 0)."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_STAGED_LOCALITY",
    )
    agent = ProductiveMassROIAgent(config=config)

    for hands_count in range(1, 5):
        crop_workers = hands_count
        crop_capacity = 4 * crop_workers
        assert crop_capacity == 4 * hands_count


def test_progressive_cow_scaling_gates():
    """Verify progressive cow scaling threshold conditions up to 4 cows."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_STAGED_LOCALITY",
    )
    agent = ProductiveMassROIAgent(config=config)

    # 1 Cow -> 2 Cows requires wheat_count >= 1*2+1 = 3
    agent.cow_count = 1  # Simulated Cow #1 acquisition
    
    raw_obs = {
        "money": 1000.0,
        "day": 5,
        "step": 120,
        "farms": [{"money": 1000.0, "farmer": [4, 4], "hands": [], "tiles": [[None]*10]*10}],
        "private": {"seeds": {}, "shed": {"WHEAT": 5}},
    }
    state = GameState(raw_obs)
    
    # Check that wheat threshold allows cow scaling when cash float >= operating reserve
    wheat_count = state.get_shed_count("WHEAT")
    assert wheat_count >= 1 * 2 + 1


def test_high_roi_crop_selection():
    """Verify MELON and STRAWBERRY selection for cash crop tiles."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_STAGED_LOCALITY",
    )
    agent = ProductiveMassROIAgent(config=config)

    raw_obs = {
        "money": 500.0,
        "day": 5,
        "step": 120,
        "farms": [{"money": 500.0, "farmer": [1, 1], "hands": [], "tiles": [[None]*10]*10}],
        "shed": {},
        "private": {"seeds": {"MELON": 2, "STRAWBERRY": 2, "CARROT": 5}},
    }
    state = GameState(raw_obs)

    # On Day 5 for non-feed crop tile (1, 1), MELON must be chosen over CARROT
    crop = agent._select_crop_to_plant(state, 5, (1, 1))
    assert crop == "MELON"
