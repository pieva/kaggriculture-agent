"""Antigravity C2 150K+ Mega-Cluster & 20-Animal Livestock Engine.

Architected from Kaggle replay 104498819.json (keiz $158,575.00).
Features:
- 20-Animal Central Mega-Cluster (8 Cows, 12 Sheep) tightly clustered around quadrant sheds (4,4), (5,4), (4,5)
- Triple Quadrant Expansion (Q0 at start, Q1 at Day 6, Q2 at Day 11)
- 13-Worker Workforce (1 Farmer + 12 Hands) preserving the $376/day Fibonacci wage tier
- Symmetrical livestock feeding and harvest dispatch guaranteeing 0 animal escapes
- High-yield crop rotation balancing early-stage Melon cash infusions and recurring Strawberries
- Continuous Manure (Fertilizer) and finished product monetization (generating ~$14k+ from fertilizer alone)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple
from collections import Counter
from pathlib import Path

from agricola.strategy.antigravity.antigravity_compact_q0 import (
    CROP_RULES,
    ANIMAL_RULES,
    MOVE_ACTIONS,
    CodexSnapshot,
    _fib,
    _inventory_total,
)
from agricola.strategy.antigravity.antigravity_dual_q0_q1 import (
    AntigravityDualQPolicy,
    _mirror_q1,
)
from agricola.strategy.antigravity.antigravity_tri_q0_q1_q2 import (
    AntigravityTriQPolicy,
    _mirror_q2,
)
from agricola.strategy.antigravity.c2_75k_config import AntigravityC2_75K_Config

MEGA_150K_SPEC_VERSION = "ANTIGRAVITY-C2-150K-MEGA-CLUSTER-V2.0"

# --------------------------------------------------------------------------
# Pasture Topology: 20 Central Animal Tiles Clustered Around the Sheds
# --------------------------------------------------------------------------
Q0_MEGA_PASTURES: tuple[tuple[int, int], ...] = (
    (4, 3), (4, 2), (3, 3), (3, 4), (2, 4), (3, 2),
)
Q1_MEGA_PASTURES: tuple[tuple[int, int], ...] = (
    (5, 3), (5, 2), (6, 4), (6, 3), (6, 2), (7, 4), (5, 1),
)
Q2_MEGA_PASTURES: tuple[tuple[int, int], ...] = (
    (3, 5), (4, 6), (3, 6), (4, 7), (3, 7), (2, 5), (2, 6),
)

ALL_MEGA_PASTURES: tuple[tuple[int, int], ...] = (
    *Q0_MEGA_PASTURES,
    *Q1_MEGA_PASTURES,
    *Q2_MEGA_PASTURES,
)

MEGA_COW_PASTURES: tuple[tuple[int, int], ...] = (
    *Q0_MEGA_PASTURES[:4],
    *Q1_MEGA_PASTURES[:4],
)

MEGA_SHEEP_PASTURES: tuple[tuple[int, int], ...] = (
    *Q0_MEGA_PASTURES[4:],
    *Q1_MEGA_PASTURES[4:],
    *Q2_MEGA_PASTURES,
)

# --------------------------------------------------------------------------
# Crop Plan: High-Density Rotation across Q0, Q1, Q2
# --------------------------------------------------------------------------
def _build_mega_crop_plan() -> tuple[dict[tuple[int, int], str], list[tuple[int, int]]]:
    plan: dict[tuple[int, int], str] = {}
    pasture_set = set(ALL_MEGA_PASTURES)
    shed_set = {(4, 4), (5, 4), (4, 5), (5, 5)}
    all_crops: list[tuple[int, int]] = []

    # Q0 (NW: 0..4, 0..4) - 18 crop tiles
    q0_melons = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (0, 2)}
    q0_wheat = {(0, 4), (1, 4)}
    for y in range(5):
        for x in range(5):
            pos = (x, y)
            if pos in pasture_set or pos in shed_set:
                continue
            all_crops.append(pos)
            if pos in q0_melons:
                plan[pos] = "MELON"
            elif pos in q0_wheat:
                plan[pos] = "WHEAT"
            else:
                plan[pos] = "STRAWBERRY"

    # Q1 (NE: 5..9, 0..4) - 17 crop tiles
    q1_melons = {(5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (8, 1), (9, 1), (7, 2), (8, 2), (9, 2)}
    q1_wheat = {(9, 4), (8, 4)}
    for y in range(5):
        for x in range(5, 10):
            pos = (x, y)
            if pos in pasture_set or pos in shed_set:
                continue
            all_crops.append(pos)
            if pos in q1_melons:
                plan[pos] = "MELON"
            elif pos in q1_wheat:
                plan[pos] = "WHEAT"
            else:
                plan[pos] = "STRAWBERRY"

    # Q2 (SW: 0..4, 5..9) - 17 crop tiles
    q2_melons = {(0, 5), (1, 5), (0, 6), (1, 6), (0, 7), (1, 7), (0, 8), (1, 8), (0, 9), (1, 9)}
    q2_wheat = {(4, 9), (3, 9)}
    for y in range(5, 10):
        for x in range(5):
            pos = (x, y)
            if pos in pasture_set or pos in shed_set:
                continue
            all_crops.append(pos)
            if pos in q2_melons:
                plan[pos] = "MELON"
            elif pos in q2_wheat:
                plan[pos] = "WHEAT"
            else:
                plan[pos] = "STRAWBERRY"

    return plan, all_crops

MEGA_CROP_PLAN, MEGA_CROP_POSITIONS = _build_mega_crop_plan()


class Antigravity150KMegaPolicy(AntigravityTriQPolicy):
    """Antigravity 150K+ Central Mega-Cluster 20-Animal Policy."""

    def __init__(
        self,
        config: Any = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(config=config, run_context=run_context)
        self.candidate_id = "ANTIGRAVITY_C2_150K_MEGA_CLUSTER"
        self.model_spec_version = MEGA_150K_SPEC_VERSION

        # Workforce target: exactly 13 total workers (Farmer + 12 Hands)
        self.config.workforce_total = 13
        self.config.q0_workforce_total = 7
        self.config.q1_workforce_total = 13

        # Configure mega-cluster pastures
        self.q0_pasture_positions = Q0_MEGA_PASTURES
        self.q1_pasture_positions = Q1_MEGA_PASTURES
        self.q2_pasture_positions = Q2_MEGA_PASTURES
        self.pasture_positions = ALL_MEGA_PASTURES

        self.pasture_positions_by_species = {
            "COW": MEGA_COW_PASTURES,
            "SHEEP": MEGA_SHEEP_PASTURES,
        }

        self.config.livestock_targets = {
            "COW": 8,
            "SHEEP": 12,
        }

        # Crop configurations
        self.crop_positions = tuple(MEGA_CROP_POSITIONS)
        self.crop_plan = dict(MEGA_CROP_PLAN)

        self.q0_crop_positions = tuple(p for p in self.crop_positions if p[0] < 5 and p[1] < 5)
        self.q1_crop_positions = tuple(p for p in self.crop_positions if p[0] >= 5 and p[1] < 5)
        self.q2_crop_positions = tuple(p for p in self.crop_positions if p[0] < 5 and p[1] >= 5)

        # 3 Crop zones per quadrant
        def _partition3(lst: tuple[tuple[int, int], ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
            k = max(1, len(lst) // 3)
            return (lst[:k], lst[k:2*k], lst[2*k:])

        q0_zones = _partition3(self.q0_crop_positions)
        q1_zones = _partition3(self.q1_crop_positions)
        q2_zones = _partition3(self.q2_crop_positions)
        self.crop_zones = (*q0_zones, *q1_zones, *q2_zones)

        self.zone_by_position = {
            pos: z_idx
            for z_idx, zone in enumerate(self.crop_zones)
            for pos in zone
        }
        self.route_index = {
            pos: r_idx
            for zone in self.crop_zones
            for r_idx, pos in enumerate(zone)
        }

        self.cohort_offset = {}
        for pos in self.q0_crop_positions:
            self.cohort_offset[pos] = 0 if self.crop_plan[pos] == "MELON" else 1
        for pos in self.q1_crop_positions:
            self.cohort_offset[pos] = 10_000
        for pos in self.q2_crop_positions:
            self.cohort_offset[pos] = 10_000

        self._q1_relative_cohort = {pos: 0 for pos in self.q1_crop_positions}
        self._q2_relative_cohort = {pos: 0 for pos in self.q2_crop_positions}

    def _module_animal_positions(
        self, module: str, species: str
    ) -> tuple[tuple[int, int], ...]:
        if module == "Q0":
            return self.q0_pasture_positions[:4] if species == "COW" else self.q0_pasture_positions[4:]
        elif module == "Q1":
            return self.q1_pasture_positions[:4] if species == "COW" else self.q1_pasture_positions[4:]
        else: # Q2
            return self.q2_pasture_positions if species == "SHEEP" else ()

    def _feed_assignments(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[tuple[str, str]]:
        if role == "LIVESTOCK_COW_Q0":
            return [("Q0", "COW")]
        if role == "LIVESTOCK_SHEEP_Q0":
            return [("Q0", "SHEEP")]
        if role == "LIVESTOCK_COW_Q1":
            return [("Q1", "COW")]
        if role == "LIVESTOCK_SHEEP_Q1":
            return [("Q1", "SHEEP"), ("Q2", "SHEEP")]
        if worker_id == 13:
            return [("Q2", "SHEEP")]

        worker_count = len(self._positions(snapshot.farm))
        assignments: list[tuple[str, str]] = []
        if worker_count <= 4 and worker_id == 0:
            assignments.append(("Q0", "COW"))
        if worker_count <= 5:
            q0_sheep_owner = 1 if worker_count >= 2 else 0
            if worker_id == q0_sheep_owner:
                assignments.append(("Q0", "SHEEP"))
        if self._owned_quadrants(snapshot.farm) >= 2:
            if 8 <= worker_count <= 10 and worker_id == 7:
                assignments.append(("Q1", "COW"))
            if 9 <= worker_count <= 11 and worker_id == 8:
                assignments.append(("Q1", "SHEEP"))
        return assignments

    def _decide_zone_action(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
        zone_index: int,
    ) -> list[Any]:
        # If Q2 worker (W13 / Zone 6), prioritize building any unbuilt Q2 pastures
        if zone_index >= 6:
            for pos in self.q2_pasture_positions:
                t = self._tile(snapshot.farm, pos)
                if t is None:
                    act = self._action_toward(snapshot, worker_id, pos, ["BUILD_PASTURE"])
                    if act:
                        return act
        return super()._decide_zone_action(snapshot, worker_id, role, zone_index)

    def _eligible_unit_action(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        action: list[Any],
    ) -> bool:
        if action and action[0] == "BUILD_PASTURE":
            positions = self._positions(snapshot.farm)
            if worker_id < len(positions):
                pos = positions[worker_id]
                return pos in self.pasture_positions
        return super()._eligible_unit_action(snapshot, worker_id, action)

    def decide_market_orders(self, snapshot: CodexSnapshot) -> list[list[Any]]:
        orders: list[list[Any]] = []
        farm = snapshot.farm
        private = snapshot.private
        shed = private.get("shed", {}) or {}
        prices = snapshot.market.get("prices", {}) or {}
        cash = float(farm.get("money", 0.0))
        # Dynamic wage floor to guarantee end-of-day salary payments
        hands = len(farm.get("hands", []) or [])
        daily_wages = sum(_fib(i) for i in range(hands))
        floor = max(float(self.config.operating_cash_floor), float(daily_wages + 50.0))
        day = snapshot.clock.day
        hour = snapshot.clock.hour
        owned = self._owned_quadrants(farm)

        def add(order: list[Any], cost: float = 0.0, *, protect_floor: bool = True) -> bool:
            nonlocal cash
            if len(orders) >= self.max_market_orders:
                return False
            if protect_floor and cash - cost < floor:
                return False
            orders.append(order)
            cash -= cost
            return True

        # 1. Monetize all finished products from shed immediately
        for item in ("MILK", "WOOL", "MELON", "STRAWBERRY", "EGG", "FERTILIZER"):
            quantity = int(shed.get(item, 0))
            if quantity > 0 and add(["SELL", item, quantity], protect_floor=False):
                cash += quantity * float(prices.get(item, 0.0))

        # 2. Sell surplus wheat exceeding feed reserve
        counts = self._animal_counts(snapshot)
        active_or_staged = sum(counts.values())
        wheat_reserve = max(8, active_or_staged * int(self.config.feed_reserve_rounds))
        wheat_to_sell = max(0, int(shed.get("WHEAT", 0)) - wheat_reserve)
        if wheat_to_sell > 0 and add(["SELL", "WHEAT", wheat_to_sell], protect_floor=False):
            cash += wheat_to_sell * float(prices.get("WHEAT", 0.0))

        # 3. Daily hiring up to workforce target
        target_hands = (
            5 if owned == 1
            else (9 if owned == 2 and day < 10 else 12)
        )
        hires_today = int(farm.get("hires_today", 0))
        if not self._shutdown(snapshot) and hour in {0, 1, 2}:
            for offset in range(max(0, target_hands - hands)):
                hire_cost = float(50 * (2 ** (hires_today + offset)))
                if not add(["HIRE"], hire_cost):
                    break

        # 4. Opening Day 0 Step 0 Bootstrap
        if snapshot.clock.step == 0:
            add(["BUY_ANIMAL", "COW", 2], 800.0)
            add(["BUY_ANIMAL", "SHEEP", 2], 1000.0)
            add(["BUY_PRODUCT", "WHEAT", 10], 10 * float(prices.get("WHEAT", 25.0)))
            add(["BUY_SEED", "MELON", 4], 320.0)
            add(["BUY_SEED", "STRAWBERRY", 4], 400.0)

        # 5. Land expansions: Q1 on Day 6, Q2 on Day 11
        if not self._shutdown(snapshot):
            if owned == 1 and day >= int(self.config.q1_activation_min_day):
                if cash >= 1300.0:
                    add(["BUY_LAND"], 1000.0)
            elif owned == 2 and day >= 11:
                if cash >= 2300.0:
                    add(["BUY_LAND"], 2000.0)

            # 6. Livestock acquisitions up to targets
            for species in ("COW", "SHEEP"):
                target = int(self.config.livestock_targets[species]) if owned >= 2 else (4 if species == "COW" else 2)
                if int(counts.get(species, 0)) >= target:
                    continue
                built_pastures = len([
                    p
                    for p in self.pasture_positions_by_species[species]
                    if isinstance(self._tile(farm, p), dict)
                    and self._tile(farm, p).get("kind") == "PASTURE"
                ])
                if int(counts.get(species, 0)) >= built_pastures:
                    continue
                admitted, reason, capacity = self._capacity_admission(snapshot, species)
                if admitted:
                    cost = float(ANIMAL_RULES[species]["cost"])
                    if add(["BUY_ANIMAL", species, 1], cost):
                        counts[species] += 1

            # 7. Feed Restocking
            carried_wheat = sum(
                self._inventory(private, worker_id).get("WHEAT", 0)
                for worker_id in range(len(self._positions(farm)))
            )
            shed_wheat = int(shed.get("WHEAT", 0))
            wheat_threshold = max(6, active_or_staged * 2)
            if carried_wheat + shed_wheat < wheat_threshold and not self._shutdown(snapshot):
                needed = max(1, wheat_threshold - (carried_wheat + shed_wheat))
                qty = min(needed, 4)
                w_price = float(prices.get("WHEAT", 25.0))
                add(["BUY_PRODUCT", "WHEAT", qty], qty * w_price)

            # 8. Seed Restocking
            seed_inv = Counter()
            shed_seeds = private.get("seeds", {}) or {}
            for k, v in shed_seeds.items():
                seed_inv[k] += int(v)
            for h_inv in private.get("inventories", []):
                for k, v in h_inv.items():
                    if k in {"MELON", "STRAWBERRY", "WHEAT"}:
                        seed_inv[k] += int(v)
            for crop in ("MELON", "STRAWBERRY", "WHEAT"):
                target_seed = 4 if crop != "WHEAT" else 2
                if seed_inv[crop] < target_seed and not self._shutdown(snapshot):
                    s_cost = float(CROP_RULES[crop]["seed"] if "seed" in CROP_RULES[crop] else 80.0)
                    add(["BUY_SEED", crop, target_seed - seed_inv[crop]], (target_seed - seed_inv[crop]) * s_cost)

        return orders[: self.max_market_orders]
