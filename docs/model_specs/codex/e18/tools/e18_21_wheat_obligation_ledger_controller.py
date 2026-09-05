#!/usr/bin/env python3
"""E18.21 worker-aware Wheat obligation ledger.

E18.20 removes same-batch Wheat round trips, but its parent advances a worker's
route cursor before composing market orders.  A Wheat pickup emitted in the
current step therefore disappears from the aggregate requirement even though
the engine has not executed it yet.  This controller records those in-flight
pickup obligations per worker and prevents the market bridge from selling the
same units.

The ledger also source-tags only far-horizon Wheat that the controller actually
requests from the market.  Tagged units are protected until the obligation
enters the parent's existing D+1 reserve.  Harvested Wheat remains free, which
avoids the over-reservation regression rejected during E18.20 development.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from docs.model_specs.codex.e18.tools.e18_20_wheat_market_netting_controller import (
    WheatMarketNettingController,
)


class WheatObligationLedgerController(WheatMarketNettingController):
    """Protect in-flight and source-tagged Wheat without changing the route."""

    activation_day = 11
    procurement_horizon_days = 2
    protect_inflight_pickups = True
    protect_procurement_contracts = False

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.inflight_wheat: dict[tuple[int, int], Counter[int]] = defaultdict(
            Counter
        )
        self.wheat_contracts: Counter[tuple[int, int]] = Counter()
        self.wheat_ledger_metrics: Counter[str] = Counter()
        self.wheat_ledger_trace: list[dict[str, Any]] = []

    def _worker_command(
        self,
        day: int,
        turn: int,
        worker: int,
        farm: dict[str, Any],
        private: dict[str, Any],
    ) -> tuple[list[Any], dict[str, Any] | None]:
        command, row = super()._worker_command(
            day, turn, worker, farm, private
        )
        if command[:2] == ["PICKUP", "WHEAT"]:
            self.inflight_wheat[(day, turn)][worker] += int(command[2])
        return command, row

    def _worker_pickup_obligations(
        self,
        day: int,
        turn: int,
        due_day: int,
    ) -> Counter[int]:
        """Return remaining Wheat pickup units keyed by assigned worker."""
        obligations: Counter[int] = Counter()
        for (route_day, worker), rows in self.routes.items():
            if route_day != due_day:
                continue
            start = self.cursors[(route_day, worker)] if due_day == day else 0
            for index, row in enumerate(rows[start:], start=start):
                if row["opcode"] != "PICKUP":
                    continue
                args = row.get("arguments", {}) or {}
                if args.get("item") != "WHEAT":
                    continue
                if due_day == day and int(row["turn"]) < turn:
                    continue
                units = self.pickup_remaining.get(
                    (route_day, worker, index), int(args.get("units", 1))
                )
                obligations[worker] += units
        if due_day == day:
            obligations.update(self.inflight_wheat.get((day, turn), {}))
        return obligations

    def _release_near_contracts(self, day: int) -> int:
        """Release contracts once the parent's D+1 reserve covers them."""
        released = 0
        for key in list(self.wheat_contracts):
            if key[0] <= day + 1:
                released += int(self.wheat_contracts.pop(key))
        return released

    def _cap_contracts_to_shed(self, shed_wheat: int) -> int:
        """Reconcile nominal contracts with Wheat physically in the shed."""
        available = max(0, int(shed_wheat))
        removed = 0
        for key in sorted(self.wheat_contracts):
            units = int(self.wheat_contracts[key])
            kept = min(units, available)
            available -= kept
            removed += units - kept
            if kept:
                self.wheat_contracts[key] = kept
            else:
                del self.wheat_contracts[key]
        return removed

    @staticmethod
    def _reduce_wheat_sales(
        orders: list[list[Any]], reserve: int
    ) -> tuple[list[list[Any]], int]:
        """Remove up to ``reserve`` units from Wheat sales, preserving order."""
        left = max(0, int(reserve))
        protected = 0
        adjusted: list[list[Any]] = []
        for order in orders:
            if order[:2] != ["SELL", "WHEAT"]:
                adjusted.append(list(order))
                continue
            reduction = min(left, int(order[2]))
            quantity = int(order[2]) - reduction
            left -= reduction
            protected += reduction
            if quantity:
                adjusted.append(["SELL", "WHEAT", quantity])
        return adjusted, protected

    @staticmethod
    def _wheat_order_units(orders: list[list[Any]], opcode: str) -> int:
        return sum(
            int(order[2])
            for order in orders
            if order[:2] == [opcode, "WHEAT"]
        )

    def _allocate_contracts(
        self,
        due_day: int,
        obligations: Counter[int],
        units: int,
    ) -> int:
        """Assign newly requested Wheat to concrete worker obligations."""
        left = max(0, int(units))
        allocated = 0
        for worker in sorted(obligations):
            key = (due_day, worker)
            room = max(
                0,
                int(obligations[worker]) - int(self.wheat_contracts[key]),
            )
            quantity = min(left, room)
            if quantity:
                self.wheat_contracts[key] += quantity
                allocated += quantity
                left -= quantity
            if left <= 0:
                break
        return allocated

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
        released = self._release_near_contracts(day)
        reconciled = self._cap_contracts_to_shed(shed_wheat)
        inflight_by_worker = self.inflight_wheat.get((day, turn), Counter())
        inflight = sum(inflight_by_worker.values())
        contracted = sum(self.wheat_contracts.values())
        reserve = (
            inflight if self.protect_inflight_pickups else 0
        ) + (contracted if self.protect_procurement_contracts else 0)
        adjusted, protected = self._reduce_wheat_sales(orders, reserve)

        due_day = min(30, day + self.procurement_horizon_days)
        due_obligations = self._worker_pickup_obligations(
            day, turn, due_day
        )
        pending_near = self._worker_pickup_obligations(day, turn, day)
        pending_near.update(
            self._worker_pickup_obligations(day, turn, min(30, day + 1))
        )
        near_shortage = max(0, sum(pending_near.values()) - shed_wheat)
        bought = self._wheat_order_units(adjusted, "BUY_PRODUCT")
        contractable = max(0, bought - near_shortage)
        allocated = 0
        if self.protect_procurement_contracts and due_day > day + 1:
            allocated = self._allocate_contracts(
                due_day, due_obligations, contractable
            )

        self.wheat_ledger_metrics.update(
            {
                "inflight_pickup_units": inflight,
                "protected_sale_units": protected,
                "contract_allocated_units": allocated,
                "contract_released_units": released,
                "contract_reconciled_units": reconciled,
            }
        )
        if adjusted != orders:
            self.wheat_ledger_metrics["adjusted_turns"] += 1
        if turn in {1, 2, 24} or inflight or protected or allocated:
            self.wheat_ledger_trace.append(
                {
                    "day": day,
                    "turn": turn,
                    "shed_wheat": shed_wheat,
                    "inflight_by_worker": dict(sorted(inflight_by_worker.items())),
                    "pending_near_by_worker": dict(sorted(pending_near.items())),
                    "due_day": due_day,
                    "due_by_worker": dict(sorted(due_obligations.items())),
                    "contracts": {
                        f"D{contract_day}:W{worker}": units
                        for (contract_day, worker), units in sorted(
                            self.wheat_contracts.items()
                        )
                    },
                    "orders_before_ledger": orders,
                    "orders_after_ledger": adjusted,
                }
            )
        return adjusted
