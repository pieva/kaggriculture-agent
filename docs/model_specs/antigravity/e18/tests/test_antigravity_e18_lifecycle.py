"""Pytest test suite for Antigravity E18 crop lifecycle and task generation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agricola.strategy.antigravity.antigravity_e18_reactive_reboot_v1 import (
    AntigravityE18ReactiveRebootPolicy,
    create_antigravity_e18_agent,
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


def test_lifecycle_immature_crop_not_harvested() -> None:
    policy = AntigravityE18ReactiveRebootPolicy(config_path=CONFIG_PATH)
    regime_cfg = policy._active_regime_config()

    # Farm with a newly planted CARROT (planted today, age 0, yield_units 1)
    farm = {
        "unlocked_quadrants": ["NW"],
        "tiles": [[None for _ in range(10)] for _ in range(10)],
    }
    farm["tiles"][0][0] = {
        "kind": "PLANT",
        "crop": "CARROT",
        "planted_day": 5,
        "watered_today": False,
        "yield_units": 1,
    }
    private = {"seeds": {"CARROT": 5, "WHEAT": 5}}

    tasks = policy._generate_tasks(farm, private, day=5, owned_quadrants={"Q0"}, regime_cfg=regime_cfg)

    # Must be WATER task, NOT HARVEST
    verbs = [t[2] for t in tasks if t[1] == (0, 0)]
    assert verbs == ["WATER"], f"Expected WATER for day 0 crop, got {verbs}"


def test_lifecycle_mature_crop_is_harvested() -> None:
    policy = AntigravityE18ReactiveRebootPolicy(config_path=CONFIG_PATH)
    regime_cfg = policy._active_regime_config()

    # Farm with a mature CARROT (planted day 1, today is day 4, age 3 >= max_yield_day)
    farm = {
        "unlocked_quadrants": ["NW"],
        "tiles": [[None for _ in range(10)] for _ in range(10)],
    }
    farm["tiles"][0][0] = {
        "kind": "PLANT",
        "crop": "CARROT",
        "planted_day": 1,
        "watered_today": True,
        "yield_units": 4,
    }
    private = {"seeds": {"CARROT": 5, "WHEAT": 5}}

    tasks = policy._generate_tasks(farm, private, day=4, owned_quadrants={"Q0"}, regime_cfg=regime_cfg)

    verbs = [t[2] for t in tasks if t[1] == (0, 0)]
    assert verbs == ["HARVEST"], f"Expected HARVEST for mature crop, got {verbs}"


def test_lifecycle_weed_is_dug() -> None:
    policy = AntigravityE18ReactiveRebootPolicy(config_path=CONFIG_PATH)
    regime_cfg = policy._active_regime_config()

    farm = {
        "unlocked_quadrants": ["NW"],
        "tiles": [[None for _ in range(10)] for _ in range(10)],
    }
    farm["tiles"][1][1] = {"kind": "WEED"}
    private = {"seeds": {"CARROT": 5, "WHEAT": 5}}

    tasks = policy._generate_tasks(farm, private, day=1, owned_quadrants={"Q0"}, regime_cfg=regime_cfg)
    verbs = [t[2] for t in tasks if t[1] == (1, 1)]
    assert verbs == ["DIG"], f"Expected DIG for weed, got {verbs}"
