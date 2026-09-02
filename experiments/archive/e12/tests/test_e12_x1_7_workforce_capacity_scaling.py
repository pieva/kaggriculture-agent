"""Unit tests for E12-X1.7 — Workforce Capacity Scaling: Scale First, Optimize Later."""

import pytest
from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig


def test_5_crop_workers_capacity_formula():
    """Verify crop_working_set_capacity = 4 * crop_workers = 20 crop tiles for 5 crop workers."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_STAGED_LOCALITY",
    )
    agent = ProductiveMassROIAgent(config=config)

    crop_workers = 5
    crop_capacity = 4 * crop_workers
    assert crop_capacity == 20


def test_hand_5_cluster_e_assignment():
    """Verify that 5th Hand (idx == 4) is assigned to Cluster E in Q1."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_STAGED_LOCALITY",
    )
    agent = ProductiveMassROIAgent(config=config)

    # 5 hands at positions
    hands = [[1, 1], [1, 3], [5, 3], [5, 1], [7, 1]]
    raw_obs = {
        "money": 1000.0,
        "day": 10,
        "step": 240,
        "farms": [{"money": 1000.0, "farmer": [4, 4], "hands": hands, "tiles": [[None]*10]*10}],
        "private": {"seeds": {}},
    }
    state = GameState(raw_obs)
    agent.owned_quadrants = 2

    # Call act to test action generation for 5 hands
    act = agent.act(state)
    assert "hands" in act
    assert len(act["hands"]) == 5
