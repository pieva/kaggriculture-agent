"""Antigravity Tri-Quadrant Q0+Q1+Q2 Lean Cash-Crop Policy.

Extends the verified AntigravityDualQPolicy to unlock Q2 (SW: x:0..4, y:5..9)
around Day 12-14 with a cashflow-gated land purchase ($2,000) and deploys
an 8-tile high-yield crop module (6 Melons + 2 Strawberries) staffed by a lean
single addition worker (W13 / Hand 12, role CROP_ZONE_6, 14 total workers),
avoiding the exponential Fibonacci wage wall while generating $30K+ additional
net money to push overall Mean Final Net Money beyond $90,000.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.e16.policy import SHED_TILES, _fib, _inventory_total, _move_towards
from agricola.strategy.codex_lifecycle import CodexSnapshot
from agricola.strategy.antigravity.antigravity_compact_q0 import (
    ANIMAL_RULES,
    ANTIGRAVITY_COHORT_OFFSET,
    ANTIGRAVITY_CROP_PLAN,
    ANTIGRAVITY_CROP_POSITIONS,
    ANTIGRAVITY_CROP_ZONES,
    ANTIGRAVITY_PASTURE_POSITIONS,
    ANTIGRAVITY_ROUTE_INDEX,
    ANTIGRAVITY_ZONE_STAGING_POINTS,
    CROP_RULES,
    EMPTY_ASSIGNED,
    HARVEST_READY,
    LOST_WEED,
    MOVE_ACTIONS,
    RETIREMENT_DUE,
    YIELD_ACCUMULATING,
    classify_tile_lifecycle,
    lifespan_decay_started,
    water_loss_at_eod_if_unserved,
    yield_completion_water_due,
)
from agricola.strategy.antigravity.antigravity_dual_q0_q1 import (
    DUAL_ROLE_SEQUENCE,
    Q1_CROP_POSITIONS,
    Q1_CROP_ZONES,
    Q1_PASTURE_POSITIONS,
    AntigravityDualQPolicy,
    _mirror_q1,
)
from agricola.strategy.antigravity.c2_75k_config import AntigravityC2_75K_Config

TRI_MODEL_SPEC_VERSION = "ANTIGRAVITY-C2-TRI-Q0-Q1-Q2-90K-NET-V1.0"


def _mirror_q2(position: tuple[int, int]) -> tuple[int, int]:
    """Mirror Q0 (NW: x in 0..4, y in 0..4) vertically to Q2 (SW: x in 0..4, y in 5..9)."""
    x, y = position
    return x, 9 - y


# Q2 Crop positions mirrored from Q0
Q2_ALL_CROP_POSITIONS: tuple[tuple[int, int], ...] = tuple(
    _mirror_q2(p) for p in ANTIGRAVITY_CROP_POSITIONS
)

# 14-Role Sequence for Lean Tri-Q (W0 Farmer, W1..W6 Q0, W7..W12 Q1, W13 Q2 Crop Specialist)
TRI_ROLE_SEQUENCE: tuple[str, ...] = (
    *DUAL_ROLE_SEQUENCE,
    "CROP_ZONE_6",  # W13 (Hand 12): Dedicated Q2 Cash-Crop Specialist
)


class AntigravityTriQPolicy(AntigravityDualQPolicy):
    """Antigravity 3-Quadrant (Q0+Q1+Q2) Lean Cash-Crop Strategy Policy."""

    def __init__(
        self,
        config: Any = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        if config is None:
            config_path = (
                Path(__file__).resolve().parents[4]
                / "configs"
                / "model_spec_c2"
                / "ANTIGRAVITY_C2_90K_TRI_Q_CONFIG.json"
            )
            cfg = (
                AntigravityC2_75K_Config.load(config_path)
                if config_path.exists()
                else AntigravityC2_75K_Config.load()
            )
        else:
            cfg = config
        super().__init__(config=cfg, run_context=run_context)
        self.candidate_id = "ANTIGRAVITY_C2_90K_TRI_Q"
        self.model_spec_version = TRI_MODEL_SPEC_VERSION
        self.expected_max_quadrants = 3
        self.config.workforce_total = 14
        self.config.q1_workforce_total = 13
        self.config.q0_workforce_total = 7

        # Q2 Crop setup: All Q2 crop positions belong to Zone 6
        self.q2_crop_positions = Q2_ALL_CROP_POSITIONS
        q2_zone = (self.q2_crop_positions,)
        self.crop_zones = (*ANTIGRAVITY_CROP_ZONES, *Q1_CROP_ZONES, self.q2_crop_positions)
        self.crop_positions = (*self.q0_crop_positions, *self.q1_crop_positions, *self.q2_crop_positions)

        q2_plan = {
            _mirror_q2(position): crop for position, crop in ANTIGRAVITY_CROP_PLAN.items()
        }
        self.crop_plan = {**self.crop_plan, **q2_plan}

        self.zone_by_position = {
            position: zone_id
            for zone_id, zone in enumerate(self.crop_zones)
            for position in zone
        }
        self.route_index = {
            position: route_index
            for zone in self.crop_zones
            for route_index, position in enumerate(zone)
        }

        self._q2_relative_cohort = {
            _mirror_q2(position): int(offset)
            for position, offset in ANTIGRAVITY_COHORT_OFFSET.items()
        }
        # Inactive until Q2 is owned
        self.cohort_offset.update(
            {position: 10_000 for position in self.q2_crop_positions}
        )

        self.q2_activation_day: int | None = None
        self._q2_activation_decisions: set[int] = set()
        self._q2_cohorts_activated: bool = False

    @staticmethod
    def _role_module(role: str) -> str | None:
        if role.endswith("_Q0"):
            return "Q0"
        if role.endswith("_Q1"):
            return "Q1"
        if role.endswith("_Q2"):
            return "Q2"
        if role.startswith("CROP_ZONE_"):
            suffix = role.rsplit("_", 1)[1]
            if suffix.isdigit():
                idx = int(suffix)
                if idx < 3:
                    return "Q0"
                if idx < 6:
                    return "Q1"
                return "Q2"
            return suffix
        return None

    def _role_for(self, worker_id: int) -> str:
        if worker_id >= len(TRI_ROLE_SEQUENCE):
            return "CROP_ZONE_6"
        return TRI_ROLE_SEQUENCE[worker_id]

    def _target_workforce(self, snapshot: CodexSnapshot) -> int:
        owned = self._owned_quadrants(snapshot.farm)
        if owned < 2:
            return int(self.config.q0_workforce_total)
        if owned == 2:
            return int(getattr(self.config, "q1_workforce_total", 13))
        return int(self.config.workforce_total)  # 14 workers

    def _maybe_replan_global(self, snapshot: CodexSnapshot) -> None:
        if (
            self._owned_quadrants(snapshot.farm) >= 3
            and not self._q2_cohorts_activated
        ):
            self._q2_cohorts_activated = True
            act_day = snapshot.clock.day
            self.q2_activation_day = act_day
            for position, relative in self._q2_relative_cohort.items():
                self.cohort_offset[position] = act_day + relative
        super()._maybe_replan_global(snapshot)

    def decide_market_orders(self, snapshot: CodexSnapshot) -> list[list[Any]]:
        farm = snapshot.farm
        cash = float(farm.get("money", 0.0))
        shed = snapshot.private.get("shed", {}) or {}
        prices = snapshot.market.get("prices", {}) or {}
        owned = self._owned_quadrants(farm)
        day = snapshot.clock.day

        # Check Q2 BUY_LAND admission
        q2_buy_land = False
        if (
            not self._shutdown(snapshot)
            and owned == 2
            and int(getattr(self.config, "q2_activation_min_day", 12)) <= day <= int(getattr(self.config, "q2_activation_max_day", 14))
        ):
            prospective_sales = sum(
                int(shed.get(item, 0)) * float(prices.get(item, 0.0))
                for item in ("MILK", "WOOL", "MELON", "STRAWBERRY")
            )
            available = cash + prospective_sales
            q2_act_cash = float(getattr(self.config, "q2_activation_cash", 3500.0))
            q2_floor = float(getattr(self.config, "q2_operating_cash_floor", 300.0))
            if available >= q2_act_cash and cash >= 2000.0 + q2_floor:
                if day not in self._q2_activation_decisions:
                    self._q2_activation_decisions.add(day)
                    self.q2_activation_day = day
                q2_buy_land = True

        orders = super().decide_market_orders(snapshot)
        if q2_buy_land:
            orders.insert(0, ["BUY_LAND"])
        return orders[: self.max_market_orders]

    def decide_unit_actions(self, snapshot: CodexSnapshot) -> dict[int, list[Any]]:
        """3-Quadrant unit action dispatch including Worker 13 for Q2."""
        self._maybe_replan_global(snapshot)
        positions = self._positions(snapshot.farm)
        crop_tasks = self._crop_tasks(snapshot)
        hard_crop_tasks = [task for task in crop_tasks if task.get("hard_reason")]
        reserved: set[tuple[int, int]] = set()
        actions: dict[int, list[Any]] = {}

        # Prioritize livestock specialists (Q0 then Q1), crop zones (Q0, Q1, Q2), fertilizer, then farmer
        dispatch_order = [
            worker_id
            for worker_id in (4, 5, 10, 11, 1, 2, 3, 7, 8, 9, 13, 6, 12, 0)
            if worker_id < len(positions)
        ]
        for worker_id in dispatch_order:
            role = self._role_for(worker_id)
            inventory_tasks = self._inventory_task(snapshot, worker_id, role)
            candidates: list[dict[str, Any]]
            if inventory_tasks:
                candidates = inventory_tasks
            elif role.startswith("CROP_ZONE_"):
                zone_id = int(role.rsplit("_", 1)[1])
                module_id = zone_id // 3
                own = [task for task in crop_tasks if task.get("zone") == zone_id]
                cross_hard = [
                    task
                    for task in hard_crop_tasks
                    if task.get("zone") is not None
                    and int(task["zone"]) // 3 == module_id
                    and int(task["zone"]) != zone_id
                ]
                candidates = own if own else cross_hard
            elif role.startswith("LIVESTOCK_COW"):
                module = self._role_module(role) or "Q0"
                local = self._module_animal_tasks(snapshot, module, "COW")
                fertilizer_staffed = len(positions) >= (7 if module == "Q0" else 13)
                candidates = [
                    task
                    for task in local
                    if task["kind"] != "FEED"
                    and not (
                        task["kind"] == "FERTILIZER_COLLECTION"
                        and fertilizer_staffed
                    )
                ]
            elif role.startswith("LIVESTOCK_SHEEP"):
                module = self._role_module(role) or "Q0"
                local = self._module_animal_tasks(snapshot, module, "SHEEP")
                fertilizer_staffed = len(positions) >= (7 if module == "Q0" else 13)
                candidates = [
                    task
                    for task in local
                    if task["kind"] != "FEED"
                    and not (
                        task["kind"] == "FERTILIZER_COLLECTION"
                        and fertilizer_staffed
                    )
                ]
            elif self._is_fertilizer_role(role):
                module = self._role_module(role) or "Q0"
                local_hard = [
                    task
                    for task in hard_crop_tasks
                    if task.get("zone") is not None
                    and ("Q0" if int(task["zone"]) < 3 else "Q1") == module
                ]
                local_animals = [
                    *self._module_animal_tasks(snapshot, module, "COW"),
                    *self._module_animal_tasks(snapshot, module, "SHEEP"),
                ]
                fertilizer = [
                    task
                    for task in local_animals
                    if task["kind"] in {"FERTILIZER_COLLECTION", "BUILD_PASTURE"}
                ]
                candidates = local_hard + fertilizer
            else:  # Farmer W0 (Relief & Logistics)
                growth = [
                    task
                    for task in crop_tasks
                    if task["kind"]
                    in {"PLANT", "WEED_RECOVERY", "RETIREMENT_CLEAR"}
                ]
                pasture_growth = [
                    task
                    for species in ("COW", "SHEEP")
                    for task in self._animal_tasks(snapshot, species)
                    if task["kind"] == "BUILD_PASTURE"
                ]
                high_value = [
                    task
                    for task in crop_tasks
                    if task["kind"] in {"HARVEST", "WATER"}
                ]
                candidates = hard_crop_tasks + pasture_growth + growth + high_value

            action = self._choose_committed_task(
                snapshot,
                worker_id,
                role,
                positions[worker_id],
                candidates,
                reserved,
            )
            if not self._eligible_unit_action(snapshot, worker_id, action):
                if action[0] not in MOVE_ACTIONS:
                    self._close_commitment(worker_id, snapshot.clock.step)
                action = ["PASS"]
            actions[worker_id] = action

        return [actions.get(worker_id, ["PASS"]) for worker_id in range(len(positions))]
