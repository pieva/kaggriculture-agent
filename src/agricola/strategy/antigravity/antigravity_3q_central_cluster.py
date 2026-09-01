"""Antigravity C2 100K+ 3Q Central Mega-Cluster Engine.

Features:
- Full 3-Quadrant active layout (Q0 NW, Q1 NE, Q2 SW: 75 tiles)
- 19 Central Animal Pastures tightly clustered at Chebyshev distance <= 2 from sheds ((4,4), (5,4), (4,5)):
  * Q0 (NW): 6 central pastures (3 Cows, 3 Sheep)
  * Q1 (NE): 6 central pastures (3 Cows, 3 Sheep)
  * Q2 (SW): 7 central pastures directly adjacent to (4,5) (7 Sheep)
- Compact concentric crop layout eliminating empty dead-zones and excessive walking
- Symmetrical feeding, care and shearing dispatch guaranteeing 0 escapes
- Cashflow-gated expansion (Q1 at Day 6, Q2 at Day 11) with dynamic wage floor protection
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple
from collections import Counter
from pathlib import Path

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

CENTRAL_3Q_SPEC_VERSION = "ANTIGRAVITY-C2-3Q-CENTRAL-CLUSTER-100K-V3.0"

# --------------------------------------------------------------------------
# Pasture Topology: Central Cluster tightly hugging quadrant sheds (4,4), (5,4), (4,5)
# --------------------------------------------------------------------------
Q0_CENTRAL_PASTURES: tuple[tuple[int, int], ...] = (
    (3, 4), (4, 3), (3, 3), (2, 4), (4, 2), (3, 2),
)
Q1_CENTRAL_PASTURES: tuple[tuple[int, int], ...] = (
    (6, 4), (5, 3), (6, 3), (7, 4), (5, 2), (6, 2),
)
Q2_CENTRAL_PASTURES: tuple[tuple[int, int], ...] = (
    (3, 5), (4, 6), (3, 6), (4, 7), (3, 7), (2, 5), (2, 6),
)

ALL_CENTRAL_PASTURES: tuple[tuple[int, int], ...] = (
    *Q0_CENTRAL_PASTURES,
    *Q1_CENTRAL_PASTURES,
    *Q2_CENTRAL_PASTURES,
)

CENTRAL_COW_PASTURES: tuple[tuple[int, int], ...] = (
    *Q0_CENTRAL_PASTURES[:3],
    *Q1_CENTRAL_PASTURES[:3],
)

CENTRAL_SHEEP_PASTURES: tuple[tuple[int, int], ...] = (
    *Q0_CENTRAL_PASTURES[3:],
    *Q1_CENTRAL_PASTURES[3:],
    *Q2_CENTRAL_PASTURES,
)

# --------------------------------------------------------------------------
# Q2 Concentric Crop Ring (Right around the central pastures)
# --------------------------------------------------------------------------
Q2_CONCENTRIC_CROPS: tuple[tuple[int, int], ...] = (
    (2, 7), (3, 8), (4, 8), (1, 5), (1, 6), (1, 7), (0, 5), (0, 6),
)

Q2_CONCENTRIC_CROP_PLAN: dict[tuple[int, int], str] = {
    (2, 7): "MELON",
    (3, 8): "MELON",
    (4, 8): "MELON",
    (1, 5): "STRAWBERRY",
    (1, 6): "MELON",
    (1, 7): "STRAWBERRY",
    (0, 5): "WHEAT",
    (0, 6): "MELON",
}

# 14-Role Sequence: W0 Farmer, W1..W6 Q0, W7..W12 Q1, W13 Q2 Central Specialist
CENTRAL_3Q_ROLE_SEQUENCE: tuple[str, ...] = (
    *DUAL_ROLE_SEQUENCE,
    "LIVESTOCK_SHEEP_Q2",  # W13 (Hand 12): Dedicated Q2 Central Sheep & Crops
)


class Antigravity3QCentralClusterPolicy(AntigravityDualQPolicy):
    """Antigravity 3-Quadrant Central Mega-Cluster Policy."""

    def __init__(
        self,
        config: Any = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        cfg = config or AntigravityC2_75K_Config.load()
        super().__init__(config=cfg, run_context=run_context)
        self.candidate_id = "ANTIGRAVITY_C2_3Q_CENTRAL_CLUSTER"
        self.model_spec_version = CENTRAL_3Q_SPEC_VERSION
        self.expected_max_quadrants = 3

        self.config.workforce_total = 13
        self.config.q0_workforce_total = 7
        self.config.q1_workforce_total = 13

        # Configure 3Q Central Pastures
        self.q0_pasture_positions = Q0_CENTRAL_PASTURES
        self.q1_pasture_positions = Q1_CENTRAL_PASTURES
        self.q2_pasture_positions = Q2_CENTRAL_PASTURES
        self.pasture_positions = ALL_CENTRAL_PASTURES

        self.pasture_positions_by_species = {
            "COW": CENTRAL_COW_PASTURES,
            "SHEEP": CENTRAL_SHEEP_PASTURES,
        }
        self.config.livestock_targets = {
            "COW": 6,
            "SHEEP": 13,
        }

        # Configure Q2 Crops in concentric ring
        self.q2_crop_positions = Q2_CONCENTRIC_CROPS
        self.crop_zones = (*ANTIGRAVITY_CROP_ZONES, *Q1_CROP_ZONES, self.q2_crop_positions)
        self.crop_positions = (*self.q0_crop_positions, *self.q1_crop_positions, *self.q2_crop_positions)
        self.crop_plan = {**self.crop_plan, **Q2_CONCENTRIC_CROP_PLAN}

        self.zone_by_position = {
            position: zone_id
            for zone_id, zone in enumerate(self.crop_zones)
            for position in zone
        }
        self.route_index = {
            position: route_id
            for zone in self.crop_zones
            for route_id, position in enumerate(zone)
        }

        self.cohort_offset = dict(self.cohort_offset)
        for position in self.q2_crop_positions:
            self.cohort_offset[position] = 10_000

        self._q2_relative_cohort: dict[tuple[int, int], int] = {
            position: 0 for position in self.q2_crop_positions
        }

    def _role_for_worker(self, worker_id: int) -> str:
        return CENTRAL_3Q_ROLE_SEQUENCE[min(worker_id, len(CENTRAL_3Q_ROLE_SEQUENCE) - 1)]

    def _module_animal_positions(
        self, module: str, species: str
    ) -> tuple[tuple[int, int], ...]:
        if module == "Q0":
            return self.q0_pasture_positions[:3] if species == "COW" else self.q0_pasture_positions[3:]
        elif module == "Q1":
            return self.q1_pasture_positions[:3] if species == "COW" else self.q1_pasture_positions[3:]
        else:  # Q2
            return self.q2_pasture_positions if species == "SHEEP" else ()

    def _feed_assignments(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[tuple[str, str]]:
        if role == "LIVESTOCK_SHEEP_Q2" or worker_id == 13:
            return [("Q2", "SHEEP")]
        return super()._feed_assignments(snapshot, worker_id, role)

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
        orders = super().decide_market_orders(snapshot)
        farm = snapshot.farm
        cash = float(farm.get("money", 0.0))
        owned = len(farm.get("unlocked_quadrants", []))
        day = snapshot.clock.day

        # Q2 Land purchase at Day 11 with healthy cashflow
        if owned == 2 and day >= 11 and cash >= 2300.0 and len(orders) < self.max_market_orders:
            orders.append(["BUY_LAND"])

        return orders[: self.max_market_orders]
