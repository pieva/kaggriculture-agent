#!/usr/bin/env python3
"""E18.23 pre-funds the D10 SW unlock with one earlier JIT day."""

from __future__ import annotations

from typing import Any

from docs.model_specs.codex.e18.tools.e18_19_retrying_trajectory_controller import (
    _farm,
)
from docs.model_specs.codex.e18.tools.e18_22_wheat_jit_d1_controller import (
    WheatJitD1Controller,
)


class SwUnlockLiquidityController(WheatJitD1Controller):
    """Activate validated Wheat JIT on D10 so SW is unlocked before D11."""

    activation_day = 10

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.unlock_first_seen: dict[str, dict[str, int]] = {}

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        day = int(observation.get("day", 0)) + 1
        turn = int(observation.get("hour", 0)) + 1
        farm = _farm(observation, self.seat)
        for quadrant in farm.get("unlocked_quadrants", []) or []:
            self.unlock_first_seen.setdefault(
                str(quadrant), {"day": day, "turn": turn}
            )
        return super().__call__(observation, configuration)
