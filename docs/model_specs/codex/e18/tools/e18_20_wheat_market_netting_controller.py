#!/usr/bin/env python3
"""E18.20 market ablation: net same-batch Wheat round trips.

E18.19 reserves Wheat only through tomorrow when deciding what to sell, but
buys Wheat for a horizon that also includes the following day.  Under market
contention this creates alternating SELL/BUY_PRODUCT orders and frequent
same-batch round trips. E18.20 selects only the lossless same-batch netting;
the broader multi-day reserve alignment remains an explicitly rejected
pre-gate variant.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from docs.model_specs.codex.e18.tools.e18_19_retrying_trajectory_controller import (
    RetryingTrajectoryController,
)


class WheatMarketNettingController(RetryingTrajectoryController):
    """Net simultaneous Wheat sales and purchases before market execution."""

    activation_day = 11
    align_sale_and_buy_horizons = False
    net_same_batch_round_trips = True

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.wheat_market_adjustments: Counter[str] = Counter()

    @staticmethod
    def _net_wheat_orders(
        orders: list[list[Any]],
        extra_reserve: int,
        *,
        net_round_trips: bool = True,
    ) -> tuple[list[list[Any]], dict[str, int]]:
        adjusted = [list(order) for order in orders]
        reserve_left = max(0, int(extra_reserve))
        reserved = 0
        for order in adjusted:
            if order[:2] != ["SELL", "WHEAT"]:
                continue
            reduction = min(reserve_left, int(order[2]))
            order[2] = int(order[2]) - reduction
            reserve_left -= reduction
            reserved += reduction

        sell_total = sum(
            int(order[2])
            for order in adjusted
            if order[:2] == ["SELL", "WHEAT"]
        )
        buy_total = sum(
            int(order[2])
            for order in adjusted
            if order[:2] == ["BUY_PRODUCT", "WHEAT"]
        )
        canceled = min(sell_total, buy_total) if net_round_trips else 0
        sell_remaining = sell_total - canceled
        buy_remaining = buy_total - canceled
        output: list[list[Any]] = []
        for order in adjusted:
            if order[:2] == ["SELL", "WHEAT"]:
                quantity = min(int(order[2]), sell_remaining)
                sell_remaining -= quantity
                if quantity:
                    output.append(["SELL", "WHEAT", quantity])
            elif order[:2] == ["BUY_PRODUCT", "WHEAT"]:
                quantity = min(int(order[2]), buy_remaining)
                buy_remaining -= quantity
                if quantity:
                    output.append(["BUY_PRODUCT", "WHEAT", quantity])
            else:
                output.append(order)
        return output, {
            "reserved_sell_units": reserved,
            "netted_round_trip_units": canceled,
        }

    def _market_orders(
        self,
        observation: dict[str, Any],
        day: int,
        turn: int,
    ) -> list[list[Any]]:
        orders = super()._market_orders(observation, day, turn)
        if day < self.activation_day:
            return orders

        tomorrow = self._remaining(
            day, turn, "pickup", include_tomorrow=True
        )
        buy_horizon = self._remaining_horizon(
            day, turn, "pickup", horizon_days=2
        )
        extra_reserve = (
            max(
                0,
                int(buy_horizon.get("WHEAT", 0))
                - int(tomorrow.get("WHEAT", 0)),
            )
            if self.align_sale_and_buy_horizons
            else 0
        )
        adjusted, metrics = self._net_wheat_orders(
            orders,
            extra_reserve,
            net_round_trips=self.net_same_batch_round_trips,
        )
        self.wheat_market_adjustments.update(metrics)
        if adjusted != orders:
            self.wheat_market_adjustments["adjusted_turns"] += 1
        return adjusted
