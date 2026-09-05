#!/usr/bin/env python3
"""E18.25 D10 labor step.

The candidate keeps E18.22's economics and state-aware execution, but executes
a replanned immutable trajectory whose only planning constraint change is a
minimum of eleven hired hands on D10 (twelve active units with the farmer).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from docs.model_specs.codex.e18.tools.e18_18_capacity_trajectory_planner import (
    CapacityTrajectoryPlanner,
)
from docs.model_specs.codex.e18.tools.e18_22_wheat_jit_d1_controller import (
    WheatJitD1Controller,
)

CONFIG = (
    Path(__file__).resolve().parents[1]
    / "configs/CODEX_E18_25_770_D10_LABOR_STEP_V1.json"
)


def load_candidate_config(path: Path | str = CONFIG) -> dict[str, Any]:
    """Load and validate the deliberately narrow D10 ablation."""
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    expected = {
        "topology": "7-7-0",
        "pasture_fill_target": 14,
        "livestock_resource_cap": 14,
        "livestock_mix": {"COW": 9, "SHEEP": 5},
        "workers_peak_hands": 12,
        "minimum_hands_by_day": {"10": 11},
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"E18.25 invariant mismatch for {key}")
    return config


def build_candidate_plan(path: Path | str = CONFIG) -> dict[str, Any]:
    """Build the candidate plan without mutating the frozen E18.18 artifact."""
    return CapacityTrajectoryPlanner(load_candidate_config(path)).build()


class D10LaborStepController(WheatJitD1Controller):
    """E18.22 controller bound to the D10 labor-step trajectory."""
