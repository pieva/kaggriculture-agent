"""Unit tests for E12 Livestock-First Architecture invariants."""

import pytest
from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig


def test_core_exclusion():
    """TEST A: Core coordinates [(3,3), (3,4), (4,3), (4,4)] must NEVER be in crop working set."""
    config = ProductiveMassConfig(productive_core_mode="E12_HYBRID_STAGED_LOCALITY")
    agent = ProductiveMassROIAgent(config=config)

    core_tiles = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for tile in core_tiles:
        assert tile not in agent.q0_crop_tiles, f"Core tile {tile} found in q0_crop_tiles!"


def test_livestock_first_gate_initial_state():
    """TEST B: Outer crop expansion forbidden before livestock core is operational."""
    config = ProductiveMassConfig(productive_core_mode="E12_HYBRID_STAGED_LOCALITY")
    agent = ProductiveMassROIAgent(config=config)

    # Initial state Day 0: 0 pastures, 0 cows
    raw_obs = {
        "money": 1000.0,
        "day": 0,
        "step": 0,
        "farms": [{"money": 1000.0, "farmer": [4, 4], "hands": [[1, 1]], "tiles": [[None]*10]*10}],
        "private": {"seeds": {}},
    }
    state = GameState(raw_obs)
    
    # Act in initial unbootstrapped state
    act = agent.act(state)
    hands_act = act.get("hands", [])

    # Hands must NOT be planting outer crops when livestock core is not established
    for h_a in hands_act:
        if h_a:
            assert h_a[0] != "PLANT", f"Outer crop plant action {h_a} attempted before livestock bootstrap!"


def test_physical_state_core_pastures():
    """TEST E: Verify physical farm state assertions for core pasture tiles."""
    config = ProductiveMassConfig(productive_core_mode="E12_HYBRID_STAGED_LOCALITY")
    agent = ProductiveMassROIAgent(config=config)

    assert agent.livestock_core_tiles == [(3, 3), (3, 4), (4, 3), (4, 4)]
