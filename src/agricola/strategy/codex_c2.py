"""Codex C2 lifecycle-aware tournament candidate.

The candidate reuses the E16 infrastructure and changes only crop task
eligibility and arbitration. It is intentionally exposed through ``create_agent``
so a neutral tournament runner can instantiate one isolated policy per episode.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.e16.policy import (
    CROP_MIX,
    CROP_POSITIONS,
    PASTURE_POSITIONS,
    SHED_TILES,
    E16TrainingAgent,
    _inventory_total,
    _move_towards,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = (
    REPO_ROOT / "configs" / "model_spec_c2" / "CODEX_C2_CONFIG.json"
)

CROP_RULES = {
    "WHEAT": {"first_yield_day": 2, "ongoing": False},
    "STRAWBERRY": {"first_yield_day": 10, "ongoing": True},
    "MELON": {"first_yield_day": 10, "ongoing": False},
}

OUT_OF_SCOPE = "OUT_OF_SCOPE"
EMPTY_ASSIGNED = "EMPTY_ASSIGNED"
GROWING = "GROWING"
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
    }
    missing = required - set(config)
    if missing:
        raise ValueError(f"missing Codex C2 config fields: {sorted(missing)}")
    if config["candidate_id"] != "CODEX_C2":
        raise ValueError("unexpected candidate_id")
    if config["schema_version"] != "model_spec_c2.codex.v1":
        raise ValueError("unexpected Codex C2 config schema")

    target = int(config["crop_working_set_target"])
    if not 1 <= target <= len(CROP_POSITIONS):
        raise ValueError("crop_working_set_target is outside the supported board")
    pattern = list(config["crop_pattern"])
    if not pattern or any(crop not in CROP_RULES for crop in pattern):
        raise ValueError("crop_pattern contains an unsupported crop")
    if set(pattern) != set(CROP_MIX):
        raise ValueError("crop_pattern must preserve the E16 crop mix")
    if int(config["turns_per_day"]) <= 0:
        raise ValueError("turns_per_day must be positive")
    if int(config["minimum_post_plant_action_phases"]) < 1:
        raise ValueError("new PLANT must leave at least one later action phase")
    return deepcopy(config)


def _stable_crop_plan(
    target: int, pattern: list[str] | tuple[str, ...]
) -> dict[tuple[int, int], str]:
    """Assign a stable crop role to each working-set position."""

    return {
        position: pattern[index % len(pattern)]
        for index, position in enumerate(CROP_POSITIONS[:target])
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

    ready = (
        yield_units > 0
        and day - planted_day >= int(rules["first_yield_day"])
    )
    if ready:
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


class CodexC2Agent(E16TrainingAgent):
    """E16-compatible policy with C2 crop lifecycle realization."""

    def __init__(self, candidate_config: dict[str, Any] | None = None):
        config = candidate_config or load_candidate_config()
        super().__init__(config)
        self.candidate_id = "CODEX_C2"
        self.crop_pattern = tuple(config["crop_pattern"])
        self.turns_per_day = int(config["turns_per_day"])
        self.minimum_post_plant_action_phases = int(
            config["minimum_post_plant_action_phases"]
        )

    def _plant_serviceable_before_eod(self, hour: int) -> bool:
        later_phases = self.turns_per_day - 1 - hour
        return later_phases >= self.minimum_post_plant_action_phases

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
        crop_plan = _stable_crop_plan(crop_target, self.crop_pattern)
        pasture_positions = PASTURE_POSITIONS[:pasture_target]
        reserved: set[tuple[int, int]] = set()
        reserved_cow_pickups = 0
        reserved_wheat_pickups = 0

        day = int(observation.get("day", 0))
        hour = int(observation.get("hour", 0))
        engine_step = int(observation.get("step", 0))
        allow_plant = not shutdown and self._plant_serviceable_before_eod(hour)

        decay_harvest: list[tuple[tuple[int, int], list[str]]] = []
        critical_water: list[tuple[tuple[int, int], list[str]]] = []
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
                if allow_plant and available_seeds[crop] > 0:
                    crop_plant.append((target, ["PLANT", crop]))
                    available_seeds[crop] -= 1
                continue

            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                if not bool(tile.get("watered_today", False)):
                    target_list = (
                        critical_water
                        if water_loss_at_eod_if_unserved(tile)
                        else regular_water
                    )
                    target_list.append((target, ["WATER"]))
                if state == HARVEST_READY:
                    target_list = (
                        decay_harvest
                        if lifespan_decay_started(tile, engine_step)
                        else crop_harvest
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
            regular_water,
            crop_harvest,
            retirement_clearance,
            weed_recovery,
            fertilizer_targets,
            animal_harvest,
            care_targets,
            pasture_build,
            crop_plant,
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
                action = self._target_action(position, feed_targets, reserved)
                if action is not None:
                    actions.append(action)
                    continue

            if (
                carried_non_feed
                or (carried_wheat and not feed_targets)
                or total_inventory >= 5
            ):
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
                    reserved_cow_pickups += 1
                    actions.append(["PICKUP", "COW", 1])
                    continue
                available_wheat = max(
                    0, int(shed.get("WHEAT", 0)) - reserved_wheat_pickups
                )
                remaining_feed = max(0, len(feed_targets) - reserved_wheat_pickups)
                if available_wheat > 0 and remaining_feed > 0:
                    quantity = min(5, available_wheat, remaining_feed)
                    reserved_wheat_pickups += quantity
                    actions.append(["PICKUP", "WHEAT", quantity])
                    continue

            action = None
            for group in priority_groups:
                action = self._target_action(position, group, reserved)
                if action is not None:
                    break
            actions.append(action or ["PASS"])

        return actions

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        if isinstance(configuration, dict):
            turns_per_day = configuration.get("turnsPerDay", self.turns_per_day)
        else:
            turns_per_day = getattr(
                configuration, "turnsPerDay", self.turns_per_day
            )
        try:
            parsed_turns = int(turns_per_day)
        except (TypeError, ValueError):
            parsed_turns = self.turns_per_day
        if parsed_turns > 0:
            self.turns_per_day = parsed_turns
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
        except (AttributeError, IndexError, KeyError, RuntimeError, TypeError, ValueError):
            return deepcopy(_SAFE_PASS)

    tournament_agent.codex_c2_instance = instance  # type: ignore[attr-defined]
    tournament_agent.candidate_id = "CODEX_C2"  # type: ignore[attr-defined]
    return tournament_agent
