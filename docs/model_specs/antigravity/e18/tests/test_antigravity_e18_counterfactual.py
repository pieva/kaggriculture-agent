"""Pytest counterfactual tests for Antigravity E18 opponent reactivity."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agricola.strategy.antigravity.antigravity_e18_reactive_reboot_v1 import (
    AntigravityE18ReactiveRebootPolicy,
)

ROOT = Path(__file__).resolve().parents[5]
CONFIG_PATH = (
    ROOT
    / "docs"
    / "model_specs"
    / "antigravity"
    / "e18"
    / "configs"
    / "ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1.json"
)


def test_counterfactual_regime_divergence() -> None:
    # 1. Low pressure opponent (inert): 0 crops, 0 hands, 2 weeds -> pressure ~ 6
    low_opp = {
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "hands": [],
        "unlocked_quadrants": ["NW"],
        "money": 1000.0,
    }
    low_opp["tiles"][0][0] = {"kind": "WEED"}
    low_opp["tiles"][0][1] = {"kind": "WEED"}

    obs_low = {
        "step": 96,
        "day": 4,
        "hour": 0,
        "player": 0,
        "farms": [
            {"farmer": [4, 4], "hands": [], "unlocked_quadrants": ["NW"], "tiles": [[None]*10]*10, "money": 3000.0},
            low_opp,
        ],
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
    }

    policy_low = AntigravityE18ReactiveRebootPolicy(config_path=CONFIG_PATH)
    snap_low = policy_low._public_opponent_snapshot(obs_low, my_seat=0)
    policy_low._classify_and_select_regime(day=4, hour=0, snapshot=snap_low)

    assert snap_low["pressure_score"] < 25.0
    assert policy_low.current_regime == "BALANCED_SERVICE"
    assert policy_low._active_regime_config()["allowed_quadrants"] == ["Q0", "Q1"]
    assert policy_low._active_regime_config()["target_hands"] <= 5

    # 2. High pressure opponent (active): 15 crops, 4 hands, 2 weeds -> pressure = 15*2 + 2*3 + 4*3 = 48
    high_opp = {
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "hands": [[1, 1], [1, 2], [1, 3], [1, 4]],
        "unlocked_quadrants": ["NW", "NE"],
        "money": 5000.0,
    }
    for i in range(15):
        high_opp["tiles"][i // 5][i % 5] = {"kind": "PLANT", "crop": "CARROT"}
    high_opp["tiles"][3][0] = {"kind": "WEED"}
    high_opp["tiles"][3][1] = {"kind": "WEED"}

    obs_high = {
        "step": 96,
        "day": 4,
        "hour": 0,
        "player": 0,
        "farms": [
            {"farmer": [4, 4], "hands": [], "unlocked_quadrants": ["NW"], "tiles": [[None]*10]*10, "money": 3000.0},
            high_opp,
        ],
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
    }

    policy_high = AntigravityE18ReactiveRebootPolicy(config_path=CONFIG_PATH)
    snap_high = policy_high._public_opponent_snapshot(obs_high, my_seat=0)
    policy_high._classify_and_select_regime(day=4, hour=0, snapshot=snap_high)

    assert snap_high["pressure_score"] >= 25.0
    assert policy_high.current_regime == "EXPANSION_TEMPO"
    assert policy_high._active_regime_config()["allowed_quadrants"] == ["Q0", "Q1", "Q2"]
    assert policy_high._active_regime_config()["target_hands"] >= 7


def test_regime_is_sticky() -> None:
    policy = AntigravityE18ReactiveRebootPolicy(config_path=CONFIG_PATH)

    # First trigger at day 4
    snap1 = {"pressure_score": 50.0}
    policy._classify_and_select_regime(day=4, hour=0, snapshot=snap1)
    assert policy.current_regime == "EXPANSION_TEMPO"
    assert policy.mode_decisions == 1

    # Second call at day 6 with different pressure: MUST REMAIN STICKY
    snap2 = {"pressure_score": 5.0}
    policy._classify_and_select_regime(day=6, hour=0, snapshot=snap2)
    assert policy.current_regime == "EXPANSION_TEMPO"
    assert policy.mode_decisions == 1
