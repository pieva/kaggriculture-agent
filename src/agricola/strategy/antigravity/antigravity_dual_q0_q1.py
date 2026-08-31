"""Antigravity C2 Dual-Quadrant (Q0 + Q1) 75K Candidate Policy.

Scales the proven Antigravity compact Q0 high-density routine to two quadrants.
Q0 operates from Day 0 with 7 workers. Q1 is unlocked at Day 7-8 when cash reserves
and revenue milestones allow, adding 6 dedicated workers (13 total).
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

import statistics
from agricola.e16.policy import _fib
from agricola.strategy.antigravity.antigravity_compact_q0 import (
    ANIMAL_RULES,
    ANTIGRAVITY_COHORT_OFFSET,
    ANTIGRAVITY_CROP_PLAN,
    ANTIGRAVITY_CROP_POSITIONS,
    ANTIGRAVITY_CROP_ZONES,
    ANTIGRAVITY_PASTURE_POSITIONS,
    CROP_RULES,
    EMPTY_ASSIGNED,
    HARVEST_READY,
    LOST_WEED,
    MOVE_ACTIONS,
    RETIREMENT_DUE,
    AntigravityC2_50K_Policy,
    _inventory_total,
    classify_tile_lifecycle,
    lifespan_decay_started,
    water_loss_at_eod_if_unserved,
    yield_completion_water_due,
)
from agricola.strategy.antigravity.c2_75k_config import AntigravityC2_75K_Config
from agricola.strategy.codex_lifecycle import CodexSnapshot



REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_DUAL_CONFIG_PATH = (
    REPO_ROOT / "configs" / "model_spec_c2" / "ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG.json"
)
DUAL_MODEL_SPEC_VERSION = "ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def _mirror_q1(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    return 9 - x, y


Q1_CROP_ZONES: tuple[tuple[tuple[int, int], ...], ...] = tuple(
    tuple(_mirror_q1(position) for position in zone)
    for zone in ANTIGRAVITY_CROP_ZONES
)
Q1_CROP_POSITIONS: tuple[tuple[int, int], ...] = tuple(
    position for zone in Q1_CROP_ZONES for position in zone
)
Q1_PASTURE_POSITIONS: tuple[tuple[int, int], ...] = tuple(
    _mirror_q1(position) for position in ANTIGRAVITY_PASTURE_POSITIONS
)

DUAL_ROLE_SEQUENCE = (
    "RELIEF_LOGISTICS",        # W0: Farmer (Center/Shed (4,4), market sales, relief)
    "CROP_ZONE_0",             # W1: Q0 Zone 0
    "CROP_ZONE_1",             # W2: Q0 Zone 1
    "CROP_ZONE_2",             # W3: Q0 Zone 2
    "LIVESTOCK_COW_Q0",        # W4: Q0 Cow specialist
    "LIVESTOCK_SHEEP_Q0",      # W5: Q0 Sheep specialist
    "FERTILIZER_LOGISTICS_Q0", # W6: Q0 Fertilizer specialist
    "CROP_ZONE_3",             # W7: Q1 Zone 3
    "CROP_ZONE_4",             # W8: Q1 Zone 4
    "CROP_ZONE_5",             # W9: Q1 Zone 5
    "LIVESTOCK_COW_Q1",        # W10: Q1 Cow specialist
    "LIVESTOCK_SHEEP_Q1",      # W11: Q1 Sheep specialist
    "FERTILIZER_LOGISTICS_Q1", # W12: Q1 Fertilizer specialist
)


class AntigravityDualQPolicy(AntigravityC2_50K_Policy):
    """Antigravity Dual-Quadrant Q0+Q1 strategy policy."""

    def __init__(
        self,
        config: Any = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        cfg = config or AntigravityC2_75K_Config.load()
        super().__init__(config=cfg, run_context=run_context)
        self.candidate_id = "ANTIGRAVITY_C2_75K_DUAL_Q"
        self.model_spec_version = DUAL_MODEL_SPEC_VERSION
        self.expected_max_quadrants = 2

        self.q0_crop_positions = ANTIGRAVITY_CROP_POSITIONS
        self.q1_crop_positions = Q1_CROP_POSITIONS
        self.crop_zones = (*ANTIGRAVITY_CROP_ZONES, *Q1_CROP_ZONES)
        self.crop_positions = (*self.q0_crop_positions, *self.q1_crop_positions)

        q1_plan = {
            _mirror_q1(position): crop for position, crop in ANTIGRAVITY_CROP_PLAN.items()
        }
        self.crop_plan = {**ANTIGRAVITY_CROP_PLAN, **q1_plan}
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
        self.cohort_offset = dict(ANTIGRAVITY_COHORT_OFFSET)
        self._q1_relative_cohort = {
            _mirror_q1(position): int(offset)
            for position, offset in ANTIGRAVITY_COHORT_OFFSET.items()
        }
        self.cohort_offset.update(
            {position: 10_000 for position in self.q1_crop_positions}
        )

        self.q0_pasture_positions = ANTIGRAVITY_PASTURE_POSITIONS
        self.q1_pasture_positions = Q1_PASTURE_POSITIONS
        self.pasture_positions = (
            *self.q0_pasture_positions,
            *self.q1_pasture_positions,
        )
        self.pasture_positions_by_species = {
            "COW": (
                *self.q0_pasture_positions[:3],
                *self.q1_pasture_positions[:3],
            ),
            "SHEEP": (
                *self.q0_pasture_positions[3:],
                *self.q1_pasture_positions[3:],
            ),
        }

        self.q1_activation_day: int | None = None
        self.q1_full_module_day: int | None = None
        self.q1_activation_records: list[dict[str, Any]] = []
        self._q1_activation_decisions: set[int] = set()

    def _role_for(self, worker_id: int) -> str:
        return DUAL_ROLE_SEQUENCE[min(worker_id, len(DUAL_ROLE_SEQUENCE) - 1)]

    def _target_workforce(self, snapshot: CodexSnapshot) -> int:
        if self._owned_quadrants(snapshot.farm) < 2:
            return int(self.config.q0_workforce_total)
        return int(self.config.workforce_total)

    def _crop_positions_for_role(
        self, role: str
    ) -> tuple[tuple[int, int], ...]:
        if role.endswith("_Q0"):
            return self.q0_crop_positions
        if role.endswith("_Q1"):
            return self.q1_crop_positions
        return self.crop_positions

    @staticmethod
    def _role_module(role: str) -> str | None:
        if role.endswith("_Q0"):
            return "Q0"
        if role.endswith("_Q1"):
            return "Q1"
        if role.startswith("CROP_ZONE_"):
            return "Q0" if int(role.rsplit("_", 1)[1]) < 3 else "Q1"
        return None

    @staticmethod
    def _is_fertilizer_role(role: str) -> bool:
        return role in (
            "FERTILIZER_LOGISTICS",
            "FERTILIZER_LOGISTICS_Q0",
            "FERTILIZER_LOGISTICS_Q1",
        )


    def _module_animal_positions(
        self, module: str, species: str
    ) -> tuple[tuple[int, int], ...]:
        positions = (
            self.q0_pasture_positions if module == "Q0" else self.q1_pasture_positions
        )
        return positions[:3] if species == "COW" else positions[3:]

    def _module_animal_tasks(
        self, snapshot: CodexSnapshot, module: str, species: str
    ) -> list[dict[str, Any]]:
        allowed = set(self._module_animal_positions(module, species))
        return [
            task
            for task in self._animal_tasks(snapshot, species)
            if tuple(task["target"]) in allowed
        ]

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
            return [("Q1", "SHEEP")]

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

    def _feed_tasks_for_worker(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[dict[str, Any]]:
        tasks: list[dict[str, Any]] = []
        for module, species in self._feed_assignments(snapshot, worker_id, role):
            tasks.extend(
                task
                for task in self._module_animal_tasks(snapshot, module, species)
                if task["kind"] == "FEED"
            )
        return tasks

    def _free_pastures(
        self, snapshot: CodexSnapshot, species: str, module: str | None = None
    ) -> list[tuple[int, int]]:
        positions = (
            self._module_animal_positions(module, species)
            if module in {"Q0", "Q1"}
            else self.pasture_positions_by_species[species]
        )
        return [
            position
            for position in positions
            if isinstance(self._tile(snapshot.farm, position), dict)
            and self._tile(snapshot.farm, position).get("kind") == "PASTURE"
            and not self._tile(snapshot.farm, position).get("animal")
        ]

    def _inventory_task(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[dict[str, Any]]:
        inventory = self._inventory(snapshot.private, worker_id)
        shed = snapshot.private.get("shed", {}) or {}
        module = self._role_module(role) or ("Q1" if worker_id >= 7 else "Q0")
        shed_tile = (5, 4) if (module == "Q1" or worker_id >= 7) else (4, 4)
        tasks: list[dict[str, Any]] = []

        # 1. Animal placement
        for species in ("COW", "SHEEP"):
            if int(inventory.get(species, 0)) <= 0:
                continue
            for target in self._free_pastures(snapshot, species, module):
                tasks.append(
                    self._task(
                        target,
                        ["PLACE", species],
                        kind="PLACE_ANIMAL",
                        loss_rank=1,
                        value=int(ANIMAL_RULES[species]["cost"]),
                        slack=12,
                    )
                )
            return tasks

        # 2. INVENTORY_AWARE_FEED_DISPATCH & FEED_FIRST_CLUSTER_BATCHING
        feed_tasks = self._feed_tasks_for_worker(snapshot, worker_id, role)
        wheat = int(inventory.get("WHEAT", 0))
        if feed_tasks and wheat > 0:
            return feed_tasks
        if feed_tasks and int(shed.get("WHEAT", 0)) > 0:
            quantity = min(len(feed_tasks), int(shed.get("WHEAT", 0)))
            tasks.append(
                self._task(
                    shed_tile,
                    ["PICKUP", "WHEAT", quantity],
                    kind="FEED_STAGING",
                    loss_rank=min(task["loss_rank"] for task in feed_tasks),
                    value=max(int(task["value"]) for task in feed_tasks),
                    slack=min(task["slack"] for task in feed_tasks),
                    hard_reason=next(
                        (
                            task["hard_reason"]
                            for task in feed_tasks
                            if task["hard_reason"]
                        ),
                        None,
                    ),
                )
            )
            return tasks

        # 3. CLOSED_LOOP_FERTILIZER: Apply fertilizer to same-day-watered crops (Day >= 6 with secure cash)
        fertilizer = int(inventory.get("FERTILIZER", 0))
        if (
            fertilizer > 0
            and self._is_fertilizer_role(role)
            and snapshot.clock.day >= 6
            and float(snapshot.farm.get("money", 0.0)) >= 300.0
        ):
            positions = (
                self.q0_crop_positions
                if module == "Q0"
                else (self.q1_crop_positions if module == "Q1" else self.crop_positions)
            )
            eligible: list[tuple[int, int]] = []
            for position in positions:
                tile = self._tile(snapshot.farm, position)
                if (
                    isinstance(tile, dict)
                    and tile.get("kind") == "PLANT"
                    and tile.get("crop") in {"MELON", "STRAWBERRY"}
                    and bool(tile.get("watered_today", False))
                    and int(tile.get("fertilized_until_day", -1)) < snapshot.clock.day
                ):
                    eligible.append(position)
            # Prioritize MELON first, then STRAWBERRY by cohort and route index
            eligible.sort(
                key=lambda pos: (
                    self.crop_plan[pos] != "MELON",
                    self.cohort_offset.get(pos, 0),
                    self.route_index.get(pos, 0),
                )
            )
            for position in eligible[:fertilizer]:
                tasks.append(
                    self._task(
                        position,
                        ["FERTILIZE"],
                        kind="FERTILIZER_APPLICATION",
                        loss_rank=2,
                        value=int(CROP_RULES[self.crop_plan[position]]["value"]),
                        slack=max(1, self.turns_per_day - snapshot.clock.hour),
                        zone=self.zone_by_position[position],
                    )
                )
            if tasks:
                return tasks

        # 4. Product / fertilizer drop-off in shed
        carried_products = [
            item
            for item in ("MILK", "WOOL", "MELON", "STRAWBERRY", "FERTILIZER")
            if int(inventory.get(item, 0)) > 0
        ]
        if carried_products:
            item = carried_products[0]
            amount = int(inventory[item])
            free = max(0, self.shed_capacity - _inventory_total(shed))
            if free > 0:
                tasks.append(
                    self._task(
                        shed_tile,
                        ["PLACE", item, min(amount, free)],
                        kind="INVENTORY_UNBLOCK",
                        loss_rank=1 if snapshot.clock.hour >= 20 else 2,
                        value=100,
                        slack=max(1, self.turns_per_day - snapshot.clock.hour),
                        hard_reason=(
                            "BLOCKING_INVENTORY_LOSS"
                            if snapshot.clock.hour >= 22
                            else None
                        ),
                    )
                )
            return tasks

        # 5. Return extra wheat to shed if no feed needed
        if wheat > 0 and not any(
            task["kind"] == "FEED"
            for candidate in ("COW", "SHEEP")
            for task in self._animal_tasks(snapshot, candidate)
        ):
            tasks.append(
                self._task(
                    shed_tile,
                    ["PLACE", "WHEAT", wheat],
                    kind="INVENTORY_UNBLOCK",
                    loss_rank=2,
                    value=10,
                    slack=12,
                )
            )
            return tasks

        # 6. Animal staging pickup from shed if empty hands and free pastures exist
        if _inventory_total(inventory) == 0 and (
            self._is_fertilizer_role(role)
            or role == "RELIEF_LOGISTICS"
            or worker_id in {0, 6, 12}
        ):
            for species in ("COW", "SHEEP"):
                if int(shed.get(species, 0)) > 0 and self._free_pastures(
                    snapshot, species, module
                ):
                    tasks.append(
                        self._task(
                            shed_tile,
                            ["PICKUP", species, 1],
                            kind="ANIMAL_STAGING",
                            loss_rank=1,
                            value=int(ANIMAL_RULES[species]["cost"]),
                            slack=12,
                        )
                    )
                    return tasks

        return tasks





    def _active_animal_positions(
        self, farm: dict[str, Any], species: str | None = None
    ) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []
        for position in self.pasture_positions:
            tile = self._tile(farm, position)
            if not isinstance(tile, dict) or not tile.get("animal"):
                continue
            if species is None or tile.get("animal") == species:
                positions.append(position)
        return positions

    def _animal_counts(self, snapshot: CodexSnapshot) -> Counter[str]:
        counts: Counter[str] = Counter()
        for position in self.pasture_positions:
            tile = self._tile(snapshot.farm, position)
            if isinstance(tile, dict) and tile.get("animal") in ANIMAL_RULES:
                counts[str(tile["animal"])] += 1
        shed = snapshot.private.get("shed", {}) or {}
        for species in ANIMAL_RULES:
            counts[species] += int(shed.get(species, 0))
            for worker_id in range(len(self._positions(snapshot.farm))):
                counts[species] += int(
                    self._inventory(snapshot.private, worker_id).get(species, 0)
                )
        return counts

    def _record_day_due(self, snapshot: CodexSnapshot) -> None:
        day = snapshot.clock.day
        farm = snapshot.farm
        for position in self.crop_positions:
            tile = self._tile(farm, position)
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue
            if not bool(tile.get("watered_today", False)):
                self.daily_due[day].add(f"WATER:{position[0]}:{position[1]}")
            state = classify_tile_lifecycle(tile, in_working_set=True, day=day)
            if state in {HARVEST_READY, RETIREMENT_DUE}:
                self.daily_due[day].add(f"HARVEST:{position[0]}:{position[1]}")

    def _replan_global(self, snapshot: CodexSnapshot, reason: str) -> None:
        signature = self._asset_signature(snapshot)
        positions = self._positions(snapshot.farm)
        self._update_roles(len(positions))
        self._record_day_due(snapshot)
        capacity = self._capacity_snapshot(snapshot, candidate_species=None)
        self._global_plan = {
            "opened_step": snapshot.clock.step,
            "day": snapshot.clock.day,
            "reason": reason,
            "roles": deepcopy(self._roles),
            "zones": {
                str(zone_id): [list(position) for position in zone]
                for zone_id, zone in enumerate(self.crop_zones)
            },
            "hard_horizon": "CURRENT_DAY_AND_NEXT_SERVICE_BOUNDARY",
            "soft_horizon": "FIRST_MONETIZABLE_OUTPUT",
            "capacity": capacity,
        }
        self._last_global_signature = signature
        self._last_day = snapshot.clock.day
        self.global_replan_count += 1

    def _capacity_snapshot(
        self, snapshot: CodexSnapshot, candidate_species: str | None
    ) -> dict[str, Any]:
        farm = snapshot.farm
        unit_count = len(self._positions(farm))
        active_crops = sum(
            1
            for position in self.crop_positions
            if isinstance(self._tile(farm, position), dict)
            and self._tile(farm, position).get("kind") == "PLANT"
        )
        active_animals = len(self._active_animal_positions(farm))
        ready_crop = sum(
            1
            for position in self.crop_positions
            if classify_tile_lifecycle(
                self._tile(farm, position),
                in_working_set=True,
                day=snapshot.clock.day,
            )
            == HARVEST_READY
        )
        ready_animals = sum(
            1
            for position in self.pasture_positions
            if isinstance(self._tile(farm, position), dict)
            and int(self._tile(farm, position).get("yield_units", 0)) > 0
        )
        candidate_actions = 0
        if candidate_species is not None:
            candidate_actions = 4
        required_services = (
            active_crops
            + active_animals * 2
            + ready_crop
            + ready_animals
            + candidate_actions
        )
        history_days = [d for d in self.daily_completed if d < snapshot.clock.day]
        raw_capacity = (
            statistics.mean(
                sum(self.daily_completed[d].values())
                for d in history_days[-int(self.config.observed_capacity_days) :]
            )
            if len(history_days) >= int(self.config.observed_capacity_days)
            else None
        )
        target_workforce = self._target_workforce(snapshot)
        effective_units = max(unit_count, target_workforce)
        base_workforce = int(self.config.q0_workforce_total)
        if raw_capacity is not None and effective_units > base_workforce:
            observed_capacity = (raw_capacity / base_workforce) * effective_units
        else:
            observed_capacity = raw_capacity

        slack = (
            observed_capacity - required_services
            if observed_capacity is not None
            else effective_units * self.turns_per_day - required_services
        )
        return {
            "unit_count": unit_count,
            "required_services": required_services,
            "observed_capacity": observed_capacity,
            "minimum_slack": slack,
            "history_days": history_days,
            "forecast_within_observed": observed_capacity is None
            or required_services <= observed_capacity,
        }


    def _crop_tasks(self, snapshot: CodexSnapshot) -> list[dict[str, Any]]:
        tasks: list[dict[str, Any]] = []
        day = snapshot.clock.day
        hour = snapshot.clock.hour
        step = snapshot.clock.step
        seeds = snapshot.private.get("seeds", {}) or {}
        shutdown = self._shutdown(snapshot)
        for position in self.crop_positions:
            crop = self.crop_plan[position]
            zone = self.zone_by_position[position]
            tile = self._tile(snapshot.farm, position)
            state = classify_tile_lifecycle(tile, in_working_set=True, day=day)
            if state == LOST_WEED:
                tasks.append(
                    self._task(position, ["DIG"], kind="WEED_RECOVERY", loss_rank=1, value=0, slack=24, zone=zone)
                )
                continue
            if state == RETIREMENT_DUE:
                tasks.append(
                    self._task(position, ["DIG"], kind="RETIREMENT_CLEAR", loss_rank=1, value=0, slack=1, hard_reason="HARVEST_TERMINAL_RISK", zone=zone)
                )
                continue
            if state == EMPTY_ASSIGNED:
                cohort_open = day >= int(self.cohort_offset[position])
                if (
                    not shutdown
                    and cohort_open
                    and self._plant_serviceable_before_eod(hour)
                    and self._crop_serviceable_before_terminal(crop, step)
                    and int(seeds.get(crop, 0)) > 0
                ):
                    tasks.append(
                        self._task(position, ["PLANT", crop], kind="PLANT", loss_rank=2, value=int(CROP_RULES[crop]["value"]), slack=max(1, 23 - hour), zone=zone)
                    )
                continue
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue
            if lifespan_decay_started(tile, step):
                tasks.append(
                    self._task(position, ["HARVEST"], kind="HARVEST", loss_rank=1, value=int(CROP_RULES[crop]["value"]), slack=1, hard_reason="HARVEST_TERMINAL_RISK", zone=zone)
                )
                continue
            if water_loss_at_eod_if_unserved(tile):
                tasks.append(
                    self._task(position, ["WATER"], kind="WATER", loss_rank=0, value=int(CROP_RULES[crop]["value"]), slack=max(0, 23 - hour), hard_reason="WATER_DEADLINE_RISK", zone=zone)
                )
                continue
            if yield_completion_water_due(tile, day):
                tasks.append(
                    self._task(position, ["WATER"], kind="WATER", loss_rank=1, value=int(CROP_RULES[crop]["value"]), slack=max(0, 23 - hour), zone=zone)
                )
                continue
            if state == HARVEST_READY:
                tasks.append(
                    self._task(position, ["HARVEST"], kind="HARVEST", loss_rank=1, value=int(CROP_RULES[crop]["value"]), slack=24, zone=zone)
                )
                continue
            if not bool(tile.get("watered_today", False)):
                tasks.append(
                    self._task(position, ["WATER"], kind="WATER", loss_rank=2, value=int(CROP_RULES[crop]["value"]), slack=max(0, 23 - hour), zone=zone)
                )
        return tasks

    def _animal_tasks(
        self, snapshot: CodexSnapshot, species: str
    ) -> list[dict[str, Any]]:
        tasks: list[dict[str, Any]] = []
        positions = self.pasture_positions_by_species[species]
        for position in positions:
            tile = self._tile(snapshot.farm, position)
            if tile is None:
                tasks.append(
                    self._task(position, ["BUILD_PASTURE"], kind="BUILD_PASTURE", loss_rank=3, value=0, slack=24)
                )
                continue
            if not isinstance(tile, dict) or tile.get("kind") != "PASTURE":
                continue
            if tile.get("animal") != species:
                continue
            unfed = not bool(tile.get("fed_today", False))
            consecutive = int(tile.get("consecutive_unfed", 0))
            if unfed:
                hard = consecutive >= 1 or snapshot.clock.hour >= 20
                tasks.append(
                    self._task(
                        position,
                        ["FEED"],
                        kind="FEED",
                        loss_rank=0 if hard else 1,
                        value=200 if species == "SHEEP" else 160,
                        slack=max(0, self.turns_per_day - snapshot.clock.hour - 1),
                        hard_reason="ANIMAL_ESCAPE_PREVENTION" if hard else None,
                    )
                )
            if int(tile.get("yield_units", 0)) > 0:
                tasks.append(
                    self._task(position, ["HARVEST"], kind="ANIMAL_COLLECTION", loss_rank=1, value=200 if species == "SHEEP" else 160, slack=int(ANIMAL_RULES[species]["period"]) * self.turns_per_day)
                )
            if not bool(tile.get("cared_today", False)):
                tasks.append(
                    self._task(position, ["CARE"], kind="CARE", loss_rank=2, value=80, slack=max(1, self.turns_per_day - snapshot.clock.hour))
                )
            if bool(tile.get("fertilizer_available", False)):
                tasks.append(
                    self._task(position, ["COLLECT_FERTILIZER"], kind="FERTILIZER_COLLECTION", loss_rank=2, value=100, slack=max(1, self.turns_per_day - snapshot.clock.hour))
                )
        return tasks

    def _maybe_replan_global(self, snapshot: CodexSnapshot) -> None:
        if (
            self._owned_quadrants(snapshot.farm) >= 2
            and self.q1_activation_day is None
        ):
            self.q1_activation_day = snapshot.clock.day
            for position, relative in self._q1_relative_cohort.items():
                self.cohort_offset[position] = self.q1_activation_day + relative
            self.q1_activation_records.append(
                {
                    "event": "Q1_OBSERVED_ACTIVE",
                    "day": snapshot.clock.day,
                    "step": snapshot.clock.step,
                    "money": float(snapshot.farm.get("money", 0.0)),
                }
            )
        super()._maybe_replan_global(snapshot)


    def decide_unit_actions(self, snapshot: CodexSnapshot) -> dict[int, list[Any]]:
        """Dual-quadrant unit action dispatch with spatial isolation."""
        self._maybe_replan_global(snapshot)
        positions = self._positions(snapshot.farm)
        crop_tasks = self._crop_tasks(snapshot)
        hard_crop_tasks = [task for task in crop_tasks if task.get("hard_reason")]
        reserved: set[tuple[int, int]] = set()
        actions: dict[int, list[Any]] = {}

        # Prioritize livestock specialists (Q0 then Q1), crop zones, fertilizer, then farmer
        dispatch_order = [
            worker_id
            for worker_id in (4, 5, 10, 11, 1, 2, 3, 7, 8, 9, 6, 12, 0)
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

    def _asset_signature(self, snapshot: CodexSnapshot) -> tuple[Any, ...]:
        farm = snapshot.farm
        crop_signature = tuple(
            (
                position,
                (
                    self._tile(farm, position).get("crop")
                    if isinstance(self._tile(farm, position), dict)
                    else None
                ),
                (
                    self._tile(farm, position).get("kind")
                    if isinstance(self._tile(farm, position), dict)
                    else self._tile(farm, position)
                ),
            )
            for position in self.crop_positions
        )
        animal_signature = tuple(
            (
                position,
                (
                    self._tile(farm, position).get("animal")
                    if isinstance(self._tile(farm, position), dict)
                    else None
                ),
                (
                    self._tile(farm, position).get("kind")
                    if isinstance(self._tile(farm, position), dict)
                    else self._tile(farm, position)
                ),
            )
            for position in self.pasture_positions
        )
        return (
            len(farm.get("hands", []) or []),
            self._owned_quadrants(farm),
            crop_signature,
            animal_signature,
        )

    def _attribute_execution(
        self, previous: CodexSnapshot, current: CodexSnapshot
    ) -> None:
        p_farm = previous.farm
        c_farm = current.farm
        day = previous.clock.day

        # Track completed actions and productions across all 36 crops
        for position in self.crop_positions:
            p_tile = self._tile(p_farm, position)
            c_tile = self._tile(c_farm, position)
            if isinstance(p_tile, dict) and p_tile.get("kind") == "PLANT":
                p_yield = int(p_tile.get("yield_units", 0))
                c_yield = int(c_tile.get("yield_units", 0)) if isinstance(c_tile, dict) else 0
                if p_yield > c_yield:
                    crop = str(p_tile.get("crop", "CROP"))
                    harvested = p_yield - c_yield
                    self.production_units[crop] += harvested
                    self.daily_completed[day]["HARVEST"] += 1
                    self.daily_due_completed[day].add(f"HARVEST:{position[0]}:{position[1]}")
            if not isinstance(p_tile, dict) or not isinstance(c_tile, dict):
                continue
            if not p_tile.get("watered_today", False) and c_tile.get("watered_today", False):
                self.daily_completed[day]["WATER"] += 1
                self.daily_due_completed[day].add(f"WATER:{position[0]}:{position[1]}")


        # Track animals across all 12 pastures
        for position in self.pasture_positions:
            p_tile = self._tile(p_farm, position)
            c_tile = self._tile(c_farm, position)
            if not isinstance(p_tile, dict) or not isinstance(c_tile, dict):
                continue
            if not p_tile.get("fed_today", False) and c_tile.get("fed_today", False):
                self.daily_completed[day]["FEED"] += 1
            if not p_tile.get("cared_today", False) and c_tile.get("cared_today", False):
                self.daily_completed[day]["CARE"] += 1
            if p_tile.get("fertilizer_available", False) and not c_tile.get("fertilizer_available", False):
                self.production_units["FERTILIZER_COLLECTED"] += 1
                self.daily_completed[day]["COLLECT_FERTILIZER"] += 1
            if int(p_tile.get("yield_units", 0)) > int(c_tile.get("yield_units", 0)):
                animal = str(p_tile.get("animal", ""))
                product = ANIMAL_RULES.get(animal, {}).get("product", "PRODUCT")
                collected = int(p_tile.get("yield_units", 0)) - int(c_tile.get("yield_units", 0))
                self.production_units[product] += collected
                self.daily_completed[day]["ANIMAL_COLLECTION"] += 1

        # Check animal escapes at day boundary
        if current.clock.day != previous.clock.day:
            for position in self.pasture_positions:
                p_tile = self._tile(p_farm, position)
                c_tile = self._tile(c_farm, position)
                if (
                    isinstance(p_tile, dict)
                    and p_tile.get("animal")
                    and (not isinstance(c_tile, dict) or not c_tile.get("animal"))
                ):
                    self.animal_escapes += 1

        # Track fertilizer application across all 36 crops
        for position in self.crop_positions:
            p_tile = self._tile(p_farm, position)
            c_tile = self._tile(c_farm, position)
            if isinstance(p_tile, dict) and isinstance(c_tile, dict):
                if int(p_tile.get("fertilized_until_day", -1)) < int(c_tile.get("fertilized_until_day", -1)):
                    self.production_units["FERTILIZER_APPLIED"] += 1
                    self.daily_completed[day]["FERTILIZE"] += 1

    def decide_market_orders(self, snapshot: CodexSnapshot) -> list[list[Any]]:
        """Compute atomic market orders adhering to capacity, cash rules, and Q1 expansion."""
        orders: list[list[Any]] = []
        farm = snapshot.farm
        private = snapshot.private
        shed = private.get("shed", {}) or {}
        prices = snapshot.market.get("prices", {}) or {}
        cash = float(farm.get("money", 0.0))
        floor = float(self.config.operating_cash_floor)

        def add(order: list[Any], cost: float = 0.0, *, protect_floor: bool = True) -> bool:
            nonlocal cash
            if len(orders) >= self.max_market_orders:
                return False
            if protect_floor and cash - cost < floor:
                return False
            orders.append(order)
            cash -= cost
            return True

        # 1. Monetize finished products from shed immediately
        for item in ("MILK", "WOOL", "MELON", "STRAWBERRY", "FERTILIZER"):
            quantity = int(shed.get(item, 0))
            if quantity > 0 and add(["SELL", item, quantity], protect_floor=False):
                cash += quantity * float(prices.get(item, 0.0))

        # 2. Sell surplus wheat exceeding the 2-round reserve
        counts = self._animal_counts(snapshot)
        active_or_staged_animals = sum(counts.values())
        wheat_reserve = active_or_staged_animals * int(self.config.feed_reserve_rounds)
        wheat_to_sell = max(0, int(shed.get("WHEAT", 0)) - wheat_reserve)
        if wheat_to_sell > 0 and add(["SELL", "WHEAT", wheat_to_sell], protect_floor=False):
            cash += wheat_to_sell * float(prices.get("WHEAT", 0.0))

        # 3. Daily hiring up to current module target workforce during hours 0/1
        target_hands = self._target_workforce(snapshot) - 1
        hands = len(farm.get("hands", []) or [])
        hires_today = int(farm.get("hires_today", 0))
        if not self._shutdown(snapshot) and snapshot.clock.hour in {0, 1}:
            for offset in range(max(0, target_hands - hands)):
                hire_cost = float(_fib(hires_today + offset))
                if not add(["HIRE"], hire_cost):
                    break

        # 4. Opening Day 0 Step 0: Bootstrap 2 COW + 2 SHEEP + 10 WHEAT feed + opening seeds
        if snapshot.clock.step == 0:
            add(["BUY_ANIMAL", "COW", 2], 800.0)
            add(["BUY_ANIMAL", "SHEEP", 2], 1000.0)
            add(["BUY_PRODUCT", "WHEAT", 10], 10 * float(prices.get("WHEAT", 25.0)))
            add(["BUY_SEED", "MELON", 3], 240.0)
            return orders[: self.max_market_orders]

        if not self._shutdown(snapshot):
            # Check Q1 BUY_LAND admission
            owned = self._owned_quadrants(farm)
            day = snapshot.clock.day
            if owned < 2 and int(self.config.q1_activation_min_day) <= day <= int(self.config.q1_activation_max_day):
                prospective_sales = sum(
                    int(shed.get(item, 0)) * float(prices.get(item, 0.0))
                    for item in ("MILK", "WOOL", "MELON", "STRAWBERRY")
                )
                available = cash + prospective_sales
                threshold = float(self.config.q1_activation_cash)
                admitted = available >= threshold
                if day not in self._q1_activation_decisions:
                    self._q1_activation_decisions.add(day)
                    self.q1_activation_records.append(
                        {
                            "event": "Q1_ADMISSION_DECISION",
                            "day": day,
                            "step": snapshot.clock.step,
                            "admitted": admitted,
                            "money": cash,
                            "prospective_sales": prospective_sales,
                            "available": available,
                            "threshold": threshold,
                        }
                    )
                if admitted and cash >= 1000.0 + float(self.config.q1_operating_cash_floor):
                    if add(["BUY_LAND"], 1000.0, protect_floor=True):
                        owned = 2

            # Repair bootstrap deficit if any
            for species in ("COW", "SHEEP"):
                bootstrap = int(self.config.bootstrap_livestock[species])
                deficit = max(0, bootstrap - int(counts.get(species, 0)))
                if snapshot.clock.day <= 1 and deficit > 0:
                    quantity = min(deficit, max(0, int((cash - floor) // ANIMAL_RULES[species]["cost"])))
                    if quantity > 0:
                        add(["BUY_ANIMAL", species, quantity], quantity * float(ANIMAL_RULES[species]["cost"]))
                        counts[species] += quantity

            # Livestock expansion (3+3 in Q0, and up to 6+6 in Q1)
            for species in ("COW", "SHEEP"):
                activation_day = int(self.config.livestock_activation_days[species])
                target = int(self.config.livestock_targets[species]) if owned >= 2 else 3
                if snapshot.clock.day < activation_day or int(counts.get(species, 0)) >= target:
                    continue
                built_pastures = len([
                    p
                    for p in self.pasture_positions_by_species[species]
                    if isinstance(self._tile(farm, p), dict)
                    and self._tile(farm, p).get("kind") == "PASTURE"
                ])
                if int(counts.get(species, 0)) >= built_pastures:
                    continue
                decision_key = (species, target, snapshot.clock.day)
                admitted, reason, capacity = self._capacity_admission(snapshot, species)
                if decision_key not in self._activation_decisions:
                    self._activation_decisions.add(decision_key)
                    self.activation_records.append(
                        {
                            "animal": species,
                            "animal_activation_day": snapshot.clock.day,
                            "activation_admitted": admitted,
                            "activation_rejected": not admitted,
                            "rejection_reason": None if admitted else reason,
                            "capacity": capacity,
                        }
                    )
                if admitted:
                    quantity = min(target - int(counts.get(species, 0)), 1)
                    if add(["BUY_ANIMAL", species, quantity], quantity * float(ANIMAL_RULES[species]["cost"])):
                        counts[species] += quantity
                else:
                    self.capacity_rejections[reason] += 1


            # Feed restocking
            carried_wheat = sum(
                self._inventory(private, worker_id).get("WHEAT", 0)
                for worker_id in range(len(self._positions(farm)))
            )
            projected_animals = sum(counts.values())
            feed_target = projected_animals * int(self.config.feed_reserve_rounds)
            wheat_deficit = max(0, feed_target - int(shed.get("WHEAT", 0)) - carried_wheat)
            wheat_price = float(prices.get("WHEAT", 25.0))
            affordable_wheat = max(0, int((cash - floor) // max(1.0, wheat_price)))
            quantity = min(wheat_deficit, affordable_wheat, 16)
            if quantity > 0:
                add(["BUY_PRODUCT", "WHEAT", quantity], quantity * wheat_price)

            # Seed restocking for staggered cohorts across active working set
            active_by_crop: Counter[str] = Counter()
            for position, planned_crop in self.crop_plan.items():
                tile = self._tile(farm, position)
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    active_by_crop[str(tile.get("crop", planned_crop))] += 1
            seed_costs = {"MELON": 80.0, "STRAWBERRY": 100.0, "WHEAT": 10.0}
            for crop in ("STRAWBERRY", "MELON", "WHEAT"):
                eligible_slots = sum(
                    1
                    for position, planned_crop in self.crop_plan.items()
                    if planned_crop == crop
                    and snapshot.clock.day >= self.cohort_offset[position]
                    and self._tile(farm, position) is None
                )
                seed_stock = int((private.get("seeds", {}) or {}).get(crop, 0))
                deficit = max(0, eligible_slots - seed_stock)
                if deficit <= 0 or not self._crop_serviceable_before_terminal(crop, snapshot.clock.step):
                    continue
                affordable = max(0, int((cash - floor) // seed_costs[crop]))
                quantity = min(deficit, affordable)
                if quantity > 0:
                    add(["BUY_SEED", crop, quantity], quantity * seed_costs[crop])

        return orders[: self.max_market_orders]


