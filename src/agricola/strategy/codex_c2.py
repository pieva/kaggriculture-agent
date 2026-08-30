"""Remediated Codex C2 lifecycle and economic-cycle tournament candidate.

The candidate reuses the E16 observation adapter while owning its productive
layout, lifecycle dispatcher, worker routing, and market gates. ``create_agent``
returns one isolated, instrumented policy instance per episode.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.e16.policy import (
    CROP_MIX,
    SHED_TILES,
    E16TrainingAgent,
    _fib,
    _inventory_total,
    _move_towards,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = (
    REPO_ROOT / "configs" / "model_spec_c2" / "CODEX_C2_CONFIG.json"
)

CROP_RULES = {
    "WHEAT": {
        "first_yield_day": 2,
        "economic_harvest_day": 4,
        "max_yield_day": 4,
        "max_yield": 6,
        "pre_harvest_yield_target": 3,
        "ongoing": False,
    },
    "STRAWBERRY": {
        "first_yield_day": 10,
        "economic_harvest_day": 10,
        "max_yield_day": 10,
        "max_yield": 4,
        "pre_harvest_yield_target": 4,
        "ongoing": True,
    },
    "MELON": {
        "first_yield_day": 10,
        "economic_harvest_day": 10,
        "max_yield_day": 12,
        "max_yield": 6,
        "pre_harvest_yield_target": 6,
        "ongoing": False,
    },
}

CODEX_PASTURE_POSITIONS = ((3, 4), (6, 4), (3, 3), (6, 3), (2, 4))


def _distance_from_shed(position: tuple[int, int]) -> tuple[int, int, int]:
    x, y = position
    return abs(x - 4) + abs(y - 4), y, x


_RESERVED_PRODUCTIVE_POSITIONS = set(SHED_TILES) | set(CODEX_PASTURE_POSITIONS)
_NW_CROP_POSITIONS = sorted(
    (
        (x, y)
        for y in range(5)
        for x in range(5)
        if (x, y) not in _RESERVED_PRODUCTIVE_POSITIONS
    ),
    key=_distance_from_shed,
)
_NE_CROP_POSITIONS = sorted(
    (
        (x, y)
        for y in range(5)
        for x in range(5, 10)
        if (x, y) not in _RESERVED_PRODUCTIVE_POSITIONS
    ),
    key=_distance_from_shed,
)
CODEX_CROP_POSITIONS = tuple(_NW_CROP_POSITIONS + _NE_CROP_POSITIONS)

OUT_OF_SCOPE = "OUT_OF_SCOPE"
EMPTY_ASSIGNED = "EMPTY_ASSIGNED"
GROWING = "GROWING"
YIELD_ACCUMULATING = "YIELD_ACCUMULATING"
HARVEST_READY = "HARVEST_READY"
RETIREMENT_DUE = "RETIREMENT_DUE"
LOST_WEED = "LOST_WEED"

_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def load_candidate_config(
    path: Path | str = DEFAULT_CONFIG_PATH,
) -> dict[str, Any]:
    """Load and validate the candidate-specific configuration."""

    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    required = {
        "candidate_id",
        "schema_version",
        "crop_working_set_target",
        "crop_pattern",
        "bootstrap_crop_pattern",
        "max_wheat_plants_per_day",
        "watering_dispatch_priority",
        "livestock_headcount_target",
        "pasture_allocation_target",
        "quadrants_owned",
        "workforce_headcount",
        "livestock_species",
        "operating_cash_floor",
        "endgame_shutdown_steps",
        "turns_per_day",
        "minimum_post_plant_action_phases",
        "bootstrap_crop_target",
        "bootstrap_workforce_headcount",
        "land_expansion_min_active",
        "land_expansion_min_cash",
        "livestock_activation_min_crop_fraction",
        "livestock_activation_min_cash",
        "crop_horizon_margin_steps",
    }
    missing = required - set(config)
    if missing:
        raise ValueError(f"missing Codex C2 config fields: {sorted(missing)}")
    if config["candidate_id"] != "CODEX_C2":
        raise ValueError("unexpected candidate_id")
    if config["schema_version"] != "model_spec_c2.codex.v3":
        raise ValueError("unexpected Codex C2 config schema")

    target = int(config["crop_working_set_target"])
    if not 1 <= target <= len(CODEX_CROP_POSITIONS):
        raise ValueError("crop_working_set_target is outside the supported board")
    bootstrap_target = int(config["bootstrap_crop_target"])
    if not 1 <= bootstrap_target <= min(target, len(_NW_CROP_POSITIONS)):
        raise ValueError("bootstrap_crop_target is outside the compact NW layout")
    max_wheat_plants_per_day = int(config["max_wheat_plants_per_day"])
    if not 1 <= max_wheat_plants_per_day <= target:
        raise ValueError("max_wheat_plants_per_day must be in the working set")
    for field in ("bootstrap_crop_pattern", "crop_pattern"):
        pattern = list(config[field])
        if not pattern or any(crop not in CROP_RULES for crop in pattern):
            raise ValueError(f"{field} contains an unsupported crop")
        if set(pattern) != set(CROP_MIX):
            raise ValueError(f"{field} must preserve the E16 crop mix")
    if int(config["turns_per_day"]) <= 0:
        raise ValueError("turns_per_day must be positive")
    if int(config["minimum_post_plant_action_phases"]) < 1:
        raise ValueError("new PLANT must leave at least one later action phase")
    if not 0 < float(config["livestock_activation_min_crop_fraction"]) <= 1:
        raise ValueError("livestock activation fraction must be in (0, 1]")
    if int(config["crop_horizon_margin_steps"]) < 0:
        raise ValueError("crop_horizon_margin_steps must be non-negative")
    return deepcopy(config)


def _stable_crop_plan(
    target: int, pattern: list[str] | tuple[str, ...]
) -> dict[tuple[int, int], str]:
    """Assign a stable crop role to each working-set position."""

    return {
        position: pattern[index % len(pattern)]
        for index, position in enumerate(CODEX_CROP_POSITIONS[:target])
    }


def classify_tile_lifecycle(
    tile: Any, *, in_working_set: bool, day: int
) -> str | None:
    """Classify one native engine tile without using future information."""

    if not in_working_set or tile == "LOCKED":
        return OUT_OF_SCOPE
    if tile is None:
        return EMPTY_ASSIGNED
    if not isinstance(tile, dict):
        return None
    kind = tile.get("kind")
    if kind == "WEED":
        return LOST_WEED
    if kind != "PLANT":
        return OUT_OF_SCOPE

    crop = tile.get("crop")
    rules = CROP_RULES.get(crop)
    if rules is None:
        return None
    try:
        yield_units = int(tile["yield_units"])
        planted_day = int(tile["planted_day"])
        max_lifespan_step = int(tile.get("max_lifespan_step", -1))
    except (KeyError, TypeError, ValueError):
        return None
    if yield_units < 0 or planted_day > day:
        return None

    engine_ready = (
        yield_units > 0
        and day - planted_day >= int(rules["first_yield_day"])
    )
    if engine_ready and day - planted_day < int(rules["economic_harvest_day"]):
        return YIELD_ACCUMULATING
    if engine_ready:
        return HARVEST_READY
    retired = bool(rules["ongoing"]) and yield_units == 0 and max_lifespan_step >= 0
    if retired:
        return RETIREMENT_DUE
    return GROWING


def water_loss_at_eod_if_unserved(tile: Any) -> bool:
    """Return the deterministic EOD loss boundary for an unwatered PLANT."""

    if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
        return False
    if bool(tile.get("watered_today", False)):
        return False
    try:
        return int(tile["consecutive_unwatered"]) + 1 >= 2
    except (KeyError, TypeError, ValueError):
        return True


def lifespan_decay_started(tile: Any, engine_step: int) -> bool:
    """Return whether a PLANT has entered its engine-step decay window."""

    if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
        return False
    try:
        max_lifespan_step = int(tile.get("max_lifespan_step", -1))
    except (TypeError, ValueError):
        return False
    return max_lifespan_step >= 0 and engine_step >= max_lifespan_step


def plant_matches_cohort(tile: Any, crop: str, day: int) -> bool:
    """Return whether an observed PLANT belongs to a crop/day cohort."""

    if not isinstance(tile, dict):
        return False
    if tile.get("kind") != "PLANT" or tile.get("crop") != crop:
        return False
    try:
        return int(tile["planted_day"]) == day
    except (KeyError, TypeError, ValueError):
        return False


def yield_completion_water_due(tile: Any, day: int) -> bool:
    """Prioritize the final observable yield increment before harvesting."""

    if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
        return False
    if bool(tile.get("watered_today", False)):
        return False
    rules = CROP_RULES.get(tile.get("crop"))
    if rules is None or bool(rules["ongoing"]):
        return False
    try:
        age = day - int(tile["planted_day"])
        yield_units = int(tile["yield_units"])
    except (KeyError, TypeError, ValueError):
        return False
    return (
        age >= int(rules["economic_harvest_day"])
        and age <= int(rules["max_yield_day"])
        and yield_units < int(rules["pre_harvest_yield_target"])
    )


class CodexC2Agent(E16TrainingAgent):
    """C2 policy with lifecycle-safe crops and gated economic expansion."""

    def __init__(self, candidate_config: dict[str, Any] | None = None):
        config = candidate_config or load_candidate_config()
        super().__init__(config)
        self.candidate_id = "CODEX_C2"
        self.crop_pattern = tuple(config["crop_pattern"])
        self.bootstrap_crop_pattern = tuple(config["bootstrap_crop_pattern"])
        self.turns_per_day = int(config["turns_per_day"])
        self.minimum_post_plant_action_phases = int(
            config["minimum_post_plant_action_phases"]
        )
        self.bootstrap_crop_target = int(config["bootstrap_crop_target"])
        self.max_wheat_plants_per_day = int(config["max_wheat_plants_per_day"])
        self.bootstrap_workforce_headcount = int(
            config["bootstrap_workforce_headcount"]
        )
        self.land_expansion_min_active = int(config["land_expansion_min_active"])
        self.land_expansion_min_cash = float(config["land_expansion_min_cash"])
        self.livestock_activation_min_crop_fraction = float(
            config["livestock_activation_min_crop_fraction"]
        )
        self.livestock_activation_min_cash = float(
            config["livestock_activation_min_cash"]
        )
        self.crop_horizon_margin_steps = int(config["crop_horizon_margin_steps"])
        self.episode_steps = 720
        self._current_step = 0
        self._bootstrap_phase = True
        self._assignment_day: int | None = None
        self._sticky_targets: dict[int, tuple[tuple[int, int], int]] = {}
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None

    def _active_values(self, quadrants: int) -> tuple[int, int, int, float]:
        self._bootstrap_phase = quadrants < 2 or self.t0_step is None
        if self._bootstrap_phase:
            return self.bootstrap_crop_target, 0, 0, 0.70
        return (
            int(self.config["crop_working_set_target"]),
            int(self.config["pasture_allocation_target"]),
            int(self.config["livestock_headcount_target"]),
            float(self.config["watering_dispatch_priority"]),
        )

    def _plant_serviceable_before_eod(self, hour: int) -> bool:
        later_phases = self.turns_per_day - 1 - hour
        return later_phases >= self.minimum_post_plant_action_phases

    def _crop_serviceable_before_terminal(self, crop: str, engine_step: int) -> bool:
        maturity_steps = (
            int(CROP_RULES[crop]["economic_harvest_day"]) * self.turns_per_day
        )
        remaining_steps = self.episode_steps - engine_step
        return remaining_steps > maturity_steps + self.crop_horizon_margin_steps

    def _effective_crop_plan(
        self, crop_target: int, engine_step: int
    ) -> dict[tuple[int, int], str | None]:
        pattern = (
            self.bootstrap_crop_pattern if self._bootstrap_phase else self.crop_pattern
        )
        plan = _stable_crop_plan(crop_target, pattern)
        wheat_serviceable = self._crop_serviceable_before_terminal(
            "WHEAT", engine_step
        )
        for target, crop in tuple(plan.items()):
            if not self._crop_serviceable_before_terminal(crop, engine_step):
                if wheat_serviceable:
                    plan[target] = "WHEAT"
                else:
                    plan[target] = None
        return plan

    def _task_action(
        self,
        worker_id: int,
        position: tuple[int, int],
        priority_groups: list[list[tuple[tuple[int, int], list[str]]]],
        reserved: set[tuple[int, int]],
    ) -> list[str] | None:
        indexed: list[tuple[int, tuple[int, int], list[str]]] = []
        for rank, group in enumerate(priority_groups):
            indexed.extend(
                (rank, target, action)
                for target, action in group
                if target not in reserved
            )
        if not indexed:
            self._sticky_targets.pop(worker_id, None)
            return None

        chosen: tuple[int, tuple[int, int], list[str]] | None = None
        sticky = self._sticky_targets.get(worker_id)
        if sticky is not None:
            sticky_target, _ = sticky
            sticky_candidates = [item for item in indexed if item[1] == sticky_target]
            if sticky_candidates:
                sticky_item = min(sticky_candidates, key=lambda item: item[0])
                if not any(item[0] < sticky_item[0] for item in indexed):
                    chosen = sticky_item

        if chosen is None:
            chosen = min(
                indexed,
                key=lambda item: (
                    item[0],
                    abs(position[0] - item[1][0])
                    + abs(position[1] - item[1][1]),
                    item[1][1],
                    item[1][0],
                ),
            )

        rank, target, action = chosen
        reserved.add(target)
        if target == position:
            self._sticky_targets.pop(worker_id, None)
            return action
        self._sticky_targets[worker_id] = (target, rank)
        return _move_towards(position, target)

    def _unit_actions(
        self,
        observation: dict[str, Any],
        farm: dict[str, Any],
        private: dict[str, Any],
        crop_target: int,
        pasture_target: int,
        herd_target: int,
        watering_priority: float,
        shutdown: bool,
    ) -> list[list[str]]:
        del watering_priority  # HIGH is preserved; C2 orders needs by engine deadline.

        positions = self._positions(farm)
        inventories = list(private.get("inventories", []))
        while len(inventories) < len(positions):
            inventories.append({})
        shed = private.get("shed", {}) or {}
        day = int(observation.get("day", 0))
        hour = int(observation.get("hour", 0))
        engine_step = int(observation.get("step", 0))
        if self._assignment_day != day:
            self._assignment_day = day
            self._sticky_targets.clear()

        crop_plan = self._effective_crop_plan(crop_target, engine_step)
        pasture_positions = CODEX_PASTURE_POSITIONS[:pasture_target]
        reserved: set[tuple[int, int]] = set()
        reserved_cow_pickups = 0
        reserved_wheat_pickups = 0

        allow_plant = self._plant_serviceable_before_eod(hour)

        decay_harvest: list[tuple[tuple[int, int], list[str]]] = []
        critical_water: list[tuple[tuple[int, int], list[str]]] = []
        yield_window_water: list[tuple[tuple[int, int], list[str]]] = []
        yield_completion_water: list[tuple[tuple[int, int], list[str]]] = []
        regular_water: list[tuple[tuple[int, int], list[str]]] = []
        crop_harvest: list[tuple[tuple[int, int], list[str]]] = []
        retirement_clearance: list[tuple[tuple[int, int], list[str]]] = []
        weed_recovery: list[tuple[tuple[int, int], list[str]]] = []
        crop_plant: list[tuple[tuple[int, int], list[str]]] = []
        pasture_build: list[tuple[tuple[int, int], list[str]]] = []
        empty_pasture: list[tuple[tuple[int, int], list[str]]] = []
        feed_targets: list[tuple[tuple[int, int], list[str]]] = []
        care_targets: list[tuple[tuple[int, int], list[str]]] = []
        fertilizer_targets: list[tuple[tuple[int, int], list[str]]] = []
        animal_harvest: list[tuple[tuple[int, int], list[str]]] = []

        available_seeds = {
            crop: int(private.get("seeds", {}).get(crop, 0)) for crop in CROP_MIX
        }
        wheat_planted_today = sum(
            1
            for target in crop_plan
            if plant_matches_cohort(self._tile(farm, target), "WHEAT", day)
        )
        wheat_plant_slots = max(
            0, self.max_wheat_plants_per_day - wheat_planted_today
        )
        for target, crop in crop_plan.items():
            tile = self._tile(farm, target)
            state = classify_tile_lifecycle(tile, in_working_set=True, day=day)

            if state == RETIREMENT_DUE:
                if not shutdown:
                    retirement_clearance.append((target, ["DIG"]))
                continue
            if state == LOST_WEED:
                if not shutdown:
                    weed_recovery.append((target, ["DIG"]))
                continue
            if state == EMPTY_ASSIGNED:
                if (
                    not shutdown
                    and allow_plant
                    and crop is not None
                    and self._crop_serviceable_before_terminal(crop, engine_step)
                    and available_seeds[crop] > 0
                    and (crop != "WHEAT" or wheat_plant_slots > 0)
                ):
                    crop_plant.append((target, ["PLANT", crop]))
                    available_seeds[crop] -= 1
                    if crop == "WHEAT":
                        wheat_plant_slots -= 1
                continue

            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                if not bool(tile.get("watered_today", False)):
                    if water_loss_at_eod_if_unserved(tile):
                        target_list = critical_water
                    elif state == YIELD_ACCUMULATING:
                        target_list = yield_window_water
                    elif yield_completion_water_due(tile, day):
                        target_list = yield_completion_water
                    else:
                        target_list = regular_water
                    target_list.append((target, ["WATER"]))
                if state in {YIELD_ACCUMULATING, HARVEST_READY} and (
                    lifespan_decay_started(tile, engine_step)
                ):
                    decay_harvest.append((target, ["HARVEST"]))
                elif state == HARVEST_READY:
                    target_list = (
                        crop_harvest
                    )
                    target_list.append((target, ["HARVEST"]))

        for target in pasture_positions:
            tile = self._tile(farm, target)
            if tile is None and not shutdown:
                pasture_build.append((target, ["BUILD_PASTURE"]))
            elif (
                isinstance(tile, dict)
                and tile.get("kind") == "PASTURE"
                and not tile.get("animal")
            ):
                empty_pasture.append((target, ["PASS"]))
            elif isinstance(tile, dict) and tile.get("animal") == "COW":
                if not tile.get("fed_today", False):
                    feed_targets.append((target, ["FEED"]))
                if not tile.get("cared_today", False):
                    care_targets.append((target, ["CARE"]))
                if tile.get("fertilizer_available", False):
                    fertilizer_targets.append((target, ["COLLECT_FERTILIZER"]))
                if int(tile.get("yield_units", 0)) > 0:
                    animal_harvest.append((target, ["HARVEST"]))

        priority_groups = [
            decay_harvest,
            critical_water,
            yield_window_water,
            yield_completion_water,
            crop_harvest,
            regular_water,
            retirement_clearance,
            weed_recovery,
            crop_plant,
            fertilizer_targets,
            animal_harvest,
            care_targets,
            pasture_build,
        ]

        actions: list[list[str]] = []
        for worker_id, position in enumerate(positions):
            inventory = (
                inventories[worker_id]
                if isinstance(inventories[worker_id], dict)
                else {}
            )
            total_inventory = _inventory_total(inventory)
            carried_cow = int(inventory.get("COW", 0)) > 0
            carried_wheat = int(inventory.get("WHEAT", 0)) > 0
            carried_non_feed = any(
                item not in {"WHEAT", "COW"} and amount > 0
                for item, amount in inventory.items()
            )

            if carried_cow:
                self._sticky_targets.pop(worker_id, None)
                choices = [(target, ["PLACE", "COW"]) for target, _ in empty_pasture]
                action = self._target_action(position, choices, reserved)
                actions.append(
                    action
                    or (
                        ["DROP"]
                        if position in SHED_TILES
                        else _move_towards(position, (4, 4))
                    )
                )
                continue

            if carried_wheat and feed_targets:
                self._sticky_targets.pop(worker_id, None)
                action = self._target_action(position, feed_targets, reserved)
                if action is not None:
                    actions.append(action)
                    continue

            if (
                carried_non_feed
                or (carried_wheat and not feed_targets)
                or total_inventory >= 5
            ):
                self._sticky_targets.pop(worker_id, None)
                actions.append(
                    ["DROP"]
                    if position in SHED_TILES
                    else _move_towards(position, (4, 4))
                )
                continue

            if position in SHED_TILES and total_inventory == 0:
                available_cows = max(
                    0, int(shed.get("COW", 0)) - reserved_cow_pickups
                )
                if len(empty_pasture) > reserved_cow_pickups and available_cows > 0:
                    self._sticky_targets.pop(worker_id, None)
                    reserved_cow_pickups += 1
                    actions.append(["PICKUP", "COW", 1])
                    continue
                available_wheat = max(
                    0, int(shed.get("WHEAT", 0)) - reserved_wheat_pickups
                )
                remaining_feed = max(0, len(feed_targets) - reserved_wheat_pickups)
                if available_wheat > 0 and remaining_feed > 0:
                    self._sticky_targets.pop(worker_id, None)
                    quantity = min(5, available_wheat, remaining_feed)
                    reserved_wheat_pickups += quantity
                    actions.append(["PICKUP", "WHEAT", quantity])
                    continue

            action = self._task_action(
                worker_id, position, priority_groups, reserved
            )
            actions.append(action or ["PASS"])

        return actions

    def _market_orders(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        market: dict[str, Any],
        quadrants: int,
        crop_target: int,
        pasture_target: int,
        herd_target: int,
        shutdown: bool,
    ) -> list[list[Any]]:
        del shutdown
        orders: list[list[Any]] = []
        cash = float(farm.get("money", 0.0))
        floor = float(self.config["operating_cash_floor"])

        def add(order: list[Any], estimated_cost: float = 0.0) -> bool:
            nonlocal cash
            if len(orders) >= 10 or cash - estimated_cost < floor:
                return False
            orders.append(order)
            cash -= estimated_cost
            return True

        crop_plan = self._effective_crop_plan(crop_target, self._current_step)
        active_by_crop = {crop: 0 for crop in CROP_MIX}
        for position in CODEX_CROP_POSITIONS[:crop_target]:
            tile = self._tile(farm, position)
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") in active_by_crop
            ):
                active_by_crop[tile["crop"]] += 1
        active_total = sum(active_by_crop.values())

        desired_by_crop = {crop: 0 for crop in CROP_MIX}
        for crop in crop_plan.values():
            if crop is not None:
                desired_by_crop[crop] += 1
        seed_costs = {"WHEAT": 10, "STRAWBERRY": 100, "MELON": 80}
        for crop in CROP_MIX:
            deficit = max(
                0,
                desired_by_crop[crop]
                - active_by_crop[crop]
                - int(private.get("seeds", {}).get(crop, 0)),
            )
            affordable = max(0, int((cash - floor) // seed_costs[crop]))
            quantity = min(deficit, affordable)
            if quantity:
                add(["BUY_SEED", crop, quantity], quantity * seed_costs[crop])

        if (
            quadrants < int(self.config["quadrants_owned"])
            and active_total >= self.land_expansion_min_active
            and cash >= self.land_expansion_min_cash
        ):
            add(["BUY_LAND"], 1000.0)

        hands = len(farm.get("hands", []))
        target_hands = (
            self.bootstrap_workforce_headcount
            if quadrants < 2
            else int(self.config["workforce_headcount"])
        )
        hires_today = int(farm.get("hires_today", 0))
        for offset in range(max(0, target_hands - hands)):
            if not add(["HIRE"], float(_fib(hires_today + offset))):
                break

        shed = private.get("shed", {}) or {}
        inventories = private.get("inventories", []) or []
        pasture_count = sum(
            1
            for position in CODEX_PASTURE_POSITIONS[:pasture_target]
            if isinstance(self._tile(farm, position), dict)
            and self._tile(farm, position).get("kind") == "PASTURE"
        )
        cows_on_tiles = sum(
            1
            for position in CODEX_PASTURE_POSITIONS[:pasture_target]
            if isinstance(self._tile(farm, position), dict)
            and self._tile(farm, position).get("animal") == "COW"
        )
        cows_in_transit = int(shed.get("COW", 0)) + sum(
            int(inv.get("COW", 0)) for inv in inventories if isinstance(inv, dict)
        )
        livestock_activation_target = int(
            crop_target * self.livestock_activation_min_crop_fraction
        )
        if (
            quadrants >= 2
            and active_total >= livestock_activation_target
            and cash >= self.livestock_activation_min_cash
        ):
            cow_deficit = max(
                0, min(herd_target, pasture_count) - cows_on_tiles - cows_in_transit
            )
            affordable = max(0, int((cash - floor) // 400))
            quantity = min(cow_deficit, affordable, 10)
            if quantity:
                add(["BUY_ANIMAL", "COW", quantity], quantity * 400.0)

        feed_demand = cows_on_tiles * 3 + (2 if cows_on_tiles else 0)
        wheat_carried = sum(
            int(inv.get("WHEAT", 0)) for inv in inventories if isinstance(inv, dict)
        )
        wheat_deficit = max(
            0, feed_demand - int(shed.get("WHEAT", 0)) - wheat_carried
        )
        wheat_price = float((market.get("prices", {}) or {}).get("WHEAT", 10.0))
        if wheat_deficit and wheat_price > 0:
            quantity = min(
                wheat_deficit, max(0, int((cash - floor) // wheat_price)), 10
            )
            if quantity:
                add(["BUY_PRODUCT", "WHEAT", quantity], quantity * wheat_price)

        reserve = feed_demand
        for product in ("MILK", "STRAWBERRY", "MELON", "WHEAT", "FERTILIZER"):
            quantity = int(shed.get(product, 0))
            if product == "WHEAT":
                quantity = max(0, quantity - reserve)
            if quantity > 0 and len(orders) < 10:
                orders.append(["SELL", product, quantity])
        return orders[:10]

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        if isinstance(configuration, dict):
            turns_per_day = configuration.get("turnsPerDay", self.turns_per_day)
            episode_steps = configuration.get("episodeSteps", self.episode_steps)
        else:
            turns_per_day = getattr(
                configuration, "turnsPerDay", self.turns_per_day
            )
            episode_steps = getattr(
                configuration, "episodeSteps", self.episode_steps
            )
        try:
            parsed_turns = int(turns_per_day)
        except (TypeError, ValueError):
            parsed_turns = self.turns_per_day
        if parsed_turns > 0:
            self.turns_per_day = parsed_turns
        try:
            parsed_episode_steps = int(episode_steps)
        except (TypeError, ValueError):
            parsed_episode_steps = self.episode_steps
        if parsed_episode_steps > 0:
            self.episode_steps = parsed_episode_steps
        self._current_step = int(observation.get("step", 0))
        return super().__call__(observation, configuration)


def create_agent(
    candidate_config: dict[str, Any] | None = None,
) -> Callable[[dict[str, Any], Any], dict[str, Any]]:
    """Create one isolated, fail-closed Codex C2 episode agent."""

    instance = CodexC2Agent(candidate_config)

    def tournament_agent(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            return instance(observation, configuration)
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            return deepcopy(_SAFE_PASS)

    tournament_agent.codex_c2_instance = instance  # type: ignore[attr-defined]
    tournament_agent.candidate_id = "CODEX_C2"  # type: ignore[attr-defined]
    return tournament_agent
