#!/usr/bin/env python3
"""E18.26 Jesse-shaped D1-D10 boost on the locked 7-7-0 architecture."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
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
    / "configs/CODEX_E18_26_770_JESSE_BOOST_D10_V1.json"
)


def load_candidate_config(path: Path | str = CONFIG) -> dict[str, Any]:
    """Load and validate the BoostD10 treatment and frozen invariants."""
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    expected = {
        "topology": "7-7-0",
        "pasture_fill_target": 14,
        "livestock_resource_cap": 14,
        "livestock_mix": {"COW": 9, "SHEEP": 5},
        "workers_peak_hands": 12,
        "d10_wheat_fast_cycle_days": [3, 5, 7, 9],
        "d10_full_water_through_day": 10,
        "skip_water_cells_by_day": {
            "5": ["0,2", "1,2", "4,1", "3,1", "2,1", "1,1", "0,1", "0,0"]
        },
        "allow_deferred_spawn_recovery": True,
        "d7_reuse_unlock_workers": True,
        "d13_fertilizer_payroll_bridge": True,
        "minimum_hands_by_day": {
            "1": 5,
            "2": 4,
            "3": 4,
            "4": 5,
            "5": 4,
            "6": 5,
            "7": 8,
            "8": 8,
            "9": 10,
            "10": 11,
        },
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"E18.26 invariant mismatch for {key}")
    return config


def build_candidate_plan(path: Path | str = CONFIG) -> dict[str, Any]:
    """Build the BoostD10 plan without mutating prior candidate artifacts."""
    return CapacityTrajectoryPlanner(load_candidate_config(path)).build()


class JesseBoostD10Controller(WheatJitD1Controller):
    """E18.22 execution guards bound to the Jesse-shaped D1-D10 plan."""

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.skipped_bounded_by_day: defaultdict[int, Counter[str]] = defaultdict(
            Counter
        )

    def _bounded_defer(
        self,
        key: tuple[int, int],
        opcode: str,
        *,
        max_waits: int = 1,
    ) -> None:
        if key[0] == 13 and opcode == "PICKUP":
            # D13 feed is funded at T2 by the fertilizer bridge. The default
            # one-turn pickup wait expires immediately before that settlement.
            max_waits = max(max_waits, 2)
        skipped_before = int(self.skipped_stale[opcode])
        super()._bounded_defer(key, opcode, max_waits=max_waits)
        if int(self.skipped_stale[opcode]) > skipped_before:
            self.skipped_bounded_by_day[key[0]][opcode] += 1

    def _market_orders(
        self,
        observation: dict[str, Any],
        day: int,
        turn: int,
    ) -> list[list[Any]]:
        """Liquidate the D12 fertilizer bridge before the D13 payroll."""
        orders = super()._market_orders(observation, day, turn)
        private = observation.get("private", {}) or {}
        fertilizer = int((private.get("shed", {}) or {}).get("FERTILIZER", 0))
        bridged = orders
        if day == 12 and fertilizer > 0:
            # Monetize fertilizer already dropped by T21. The final D12 drop is
            # retained to finance the second D13 hire batch.
            remaining = [
                order for order in orders if order[:2] != ["SELL", "FERTILIZER"]
            ]
            bridged = [["SELL", "FERTILIZER", fertilizer], *remaining][:10]
        elif day == 13 and turn == 1:
            # Nine hires consume all but one market slot. Pre-stage the four
            # Wheat units needed by the first D13 pickup; the other nine are
            # bought with the second hire batch.
            hires = [order for order in orders if order[0] == "HIRE"][:9]
            bridged = [*hires, ["BUY_PRODUCT", "WHEAT", 4]][:10]
        elif day == 13 and turn == 2 and fertilizer > 0:
            remaining = [
                order for order in orders if order[:2] != ["SELL", "FERTILIZER"]
            ]
            bridged = [["SELL", "FERTILIZER", fertilizer], *remaining][:10]

        if (
            bridged is not orders
            and self.market_trace
            and self.market_trace[-1]["day"] == day
        ):
            self.market_trace[-1]["orders"] = [list(order) for order in bridged]
        return bridged
