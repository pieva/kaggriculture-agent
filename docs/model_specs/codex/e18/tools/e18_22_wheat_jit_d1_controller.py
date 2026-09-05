#!/usr/bin/env python3
"""E18.22 Wheat just-in-time procurement through D+1.

E18.21 showed that protecting Wheat bought for D+2 reduces missed feeds but
destroys more liquidity than it creates.  This ablation takes the inverse
approach: it preserves the in-flight pickup sale guard, but caps Wheat market
purchases at the shortage for current in-flight/pending pickups plus D+1.
Purchases attributable only to D+2 are removed before market execution.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from docs.model_specs.codex.e18.tools.e18_21_wheat_obligation_ledger_controller import (
    WheatObligationLedgerController,
)


class WheatJitD1Controller(WheatObligationLedgerController):
    """Buy Wheat only for worker obligations due no later than tomorrow."""

    activation_day = 11
    procurement_horizon_days = 1

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.wheat_jit_metrics: Counter[str] = Counter()

    @staticmethod
    def _cap_wheat_buys(
        orders: list[list[Any]], cap: int
    ) -> tuple[list[list[Any]], int]:
        """Cap aggregate Wheat buys while preserving all unrelated orders."""
        left = max(0, int(cap))
        removed = 0
        adjusted: list[list[Any]] = []
        for order in orders:
            if order[:2] != ["BUY_PRODUCT", "WHEAT"]:
                adjusted.append(list(order))
                continue
            quantity = min(int(order[2]), left)
            removed += int(order[2]) - quantity
            left -= quantity
            if quantity:
                adjusted.append(["BUY_PRODUCT", "WHEAT", quantity])
        return adjusted, removed

    def _market_orders(
        self,
        observation: dict[str, Any],
        day: int,
        turn: int,
    ) -> list[list[Any]]:
        orders = super()._market_orders(observation, day, turn)
        if day < self.activation_day:
            return orders

        private = observation.get("private", {}) or {}
        shed_wheat = int((private.get("shed", {}) or {}).get("WHEAT", 0))
        near_by_worker = self._worker_pickup_obligations(day, turn, day)
        if day < 30:
            near_by_worker.update(
                self._worker_pickup_obligations(day, turn, day + 1)
            )
        near_required = sum(near_by_worker.values())
        buy_cap = max(0, near_required - shed_wheat)
        adjusted, removed = self._cap_wheat_buys(orders, buy_cap)
        requested = self._wheat_order_units(orders, "BUY_PRODUCT")
        retained = self._wheat_order_units(adjusted, "BUY_PRODUCT")
        self.wheat_jit_metrics.update(
            {
                "nominal_buy_units": requested,
                "retained_buy_units": retained,
                "removed_d2_buy_units": removed,
            }
        )
        if removed:
            self.wheat_jit_metrics["adjusted_turns"] += 1
        return adjusted
