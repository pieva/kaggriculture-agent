#!/usr/bin/env python3
"""Deterministic Gate-0A planner for the E18.18 native 7-7-0 plan.

This module deliberately is not an agent policy.  It turns the composition
constraints inferred from the exact Jesse 7-7-0 cohort into tile-local task
bundles, routes those bundles over a conservative observed capacity envelope,
and checks biological safety in a deterministic shadow model.  Exact engine,
cash, shed and market parity remain Gate 0B and must pass before an executor is
created.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass, field
from functools import cache
from itertools import pairwise
from pathlib import Path
from typing import Any

from agricola.core.state import CROPS

ROOT = Path(__file__).resolve().parents[5]
DEFAULT_CONFIG = (
    ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_18_770_CAPACITY_TRAJECTORY_PLANNER_V1.json"
)

Coord = tuple[int, int]
SPAWN: Coord = (4, 4)
SHED_ACCESS: tuple[Coord, ...] = ((4, 4), (5, 4), (4, 5), (5, 5))
CHECKPOINT_DAYS = (1, 5, 10, 15, 20, 25, 30)
ANIMALS = {
    "COW": {"first_yield_day": 8, "interval": 2, "max_held": 6},
    "SHEEP": {"first_yield_day": 6, "interval": 3, "max_held": 6},
}


def _quadrant(coord: Coord) -> str:
    x, y = coord
    if x < 5 and y < 5:
        return "Q0"
    if x >= 5 and y < 5:
        return "Q1"
    if x < 5 and y >= 5:
        return "Q2"
    return "Q3"


def _manhattan(left: Coord, right: Coord) -> int:
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def _serpentine(coords: Iterable[Coord]) -> list[Coord]:
    return sorted(coords, key=lambda p: (p[1], p[0] if p[1] % 2 == 0 else -p[0]))


def load_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_18_770_CAPACITY_TRAJECTORY_PLANNER_V1",
        "model_spec_version": "CODEX-E18.18-770-CAPACITY-TRAJECTORY-PLANNER-V1",
        "epistemic_role": "DEVELOPMENT_GATE_0A_ONLY",
        "topology": "7-7-0",
        "pasture_fill_target": 14,
        "livestock_resource_cap": 14,
        "livestock_mix": {"COW": 9, "SHEEP": 5},
        "workers_peak_hands": 12,
        "workers_peak_units": 13,
        "turns_per_day": 24,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    pastures = [tuple(value) for value in config["pasture_targets"]]
    if len(pastures) != 14 or len(set(pastures)) != 14:
        raise ValueError("pasture_targets must contain fourteen unique cells")
    counts = Counter(_quadrant(coord) for coord in pastures)
    if counts != Counter({"Q0": 7, "Q1": 7}):
        raise ValueError("pasture topology must be exactly 7-7-0")
    if tuple(config["late_q0_pasture"]) not in pastures:
        raise ValueError("late_q0_pasture must be a target pasture")
    slots = config["daily_available_action_slots"]
    if len(slots) != 30 or any(int(value) <= 0 for value in slots):
        raise ValueError("daily capacity envelope must cover all thirty days")
    reserve = float(config["reserve_ratio"])
    if not 0.0 < reserve < 1.0:
        raise ValueError("reserve_ratio must be between zero and one")
    return deepcopy(config)


@dataclass
class CropState:
    crop: str
    planted_day: int
    watered_today: bool = False
    consecutive_unwatered: int = 0
    yield_units: int = 0
    production_count: int = 0
    fertilized_until_day: int = -1


@dataclass
class AnimalState:
    species: str
    placed_day: int
    fed_today: bool = False
    cared_today: bool = False
    consecutive_unfed: int = 0
    fertilizer_available: bool = False
    pending_care_bonus: int = 0
    yield_units: int = 0


@dataclass
class Bundle:
    coord: Coord
    role: str
    actions: list[dict[str, Any]] = field(default_factory=list)

    @property
    def carries_output(self) -> bool:
        return any(
            action["opcode"] in {"HARVEST", "COLLECT_FERTILIZER"}
            for action in self.actions
        )

    @property
    def needs_feed(self) -> bool:
        return any(action["opcode"] == "FEED" for action in self.actions)

    @property
    def needs_fertilizer(self) -> bool:
        return any(action["opcode"] == "FERTILIZE" for action in self.actions)

    @property
    def pickup_items(self) -> Counter[str]:
        items: Counter[str] = Counter()
        for action in self.actions:
            opcode = action["opcode"]
            if opcode == "FEED":
                items["WHEAT"] += int(action["arguments"].get("units", 1))
            elif opcode == "FERTILIZE":
                items["FERTILIZER"] += int(action["arguments"].get("units", 1))
            elif opcode == "PLACE":
                items[str(action["arguments"]["animal"])] += 1
        return items


@dataclass
class WorkerRoute:
    worker: int
    capacity: int
    available_from_turn: int
    position: Coord = SPAWN
    actions: list[dict[str, Any]] = field(default_factory=list)
    carries_output: bool = False
    expected_output: Counter[str] = field(default_factory=Counter)

    @property
    def used(self) -> int:
        return len(self.actions)


class CapacityTrajectoryPlanner:
    """Build and route the frozen E18.18 composition plan."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = load_config() if config is None else deepcopy(config)
        self.pasture_targets = frozenset(
            tuple(value) for value in self.config["pasture_targets"]
        )
        self.late_pasture = tuple(self.config["late_q0_pasture"])
        footprint = {
            (x, y)
            for y in range(10)
            for x in range(10)
            if _quadrant((x, y)) in {"Q0", "Q1", "Q2"}
        }
        self.final_crop_targets = frozenset(footprint - self.pasture_targets)
        if len(self.final_crop_targets) != 61:
            raise AssertionError("7-7-0 layout must expose exactly 61 crop cells")

        q0 = _serpentine(
            coord for coord in self.final_crop_targets if _quadrant(coord) == "Q0"
        )
        q1 = _serpentine(
            coord for coord in self.final_crop_targets if _quadrant(coord) == "Q1"
        )
        q2 = _serpentine(
            coord for coord in self.final_crop_targets if _quadrant(coord) == "Q2"
        )
        if (len(q0), len(q1), len(q2)) != (18, 18, 25):
            raise AssertionError("unexpected crop capacity by quadrant")

        self.melon_coords = tuple(q0[:12])
        self.opening_wheat_coords = (*q0[12:], self.late_pasture)
        self.q0_early_strawberry = tuple(self.opening_wheat_coords[:2])
        self.q1_strawberry = tuple(q1)
        # Keep the frequently rotated annuals close to the central shed. The
        # ongoing Strawberry footprint absorbs the remote Q2 cells because it
        # avoids DIG+PLANT on every four-day Wheat cycle.
        self.q2_wheat = tuple(q2[:7])
        self.q2_strawberry = tuple(q2[7:])
        self.all_strawberry = frozenset(
            (*self.q0_early_strawberry, *self.q1_strawberry, *self.q2_strawberry)
        )
        if len(self.all_strawberry) != 38:
            raise AssertionError("strawberry footprint must contain 38 cells")

        self.crops: dict[Coord, CropState] = {}
        self.animals: dict[Coord, AnimalState] = {}
        self.structures: set[Coord] = set()
        self.crop_losses = 0
        self.animal_losses = 0
        self.illegal_actions: list[str] = []
        self.harvested = Counter()
        self.seed_use = Counter()
        self.fertilizer_stock = 0
        self.fertilizer_collected_today = 0
        self.fertilizer_used = 0
        self.fertilizer_used_by_crop: Counter[str] = Counter()
        self.fertilizer_used_today_by_crop: Counter[str] = Counter()
        self.daily: list[dict[str, Any]] = []
        self.trajectory: list[dict[str, Any]] = []

        self.crop_plant_day: dict[Coord, int] = {}
        self.strawberry_retire_day: dict[Coord, int] = {}
        self._define_crop_calendar()
        self.animal_plan = self._define_animal_calendar()

    def _define_crop_calendar(self) -> None:
        for coord in (*self.melon_coords, *self.opening_wheat_coords):
            self.crop_plant_day[coord] = 1
        for coord in self.q0_early_strawberry:
            self.crop_plant_day[coord] = 6
        for index, coord in enumerate(self.q1_strawberry):
            self.crop_plant_day[coord] = 7 + min(index // 5, 3)
        for index, coord in enumerate(self.q2_strawberry):
            self.crop_plant_day[coord] = 11 + index // 9
        q2_wheat_days = (11, 11, 12, 12, 12, 12, 12)
        for coord, plant_day in zip(self.q2_wheat, q2_wheat_days, strict=True):
            self.crop_plant_day[coord] = plant_day

        early = [*self.q0_early_strawberry, *self.q1_strawberry[:14]]
        for index, coord in enumerate(early):
            self.strawberry_retire_day[coord] = 21 + min(index // 3, 4)
        for coord in self.all_strawberry.difference(early):
            planted = self.crop_plant_day[coord]
            self.strawberry_retire_day[coord] = min(29, planted + 18)

    def _define_animal_calendar(self) -> dict[Coord, tuple[int, str]]:
        q0 = _serpentine(
            coord for coord in self.pasture_targets if _quadrant(coord) == "Q0"
        )
        q0_regular = [coord for coord in q0 if coord != self.late_pasture]
        q1 = _serpentine(
            coord for coord in self.pasture_targets if _quadrant(coord) == "Q1"
        )
        plan: dict[Coord, tuple[int, str]] = {}
        opening_species = ("COW", "COW", "SHEEP", "SHEEP")
        for coord, species in zip(q0_regular[:4], opening_species, strict=True):
            plan[coord] = (1, species)
        for coord in q0_regular[4:]:
            plan[coord] = (5, "COW")
        q1_species = ("COW", "COW", "COW", "COW", "COW", "SHEEP", "SHEEP")
        for coord, species in zip(q1, q1_species, strict=True):
            plan[coord] = (10, species)
        plan[self.late_pasture] = (14, "SHEEP")
        if Counter(species for _, species in plan.values()) != Counter(
            {"COW": 9, "SHEEP": 5}
        ):
            raise AssertionError("animal calendar does not implement 9+5")
        return plan

    @staticmethod
    def _op(opcode: str, **arguments: Any) -> dict[str, Any]:
        return {"opcode": opcode, "arguments": arguments}

    def _crop_mix(self) -> dict[str, int]:
        return dict(
            sorted(Counter(state.crop for state in self.crops.values()).items())
        )

    def _animal_mix(self) -> dict[str, int]:
        return dict(
            sorted(Counter(state.species for state in self.animals.values()).items())
        )

    def _plant(self, coord: Coord, crop: str, day: int, bundle: Bundle) -> None:
        if coord in self.crops or coord in self.structures:
            self.illegal_actions.append(f"D{day}: PLANT occupied {coord}")
            return
        state = CropState(
            crop=crop,
            planted_day=day,
            yield_units=0 if CROPS[crop]["ongoing"] else 1,
        )
        self.crops[coord] = state
        self.seed_use[crop] += 1
        bundle.actions.append(self._op("PLANT", crop=crop))
        self._water(coord, day, bundle)

    def _water(self, coord: Coord, day: int, bundle: Bundle) -> None:
        state = self.crops.get(coord)
        if state is None or state.watered_today:
            self.illegal_actions.append(f"D{day}: invalid/duplicate WATER {coord}")
            return
        state.watered_today = True
        crop = CROPS[state.crop]
        if not crop["ongoing"]:
            age = day - state.planted_day
            window_start = (int(crop["max_yield_day"]) + 1) // 2
            if window_start <= age <= int(crop["max_yield_day"]):
                bonus = 2 if state.fertilized_until_day >= day else 1
                state.yield_units = min(
                    int(crop["max_yield"]), state.yield_units + bonus
                )
        bundle.actions.append(self._op("WATER"))

    def _fertilize(self, coord: Coord, day: int, bundle: Bundle) -> bool:
        state = self.crops.get(coord)
        if state is None or self.fertilizer_stock <= 0:
            return False
        # One application remains active for the current day and the following
        # two days. Reapplying inside that window spends both fertilizer and a
        # scarce route slot without increasing the biological bonus.
        if state.fertilized_until_day >= day:
            return False
        budget = int(
            self.config.get("fertilizer_budget_by_crop", {}).get(state.crop, 0)
        )
        if self.fertilizer_used_by_crop[state.crop] >= budget:
            return False
        daily_cap = int(
            self.config.get("fertilizer_daily_caps_by_crop", {})
            .get(state.crop, {})
            .get(str(day), budget)
        )
        if self.fertilizer_used_today_by_crop[state.crop] >= daily_cap:
            return False
        self.fertilizer_stock -= 1
        self.fertilizer_used += 1
        self.fertilizer_used_by_crop[state.crop] += 1
        self.fertilizer_used_today_by_crop[state.crop] += 1
        state.fertilized_until_day = max(state.fertilized_until_day, day + 2)
        bundle.actions.append(self._op("FERTILIZE", units=1))
        return True

    def _harvest_crop(self, coord: Coord, day: int, bundle: Bundle) -> None:
        state = self.crops.get(coord)
        if state is None:
            self.illegal_actions.append(f"D{day}: HARVEST missing crop {coord}")
            return
        crop = CROPS[state.crop]
        age = day - state.planted_day
        if age < int(crop["first_yield_day"]) or state.yield_units <= 0:
            self.illegal_actions.append(f"D{day}: immature/empty HARVEST {coord}")
            return
        expected_units = state.yield_units
        self.harvested[state.crop] += expected_units
        state.yield_units = 0
        bundle.actions.append(
            self._op(
                "HARVEST",
                crop=state.crop,
                expected_units=expected_units,
            )
        )
        if not crop["ongoing"]:
            del self.crops[coord]

    def _dig_crop(self, coord: Coord, day: int, bundle: Bundle) -> None:
        if coord not in self.crops:
            self.illegal_actions.append(f"D{day}: DIG missing crop {coord}")
            return
        del self.crops[coord]
        bundle.actions.append(self._op("DIG"))

    def _should_water(self, coord: Coord, state: CropState, day: int) -> bool:
        skip_today = set(
            self.config.get("skip_water_cells_by_day", {}).get(str(day), [])
        )
        if f"{coord[0]},{coord[1]}" in skip_today:
            return False
        if day <= int(self.config.get("d10_full_water_through_day", 0)):
            return True
        if state.consecutive_unwatered >= 1:
            return True
        crop = CROPS[state.crop]
        age = day - state.planted_day
        if day in {13, 22, 26} and crop["ongoing"]:
            return False
        if not crop["ongoing"]:
            window_start = (int(crop["max_yield_day"]) + 1) // 2
            if window_start <= age <= int(crop["max_yield_day"]):
                return True
        # Outside annual yield windows, alternate service by tile parity.  This
        # preserves the hard one-day starvation margin without spending a WATER
        # action that cannot improve nominal yield.
        return (day + coord[0] + coord[1]) % 2 == 0

    def _crop_bundles(self, day: int) -> list[Bundle]:
        bundles: dict[Coord, Bundle] = {}

        def get_bundle(coord: Coord) -> Bundle:
            return bundles.setdefault(coord, Bundle(coord=coord, role="CROP"))

        # Initial planting and expansion. Four opening Wheat cells are monetized
        # on D4 and immediately replanted: their first valid yield finances the
        # D5 livestock increment without changing the crop checkpoint. The three
        # remaining cells rotate on D5, keeping later annual work staggered. Two
        # of the replacement cells become the first Strawberry cells on D6.
        if day == 1:
            for coord in self.melon_coords:
                self._plant(coord, "MELON", day, get_bundle(coord))
            for coord in self.opening_wheat_coords:
                self._plant(coord, "WHEAT", day, get_bundle(coord))

        # Jesse's exact 7-7-0 cohort monetizes the opening Wheat on a two-day
        # cadence through D10.  This optional candidate-only calendar keeps the
        # D1/D5/D10 composition checkpoints unchanged while moving liquidity
        # forward: seven cells rotate on D3/D5 and the five cells not converted
        # to Strawberry rotate again on D7/D9.
        fast_wheat_days = {
            int(value) for value in self.config.get("d10_wheat_fast_cycle_days", [])
        }
        if day in fast_wheat_days:
            fast_fertilize_days = {
                int(value)
                for value in self.config.get("d10_fast_wheat_fertilize_days", [])
            }
            fast_coords = (
                self.opening_wheat_coords
                if day <= 5
                else tuple(
                    coord
                    for coord in self.opening_wheat_coords
                    if coord not in self.q0_early_strawberry
                )
            )
            for coord in fast_coords:
                state = self.crops.get(coord)
                if state is None or state.crop != "WHEAT":
                    self.illegal_actions.append(
                        f"D{day}: fast Wheat rotation missing WHEAT {coord}"
                    )
                    continue
                bundle = get_bundle(coord)
                if day in fast_fertilize_days:
                    self._fertilize(coord, day, bundle)
                self._water(coord, day, bundle)
                self._harvest_crop(coord, day, bundle)
                self._plant(coord, "WHEAT", day, bundle)

        if day == 4 and not fast_wheat_days:
            for coord in self.opening_wheat_coords:
                if (coord[0] + coord[1]) % 2 != 0:
                    continue
                bundle = get_bundle(coord)
                self._water(coord, day, bundle)
                self._harvest_crop(coord, day, bundle)
                self._plant(coord, "WHEAT", day, bundle)

        if day == 6:
            for coord in self.opening_wheat_coords:
                if coord not in self.q0_early_strawberry:
                    continue
                bundle = get_bundle(coord)
                self._dig_crop(coord, day, bundle)
                self._plant(coord, "STRAWBERRY", day, bundle)

        for coord in (*self.q1_strawberry, *self.q2_strawberry):
            if self.crop_plant_day[coord] == day:
                self._plant(coord, "STRAWBERRY", day, get_bundle(coord))
        for coord in self.q2_wheat:
            if self.crop_plant_day[coord] == day:
                self._plant(coord, "WHEAT", day, get_bundle(coord))

        melon_harvest_day = int(self.config.get("melon_harvest_day", 13))
        if day == melon_harvest_day:
            for coord in self.melon_coords:
                bundle = get_bundle(coord)
                self._water(coord, day, bundle)
                self._harvest_crop(coord, day, bundle)

        if day in {14, 15}:
            offset = 0 if day == 14 else 6
            for coord in self.melon_coords[offset : offset + 6]:
                self._plant(coord, "WHEAT", day, get_bundle(coord))

        if day == int(self.config["late_q0_pasture_day"]):
            coord = self.late_pasture
            bundle = get_bundle(coord)
            state = self.crops.get(coord)
            if state is not None:
                self._water(coord, day, bundle)
                if state.yield_units > 0 and day - state.planted_day >= int(
                    CROPS[state.crop]["first_yield_day"]
                ):
                    self._harvest_crop(coord, day, bundle)
                if coord in self.crops:
                    self._dig_crop(coord, day, bundle)

        # Planned Strawberry retirement. Sixteen early cells rotate to Wheat;
        # the remaining twenty-two are cleared by D29 without replacement.
        for coord, retire_day in sorted(self.strawberry_retire_day.items()):
            if retire_day != day or coord not in self.crops:
                continue
            bundle = get_bundle(coord)
            state = self.crops[coord]
            if state.yield_units > 0 and day - state.planted_day >= int(
                CROPS[state.crop]["first_yield_day"]
            ):
                self._harvest_crop(coord, day, bundle)
            if coord in self.crops:
                self._dig_crop(coord, day, bundle)
            if retire_day <= 25:
                self._plant(coord, "WHEAT", day, bundle)

        # Normal service and annual rotation. A tile already touched by a
        # transition is complete for the day, including its replacement WATER.
        touched = set(bundles)
        for coord, state in sorted(self.crops.items()):
            if coord in touched:
                continue
            crop = CROPS[state.crop]
            age = day - state.planted_day
            ongoing_production_today = False
            if crop["ongoing"]:
                next_age = day + 1 - state.planted_day
                first = int(crop["first_yield_day"])
                interval = int(crop["interval"])
                ongoing_production_today = (
                    next_age >= first
                    and (next_age - first) % interval == 0
                    and (next_age - first) // interval + 1 <= int(crop["max_yield"])
                )
            annual_yield_window_start = (
                (int(crop["max_yield_day"]) + 1) // 2 if not crop["ongoing"] else -1
            )
            fertilizer_due = bool(
                ongoing_production_today
                or (state.crop == "WHEAT" and age == annual_yield_window_start)
            )
            needs_harvest = bool(
                crop["ongoing"]
                # Batch ongoing output. Carrying a single unit back to the shed
                # creates more movement and DROP overhead than waiting one more
                # production cycle; retirement handling above remains lossless.
                and state.yield_units >= 2
                and age >= int(crop["first_yield_day"])
            ) or bool(
                not crop["ongoing"]
                and age
                >= (
                    3
                    if state.crop == "WHEAT" and (coord[0] + coord[1]) % 2 == 0
                    else int(crop["max_yield_day"])
                )
            )
            if (
                needs_harvest
                and crop["ongoing"]
                and day < int(self.config["terminal_crop_clear_day"])
                and (day + coord[0] + coord[1])
                % int(self.config.get("ongoing_harvest_phase_modulus", 1))
                != 0
            ):
                needs_harvest = False
            defer_remote_water = bool(
                crop["ongoing"]
                and _quadrant(coord) == "Q2"
                and day in set(self.config.get("q2_water_defer_days", []))
                and state.consecutive_unwatered == 0
            )
            if defer_remote_water:
                fertilizer_due = False
                should_water = False
            else:
                should_water = self._should_water(coord, state, day) or fertilizer_due
            if not needs_harvest and not should_water and not fertilizer_due:
                continue
            bundle = get_bundle(coord)
            if fertilizer_due:
                self._fertilize(coord, day, bundle)
            if should_water:
                self._water(coord, day, bundle)
            if crop["ongoing"]:
                if needs_harvest:
                    self._harvest_crop(coord, day, bundle)
                continue
            if age < int(crop["max_yield_day"]):
                continue
            self._harvest_crop(coord, day, bundle)
            if state.crop == "WHEAT" and day <= int(
                self.config["annual_replant_last_day"]
            ):
                self._plant(coord, "WHEAT", day, bundle)

        return list(bundles.values())

    def _animal_bundles(self, day: int) -> list[Bundle]:
        bundles: list[Bundle] = []
        self.fertilizer_collected_today = 0
        collection_cap = int(
            self.config.get("fertilizer_collection_caps_by_day", {}).get(
                str(day), len(self.animal_plan)
            )
        )
        collected = 0
        for coord, (placement_day, species) in sorted(self.animal_plan.items()):
            if placement_day == day:
                if coord in self.crops or coord in self.structures:
                    self.illegal_actions.append(f"D{day}: BUILD occupied {coord}")
                    continue
                self.structures.add(coord)
                self.animals[coord] = AnimalState(species=species, placed_day=day)
                bundle = Bundle(coord=coord, role="ANIMAL")
                bundle.actions.extend(
                    [
                        self._op("BUILD_PASTURE"),
                        self._op("PLACE", animal=species),
                    ]
                )
            elif coord in self.animals:
                bundle = Bundle(coord=coord, role="ANIMAL")
            else:
                continue

            state = self.animals[coord]
            if day not in set(self.config.get("animal_feed_blackout_days", [])):
                bundle.actions.append(self._op("FEED", units=1))
                state.fed_today = True
            if day not in set(self.config.get("animal_care_blackout_days", [])):
                bundle.actions.append(self._op("CARE"))
                state.cared_today = True
            if state.fertilizer_available and collected < collection_cap:
                bundle.actions.append(self._op("COLLECT_FERTILIZER"))
                state.fertilizer_available = False
                collected += 1
                self.fertilizer_collected_today += 1
            # Animal output can accumulate safely up to six units.  A threshold
            # of three amortizes the shed return while retaining ample headroom.
            if state.yield_units >= 3 or (day == 30 and state.yield_units > 0):
                expected_units = state.yield_units
                bundle.actions.append(
                    self._op(
                        "HARVEST",
                        product=species,
                        expected_units=expected_units,
                    )
                )
                self.harvested[species] += expected_units
                state.yield_units = 0
            bundles.append(bundle)
        return bundles

    def _end_day(self, day: int) -> None:
        for coord, state in list(self.crops.items()):
            was_watered = state.watered_today
            if was_watered:
                state.consecutive_unwatered = 0
            else:
                state.consecutive_unwatered += 1
            state.watered_today = False
            if state.consecutive_unwatered >= 2:
                self.crop_losses += 1
                del self.crops[coord]
                continue
            crop = CROPS[state.crop]
            if not crop["ongoing"]:
                continue
            next_age = day + 1 - state.planted_day
            first = int(crop["first_yield_day"])
            interval = int(crop["interval"])
            if next_age < first or (next_age - first) % interval:
                continue
            production_count = (next_age - first) // interval + 1
            if production_count > int(crop["max_yield"]):
                continue
            state.production_count = production_count
            bonus = 2 if was_watered and state.fertilized_until_day >= day else 1
            state.yield_units = min(int(crop["max_yield"]), state.yield_units + bonus)

        for coord, state in list(self.animals.items()):
            if state.fed_today:
                state.consecutive_unfed = 0
            else:
                state.consecutive_unfed += 1
            if state.consecutive_unfed >= 2:
                self.animal_losses += 1
                del self.animals[coord]
                continue
            animal = ANIMALS[state.species]
            next_age = day + 1 - state.placed_day
            first = int(animal["first_yield_day"])
            interval = int(animal["interval"])
            if next_age >= first and (next_age - first) % interval == 0:
                bonus = state.pending_care_bonus if state.fed_today else 0
                state.yield_units = min(
                    int(animal["max_held"]), state.yield_units + 1 + bonus
                )
                state.pending_care_bonus = 0
            if state.cared_today and state.fed_today:
                state.pending_care_bonus += 1
            state.fertilizer_available = True
            state.fed_today = False
            state.cared_today = False
        self.fertilizer_stock += self.fertilizer_collected_today

    @staticmethod
    def _worker_spawns(hands: int) -> list[Coord]:
        occupancy = Counter({SPAWN: 1})
        spawns = [SPAWN]
        for _ in range(hands):
            spawn = min(
                SHED_ACCESS,
                key=lambda coord: (occupancy[coord], SHED_ACCESS.index(coord)),
            )
            occupancy[spawn] += 1
            spawns.append(spawn)
        return spawns

    def _worker_capacities(self, hands: int) -> list[tuple[int, int, int, Coord]]:
        turns = int(self.config["turns_per_day"])
        first_turn_hires = int(self.config.get("max_hires_per_turn", 10))
        # Turn 1 is reserved for procurement.  Market orders execute after unit
        # actions, so even the farmer starts at T2 with supplies acknowledged.
        starts = self._worker_spawns(hands)
        capacities = [(0, turns - 1, 2, starts[0])]
        for hand in range(hands):
            available_from = 2 if hand < first_turn_hires else 3
            capacities.append(
                (
                    hand + 1,
                    turns - available_from + 1,
                    available_from,
                    starts[hand + 1],
                )
            )
        return capacities

    @staticmethod
    def _reconcile_deferred_hire_spawns(
        routes: list[WorkerRoute],
        worker_specs: list[tuple[int, int, int, Coord]],
    ) -> list[tuple[int, int, int, Coord]]:
        """Match T2 hire spawns after the already-active units have acted.

        The eleventh and twelfth hands are hired at the end of T2. Their spawn
        therefore depends on the T2 positions of the farmer and first ten
        hands, rather than on the all-units-at-start approximation.
        """
        if len(worker_specs) <= 11:
            return worker_specs
        route_by_worker = {route.worker: route for route in routes}
        spec_by_worker = {spec[0]: spec for spec in worker_specs}
        positions: list[Coord] = []
        for worker in range(11):
            spec = spec_by_worker[worker]
            route = route_by_worker[worker]
            position = spec[3]
            if route.available_from_turn <= 2 and route.actions:
                position = tuple(route.actions[0]["position"])
            positions.append(position)

        occupancy = Counter({coord: 0 for coord in SHED_ACCESS})
        for position in positions:
            if position in occupancy:
                occupancy[position] += 1
        corrected: dict[int, Coord] = {}
        for worker in range(11, len(worker_specs)):
            spawn = min(
                SHED_ACCESS,
                key=lambda coord: (occupancy[coord], SHED_ACCESS.index(coord)),
            )
            corrected[worker] = spawn
            occupancy[spawn] += 1
        return [
            (worker, capacity, start, corrected.get(worker, spawn))
            for worker, capacity, start, spawn in worker_specs
        ]

    @staticmethod
    def _move_actions(source: Coord, target: Coord) -> list[dict[str, Any]]:
        x, y = source
        tx, ty = target
        actions: list[dict[str, Any]] = []
        while x != tx:
            opcode = "EAST" if tx > x else "WEST"
            x += 1 if tx > x else -1
            actions.append({"opcode": opcode, "arguments": {}, "position": [x, y]})
        while y != ty:
            opcode = "SOUTH" if ty > y else "NORTH"
            y += 1 if ty > y else -1
            actions.append({"opcode": opcode, "arguments": {}, "position": [x, y]})
        return actions

    @staticmethod
    def _route_order_variants(bundles: list[Bundle]) -> list[list[Bundle]]:
        by_coord = {bundle.coord: bundle for bundle in bundles}
        variants: list[list[Bundle]] = []
        coordinate_orders = [
            sorted(by_coord, key=lambda p: (p[1], p[0] if p[1] % 2 == 0 else -p[0])),
            sorted(by_coord, key=lambda p: (-p[1], p[0] if p[1] % 2 == 0 else -p[0])),
            sorted(by_coord, key=lambda p: (p[0], p[1] if p[0] % 2 == 0 else -p[1])),
            sorted(by_coord, key=lambda p: (-p[0], p[1] if p[0] % 2 == 0 else -p[1])),
        ]
        for coords in coordinate_orders:
            variants.append([by_coord[coord] for coord in coords])
            variants.append(
                sorted(
                    (by_coord[coord] for coord in coords),
                    key=lambda bundle: (
                        bundle.role != "ANIMAL",
                        coords.index(bundle.coord),
                    ),
                )
            )
            variants.append(
                sorted(
                    (by_coord[coord] for coord in coords),
                    key=lambda bundle: (
                        bundle.role == "ANIMAL",
                        coords.index(bundle.coord),
                    ),
                )
            )
            variants.append(
                sorted(
                    (by_coord[coord] for coord in coords),
                    key=lambda bundle: (
                        not bundle.carries_output,
                        coords.index(bundle.coord),
                    ),
                )
            )
            variants.append(
                sorted(
                    (by_coord[coord] for coord in coords),
                    key=lambda bundle: (
                        bundle.carries_output,
                        coords.index(bundle.coord),
                    ),
                )
            )
        return variants

    @staticmethod
    def _segment_cost(
        day: int,
        segment: tuple[Bundle, ...],
        start_position: Coord,
    ) -> int:
        if not segment:
            return 0
        cost = _manhattan(start_position, segment[0].coord)
        cost += sum(len(bundle.actions) for bundle in segment)
        cost += sum(
            _manhattan(left.coord, right.coord) for left, right in pairwise(segment)
        )
        pickup_items = Counter()
        for bundle in segment:
            pickup_items.update(bundle.pickup_items)
        cost += len(pickup_items)
        if any(bundle.carries_output for bundle in segment):
            cost += min(_manhattan(segment[-1].coord, shed) for shed in SHED_ACCESS) + 1
        return cost

    def _partition_routes(
        self,
        day: int,
        ordered: list[Bundle],
        worker_specs: list[tuple[int, int, int, Coord]],
    ) -> list[tuple[int, int]] | None:
        count = len(ordered)

        @cache
        def solve(
            route_index: int, bundle_index: int
        ) -> tuple[tuple[int, int], ...] | None:
            if bundle_index == count:
                return ()
            if route_index == len(worker_specs):
                return None
            best = None
            for end in range(bundle_index + 1, count + 1):
                segment = tuple(ordered[bundle_index:end])
                _, capacity, _, start_position = worker_specs[route_index]
                if self._segment_cost(day, segment, start_position) > capacity:
                    break
                suffix = solve(route_index + 1, end)
                if suffix is None:
                    continue
                candidate = ((bundle_index, end), *suffix)
                candidate_cost = sum(
                    self._segment_cost(
                        day,
                        tuple(ordered[left:right]),
                        worker_specs[route_index + route_offset][3],
                    )
                    for route_offset, (left, right) in enumerate(candidate)
                )
                best_cost = (
                    sum(
                        self._segment_cost(
                            day,
                            tuple(ordered[left:right]),
                            worker_specs[route_index + route_offset][3],
                        )
                        for route_offset, (left, right) in enumerate(best)
                    )
                    if best is not None
                    else 10**9
                )
                if best is None or candidate_cost < best_cost:
                    best = candidate
            return best

        result = solve(0, 0)
        return list(result) if result is not None else None

    def _greedy_partition(
        self,
        day: int,
        ordered: list[Bundle],
        worker_specs: list[tuple[int, int, int, Coord]],
    ) -> list[list[Bundle]] | None:
        """Insert hard bundles first into the cheapest feasible worker tour."""
        segments: list[list[Bundle]] = [[] for _ in worker_specs]
        costs = [0 for _ in worker_specs]
        for bundle in ordered:
            best: tuple[int, int, int, int] | None = None
            for route_index, (_, capacity, _, start_position) in enumerate(
                worker_specs
            ):
                for insertion in range(len(segments[route_index]) + 1):
                    candidate = [*segments[route_index]]
                    candidate.insert(insertion, bundle)
                    cost = self._segment_cost(day, tuple(candidate), start_position)
                    if cost > capacity:
                        continue
                    choice = (cost - costs[route_index], cost, route_index, insertion)
                    if best is None or choice < best:
                        best = choice
            if best is None:
                return None
            _, cost, route_index, insertion = best
            segments[route_index].insert(insertion, bundle)
            costs[route_index] = cost
        return segments

    def _route_day7_unlock(
        self,
        day: int,
        bundles: list[Bundle],
        raw_capacities: list[tuple[int, int, int, Coord]],
    ) -> list[WorkerRoute]:
        """Schedule the D7 wool sale before any work in the locked NE land.

        The nominal market ledger cannot finance NE at T1. Two opening sheep
        can, however, be harvested and returned independently before noon. A
        same-batch WOOL sale then buys the quadrant, after which the five NE
        planting bundles may legally start.
        """
        reuse_unlock_workers = bool(self.config.get("d7_reuse_unlock_workers", False))
        if reuse_unlock_workers:
            if len(raw_capacities) < 9:
                raise RuntimeError(
                    "D7: wool-financed NE unlock requires at least nine active units"
                )
        elif len(raw_capacities) != int(self.config["workers_peak_units"]):
            raise RuntimeError(
                "D7: legacy wool-financed NE unlock requires all peak units"
            )
        financing = sorted(
            (
                bundle
                for bundle in bundles
                if bundle.role == "ANIMAL"
                and any(
                    action["opcode"] == "HARVEST"
                    and action["arguments"].get("product") == "SHEEP"
                    for action in bundle.actions
                )
            ),
            key=lambda bundle: bundle.coord,
        )
        northeast = sorted(
            (
                bundle
                for bundle in bundles
                if bundle.role == "CROP"
                and _quadrant(bundle.coord) == "Q1"
                and any(action["opcode"] == "PLANT" for action in bundle.actions)
            ),
            key=lambda bundle: bundle.coord,
        )
        if len(financing) != 2 or len(northeast) != 5:
            raise RuntimeError(
                "D7: expected two sheep finance bundles and five NE plant bundles"
            )

        finance_routes: list[WorkerRoute] = []
        for bundle, worker_spec in zip(financing, raw_capacities[:2], strict=True):
            finance_routes.extend(
                self._route(
                    day,
                    [bundle],
                    [worker_spec],
                    apply_unlock_dependency=False,
                )
            )
        unlock_ready_turn = max(
            route.available_from_turn + route.used for route in finance_routes
        )
        if unlock_ready_turn > int(self.config["turns_per_day"]):
            raise RuntimeError("D7: wool-financed NE unlock misses the day")

        # Five workers are reserved for the newly unlocked cells. Each route
        # starts one turn after the second WOOL DROP because market orders are
        # applied after unit actions in a turn.
        northeast_specs = []
        for worker, _, _, spawn in raw_capacities[2:7]:
            northeast_specs.append(
                (
                    worker,
                    int(self.config["turns_per_day"]) - unlock_ready_turn + 1,
                    unlock_ready_turn,
                    spawn,
                )
            )
        northeast_routes = self._route(
            day,
            northeast,
            northeast_specs,
            apply_unlock_dependency=False,
        )

        assigned = {bundle.coord for bundle in (*financing, *northeast)}
        remaining = [bundle for bundle in bundles if bundle.coord not in assigned]

        if not reuse_unlock_workers:
            # Preserve the frozen E18.18-E18.25 behavior. Those plans reserve
            # the first seven units for the unlock prefixes and route all
            # remaining work on the unused peak workers.
            remaining_specs = []
            for worker, _, available_from, spawn in raw_capacities[7:]:
                start = max(3, available_from)
                remaining_specs.append(
                    (
                        worker,
                        int(self.config["turns_per_day"]) - start + 1,
                        start,
                        spawn,
                    )
                )
            remaining_routes = self._route(
                day,
                remaining,
                remaining_specs,
                apply_unlock_dependency=False,
            )
            return [*finance_routes, *northeast_routes, *remaining_routes]

        # Reuse every unit after its unlock prefix instead of reserving thirteen
        # workers for three disjoint route groups. This is the key D7 capacity
        # pattern in the Jesse envelope: 2 finance + 5 NE starters, followed by
        # a common suffix scheduled in the remaining slots of nine units.
        prefixes = {
            route.worker: route for route in (*finance_routes, *northeast_routes)
        }
        turns = int(self.config["turns_per_day"])
        suffix_specs: list[tuple[int, int, int, Coord]] = []
        for worker, capacity, available_from, spawn in raw_capacities:
            prefix = prefixes.get(worker)
            if prefix is None:
                start = max(3, available_from)
                position = spawn
            else:
                start = prefix.available_from_turn + prefix.used
                position = prefix.position
            remaining_capacity = turns - start + 1
            if remaining_capacity > 0:
                suffix_specs.append((worker, remaining_capacity, start, position))
            if prefix is None:
                prefixes[worker] = WorkerRoute(
                    worker=worker,
                    capacity=capacity,
                    available_from_turn=available_from,
                    position=spawn,
                )

        suffix_routes = self._route(
            day,
            remaining,
            suffix_specs,
            apply_unlock_dependency=False,
        )
        for suffix in suffix_routes:
            prefix = prefixes[suffix.worker]
            prefix.actions.extend(suffix.actions)
            prefix.position = suffix.position
            prefix.carries_output = prefix.carries_output or suffix.carries_output
            prefix.expected_output.update(suffix.expected_output)
            if prefix.used > prefix.capacity:
                raise RuntimeError("D7: unlock prefix plus suffix exceeds capacity")
        return sorted(prefixes.values(), key=lambda route: route.worker)

    def _route(
        self,
        day: int,
        bundles: list[Bundle],
        raw_capacities: list[tuple[int, int, int, Coord]],
        *,
        apply_unlock_dependency: bool = True,
    ) -> list[WorkerRoute]:
        if (
            day == 7
            and apply_unlock_dependency
            and self.config.get("d7_wool_financed_unlock", True)
        ):
            return self._route_day7_unlock(day, bundles, raw_capacities)
        total_slots = sum(capacity for _, capacity, _, _ in raw_capacities)
        selected: (
            tuple[
                list[list[Bundle]],
                list[tuple[int, int, int, Coord]],
            ]
            | None
        ) = None
        selected_cost = 10**9
        worker_orders = [raw_capacities]
        for worker_specs in worker_orders:
            for ordered in self._route_order_variants(bundles):
                partition = self._partition_routes(day, ordered, worker_specs)
                if partition is not None:
                    cost = sum(
                        self._segment_cost(
                            day,
                            tuple(ordered[start:end]),
                            worker_specs[route_index][3],
                        )
                        for route_index, (start, end) in enumerate(partition)
                    )
                    if cost < selected_cost:
                        segments = [ordered[start:end] for start, end in partition]
                        segments.extend(
                            [] for _ in range(len(worker_specs) - len(segments))
                        )
                        selected = (
                            segments,
                            worker_specs,
                        )
                        selected_cost = cost
            hard_first_orders = [
                sorted(
                    bundles,
                    key=lambda bundle: (
                        self._segment_cost(day, (bundle,), worker_specs[0][3]),
                        len(bundle.actions),
                        bundle.carries_output,
                        bundle.coord,
                    ),
                    reverse=True,
                ),
                sorted(
                    bundles,
                    key=lambda bundle: (
                        bundle.carries_output,
                        min(_manhattan(bundle.coord, shed) for shed in SHED_ACCESS),
                        len(bundle.actions),
                        bundle.coord,
                    ),
                    reverse=True,
                ),
                sorted(
                    bundles,
                    key=lambda bundle: (
                        len(bundle.actions),
                        _manhattan(bundle.coord, SPAWN),
                        bundle.carries_output,
                        bundle.coord,
                    ),
                    reverse=True,
                ),
            ]
            shuffle_min_units = int(self.config.get("route_shuffle_min_units", 10))
            shuffle_days = {
                int(value)
                for value in self.config.get("route_shuffle_days", range(1, 31))
            }
            if (
                day in shuffle_days
                and len(worker_specs) >= shuffle_min_units
                and (selected is None or selected_cost > int(total_slots * 0.95))
            ):
                shuffle_base = hard_first_orders[0]
                for shuffle_index in range(32):
                    shuffled = [*shuffle_base]
                    random.Random(day * 10_000 + shuffle_index).shuffle(shuffled)
                    hard_first_orders.append(shuffled)
            for ordered in hard_first_orders:
                segments = self._greedy_partition(day, ordered, worker_specs)
                if segments is None:
                    continue
                cost = sum(
                    self._segment_cost(day, tuple(segment), worker_specs[index][3])
                    for index, segment in enumerate(segments)
                )
                if cost < selected_cost:
                    selected = (segments, worker_specs)
                    selected_cost = cost
        if selected is None:
            productive = sum(len(bundle.actions) for bundle in bundles)
            raise RuntimeError(
                f"D{day}: route infeasible; productive={productive}, slots={total_slots}"
            )

        segments, worker_specs = selected
        routes = [
            WorkerRoute(
                worker=worker,
                capacity=capacity,
                available_from_turn=start,
                position=spawn,
            )
            for worker, capacity, start, spawn in worker_specs
        ]
        for route, segment in zip(routes, segments, strict=True):
            pickup_items = Counter()
            for bundle in segment:
                pickup_items.update(bundle.pickup_items)
            for item, units in sorted(pickup_items.items()):
                route.actions.append(
                    {
                        "opcode": "PICKUP",
                        "arguments": {"item": item, "units": units},
                        "position": list(route.position),
                    }
                )
            for bundle in segment:
                route.actions.extend(self._move_actions(route.position, bundle.coord))
                route.position = bundle.coord
                for action in bundle.actions:
                    route.actions.append({**action, "position": list(bundle.coord)})
                    if action["opcode"] == "HARVEST":
                        item = action["arguments"].get(
                            "crop", action["arguments"].get("product")
                        )
                        if item is not None:
                            route.expected_output[str(item)] += int(
                                action["arguments"].get("expected_units", 1)
                            )
                    elif action["opcode"] == "COLLECT_FERTILIZER":
                        route.expected_output["FERTILIZER"] += 1
                route.carries_output = route.carries_output or bundle.carries_output

        for route in routes:
            if not route.carries_output:
                continue
            shed = min(
                SHED_ACCESS,
                key=lambda coord: (_manhattan(route.position, coord), coord),
            )
            route.actions.extend(self._move_actions(route.position, shed))
            route.position = shed
            route.actions.append(
                {
                    "opcode": "DROP",
                    "arguments": {
                        "item": "ALL",
                        "expected_items": dict(sorted(route.expected_output.items())),
                    },
                    "position": list(shed),
                }
            )
            if route.used > route.capacity:
                raise RuntimeError(f"D{day}: daily DROP exceeds worker capacity")
        return routes

    def _record_trajectory(self, day: int, routes: list[WorkerRoute]) -> None:
        turns = int(self.config["turns_per_day"])
        for route in routes:
            action_by_turn = {
                route.available_from_turn + offset: action
                for offset, action in enumerate(route.actions)
            }
            for turn in range(route.available_from_turn, turns + 1):
                action = action_by_turn.get(
                    turn,
                    {
                        "opcode": "PASS",
                        "arguments": {},
                        "position": list(route.position),
                    },
                )
                self.trajectory.append(
                    {
                        "step": (day - 1) * turns + turn - 1,
                        "day": day,
                        "turn": turn,
                        "worker": route.worker,
                        **action,
                    }
                )

    def build(self) -> dict[str, Any]:
        snapshots: dict[str, Any] = {}
        reserve = float(self.config["reserve_ratio"])
        for day in range(1, 31):
            fertilizer_stock_start = self.fertilizer_stock
            fertilizer_used_start = self.fertilizer_used
            self.fertilizer_used_today_by_crop = Counter()
            crop_bundles = self._crop_bundles(day)
            animal_bundles = self._animal_bundles(day)
            bundles = [*crop_bundles, *animal_bundles]
            reference_slots = int(self.config["daily_available_action_slots"][day - 1])
            force_peak = (
                int(self.config["force_peak_hands_from_day"])
                <= day
                <= int(self.config["force_peak_hands_through_day"])
            )
            minimum_hands_by_day = self.config.get("minimum_hands_by_day", {}) or {}
            minimum_hands = int(minimum_hands_by_day.get(str(day), 0))
            peak_hands = int(self.config["workers_peak_hands"])
            if not 0 <= minimum_hands <= peak_hands:
                raise ValueError(
                    f"D{day}: minimum_hands_by_day must be between 0 and {peak_hands}"
                )
            first_hands = max(peak_hands if force_peak else 0, minimum_hands)
            routes = []
            route_error = None
            selected_hands = -1
            slots = -1
            for hands in range(first_hands, peak_hands + 1):
                capacities = self._worker_capacities(hands)
                candidate_slots = sum(value[1] for value in capacities)
                try:
                    for spawn_attempt in range(8):
                        candidate_routes = self._route(day, bundles, capacities)
                        corrected = self._reconcile_deferred_hire_spawns(
                            candidate_routes, capacities
                        )
                        if corrected == capacities:
                            break
                        if spawn_attempt == 7 and self.config.get(
                            "allow_deferred_spawn_recovery", False
                        ):
                            corrected_by_worker = {
                                worker: spawn for worker, _, _, spawn in corrected
                            }
                            recovery_fits = all(
                                route.used
                                + _manhattan(
                                    next(
                                        spawn
                                        for worker, _, _, spawn in capacities
                                        if worker == route.worker
                                    ),
                                    corrected_by_worker[route.worker],
                                )
                                <= route.capacity
                                for route in candidate_routes
                                if route.worker >= 11
                            )
                            if recovery_fits:
                                # The live retrying executor already corrects a
                                # deferred hire's observed spawn before the
                                # first task. Accept the route only when its
                                # private slack pays the worst observed spawn
                                # displacement without dropping a task.
                                break
                        capacities = corrected
                    else:
                        raise RuntimeError(
                            f"D{day}: deferred HIRE spawn routing did not converge"
                        )
                except RuntimeError as exc:
                    route_error = str(exc)
                    continue
                candidate_used = sum(route.used for route in candidate_routes)
                if (candidate_slots - candidate_used) / candidate_slots < reserve:
                    route_error = (
                        f"D{day}: real hire schedule leaves less than reserve with "
                        f"{hands} hands"
                    )
                    continue
                routes = candidate_routes
                selected_hands = hands
                slots = candidate_slots
                route_error = None
                break
            used = sum(route.used for route in routes)
            slack = slots - used if routes else -1
            slack_ratio = slack / slots if routes else -1.0
            action_counts = Counter(
                action["opcode"] for route in routes for action in route.actions
            )
            self.daily.append(
                {
                    "day": day,
                    "available_action_slots": slots,
                    "reference_requested_action_slots": reference_slots,
                    "planned_action_slots": used,
                    "slack_action_slots": slack,
                    "slack_ratio": round(slack_ratio, 6),
                    "reserve_target_met": slack_ratio >= reserve,
                    "route_error": route_error,
                    "active_units": len(routes),
                    "planned_hands": selected_hands,
                    "action_counts": dict(sorted(action_counts.items())),
                    "crop_mix_end_of_actions": self._crop_mix(),
                    "animal_mix_end_of_actions": self._animal_mix(),
                    "fertilizer_stock_start": fertilizer_stock_start,
                    "fertilizer_used": self.fertilizer_used - fertilizer_used_start,
                    "fertilizer_used_by_crop": dict(
                        sorted(self.fertilizer_used_today_by_crop.items())
                    ),
                }
            )
            if routes:
                self._record_trajectory(day, routes)
            self._end_day(day)
            if day in CHECKPOINT_DAYS:
                snapshots[f"D{day:02d}"] = {
                    "crops": self._crop_mix(),
                    "animals": self._animal_mix(),
                    "crop_total": len(self.crops),
                    "animal_total": len(self.animals),
                }

        action_stream = [
            [
                row["step"],
                row["worker"],
                row["opcode"],
                row["arguments"],
                row["position"],
            ]
            for row in self.trajectory
        ]
        plan_hash = hashlib.sha256(
            json.dumps(action_stream, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        target_crop = self.config["crop_checkpoints"]
        target_animals = self.config["animal_checkpoints"]
        checkpoint_checks = {
            key: {
                "crop_match": snapshots[key]["crops"] == target_crop[key],
                "animal_match": snapshots[key]["animals"] == target_animals[key],
            }
            for key in snapshots
        }
        route_errors = [row["route_error"] for row in self.daily if row["route_error"]]
        crop_totals = [
            sum(row["crop_mix_end_of_actions"].values()) for row in self.daily
        ]
        peak_crop_total = max(crop_totals)
        peak_crop_first_day = crop_totals.index(peak_crop_total) + 1
        shadow_crop_output = sum(
            int(self.harvested.get(crop, 0))
            for crop in ("MELON", "STRAWBERRY", "WHEAT", "CARROT")
        )
        gate_0a_checks = {
            "exact_770_layout": len(self.pasture_targets) == 14
            and len(self.final_crop_targets) == 61,
            "exact_9_cow_5_sheep": self._animal_mix() == {"COW": 9, "SHEEP": 5},
            "all_composition_checkpoints": all(
                check["crop_match"] and check["animal_match"]
                for check in checkpoint_checks.values()
            ),
            "zero_shadow_crop_starvation": self.crop_losses == 0,
            "zero_shadow_animal_escape": self.animal_losses == 0,
            "zero_shadow_illegal_actions": not self.illegal_actions,
            "all_daily_routes_feasible": not route_errors,
            "real_hire_timing_and_peak_12_hands": max(
                row["planned_hands"] for row in self.daily
            )
            == int(self.config["workers_peak_hands"]),
            "daily_reserve_target_met": all(
                row["reserve_target_met"] for row in self.daily
            ),
            "terminal_residual_crops_at_most_2": len(self.crops)
            <= int(self.config["terminal_residual_crop_cap"]),
            "peak_62_crops_by_d13": peak_crop_total == 62 and peak_crop_first_day <= 13,
            "shadow_crop_output_at_least_jesse_reference_885": shadow_crop_output
            >= 885,
            "trajectory_within_720_steps": all(
                0 <= row["step"] < 720 for row in self.trajectory
            ),
        }
        return {
            "schema_version": "e18.codex.770_capacity_trajectory_gate_0a.v1",
            "candidate_id": self.config["candidate_id"],
            "epistemic_role": "DEVELOPMENT_GATE_0A_ONLY",
            "gate_0a_passed": all(gate_0a_checks.values()),
            "gate_0a_checks": gate_0a_checks,
            "gate_0b_passed": False,
            "executor_authorized": False,
            "blocking_work": [
                "exact Kaggriculture engine replay with land, hire and shop state",
                "cash, seed, Wheat feed and shed-capacity ledger",
                "nominal market execution and terminal SELL acknowledgement",
            ],
            "layout": {
                "pasture_targets": [
                    list(coord) for coord in sorted(self.pasture_targets)
                ],
                "late_q0_pasture": list(self.late_pasture),
                "final_crop_targets": [
                    list(coord) for coord in sorted(self.final_crop_targets)
                ],
                "crop_capacity_by_quadrant": {"Q0": 18, "Q1": 18, "Q2": 25},
            },
            "calendar": {
                "annual_replant_last_day": self.config["annual_replant_last_day"],
                "terminal_crop_clear_day": self.config["terminal_crop_clear_day"],
                "crop_plant_day": {
                    f"{coord[0]},{coord[1]}": day
                    for coord, day in sorted(self.crop_plant_day.items())
                },
                "strawberry_retire_day": {
                    f"{coord[0]},{coord[1]}": day
                    for coord, day in sorted(self.strawberry_retire_day.items())
                },
            },
            "snapshots": snapshots,
            "checkpoint_checks": checkpoint_checks,
            "daily": self.daily,
            "totals": {
                "action_counts": dict(
                    sorted(Counter(row["opcode"] for row in self.trajectory).items())
                ),
                "harvested": dict(sorted(self.harvested.items())),
                "seed_use": dict(sorted(self.seed_use.items())),
                "fertilizer_used": self.fertilizer_used,
                "fertilizer_used_by_crop": dict(
                    sorted(self.fertilizer_used_by_crop.items())
                ),
                "fertilizer_stock_terminal": self.fertilizer_stock,
                "crop_losses": self.crop_losses,
                "animal_losses": self.animal_losses,
                "illegal_actions": self.illegal_actions,
                "route_errors": route_errors,
                "minimum_daily_slack_ratio": min(
                    row["slack_ratio"] for row in self.daily
                ),
                "reserve_target_ratio": reserve,
                "peak_crop_total": peak_crop_total,
                "peak_crop_first_day": peak_crop_first_day,
                "shadow_crop_output": shadow_crop_output,
                "peak_planned_hands": max(row["planned_hands"] for row in self.daily),
            },
            "plan_sha256": plan_hash,
            "trajectory": self.trajectory,
        }


def build_plan(config_path: Path | str | None = None) -> dict[str, Any]:
    return CapacityTrajectoryPlanner(load_config(config_path)).build()


__all__ = [
    "DEFAULT_CONFIG",
    "CapacityTrajectoryPlanner",
    "build_plan",
    "load_config",
]
