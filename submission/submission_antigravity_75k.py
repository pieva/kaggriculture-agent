"""
Standalone Antigravity C2 75K Dual-Quadrant (Q0+Q1) routine file for Kaggle Kaggriculture.
Generated from the Foundation-f391ee2-bound Antigravity controller and adapter.
"""

from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from collections.abc import Callable
from copy import deepcopy
from dataclasses import asdict, dataclass, field
import json
import math
from pathlib import Path
import statistics
from typing import Any, Dict


# ==========================================
# --- Embedded Antigravity C2 75K Config ---
# ==========================================
ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG: dict[str, Any] = {
  "candidate_id": "ANTIGRAVITY_C2_75K_DUAL_Q",
  "schema_version": "model_spec_c2.antigravity.dual_q.v1",
  "model_spec_version": "ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0",
  "foundation_checkpoint": "f391ee2",
  "quadrants_owned": 2,
  "workforce_total": 13,
  "q0_workforce_total": 7,
  "crop_working_set_target": 36,
  "crop_counts": {
    "MELON": 18,
    "STRAWBERRY": 16,
    "WHEAT": 2
  },
  "pasture_allocation_target": 12,
  "livestock_targets": {
    "COW": 6,
    "SHEEP": 6
  },
  "bootstrap_livestock": {
    "COW": 2,
    "SHEEP": 2
  },
  "q1_livestock_targets": {
    "COW": 3,
    "SHEEP": 3
  },
  "livestock_activation_days": {
    "COW": 7,
    "SHEEP": 8
  },
  "q1_activation_min_day": 6,
  "q1_activation_max_day": 8,
  "q1_activation_cash": 2800,
  "q1_operating_cash_floor": 250,
  "operating_cash_floor": 50,
  "feed_reserve_rounds": 2,
  "observed_capacity_days": 3,
  "hard_schedule_days": 2,
  "minimum_post_plant_action_phases": 1,
  "payback_cutoff_days": 2,
  "crop_horizon_margin_days": 1,
  "endgame_shutdown_days": 2,
  "max_noop_before_invalidation": 3,
  "turns_per_day": 24
}

# ==========================================
# --- E16 Base Policy Definitions ---
# ==========================================
"""Single shared policy implementation for every frozen E16 cell.

This module intentionally depends only on the standard library so the exact file
can be frozen as the treatment build. Cell differences enter only through the
four manipulated values validated by :mod:`agricola.e16.config`.
"""



MANIPULATED_FIELDS = {
    "watering_dispatch_priority",
    "crop_working_set_target",
    "livestock_headcount_target",
    "pasture_allocation_target",
}
WATER_DISPATCH_RANKS = {
    0.20: 6,
    0.45: 3,
    0.70: 0,
}
CROP_MIX = ("WHEAT", "STRAWBERRY", "MELON")
SEED_COSTS = {"WHEAT": 10, "STRAWBERRY": 100, "MELON": 80}
SHED_TILES = ((4, 4), (5, 4), (4, 5), (5, 5))
CROP_POSITIONS = tuple((x, y) for y in range(3) for x in range(10))
PASTURE_POSITIONS = tuple(
    (x, y) for y in (3, 4) for x in range(10) if (x, y) not in {(4, 4), (5, 4)}
)
PRODUCTS = {
    "WHEAT",
    "CARROT",
    "TOMATO",
    "STRAWBERRY",
    "MELON",
    "MILK",
    "WOOL",
    "EGG",
    "FERTILIZER",
}


def _fib(index: int) -> int:
    a, b = 1, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def _distance(left: tuple[int, int], right: tuple[int, int]) -> int:
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def _move_towards(position: tuple[int, int], target: tuple[int, int]) -> list[str]:
    x, y = position
    tx, ty = target
    if x < tx:
        return ["EAST"]
    if x > tx:
        return ["WEST"]
    if y < ty:
        return ["SOUTH"]
    if y > ty:
        return ["NORTH"]
    return ["PASS"]


def _quota_counts(target: int) -> dict[str, int]:
    raw = {"WHEAT": target * 0.4, "STRAWBERRY": target * 0.4, "MELON": target * 0.2}
    counts = {crop: math.floor(value) for crop, value in raw.items()}
    remaining = target - sum(counts.values())
    order = sorted(
        CROP_MIX, key=lambda crop: (-(raw[crop] - counts[crop]), CROP_MIX.index(crop))
    )
    for crop in order[:remaining]:
        counts[crop] += 1
    return counts


def _crop_plan(target: int) -> dict[tuple[int, int], str]:
    quotas = _quota_counts(target)
    cycle: list[str] = []
    while len(cycle) < target:
        for crop in CROP_MIX:
            if quotas[crop] > 0:
                cycle.append(crop)
                quotas[crop] -= 1
    return {position: crop for position, crop in zip(CROP_POSITIONS[:target], cycle)}


def _inventory_total(inventory: dict[str, int]) -> int:
    return sum(int(value) for value in inventory.values())


def _water_dispatch_rank(priority: float) -> int:
    for level, rank in WATER_DISPATCH_RANKS.items():
        if math.isclose(priority, level, rel_tol=0.0, abs_tol=1e-12):
            return rank
    raise ValueError(f"unsupported watering dispatch priority: {priority}")


class E16TrainingAgent:
    """Deterministic treatment policy with a verified T0 treatment boundary."""

    def __init__(self, cell_config: dict[str, Any]):
        required = MANIPULATED_FIELDS | {
            "quadrants_owned",
            "workforce_headcount",
            "livestock_species",
            "operating_cash_floor",
            "endgame_shutdown_steps",
        }
        missing = required - set(cell_config)
        if missing:
            raise ValueError(f"missing E16 cell fields: {sorted(missing)}")
        if int(cell_config["quadrants_owned"]) != 2:
            raise ValueError("E16 hard cap requires quadrants_owned=2")
        if cell_config["livestock_species"] != "COW":
            raise ValueError("E16 livestock species must be COW")
        _water_dispatch_rank(float(cell_config["watering_dispatch_priority"]))

        self.config = deepcopy(cell_config)
        self.t0_step: int | None = None
        self.current_day: int | None = None
        self.watering_needs: set[tuple[int, int, int]] = set()
        self.watering_successes: set[tuple[int, int, int]] = set()
        self.last_observed_quadrants = 1

    @staticmethod
    def _farm(observation: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        player = int(observation.get("player", 0))
        farms = observation.get("farms", [])
        farm = farms[player] if player < len(farms) else {}
        private = observation.get("private", {}) or {}
        return farm, private

    @staticmethod
    def _owned_quadrants(farm: dict[str, Any]) -> int:
        raw = farm.get("unlocked_quadrants", ["NW"])
        if isinstance(raw, list):
            return len(raw)
        return int(raw)

    @staticmethod
    def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
        x, y = position
        tiles = farm.get("tiles", [])
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return "LOCKED"

    @staticmethod
    def _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:
        positions = [tuple(farm.get("farmer", [4, 4]))]
        positions.extend(tuple(position) for position in farm.get("hands", []))
        return positions

    def _active_values(self, quadrants: int) -> tuple[int, int, int, float]:
        if quadrants < 2 or self.t0_step is None:
            return 10, 0, 0, 0.45
        return (
            int(self.config["crop_working_set_target"]),
            int(self.config["pasture_allocation_target"]),
            int(self.config["livestock_headcount_target"]),
            float(self.config["watering_dispatch_priority"]),
        )

    def _sync_t0_and_water(
        self, observation: dict[str, Any], farm: dict[str, Any], quadrants: int
    ) -> None:
        step = int(observation.get("step", 0))
        day = int(observation.get("day", 0))
        if self.t0_step is None and self.last_observed_quadrants < 2 <= quadrants:
            self.t0_step = step
        self.last_observed_quadrants = quadrants

        if self.current_day != day:
            self.current_day = day
            self.watering_needs.clear()
            self.watering_successes.clear()
        for position in CROP_POSITIONS:
            tile = self._tile(farm, position)
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                key = (day, position[0], position[1])
                self.watering_needs.add(key)
                if tile.get("watered_today", False):
                    self.watering_successes.add(key)

    def _target_action(
        self,
        position: tuple[int, int],
        targets: list[tuple[tuple[int, int], list[str]]],
        reserved: set[tuple[int, int]],
    ) -> list[str] | None:
        available = [
            (target, action) for target, action in targets if target not in reserved
        ]
        if not available:
            return None
        target, action = min(
            available,
            key=lambda pair: (_distance(position, pair[0]), pair[0][1], pair[0][0]),
        )
        reserved.add(target)
        return action if target == position else _move_towards(position, target)

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
        positions = self._positions(farm)
        inventories = list(private.get("inventories", []))
        while len(inventories) < len(positions):
            inventories.append({})
        shed = private.get("shed", {}) or {}
        crop_plan = _crop_plan(crop_target)
        pasture_positions = PASTURE_POSITIONS[:pasture_target]
        reserved: set[tuple[int, int]] = set()
        reserved_cow_pickups = 0
        reserved_wheat_pickups = 0

        water_targets: list[tuple[tuple[int, int], list[str]]] = []
        crop_harvest: list[tuple[tuple[int, int], list[str]]] = []
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
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                if not tile.get("watered_today", False):
                    water_targets.append((target, ["WATER"]))
                if int(tile.get("yield_units", 0)) > 0:
                    crop_harvest.append((target, ["HARVEST"]))
            elif tile is None and not shutdown and available_seeds[crop] > 0:
                crop_plant.append((target, ["PLANT", crop]))
                available_seeds[crop] -= 1

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

        water_unmet = bool(water_targets)
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
                item != "WHEAT" and item != "COW" and amount > 0
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
                available_cows = max(0, int(shed.get("COW", 0)) - reserved_cow_pickups)
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

            priority_groups = [
                fertilizer_targets,
                animal_harvest,
                care_targets,
                pasture_build,
                crop_harvest,
                crop_plant,
            ]
            if water_unmet:
                priority_groups.insert(
                    _water_dispatch_rank(watering_priority), water_targets
                )
            action = None
            for group in priority_groups:
                action = self._target_action(position, group, reserved)
                if action is not None:
                    break
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

        # This is the sole land order. Once two quadrants are observed, no code
        # path can emit another BUY_LAND.
        if quadrants < 2:
            add(["BUY_LAND"], 1000.0)

        shed = private.get("shed", {}) or {}
        inventories = private.get("inventories", []) or []
        active_by_crop = {crop: 0 for crop in CROP_MIX}
        for position in CROP_POSITIONS[:crop_target]:
            tile = self._tile(farm, position)
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") in active_by_crop
            ):
                active_by_crop[tile["crop"]] += 1
        quotas = _quota_counts(crop_target)
        if not shutdown:
            for crop in CROP_MIX:
                deficit = max(
                    0,
                    quotas[crop]
                    - active_by_crop[crop]
                    - int(private.get("seeds", {}).get(crop, 0)),
                )
                if deficit:
                    add(["BUY_SEED", crop, deficit], deficit * SEED_COSTS[crop])

        hands = len(farm.get("hands", []))
        target_hands = int(self.config["workforce_headcount"])
        hires_today = int(farm.get("hires_today", 0))
        for offset in range(max(0, target_hands - hands)):
            if not add(["HIRE"], float(_fib(hires_today + offset))):
                break

        if quadrants >= 2 and self.t0_step is not None:
            pasture_count = sum(
                1
                for position in PASTURE_POSITIONS[:pasture_target]
                if isinstance(self._tile(farm, position), dict)
                and self._tile(farm, position).get("kind") == "PASTURE"
            )
            cows_on_tiles = sum(
                1
                for position in PASTURE_POSITIONS[:pasture_target]
                if isinstance(self._tile(farm, position), dict)
                and self._tile(farm, position).get("animal") == "COW"
            )
            cows_in_transit = int(shed.get("COW", 0)) + sum(
                int(inv.get("COW", 0)) for inv in inventories if isinstance(inv, dict)
            )
            cow_deficit = max(
                0, min(herd_target, pasture_count) - cows_on_tiles - cows_in_transit
            )
            if cow_deficit and not shutdown:
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

        # Sales are common and last in the queue. Wheat needed for feed is held.
        reserve = herd_target * 3 + (2 if herd_target else 0)
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
        farm, private = self._farm(observation)
        quadrants = self._owned_quadrants(farm)
        if quadrants > 2:
            raise RuntimeError(
                "E16 hard cap violated: observed more than two quadrants"
            )
        self._sync_t0_and_water(observation, farm, quadrants)
        crop_target, pasture_target, herd_target, watering_priority = (
            self._active_values(quadrants)
        )
        if isinstance(configuration, dict):
            episode_steps = int(configuration.get("episodeSteps", 720))
        else:
            episode_steps = int(getattr(configuration, "episodeSteps", 720))
        shutdown = episode_steps - int(observation.get("step", 0)) <= int(
            self.config["endgame_shutdown_steps"]
        )
        actions = self._unit_actions(
            observation,
            farm,
            private,
            crop_target,
            pasture_target,
            herd_target,
            watering_priority,
            shutdown,
        )
        market_orders = self._market_orders(
            farm,
            private,
            observation.get("market", {}) or {},
            quadrants,
            crop_target,
            pasture_target,
            herd_target,
            shutdown,
        )
        return {
            "farmer": actions[0] if actions else ["PASS"],
            "hands": actions[1:],
            "market": market_orders,
        }

# ==========================================
# --- Decision Lifecycle Runtime ---
# ==========================================
FOUNDATION_CHECKPOINT = "f391ee2"
FOUNDATION_VERSION = "C2"
ENGINE_FINGERPRINT = (
    "4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d"
)

DECISION_OPEN = "DECISION_OPEN"
DEFINED = "DEFINED"
PLAN_FEASIBLE = "PLAN_FEASIBLE"
INFEASIBLE = "INFEASIBLE"
REJECTED = "REJECTED"
COMMITTED_EXECUTING = "COMMITTED_EXECUTING"
REPAIR_WITHIN_COMMITMENT = "REPAIR_WITHIN_COMMITMENT"
INVALIDATED = "INVALIDATED"
CANCELLED = "CANCELLED"
SUPERSEDED = "SUPERSEDED"
COMPLETED = "COMPLETED"
REVIEW_READY = "REVIEW_READY"
TERMINAL_CLOSED = "TERMINAL_CLOSED"

ONLINE_STATES = {
    DECISION_OPEN,
    DEFINED,
    PLAN_FEASIBLE,
    INFEASIBLE,
    REJECTED,
    COMMITTED_EXECUTING,
    REPAIR_WITHIN_COMMITMENT,
    INVALIDATED,
    CANCELLED,
    SUPERSEDED,
    COMPLETED,
    REVIEW_READY,
}


def _configuration_value(configuration: Any, name: str, default: Any) -> Any:
    if isinstance(configuration, dict):
        return configuration.get(name, default)
    return getattr(configuration, name, default)


def stable_payload_hash(payload: Any) -> str:
    """Return a deterministic SHA-256 over a JSON-compatible payload."""

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class CodexClock:
    step: int
    day: int
    hour: int
    turns_per_day: int
    episode_steps: int

    @property
    def is_eod(self) -> bool:
        return self.hour == self.turns_per_day - 1

    @property
    def is_terminal_action(self) -> bool:
        # Kaggle's runner exposes the terminal state without another agent call:
        # with N environment states, the last callable observation is N - 2.
        return self.step + 2 >= self.episode_steps

    @property
    def remaining_steps(self) -> int:
        return max(0, self.episode_steps - 1 - self.step)


@dataclass(frozen=True)
class CodexSnapshot:
    clock: CodexClock
    player: int
    farm: dict[str, Any]
    private: dict[str, Any]
    market: dict[str, Any]
    evidence_snapshot_id: str
    state_id: str
    configuration_snapshot: dict[str, Any]
    configuration_hash: str
    snapshot_fingerprint: str


class CodexObservationAdapter:
    """Validate and normalize the real Kaggriculture callable observation."""

    @staticmethod
    def parse(
        observation: dict[str, Any],
        configuration: Any,
        *,
        fallback_turns_per_day: int,
        fallback_episode_steps: int,
    ) -> CodexSnapshot:
        if not isinstance(observation, dict):
            raise TypeError("observation must be a mapping")

        try:
            step = int(observation["step"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("observation.step is required and must be integral") from exc

        turns_per_day = int(
            _configuration_value(
                configuration, "turnsPerDay", fallback_turns_per_day
            )
        )
        episode_steps = int(
            _configuration_value(
                configuration, "episodeSteps", fallback_episode_steps
            )
        )
        if turns_per_day <= 0 or episode_steps <= 0:
            raise ValueError("turnsPerDay and episodeSteps must be positive")

        day = int(observation.get("day", step // turns_per_day))
        hour = int(observation.get("hour", step % turns_per_day))
        if step != day * turns_per_day + hour:
            raise ValueError("clock violates step == day * turnsPerDay + hour")
        if not 0 <= hour < turns_per_day:
            raise ValueError("observation.hour is outside the configured day")

        try:
            player = int(observation.get("player", 0))
        except (TypeError, ValueError) as exc:
            raise ValueError("observation.player must be integral") from exc
        farms = observation.get("farms")
        if not isinstance(farms, (list, tuple)) or not 0 <= player < len(farms):
            raise ValueError("observation.farms does not contain the bound player")
        farm = farms[player]
        private = observation.get("private", {}) or {}
        market = observation.get("market", {}) or {}
        if not isinstance(farm, dict) or not isinstance(private, dict):
            raise TypeError("farm and private payloads must be mappings")
        if not isinstance(market, dict):
            market = {}

        configuration_snapshot = {
            "turnsPerDay": turns_per_day,
            "episodeSteps": episode_steps,
            "boardSize": int(
                _configuration_value(configuration, "boardSize", 10)
            ),
            "shedCapacity": int(
                _configuration_value(configuration, "shedCapacity", 100)
            ),
            "maxMarketOrdersPerTurn": int(
                _configuration_value(configuration, "maxMarketOrdersPerTurn", 10)
            ),
        }
        configuration_hash = stable_payload_hash(configuration_snapshot)
        snapshot_payload = {
            "step": step,
            "day": day,
            "hour": hour,
            "player": player,
            "farm": farm,
            "private": private,
            "market": market,
            "configuration_hash": configuration_hash,
        }
        snapshot_fingerprint = stable_payload_hash(snapshot_payload)
        state_id = f"state-{step:06d}"
        return CodexSnapshot(
            clock=CodexClock(
                step=step,
                day=day,
                hour=hour,
                turns_per_day=turns_per_day,
                episode_steps=episode_steps,
            ),
            player=player,
            farm=farm,
            private=private,
            market=market,
            evidence_snapshot_id=f"evidence-{step:06d}-{snapshot_fingerprint[:12]}",
            state_id=state_id,
            configuration_snapshot=configuration_snapshot,
            configuration_hash=configuration_hash,
            snapshot_fingerprint=snapshot_fingerprint,
        )


class CodexDecisionLifecycle:
    """Append-only, deterministic realization of the frozen C2 DLC."""

    def __init__(
        self,
        *,
        run_id: str,
        episode_id: str,
        agent_id: str,
        model_spec_version: str,
    ) -> None:
        if not run_id or not episode_id:
            raise ValueError("run_id and episode_id are mandatory and distinct from seed")
        self.run_id = str(run_id)
        self.episode_id = str(episode_id)
        self.agent_id = agent_id
        self.model_spec_version = model_spec_version
        self.state = DECISION_OPEN
        self.event_sequence = 0
        self.decision_sequence = 0
        self.plan_sequence = 0
        self.commitment_sequence = 0
        self.repair_sequence = 0
        self.review_sequence = 0
        self.request_sequence = 0
        self.verify_sequence = 0
        self.terminal_sequence = 0
        self.active_commitment: dict[str, Any] | None = None
        self.pending_supersession_intent_id: str | None = None
        self.events: list[dict[str, Any]] = []
        self.feasibility_records: list[dict[str, Any]] = []
        self.repair_records: list[dict[str, Any]] = []
        self.review_records: list[dict[str, Any]] = []
        self.request_records: list[dict[str, Any]] = []
        self.outcome_records: list[dict[str, Any]] = []
        self.verify_records: list[dict[str, Any]] = []
        self.terminal_record: dict[str, Any] | None = None
        self.counts = {
            "commitment_count": 0,
            "completion_count": 0,
            "invalidation_count": 0,
            "repair_count": 0,
            "cancellation_count": 0,
            "supersession_count": 0,
            "infeasible_count": 0,
            "rejected_count": 0,
        }

    @property
    def scope_key(self) -> str:
        return f"{self.run_id}/{self.episode_id}"

    def _next_id(self, kind: str) -> str:
        self.event_sequence += 1
        return f"{self.scope_key}/{kind}-{self.event_sequence:06d}"

    def _transition(
        self,
        target: str,
        *,
        snapshot: CodexSnapshot,
        reason_code: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        source = self.state
        lifecycle_event_id = self._next_id("lifecycle")
        self.state = target
        self.events.append(
            {
                "run_id": self.run_id,
                "episode_id": self.episode_id,
                "lifecycle_event_id": lifecycle_event_id,
                "from_state": source,
                "to_state": target,
                "transition_id": snapshot.clock.step,
                "decision_boundary_id": f"boundary-{snapshot.clock.step:06d}",
                "evidence_snapshot_id": snapshot.evidence_snapshot_id,
                "reason_code": reason_code,
                "payload": deepcopy(payload or {}),
                "foundation_checkpoint": FOUNDATION_CHECKPOINT,
            }
        )

    def begin_commitment(
        self,
        snapshot: CodexSnapshot,
        *,
        intent_type: str,
        plan_payload: dict[str, Any],
        feasibility_records: list[dict[str, Any]],
        reservations: list[dict[str, Any]],
        invariants: list[str],
        invalidators: list[str],
        completion_condition: str,
        completion_invalidation_precedence_policy: str,
    ) -> bool:
        if self.state != DECISION_OPEN:
            raise RuntimeError("a new decision can only begin in DECISION_OPEN")

        self.decision_sequence += 1
        self.plan_sequence += 1
        decision_id = f"{self.scope_key}/decision-{self.decision_sequence:04d}"
        plan_id = f"{self.scope_key}/plan-{self.plan_sequence:04d}"
        decision_payload = {
            "decision_id": decision_id,
            "decision_version": 1,
            "owner_agent": self.agent_id,
            "intent_type": intent_type,
            "intent_payload": deepcopy(plan_payload.get("intent", {})),
            "created_at_transition_id": snapshot.clock.step,
            "evidence_snapshot_id": snapshot.evidence_snapshot_id,
        }
        if self.pending_supersession_intent_id is not None:
            decision_payload["supersession_intent_id"] = (
                self.pending_supersession_intent_id
            )
            decision_payload["successor_decision_id"] = decision_id
            self.pending_supersession_intent_id = None
        self._transition(
            DEFINED,
            snapshot=snapshot,
            reason_code="DEFINE_INTENT",
            payload=decision_payload,
        )

        normalized_checks: list[dict[str, Any]] = []
        failed_checks: list[dict[str, Any]] = []
        for index, record in enumerate(feasibility_records, start=1):
            normalized = {
                "feasibility_check_id": f"{plan_id}/check-{index:02d}",
                "decision_id": decision_id,
                "plan_id": plan_id,
                "snapshot_id": snapshot.evidence_snapshot_id,
                "feasibility_captured_at_transition_id": snapshot.clock.step,
                "revalidated_before_commit": True,
                **deepcopy(record),
            }
            normalized_checks.append(normalized)
            if normalized.get("check_result") == "FAIL":
                failed_checks.append(normalized)
        self.feasibility_records.extend(normalized_checks)

        if failed_checks:
            self.counts["infeasible_count"] += 1
            self._transition(
                INFEASIBLE,
                snapshot=snapshot,
                reason_code=str(
                    failed_checks[0].get(
                        "reason_code", "FEASIBILITY_CAPACITY_EXCEEDED"
                    )
                ),
                payload={
                    "decision_id": decision_id,
                    "plan_id": plan_id,
                    "failed_check_ids": [
                        check["feasibility_check_id"] for check in failed_checks
                    ],
                },
            )
            self._transition(
                DECISION_OPEN,
                snapshot=snapshot,
                reason_code="INFEASIBLE_REOPEN",
            )
            return False

        plan_fingerprint = stable_payload_hash(plan_payload)
        self._transition(
            PLAN_FEASIBLE,
            snapshot=snapshot,
            reason_code="FEASIBILITY_PASS",
            payload={
                "decision_id": decision_id,
                "plan_id": plan_id,
                "plan_version": 1,
                "plan_fingerprint": plan_fingerprint,
                "declared_reservations": deepcopy(reservations),
                "declared_invariants": list(invariants),
                "declared_invalidators": list(invalidators),
                "feasibility_valid_until": (
                    (snapshot.clock.day + 1) * snapshot.clock.turns_per_day - 1
                ),
                "revalidation_policy_version": self.model_spec_version,
                "revalidated_before_commit": True,
            },
        )

        self.commitment_sequence += 1
        commitment_id = (
            f"{self.scope_key}/commitment-{self.commitment_sequence:04d}"
        )
        self.active_commitment = {
            "commitment_id": commitment_id,
            "commitment_version": 1,
            "decision_id": decision_id,
            "decision_version": 1,
            "plan_id": plan_id,
            "plan_version": 1,
            "plan_fingerprint": plan_fingerprint,
            "plan_payload": deepcopy(plan_payload),
            "commitment_start_transition": snapshot.clock.step,
            "commitment_day": snapshot.clock.day,
            "scope": deepcopy(plan_payload.get("scope", {})),
            "declared_completion_condition": completion_condition,
            "declared_invariants": list(invariants),
            "declared_invalidators": list(invalidators),
            "completion_invalidation_precedence_policy": (
                completion_invalidation_precedence_policy
            ),
            "reservation_envelope": deepcopy(reservations),
        }
        self.counts["commitment_count"] += 1
        self._transition(
            COMMITTED_EXECUTING,
            snapshot=snapshot,
            reason_code="COMMIT",
            payload=deepcopy(self.active_commitment),
        )
        return True

    def reject_precommit(
        self, snapshot: CodexSnapshot, *, reason_code: str
    ) -> None:
        if self.state not in {DEFINED, PLAN_FEASIBLE}:
            raise RuntimeError("REJECTED is only valid before commitment")
        self.counts["rejected_count"] += 1
        self._transition(REJECTED, snapshot=snapshot, reason_code=reason_code)
        self._transition(
            DECISION_OPEN,
            snapshot=snapshot,
            reason_code="REJECTED_REOPEN",
        )

    def register_action_requests(
        self,
        snapshot: CodexSnapshot,
        requests: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            raise RuntimeError("committed actions require an active commitment")
        materialized: list[dict[str, Any]] = []
        for request in requests:
            self.request_sequence += 1
            record = {
                "action_request_id": (
                    f"{self.scope_key}/request-{self.request_sequence:07d}"
                ),
                "snapshot_eligibility_id": (
                    f"{self.scope_key}/eligibility-{self.request_sequence:07d}"
                ),
                "commitment_id": self.active_commitment["commitment_id"],
                "commitment_version": self.active_commitment[
                    "commitment_version"
                ],
                "transition_id": snapshot.clock.step,
                "source_state_id": snapshot.state_id,
                **deepcopy(request),
            }
            materialized.append(record)
        self.request_records.extend(materialized)
        return materialized

    def record_verification(
        self,
        snapshot: CodexSnapshot,
        *,
        request_records: list[dict[str, Any]],
        outcomes: list[dict[str, Any]],
        invariant_results: list[dict[str, Any]] | None = None,
        invalidator_results: list[dict[str, Any]] | None = None,
        completion_status: str = "NOT_MET",
        precedence_result: str = "CONTINUE",
    ) -> dict[str, Any]:
        self.verify_sequence += 1
        outcome_by_request = {
            outcome["action_request_id"]: outcome for outcome in outcomes
        }
        self.outcome_records.extend(deepcopy(outcomes))
        execution_outcome_ids: list[str] = []
        for request in request_records:
            outcome = outcome_by_request.get(request["action_request_id"])
            if outcome is not None:
                execution_outcome_ids.append(outcome["execution_outcome_id"])
        active = self.active_commitment or {}
        record = {
            "verify_event_id": f"{self.scope_key}/verify-{self.verify_sequence:07d}",
            "decision_id": active.get("decision_id"),
            "commitment_id": active.get("commitment_id"),
            "commitment_version": active.get("commitment_version"),
            "transition_id": snapshot.clock.step,
            "action_request_ids": [
                request["action_request_id"] for request in request_records
            ],
            "snapshot_eligibility_ids": [
                request["snapshot_eligibility_id"] for request in request_records
            ],
            "execution_outcome_ids": execution_outcome_ids,
            "post_state_evidence_id": snapshot.evidence_snapshot_id,
            "invariant_results": deepcopy(invariant_results or []),
            "invalidator_results": deepcopy(invalidator_results or []),
            "completion_status": completion_status,
            "terminal_status": (
                "TRIGGERED" if snapshot.clock.is_terminal_action else "CLEAR"
            ),
            "precedence_policy_reference": active.get(
                "completion_invalidation_precedence_policy"
            ),
            "precedence_result": precedence_result,
            "verification_result": (
                "DEVIATION"
                if any(
                    outcome.get("result") in {"NO_OP", "REJECTED"}
                    for outcome in outcomes
                )
                else "OBSERVED"
            ),
        }
        self.verify_records.append(record)
        return record

    def repair(
        self,
        snapshot: CodexSnapshot,
        *,
        trigger_evidence_snapshot_id: str,
        reason_code: str,
        succeeded: bool = True,
    ) -> None:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            return
        commitment_id = self.active_commitment["commitment_id"]
        self.repair_sequence += 1
        repair_id = f"{self.scope_key}/repair-{self.repair_sequence:05d}"
        self._transition(
            REPAIR_WITHIN_COMMITMENT,
            snapshot=snapshot,
            reason_code=reason_code,
            payload={"repair_id": repair_id, "commitment_id": commitment_id},
        )
        record = {
            "repair_id": repair_id,
            "commitment_id": commitment_id,
            "repair_attempt": sum(
                1
                for item in self.repair_records
                if item["commitment_id"] == commitment_id
            )
            + 1,
            "trigger_evidence_snapshot_id": trigger_evidence_snapshot_id,
            "repair_policy_version": self.model_spec_version,
            "plan_version_before": self.active_commitment["plan_version"],
            "plan_version_after": self.active_commitment["plan_version"],
            "repair_result": "SUCCEEDED" if succeeded else "FAILED",
        }
        self.repair_records.append(record)
        self.counts["repair_count"] += 1
        self._transition(
            COMMITTED_EXECUTING,
            snapshot=snapshot,
            reason_code="REPAIR_SUCCESSFUL" if succeeded else "REPAIR_FAILED",
            payload=record,
        )

    def close_active(
        self,
        snapshot: CodexSnapshot,
        *,
        completion: bool,
        invalidator_results: list[dict[str, Any]] | None = None,
    ) -> str:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            return self.state
        invalidators = [
            item
            for item in (invalidator_results or [])
            if bool(item.get("triggered"))
        ]
        if invalidators:
            # INVALIDATION_WINS is the pre-declared Codex conflict policy.
            target = INVALIDATED
            reason_code = str(
                invalidators[0].get(
                    "reason_code", "STATE_INVARIANT_VIOLATION"
                )
            )
            self.counts["invalidation_count"] += 1
        elif completion:
            target = COMPLETED
            reason_code = "PLAN_COMPLETED"
            self.counts["completion_count"] += 1
        else:
            return COMMITTED_EXECUTING

        self._transition(
            target,
            snapshot=snapshot,
            reason_code=reason_code,
            payload={
                "commitment_id": self.active_commitment["commitment_id"],
                "completion": completion,
                "invalidator_results": deepcopy(invalidators),
            },
        )
        self._review_and_reopen(snapshot, closure_type=target)
        return target

    def cancel(self, snapshot: CodexSnapshot, *, reason_code: str) -> None:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            raise RuntimeError("CANCELLED requires an active commitment")
        self.counts["cancellation_count"] += 1
        self._transition(
            CANCELLED,
            snapshot=snapshot,
            reason_code=reason_code,
            payload={
                "commitment_id": self.active_commitment["commitment_id"],
                "decision_boundary_id": f"boundary-{snapshot.clock.step:06d}",
                "cancellation_policy_version": self.model_spec_version,
                "authority_reference": "MODEL_SPEC_CODEX_C2_V6",
                "evidence_snapshot_id": snapshot.evidence_snapshot_id,
            },
        )
        self._review_and_reopen(snapshot, closure_type=CANCELLED)

    def supersede(
        self, snapshot: CodexSnapshot, *, supersession_reason_code: str
    ) -> str:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            raise RuntimeError("SUPERSEDED requires an active commitment")
        self.counts["supersession_count"] += 1
        intent_id = self._next_id("supersession-intent")
        self.pending_supersession_intent_id = intent_id
        self._transition(
            SUPERSEDED,
            snapshot=snapshot,
            reason_code=supersession_reason_code,
            payload={
                "superseded_commitment_id": self.active_commitment[
                    "commitment_id"
                ],
                "supersession_intent_id": intent_id,
                "decision_boundary_id": f"boundary-{snapshot.clock.step:06d}",
                "supersession_policy_version": self.model_spec_version,
                "authority_reference": "MODEL_SPEC_CODEX_C2_V6",
                "supersession_evidence_snapshot_id": (
                    snapshot.evidence_snapshot_id
                ),
                "successor_decision_id": None,
            },
        )
        self._review_and_reopen(snapshot, closure_type=SUPERSEDED)
        return intent_id

    def _review_and_reopen(
        self, snapshot: CodexSnapshot, *, closure_type: str
    ) -> None:
        active = deepcopy(self.active_commitment or {})
        self._transition(
            REVIEW_READY,
            snapshot=snapshot,
            reason_code=f"{closure_type}_REVIEW_READY",
        )
        self.review_sequence += 1
        disposition = {
            COMPLETED: "MAINTAIN",
            INVALIDATED: "REDUCE",
            CANCELLED: "INCONCLUSIVE",
            SUPERSEDED: "INCONCLUSIVE",
        }.get(closure_type, "INCONCLUSIVE")
        review = {
            "review_id": f"{self.scope_key}/review-{self.review_sequence:05d}",
            "review_version": 1,
            "decision_id": active.get("decision_id"),
            "commitment_id": active.get("commitment_id"),
            "review_status": "COMPLETE",
            "closure_type": closure_type,
            "start_evidence_snapshot": active.get("commitment_start_transition"),
            "end_evidence_snapshot": snapshot.evidence_snapshot_id,
            "execution_summary": {
                "repair_count": sum(
                    1
                    for item in self.repair_records
                    if item.get("commitment_id") == active.get("commitment_id")
                )
            },
            "diagnostic_summary": "DESCRIPTIVE_DIAGNOSTICS",
            "review_disposition": disposition,
            "completed_at_transition_id": snapshot.clock.step,
        }
        self.review_records.append(review)
        self.active_commitment = None
        self._transition(
            DECISION_OPEN,
            snapshot=snapshot,
            reason_code="REVIEW_COMPLETE",
            payload={
                "review_id": review["review_id"],
                "review_status": "COMPLETE",
            },
        )

    def close_terminal(
        self,
        snapshot: CodexSnapshot,
        *,
        closure_disposition: str = "TERMINAL_PREEMPTION",
    ) -> None:
        if self.state == TERMINAL_CLOSED:
            return
        if self.state not in ONLINE_STATES:
            raise RuntimeError(f"cannot terminal-close lifecycle state {self.state}")
        previous_state = self.state
        active = deepcopy(self.active_commitment or {})
        self.terminal_sequence += 1
        self.terminal_record = {
            "terminal_closure_id": (
                f"{self.scope_key}/terminal-{self.terminal_sequence:03d}"
            ),
            "previous_lifecycle_state": previous_state,
            "decision_id": active.get("decision_id"),
            "plan_id": active.get("plan_id"),
            "commitment_id": active.get("commitment_id"),
            "terminal_transition_id": snapshot.clock.step,
            "terminal_evidence_snapshot_id": snapshot.evidence_snapshot_id,
            "closure_disposition": closure_disposition,
        }
        self._transition(
            TERMINAL_CLOSED,
            snapshot=snapshot,
            reason_code=closure_disposition,
            payload=self.terminal_record,
        )
        self.active_commitment = None

    def summary(self) -> dict[str, Any]:
        """Return JSON-serializable lifecycle telemetry for local verification."""

        return {
            "run_id": self.run_id,
            "episode_id": self.episode_id,
            "agent_id": self.agent_id,
            "model_spec_version": self.model_spec_version,
            "foundation_checkpoint": FOUNDATION_CHECKPOINT,
            "foundation_version": FOUNDATION_VERSION,
            "engine_fingerprint": ENGINE_FINGERPRINT,
            "state": self.state,
            "active_commitment": deepcopy(self.active_commitment),
            "counts": deepcopy(self.counts),
            "event_count": len(self.events),
            "request_count": len(self.request_records),
            "outcome_count": len(self.outcome_records),
            "verify_count": len(self.verify_records),
            "review_count": len(self.review_records),
            "terminal_record": deepcopy(self.terminal_record),
        }

    def export_ledger(self) -> dict[str, Any]:
        return {
            **self.summary(),
            "events": deepcopy(self.events),
            "feasibility_records": deepcopy(self.feasibility_records),
            "repair_records": deepcopy(self.repair_records),
            "review_records": deepcopy(self.review_records),
            "request_records": deepcopy(self.request_records),
            "outcome_records": deepcopy(self.outcome_records),
            "verify_records": deepcopy(self.verify_records),
            "terminal_record": deepcopy(self.terminal_record),
        }


def snapshot_asdict(snapshot: CodexSnapshot) -> dict[str, Any]:
    """Small public helper used by tests without exposing mutable internals."""

    payload = asdict(snapshot)
    payload["farm"] = deepcopy(snapshot.farm)
    payload["private"] = deepcopy(snapshot.private)
    payload["market"] = deepcopy(snapshot.market)
    return payload

# ==========================================
# --- Antigravity C2 75K Config Class ---
# ==========================================
@dataclass
class AntigravityC2_75K_Config:
    """Parametric configuration for Antigravity C2 75K Strategy Model."""

    candidate_id: str = "ANTIGRAVITY_C2_75K_DUAL_Q"
    schema_version: str = "model_spec_c2.antigravity.dual_q.v1"
    model_spec_version: str = "ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0"
    foundation_checkpoint: str = "f391ee2"

    # Land & Layout (Q0 + Q1, 48 productive tiles)
    quadrants_owned: int = 2
    workforce_total: int = 13
    q0_workforce_total: int = 7
    crop_working_set_target: int = 36
    crop_counts: Dict[str, int] = field(
        default_factory=lambda: {"MELON": 18, "STRAWBERRY": 16, "WHEAT": 2}
    )
    pasture_allocation_target: int = 12
    livestock_targets: Dict[str, int] = field(
        default_factory=lambda: {"COW": 6, "SHEEP": 6}
    )
    bootstrap_livestock: Dict[str, int] = field(
        default_factory=lambda: {"COW": 2, "SHEEP": 2}
    )
    q1_livestock_targets: Dict[str, int] = field(
        default_factory=lambda: {"COW": 3, "SHEEP": 3}
    )
    livestock_activation_days: Dict[str, int] = field(
        default_factory=lambda: {"COW": 7, "SHEEP": 8}
    )

    # Q1 Activation Gates
    q1_activation_min_day: int = 6
    q1_activation_max_day: int = 10
    q1_activation_cash: float = 2800.0
    q1_operating_cash_floor: float = 250.0

    # Economics & Buffers
    operating_cash_floor: float = 50.0
    feed_reserve_rounds: int = 2
    observed_capacity_days: int = 3
    hard_schedule_days: int = 2
    minimum_post_plant_action_phases: int = 1
    payback_cutoff_days: int = 2
    crop_horizon_margin_days: int = 1
    endgame_shutdown_days: int = 2
    max_noop_before_invalidation: int = 3
    turns_per_day: int = 24

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AntigravityC2_75K_Config":
        """Construct config instance from dictionary."""
        return cls(
            candidate_id=data.get("candidate_id", "ANTIGRAVITY_C2_75K_DUAL_Q"),
            schema_version=data.get("schema_version", "model_spec_c2.antigravity.dual_q.v1"),
            model_spec_version=data.get("model_spec_version", "ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0"),
            foundation_checkpoint=data.get("foundation_checkpoint", "f391ee2"),
            quadrants_owned=int(data.get("quadrants_owned", 2)),
            workforce_total=int(data.get("workforce_total", 13)),
            q0_workforce_total=int(data.get("q0_workforce_total", 7)),
            crop_working_set_target=int(data.get("crop_working_set_target", 36)),
            crop_counts={str(k): int(v) for k, v in data.get("crop_counts", {}).items()} or {"MELON": 18, "STRAWBERRY": 16, "WHEAT": 2},
            pasture_allocation_target=int(data.get("pasture_allocation_target", 12)),
            livestock_targets={str(k): int(v) for k, v in data.get("livestock_targets", {}).items()} or {"COW": 6, "SHEEP": 6},
            bootstrap_livestock={str(k): int(v) for k, v in data.get("bootstrap_livestock", {}).items()} or {"COW": 2, "SHEEP": 2},
            q1_livestock_targets={str(k): int(v) for k, v in data.get("q1_livestock_targets", {}).items()} or {"COW": 3, "SHEEP": 3},
            livestock_activation_days={str(k): int(v) for k, v in data.get("livestock_activation_days", {}).items()} or {"COW": 7, "SHEEP": 8},
            q1_activation_min_day=int(data.get("q1_activation_min_day", 6)),
            q1_activation_max_day=int(data.get("q1_activation_max_day", 10)),
            q1_activation_cash=float(data.get("q1_activation_cash", 2800.0)),
            q1_operating_cash_floor=float(data.get("q1_operating_cash_floor", 250.0)),
            operating_cash_floor=float(data.get("operating_cash_floor", 50.0)),
            feed_reserve_rounds=int(data.get("feed_reserve_rounds", 2)),
            observed_capacity_days=int(data.get("observed_capacity_days", 3)),
            hard_schedule_days=int(data.get("hard_schedule_days", 2)),
            minimum_post_plant_action_phases=int(data.get("minimum_post_plant_action_phases", 1)),
            payback_cutoff_days=int(data.get("payback_cutoff_days", 2)),
            crop_horizon_margin_days=int(data.get("crop_horizon_margin_days", 1)),
            endgame_shutdown_days=int(data.get("endgame_shutdown_days", 2)),
            max_noop_before_invalidation=int(data.get("max_noop_before_invalidation", 3)),
            turns_per_day=int(data.get("turns_per_day", 24)),
        )

    @classmethod
    def load(cls, path: Path | str | None = None) -> "AntigravityC2_75K_Config":
        """Load configuration from JSON file or default."""
        if path is None and "ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG" in globals():
            return cls.from_dict(globals()["ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG"])
        config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
        if not config_path.exists():
            return cls()
        with config_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)

# ==========================================
# --- Antigravity Base Q0 Definitions ---
# ==========================================
CROP_RULES: dict[str, dict[str, Any]] = {
    "WHEAT": {
        "first_yield_day": 2,
        "economic_harvest_day": 4,
        "max_yield_day": 4,
        "pre_harvest_yield_target": 3,
        "ongoing": False,
        "final_production_day": 4,
        "value": 25,
    },
    "STRAWBERRY": {
        "first_yield_day": 10,
        "economic_harvest_day": 10,
        "max_yield_day": 10,
        "pre_harvest_yield_target": 2,
        "ongoing": True,
        "final_production_day": 16,
        "value": 120,
    },
    "MELON": {
        "first_yield_day": 10,
        "economic_harvest_day": 10,
        "max_yield_day": 12,
        "pre_harvest_yield_target": 6,
        "ongoing": False,
        "final_production_day": 12,
        "value": 250,
    },
}

ANIMAL_RULES: dict[str, dict[str, Any]] = {
    "COW": {"cost": 400, "first_output_day": 8, "period": 2, "product": "MILK"},
    "SHEEP": {"cost": 500, "first_output_day": 6, "period": 3, "product": "WOOL"},
}

# Q0 NW 5x5 layout: (4,4) is shed tile. 6 pastures + 18 crop tiles = 24 productive tiles.
ANTIGRAVITY_PASTURE_POSITIONS: tuple[tuple[int, int], ...] = (
    (3, 4),
    (4, 3),
    (3, 3),
    (2, 4),
    (4, 2),
    (3, 2),
)

ANTIGRAVITY_CROP_ZONES: tuple[tuple[tuple[int, int], ...], ...] = (
    ((0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1)),
    ((3, 0), (4, 0), (4, 1), (3, 1), (2, 2), (1, 2)),
    ((0, 2), (0, 3), (1, 3), (2, 3), (1, 4), (0, 4)),
)

ANTIGRAVITY_ZONE_STAGING_POINTS: dict[int, tuple[int, int]] = {
    0: (1, 1),
    1: (3, 1),
    2: (0, 3),
}

ANTIGRAVITY_CROP_POSITIONS: tuple[tuple[int, int], ...] = tuple(
    position for zone in ANTIGRAVITY_CROP_ZONES for position in zone
)

_MELON_POSITIONS = {
    *ANTIGRAVITY_CROP_ZONES[0][:3],
    *ANTIGRAVITY_CROP_ZONES[1][:3],
    *ANTIGRAVITY_CROP_ZONES[2][:3],
}
_WHEAT_POSITION = ANTIGRAVITY_CROP_ZONES[2][-1]

ANTIGRAVITY_CROP_PLAN: dict[tuple[int, int], str] = {
    position: (
        "MELON"
        if position in _MELON_POSITIONS
        else "WHEAT"
        if position == _WHEAT_POSITION
        else "STRAWBERRY"
    )
    for position in ANTIGRAVITY_CROP_POSITIONS
}

_STRAWBERRY_A = {
    *ANTIGRAVITY_CROP_ZONES[0][3:],
    ANTIGRAVITY_CROP_ZONES[2][3],
}

ANTIGRAVITY_COHORT_OFFSET: dict[tuple[int, int], int] = {}
for zone_id, zone in enumerate(ANTIGRAVITY_CROP_ZONES):
    for position in zone[:3]:
        ANTIGRAVITY_COHORT_OFFSET[position] = zone_id
for position, crop in ANTIGRAVITY_CROP_PLAN.items():
    if crop == "STRAWBERRY":
        ANTIGRAVITY_COHORT_OFFSET[position] = 0 if position in _STRAWBERRY_A else 2
    elif crop == "WHEAT":
        ANTIGRAVITY_COHORT_OFFSET[position] = 0

ANTIGRAVITY_ZONE_BY_POSITION: dict[tuple[int, int], int] = {
    position: zone_id
    for zone_id, zone in enumerate(ANTIGRAVITY_CROP_ZONES)
    for position in zone
}

ANTIGRAVITY_ROUTE_INDEX: dict[tuple[int, int], int] = {
    position: route_index
    for zone in ANTIGRAVITY_CROP_ZONES
    for route_index, position in enumerate(zone)
}

# Antigravity 7-Worker Routine Roles
ROLE_SEQUENCE = (
    "RELIEF_LOGISTICS",     # W0: Farmer (Shed, marketing, emergency feed/rescue)
    "CROP_ZONE_0",          # W1: 1st Hand (Zone 0: 6 tiles)
    "CROP_ZONE_1",          # W2: 2nd Hand (Zone 1: 6 tiles)
    "CROP_ZONE_2",          # W3: 3rd Hand (Zone 2: 6 tiles)
    "LIVESTOCK_COW",        # W4: 4th Hand (Feed-first COW, care, milk)
    "LIVESTOCK_SHEEP",      # W5: 5th Hand (Feed-first SHEEP, care, wool)
    "FERTILIZER_LOGISTICS", # W6: 6th Hand (Manure collection & crop fertilizing)
)


OUT_OF_SCOPE = "OUT_OF_SCOPE"
EMPTY_ASSIGNED = "EMPTY_ASSIGNED"
GROWING = "GROWING"
YIELD_ACCUMULATING = "YIELD_ACCUMULATING"
HARVEST_READY = "HARVEST_READY"
RETIREMENT_DUE = "RETIREMENT_DUE"
LOST_WEED = "LOST_WEED"

MODEL_SPEC_VERSION = "ANTIGRAVITY-C2-COMPACT-Q0-50K-ROUTINE-V1.0"
FOUNDATION_CHECKPOINT = "f391ee2"
MOVE_ACTIONS = {"NORTH", "SOUTH", "EAST", "WEST"}
HANDLING_ACTIONS = {"PICKUP", "PLACE"}
PRODUCTIVE_ACTIONS = {
    "PLANT",
    "WATER",
    "HARVEST",
    "DIG",
    "BUILD_PASTURE",
    "FEED",
    "CARE",
    "COLLECT_FERTILIZER",
    "FERTILIZE",
}
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def classify_tile_lifecycle(
    tile: Any, *, in_working_set: bool, day: int
) -> str | None:
    """Classify a crop tile from current observable state only."""
    if not in_working_set or tile == "LOCKED":
        return OUT_OF_SCOPE
    if tile is None:
        return EMPTY_ASSIGNED
    if not isinstance(tile, dict):
        return None
    if tile.get("kind") == "WEED":
        return LOST_WEED
    if tile.get("kind") != "PLANT":
        return OUT_OF_SCOPE
    crop = str(tile.get("crop", ""))
    rules = CROP_RULES.get(crop)
    if rules is None:
        return None
    try:
        age = day - int(tile["planted_day"])
        yield_units = int(tile["yield_units"])
        max_lifespan_step = int(tile.get("max_lifespan_step", -1))
    except (KeyError, TypeError, ValueError):
        return None
    if age < 0 or yield_units < 0:
        return None
    if yield_units > 0 and age < int(rules["economic_harvest_day"]):
        return YIELD_ACCUMULATING
    if yield_units > 0:
        return HARVEST_READY
    if (
        bool(rules["ongoing"])
        and max_lifespan_step >= 0
        and age >= int(rules["final_production_day"])
    ):
        return RETIREMENT_DUE
    return GROWING


def water_loss_at_eod_if_unserved(tile: Any) -> bool:
    """Check if unwatered plant will die at EOD boundary (consecutive_unwatered + 1 >= 2)."""
    if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
        return False
    if bool(tile.get("watered_today", False)):
        return False
    try:
        return int(tile.get("consecutive_unwatered", 0)) + 1 >= 2
    except (TypeError, ValueError):
        return True


def lifespan_decay_started(tile: Any, engine_step: int) -> bool:
    """Check if plant has reached its maximum lifespan step."""
    if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
        return False
    try:
        value = int(tile.get("max_lifespan_step", -1))
    except (TypeError, ValueError):
        return False
    return value >= 0 and engine_step >= value


def plant_matches_cohort(tile: Any, crop: str, day: int) -> bool:
    return (
        isinstance(tile, dict)
        and tile.get("kind") == "PLANT"
        and tile.get("crop") == crop
        and int(tile.get("planted_day", -1)) == day
    )


def yield_completion_water_due(tile: Any, day: int) -> bool:
    """Check if plant is in yield completion window and requires water."""
    if (
        not isinstance(tile, dict)
        or tile.get("kind") != "PLANT"
        or tile.get("watered_today", False)
    ):
        return False
    rules = CROP_RULES.get(str(tile.get("crop", "")))
    if rules is None or bool(rules["ongoing"]):
        return False
    try:
        age = day - int(tile["planted_day"])
        units = int(tile["yield_units"])
    except (KeyError, TypeError, ValueError):
        return False
    return (
        int(rules["economic_harvest_day"]) <= age <= int(rules["max_yield_day"])
        and units < int(rules["pre_harvest_yield_target"])
    )


class AntigravityC2_50K_Policy:
    """Seven-worker compact-Q0 hybrid policy with routine worker planning and Codex V7.1 serviceability."""

    def __init__(
        self,
        config: AntigravityC2_50K_Config | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        self.config = deepcopy(config or AntigravityC2_50K_Config.load())
        self.candidate_id = "ANTIGRAVITY_C2"
        self.model_spec_version = MODEL_SPEC_VERSION
        self.turns_per_day = int(self.config.turns_per_day)
        self.episode_steps = 720
        self.shed_capacity = 100
        self.max_market_orders = 10
        context = deepcopy(run_context or {})
        self.run_id = str(context.get("run_id", "antigravity-compact-q0-50k-local"))
        self.episode_id = str(context.get("episode_id", "antigravity-compact-q0-50k-episode"))
        self.seed = context.get("seed")
        self.opponent_id = context.get("opponent_id", "UNASSIGNED")
        self.player_position = context.get("player_position", "UNASSIGNED")

        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self._previous_snapshot: CodexSnapshot | None = None
        self._pending_requests: list[dict[str, Any]] = []
        self._last_snapshot_fingerprint: str | None = None
        self._last_action: dict[str, Any] | None = None
        self._last_day: int | None = None
        self._last_global_signature: tuple[Any, ...] | None = None
        self._global_plan: dict[str, Any] = {}
        self._commitments: dict[int, dict[str, Any]] = {}
        self._roles: dict[int, str] = {}
        self._consecutive_noops = 0
        self._terminal_closed = False

        self.action_requests_by_opcode: Counter[str] = Counter()
        self.market_requested_units: Counter[str] = Counter()
        self.execution_outcomes: Counter[str] = Counter()
        self.production_units: Counter[str] = Counter()
        self.revenue: Counter[str] = Counter()
        self.daily_requested: dict[int, Counter[str]] = defaultdict(Counter)
        self.daily_completed: dict[int, Counter[str]] = defaultdict(Counter)
        self.daily_due: dict[int, set[str]] = defaultdict(set)
        self.daily_due_completed: dict[int, set[str]] = defaultdict(set)
        self.interrupts_by_reason: Counter[str] = Counter()
        self.activation_records: list[dict[str, Any]] = []
        self._activation_decisions: set[tuple[str, int, int]] = set()
        self.role_changes = 0
        self.cross_zone_assists = 0
        self.retarget_count = 0
        self.duplicate_assignments = 0
        self.target_dwell_total = 0
        self.target_dwell_count = 0
        self.hard_deadline_misses = 0
        self.animal_escapes = 0
        self.global_replan_count = 0
        self.local_replan_count = 0
        self.capacity_rejections: Counter[str] = Counter()
        self.land_utilization_trajectory: list[dict[str, Any]] = []
        self.final_money = 0.0

    @staticmethod
    def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
        x, y = position
        tiles = farm.get("tiles", []) or []
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return "LOCKED"

    @staticmethod
    def _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:
        farmer = farm.get("farmer", [4, 4])
        hands = farm.get("hands", []) or []
        return [tuple(int(v) for v in farmer)] + [
            tuple(int(v) for v in position) for position in hands
        ]

    @staticmethod
    def _owned_quadrants(farm: dict[str, Any]) -> int:
        raw = farm.get("unlocked_quadrants", ["NW"])
        return len(raw) if isinstance(raw, list) else int(raw)

    @staticmethod
    def _inventory(private: dict[str, Any], worker_id: int) -> dict[str, int]:
        inventories = private.get("inventories", []) or []
        if 0 <= worker_id < len(inventories) and isinstance(inventories[worker_id], dict):
            return {str(k): int(v) for k, v in inventories[worker_id].items()}
        return {}

    def _role_for(self, worker_id: int) -> str:
        return ROLE_SEQUENCE[min(worker_id, len(ROLE_SEQUENCE) - 1)]

    def _feed_service_species(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> tuple[str, ...]:
        """Bind every active livestock cluster to an owner capable of staging and delivering wheat.

        W4/W5 are the dedicated livestock specialists (COW / SHEEP).
        If hands are missing before full hire, farmer (W0) covers COW (if workforce <= 4)
        and first hand / farmer covers SHEEP (if workforce <= 5).
        """
        worker_count = len(self._positions(snapshot.farm))
        if role == "LIVESTOCK_COW":
            return ("COW",)
        if role == "LIVESTOCK_SHEEP":
            return ("SHEEP",)

        species: list[str] = []
        if worker_count <= 4 and worker_id == 0:
            species.append("COW")
        if worker_count <= 5:
            sheep_owner = 1 if worker_count >= 2 else 0
            if worker_id == sheep_owner:
                species.append("SHEEP")
        return tuple(species)


    def _feed_tasks_for_worker(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[dict[str, Any]]:
        tasks: list[dict[str, Any]] = []
        for species in self._feed_service_species(snapshot, worker_id, role):
            tasks.extend(
                task
                for task in self._animal_tasks(snapshot, species)
                if task["kind"] == "FEED"
            )
        return tasks

    def _update_roles(self, worker_count: int) -> None:
        current = {worker_id: self._role_for(worker_id) for worker_id in range(worker_count)}
        for worker_id, role in current.items():
            if worker_id in self._roles and self._roles[worker_id] != role:
                self.role_changes += 1
        self._roles = current

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
            for position in ANTIGRAVITY_CROP_POSITIONS
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
            for position in ANTIGRAVITY_PASTURE_POSITIONS
        )
        return (
            len(farm.get("hands", []) or []),
            self._owned_quadrants(farm),
            crop_signature,
            animal_signature,
        )

    def _crop_serviceable_before_terminal(self, crop: str, step: int) -> bool:
        maturity = int(CROP_RULES[crop]["economic_harvest_day"]) * self.turns_per_day
        margin = math.ceil(
            float(self.config.crop_horizon_margin_days) * self.turns_per_day
        )
        return self.episode_steps - step > maturity + margin

    def _plant_serviceable_before_eod(self, hour: int) -> bool:
        return (
            self.turns_per_day - 1 - hour
            >= int(self.config.minimum_post_plant_action_phases)
        )

    def _shutdown(self, snapshot: CodexSnapshot) -> bool:
        return snapshot.clock.remaining_steps <= math.ceil(
            float(self.config.endgame_shutdown_days) * self.turns_per_day
        )

    def _active_animal_positions(
        self, farm: dict[str, Any], species: str | None = None
    ) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []
        for position in ANTIGRAVITY_PASTURE_POSITIONS:
            tile = self._tile(farm, position)
            if not isinstance(tile, dict) or not tile.get("animal"):
                continue
            if species is None or tile.get("animal") == species:
                positions.append(position)
        return positions

    def _animal_counts(self, snapshot: CodexSnapshot) -> Counter[str]:
        counts: Counter[str] = Counter()
        for position in ANTIGRAVITY_PASTURE_POSITIONS:
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
        for position in ANTIGRAVITY_CROP_POSITIONS:
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
                for zone_id, zone in enumerate(ANTIGRAVITY_CROP_ZONES)
            },
            "hard_horizon": "CURRENT_DAY_AND_NEXT_SERVICE_BOUNDARY",
            "soft_horizon": "FIRST_MONETIZABLE_OUTPUT",
            "capacity": capacity,
        }
        self._last_global_signature = signature
        self._last_day = snapshot.clock.day
        self.global_replan_count += 1

    def _maybe_replan_global(self, snapshot: CodexSnapshot) -> None:
        signature = self._asset_signature(snapshot)
        if self._last_day is None or snapshot.clock.day != self._last_day:
            self._replan_global(snapshot, "EOD_BOUNDARY")
        elif signature != self._last_global_signature:
            self._replan_global(snapshot, "WORKFORCE_OR_ASSET_CHANGE")

    def _route_cost_estimate(self, snapshot: CodexSnapshot) -> int:
        positions = self._positions(snapshot.farm)
        cost = 0
        for worker_id, position in enumerate(positions):
            role = self._role_for(worker_id)
            if role.startswith("CROP_ZONE_"):
                zone_id = int(role.rsplit("_", 1)[1])
                targets = [
                    target
                    for target in ANTIGRAVITY_CROP_ZONES[zone_id]
                    if isinstance(self._tile(snapshot.farm, target), dict)
                ]
            elif role == "LIVESTOCK_COW":
                targets = self._active_animal_positions(snapshot.farm, "COW")
            elif role == "LIVESTOCK_SHEEP":
                targets = self._active_animal_positions(snapshot.farm, "SHEEP")
            else:
                targets = []
            if targets:
                nearest = min(
                    abs(position[0] - target[0]) + abs(position[1] - target[1])
                    for target in targets
                )
                cost += nearest + max(0, len(targets) - 1)
        return cost

    def _capacity_snapshot(
        self, snapshot: CodexSnapshot, candidate_species: str | None
    ) -> dict[str, Any]:
        farm = snapshot.farm
        unit_count = len(self._positions(farm))
        active_crops = sum(
            1
            for position in ANTIGRAVITY_CROP_POSITIONS
            if isinstance(self._tile(farm, position), dict)
            and self._tile(farm, position).get("kind") == "PLANT"
        )
        active_animals = len(self._active_animal_positions(farm))
        ready_crop = sum(
            1
            for position in ANTIGRAVITY_CROP_POSITIONS
            if classify_tile_lifecycle(
                self._tile(farm, position),
                in_working_set=True,
                day=snapshot.clock.day,
            )
            == HARVEST_READY
        )
        ready_animals = sum(
            1
            for position in ANTIGRAVITY_PASTURE_POSITIONS
            if isinstance(self._tile(farm, position), dict)
            and int(self._tile(farm, position).get("yield_units", 0)) > 0
        )
        candidate_actions = 0
        if candidate_species is not None:
            candidate_actions = 4  # FEED + CARE + amortized collection/handling
        required_services = (
            active_crops
            + active_animals * 2
            + ready_crop
            + ready_animals
            + candidate_actions
        )
        travel = self._route_cost_estimate(snapshot) + (2 if candidate_species else 0)
        handling = max(1, active_animals // 2) + (2 if candidate_species else 0)
        required = required_services + travel + handling
        remaining_phases = max(0, self.turns_per_day - snapshot.clock.hour)
        available_current = unit_count * remaining_phases
        available_next = unit_count * self.turns_per_day
        slack_current = available_current - min(required, required_services + travel)
        slack_next = available_next - required

        history_days = [
            day
            for day in sorted(self.daily_completed)
            if day < snapshot.clock.day
        ][-int(self.config.observed_capacity_days):]
        observed_values = [
            int(sum(self.daily_completed[day].values())) for day in history_days
        ]
        observed_capacity = min(observed_values) if len(observed_values) >= 3 else None
        return {
            "available_current": available_current,
            "available_next": available_next,
            "required_services": required_services,
            "travel_actions": travel,
            "handling_actions": handling,
            "required_total": required,
            "slack_current": slack_current,
            "slack_next": slack_next,
            "minimum_slack": min(slack_current, slack_next),
            "history_days": history_days,
            "observed_capacity": observed_capacity,
            "forecast_within_observed": (
                observed_capacity is not None and required <= observed_capacity
            ),
        }

    def _capacity_admission(
        self, snapshot: CodexSnapshot, species: str
    ) -> tuple[bool, str, dict[str, Any]]:
        capacity = self._capacity_snapshot(snapshot, candidate_species=species)
        if len(capacity["history_days"]) < int(self.config.observed_capacity_days):
            return False, "OBSERVED_CAPACITY_INSUFFICIENT_HISTORY", capacity
        if capacity["minimum_slack"] < 0:
            return False, "NEGATIVE_ACTION_SLACK", capacity
        if not capacity["forecast_within_observed"]:
            return False, "FORECAST_EXCEEDS_OBSERVED_CAPACITY", capacity

        counts = self._animal_counts(snapshot)
        projected_animals = sum(counts.values()) + 1
        shed = snapshot.private.get("shed", {}) or {}
        carried_wheat = sum(
            self._inventory(snapshot.private, worker_id).get("WHEAT", 0)
            for worker_id in range(len(self._positions(snapshot.farm)))
        )
        wheat_on_hand = int(shed.get("WHEAT", 0)) + carried_wheat
        wheat_price = float((snapshot.market.get("prices", {}) or {}).get("WHEAT", 25))
        animal_cost = float(ANIMAL_RULES[species]["cost"])
        feed_need = projected_animals * int(self.config.feed_reserve_rounds)
        feed_deficit = max(0, feed_need - wheat_on_hand)
        cash = float(snapshot.farm.get("money", 0.0))
        committed_cost = animal_cost + feed_deficit * wheat_price
        if cash - committed_cost < float(self.config.operating_cash_floor):
            return False, "CASH_OR_FEED_BUFFER_INSUFFICIENT", capacity

        shed_total = _inventory_total(shed)
        if shed_total >= self.shed_capacity and not any(
            int(shed.get(item, 0)) > 0
            for item in ("MILK", "WOOL", "MELON", "STRAWBERRY", "FERTILIZER")
        ):
            return False, "NO_LEGAL_INVENTORY_PATH", capacity

        output_day = snapshot.clock.day + int(ANIMAL_RULES[species]["first_output_day"])
        final_day = (self.episode_steps - 1) // self.turns_per_day
        if output_day >= final_day - int(self.config.payback_cutoff_days):
            return False, "FIRST_OUTPUT_AFTER_PAYBACK_CUTOFF", capacity
        return True, "ADMITTED", capacity

    @staticmethod
    def _task(
        target: tuple[int, int],
        action: list[Any],
        *,
        kind: str,
        loss_rank: int,
        value: int,
        slack: int,
        hard_reason: str | None = None,
        zone: int | None = None,
    ) -> dict[str, Any]:
        return {
            "target": target,
            "action": action,
            "kind": kind,
            "loss_rank": loss_rank,
            "value": value,
            "slack": slack,
            "hard_reason": hard_reason,
            "zone": zone,
        }

    def _crop_tasks(self, snapshot: CodexSnapshot) -> list[dict[str, Any]]:
        tasks: list[dict[str, Any]] = []
        day = snapshot.clock.day
        hour = snapshot.clock.hour
        step = snapshot.clock.step
        seeds = snapshot.private.get("seeds", {}) or {}
        shutdown = self._shutdown(snapshot)
        for position in ANTIGRAVITY_CROP_POSITIONS:
            crop = ANTIGRAVITY_CROP_PLAN[position]
            zone = ANTIGRAVITY_ZONE_BY_POSITION[position]
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
                cohort_open = day >= int(ANTIGRAVITY_COHORT_OFFSET[position])
                if (
                    not shutdown
                    and cohort_open
                    and self._plant_serviceable_before_eod(hour)
                    and self._crop_serviceable_before_terminal(crop, step)
                    and int(seeds.get(crop, 0)) > 0
                ):
                    tasks.append(
                        self._task(position, ["PLANT", crop], kind="PLANT", loss_rank=3, value=int(CROP_RULES[crop]["value"]), slack=max(1, self.turns_per_day - hour), zone=zone)
                    )
                continue
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue

            crop = str(tile.get("crop", crop))
            rules = CROP_RULES.get(crop)
            if rules is None:
                continue
            unwatered = not bool(tile.get("watered_today", False))
            decay = lifespan_decay_started(tile, step)
            if state in {YIELD_ACCUMULATING, HARVEST_READY} and decay:
                tasks.append(
                    self._task(position, ["HARVEST"], kind="HARVEST", loss_rank=0, value=int(rules["value"]), slack=0, hard_reason="HARVEST_TERMINAL_RISK", zone=zone)
                )
                continue
            if unwatered and water_loss_at_eod_if_unserved(tile):
                tasks.append(
                    self._task(position, ["WATER"], kind="WATER", loss_rank=0, value=int(rules["value"]), slack=max(0, self.turns_per_day - hour - 1), hard_reason="CROP_WATER_LOSS", zone=zone)
                )
                continue
            if unwatered and yield_completion_water_due(tile, day):
                tasks.append(
                    self._task(position, ["WATER"], kind="WATER", loss_rank=1, value=int(rules["value"]), slack=max(0, self.turns_per_day - hour - 1), zone=zone)
                )
                continue
            if state == HARVEST_READY:
                tasks.append(
                    self._task(position, ["HARVEST"], kind="HARVEST", loss_rank=1, value=int(rules["value"]), slack=max(1, self.turns_per_day - hour), zone=zone)
                )
            elif unwatered:
                tasks.append(
                    self._task(position, ["WATER"], kind="WATER", loss_rank=2, value=int(rules["value"]), slack=max(1, self.turns_per_day - hour), zone=zone)
                )
        return tasks

    def _animal_tasks(
        self, snapshot: CodexSnapshot, species: str
    ) -> list[dict[str, Any]]:
        tasks: list[dict[str, Any]] = []
        positions = (
            ANTIGRAVITY_PASTURE_POSITIONS[:3]
            if species == "COW"
            else ANTIGRAVITY_PASTURE_POSITIONS[3:]
        )
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

    def _free_pastures(
        self, snapshot: CodexSnapshot, species: str
    ) -> list[tuple[int, int]]:
        positions = (
            ANTIGRAVITY_PASTURE_POSITIONS[:3]
            if species == "COW"
            else ANTIGRAVITY_PASTURE_POSITIONS[3:]
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
        tasks: list[dict[str, Any]] = []

        # 1. Animal placement
        for species in ("COW", "SHEEP"):
            if int(inventory.get(species, 0)) <= 0:
                continue
            for target in self._free_pastures(snapshot, species):
                tasks.append(
                    self._task(target, ["PLACE", species], kind="PLACE_ANIMAL", loss_rank=1, value=int(ANIMAL_RULES[species]["cost"]), slack=12)
                )
            return tasks

        # 2. INVENTORY_AWARE_FEED_DISPATCH & FEED_FIRST_CLUSTER_BATCHING
        # An assigned feed service owner feeds directly if carrying wheat,
        # or commits to shed pickup sized for all due animals before unloading products.
        feed_tasks = self._feed_tasks_for_worker(snapshot, worker_id, role)
        wheat = int(inventory.get("WHEAT", 0))
        if feed_tasks and wheat > 0:
            return feed_tasks
        if feed_tasks and int(shed.get("WHEAT", 0)) > 0:
            quantity = min(len(feed_tasks), int(shed.get("WHEAT", 0)))
            tasks.append(
                self._task(
                    (4, 4),
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

        # 3. CLOSED_LOOP_FERTILIZER: Apply fertilizer to same-day-watered crops
        fertilizer = int(inventory.get("FERTILIZER", 0))
        if fertilizer > 0 and role in {"FERTILIZER_LOGISTICS", "RELIEF_LOGISTICS"}:
            eligible: list[tuple[int, int]] = []
            for position in ANTIGRAVITY_CROP_POSITIONS:
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
                key=lambda position: (
                    ANTIGRAVITY_CROP_PLAN[position] != "MELON",
                    ANTIGRAVITY_COHORT_OFFSET[position],
                    ANTIGRAVITY_ROUTE_INDEX[position],
                )
            )
            for position in eligible[:fertilizer]:
                tasks.append(
                    self._task(
                        position,
                        ["FERTILIZE"],
                        kind="FERTILIZER_APPLICATION",
                        loss_rank=2,
                        value=int(CROP_RULES[ANTIGRAVITY_CROP_PLAN[position]]["value"]),
                        slack=max(1, self.turns_per_day - snapshot.clock.hour),
                        zone=ANTIGRAVITY_ZONE_BY_POSITION[position],
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
                        (4, 4),
                        ["PLACE", item, min(amount, free)],
                        kind="INVENTORY_UNBLOCK",
                        loss_rank=1 if snapshot.clock.hour >= 20 else 2,
                        value=100,
                        slack=max(1, self.turns_per_day - snapshot.clock.hour),
                        hard_reason="BLOCKING_INVENTORY_LOSS" if snapshot.clock.hour >= 22 else None,
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
                    (4, 4),
                    ["PLACE", "WHEAT", wheat],
                    kind="FEED_STAGING",
                    loss_rank=2,
                    value=25,
                    slack=max(1, self.turns_per_day - snapshot.clock.hour),
                )
            )
            return tasks

        if _inventory_total(inventory) > 0:
            item = min(
                (item for item, amount in inventory.items() if int(amount) > 0),
                key=lambda item: (item in {"COW", "SHEEP", "WHEAT"}, item),
            )
            free = max(0, self.shed_capacity - _inventory_total(shed))
            if free > 0:
                tasks.append(
                    self._task(
                        (4, 4),
                        ["PLACE", item, min(int(inventory[item]), free)],
                        kind="INVENTORY_UNBLOCK",
                        loss_rank=2,
                        value=0,
                        slack=12,
                    )
                )
            return tasks

        # 6. Pickup animal staged in shed
        if role in {"FERTILIZER_LOGISTICS", "RELIEF_LOGISTICS"}:
            for species in ("COW", "SHEEP"):
                if int(shed.get(species, 0)) > 0 and self._free_pastures(snapshot, species):
                    tasks.append(
                        self._task((4, 4), ["PICKUP", species, 1], kind="ANIMAL_STAGING", loss_rank=1, value=int(ANIMAL_RULES[species]["cost"]), slack=12)
                    )
                    return tasks
        return tasks

    @staticmethod
    def _task_priority(
        task: dict[str, Any], position: tuple[int, int]
    ) -> tuple[int, int, int, int, int, int, int]:
        target = tuple(task["target"])
        distance = abs(position[0] - target[0]) + abs(position[1] - target[1])
        route_index = ANTIGRAVITY_ROUTE_INDEX.get(target, 99)
        return (
            int(task["loss_rank"]),
            -int(task["value"]),
            int(task["slack"]),
            distance,
            route_index,
            target[1],
            target[0],
        )

    def _close_commitment(self, worker_id: int, step: int) -> None:
        commitment = self._commitments.pop(worker_id, None)
        if commitment is None:
            return
        self.target_dwell_total += max(1, step - int(commitment["assigned_step"]))
        self.target_dwell_count += 1

    def _choose_committed_task(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
        position: tuple[int, int],
        candidates: list[dict[str, Any]],
        reserved: set[tuple[int, int]],
    ) -> list[Any]:
        usable = [
            task
            for task in candidates
            if tuple(task["target"]) in SHED_TILES
            or tuple(task["target"]) not in reserved
        ]
        existing = self._commitments.get(worker_id)
        chosen: dict[str, Any] | None = None
        if existing is not None:
            matches = [
                task
                for task in usable
                if tuple(task["target"]) == tuple(existing["target"])
                and list(task["action"]) == list(existing["action"])
            ]
            if matches:
                chosen = min(matches, key=lambda task: self._task_priority(task, position))
                hard = [task for task in usable if task.get("hard_reason")]
                if hard:
                    best_hard = min(hard, key=lambda task: self._task_priority(task, position))
                    if self._task_priority(best_hard, position) < self._task_priority(chosen, position):
                        self.retarget_count += 1
                        reason = str(best_hard["hard_reason"])
                        self.interrupts_by_reason[reason] += 1
                        self._close_commitment(worker_id, snapshot.clock.step)
                        chosen = best_hard
            else:
                self._close_commitment(worker_id, snapshot.clock.step)
                self.local_replan_count += 1

        if chosen is None and usable:
            chosen = min(usable, key=lambda task: self._task_priority(task, position))
            self._commitments[worker_id] = {
                "target": tuple(chosen["target"]),
                "action": list(chosen["action"]),
                "kind": chosen["kind"],
                "role": role,
                "zone": chosen.get("zone"),
                "assigned_step": snapshot.clock.step,
                "hard_reason": chosen.get("hard_reason"),
            }
            self.local_replan_count += 1
        elif chosen is not None and worker_id not in self._commitments:
            self._commitments[worker_id] = {
                "target": tuple(chosen["target"]),
                "action": list(chosen["action"]),
                "kind": chosen["kind"],
                "role": role,
                "zone": chosen.get("zone"),
                "assigned_step": snapshot.clock.step,
                "hard_reason": chosen.get("hard_reason"),
            }

        if chosen is None:
            self._close_commitment(worker_id, snapshot.clock.step)
            # Anti-wandering: move to / hold at zone staging point
            if role.startswith("CROP_ZONE_"):
                zone_id = int(role.rsplit("_", 1)[1])
                staging_point = ANTIGRAVITY_ZONE_STAGING_POINTS.get(zone_id, (4, 4))
                if position != staging_point:
                    return _move_towards(position, staging_point)
            return ["PASS"]

        target = tuple(chosen["target"])
        if target not in SHED_TILES:
            if target in reserved:
                self.duplicate_assignments += 1
                self._close_commitment(worker_id, snapshot.clock.step)
                return ["PASS"]
            reserved.add(target)
        if role.startswith("CROP_ZONE_") and chosen.get("zone") is not None:
            home_zone = int(role.rsplit("_", 1)[1])
            if int(chosen["zone"]) != home_zone:
                self.cross_zone_assists += 1
        if position == target:
            return list(chosen["action"])
        return _move_towards(position, target)

    def _eligible_unit_action(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        action: list[Any],
    ) -> bool:
        if not action:
            return False
        opcode = str(action[0])
        positions = self._positions(snapshot.farm)
        if not 0 <= worker_id < len(positions):
            return False
        position = positions[worker_id]
        tile = self._tile(snapshot.farm, position)
        inventory = self._inventory(snapshot.private, worker_id)
        if opcode == "PASS" or opcode in MOVE_ACTIONS:
            return True
        if opcode == "PLANT" and len(action) >= 2:
            return tile is None and int((snapshot.private.get("seeds", {}) or {}).get(action[1], 0)) > 0
        if opcode == "WATER":
            return isinstance(tile, dict) and tile.get("kind") == "PLANT" and not tile.get("watered_today", False)
        if opcode == "HARVEST":
            return isinstance(tile, dict) and int(tile.get("yield_units", 0)) > 0
        if opcode == "DIG":
            return isinstance(tile, dict) and tile.get("kind") in {"WEED", "PLANT"}
        if opcode == "BUILD_PASTURE":
            return tile is None and position in ANTIGRAVITY_PASTURE_POSITIONS
        if opcode == "FEED":
            return isinstance(tile, dict) and bool(tile.get("animal")) and not tile.get("fed_today", False) and int(inventory.get("WHEAT", 0)) > 0
        if opcode == "CARE":
            return isinstance(tile, dict) and bool(tile.get("animal")) and not tile.get("cared_today", False)
        if opcode == "COLLECT_FERTILIZER":
            return isinstance(tile, dict) and bool(tile.get("fertilizer_available", False))
        if opcode == "PICKUP" and len(action) >= 3:
            return position in SHED_TILES and int((snapshot.private.get("shed", {}) or {}).get(action[1], 0)) >= int(action[2])
        if opcode == "PLACE" and len(action) >= 2:
            item = str(action[1])
            if item in ANIMAL_RULES:
                return isinstance(tile, dict) and tile.get("kind") == "PASTURE" and not tile.get("animal") and int(inventory.get(item, 0)) > 0
            return position in SHED_TILES and int(inventory.get(item, 0)) > 0
        if opcode == "FERTILIZE":
            return isinstance(tile, dict) and tile.get("kind") == "PLANT" and bool(tile.get("watered_today", False)) and int(inventory.get("FERTILIZER", 0)) > 0
        return False

    def decide_unit_actions(self, snapshot: CodexSnapshot) -> list[list[Any]]:
        """Compute actions for farmer and hands according to role hierarchy."""
        positions = self._positions(snapshot.farm)
        crop_tasks = self._crop_tasks(snapshot)
        cow_tasks = self._animal_tasks(snapshot, "COW")
        sheep_tasks = self._animal_tasks(snapshot, "SHEEP")
        hard_crop_tasks = [
            task
            for task in crop_tasks
            if task.get("hard_reason")
        ]
        reserved: set[tuple[int, int]] = set()
        actions: dict[int, list[Any]] = {}

        # Priority dispatch order: livestock specialists & crop zones first, then fertilizer & relief
        dispatch_order = [worker_id for worker_id in (4, 5, 1, 2, 3, 6, 0) if worker_id < len(positions)]

        for worker_id in dispatch_order:
            role = self._role_for(worker_id)
            inventory_tasks = self._inventory_task(snapshot, worker_id, role)
            candidates: list[dict[str, Any]]
            if inventory_tasks:
                candidates = inventory_tasks
            elif role.startswith("CROP_ZONE_"):
                zone_id = int(role.rsplit("_", 1)[1])
                own = [task for task in crop_tasks if task.get("zone") == zone_id]
                cross_hard = [
                    task
                    for task in hard_crop_tasks
                    if task.get("zone") != zone_id
                ]
                # Dedicated zone ownership: assist other zones ONLY if own zone has zero tasks
                candidates = own if own else cross_hard
            elif role == "LIVESTOCK_COW":
                candidates = [
                    task
                    for task in cow_tasks
                    if task["kind"] != "FEED"
                    and not (
                        task["kind"] == "FERTILIZER_COLLECTION"
                        and len(positions) >= 7
                    )
                ]
            elif role == "LIVESTOCK_SHEEP":
                candidates = [
                    task
                    for task in sheep_tasks
                    if task["kind"] != "FEED"
                    and not (
                        task["kind"] == "FERTILIZER_COLLECTION"
                        and len(positions) >= 7
                    )
                ]
            elif role == "FERTILIZER_LOGISTICS":
                fertilizer = [
                    task
                    for task in [*cow_tasks, *sheep_tasks]
                    if task["kind"] in {"FERTILIZER_COLLECTION", "BUILD_PASTURE"}
                ]
                candidates = hard_crop_tasks + fertilizer
            else:  # RELIEF_LOGISTICS (Farmer W0)
                emergency_animal = [
                    task
                    for task in [*cow_tasks, *sheep_tasks]
                    if task["kind"] in {"BUILD_PASTURE", "FEED"}
                ]
                growth = [
                    task
                    for task in [*crop_tasks, *cow_tasks, *sheep_tasks]
                    if task["kind"] in {"PLANT", "BUILD_PASTURE", "WEED_RECOVERY", "RETIREMENT_CLEAR"}
                ]
                high_value = [
                    task
                    for task in crop_tasks
                    if task["kind"] in {"HARVEST", "WATER"}
                ]
                candidates = emergency_animal + hard_crop_tasks + growth + high_value

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

    def decide_market_orders(self, snapshot: CodexSnapshot) -> list[list[Any]]:
        """Compute atomic market orders adhering to capacity and cash rules."""
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

        # 3. Daily hiring up to 7 workers (6 hands) during hours 0/1
        target_hands = int(self.config.workforce_total) - 1
        hands = len(farm.get("hands", []) or [])
        hires_today = int(farm.get("hires_today", 0))
        if not self._shutdown(snapshot) and snapshot.clock.hour in {0, 1}:
            for offset in range(max(0, target_hands - hands)):
                if not add(["HIRE"], float(_fib(hires_today + offset))):
                    break

        # 4. Opening Day 0 Step 0: Bootstrap 2 COW + 2 SHEEP + 10 WHEAT feed + opening seeds
        if snapshot.clock.step == 0:
            add(["BUY_ANIMAL", "COW", 2], 800.0)
            add(["BUY_ANIMAL", "SHEEP", 2], 1000.0)
            add(["BUY_PRODUCT", "WHEAT", 10], 10 * float(prices.get("WHEAT", 25.0)))
            add(["BUY_SEED", "MELON", 3], 240.0)
            return orders[: self.max_market_orders]

        if not self._shutdown(snapshot):
            # Repair bootstrap deficit if any
            for species in ("COW", "SHEEP"):
                bootstrap = int(self.config.bootstrap_livestock[species])
                deficit = max(0, bootstrap - int(counts.get(species, 0)))
                if snapshot.clock.day <= 1 and deficit > 0:
                    quantity = min(deficit, max(0, int((cash - floor) // ANIMAL_RULES[species]["cost"])))
                    if quantity > 0:
                        add(["BUY_ANIMAL", species, quantity], quantity * float(ANIMAL_RULES[species]["cost"]))
                        counts[species] += quantity

            # Livestock expansion to 3+3
            for species in ("COW", "SHEEP"):
                activation_day = int(self.config.livestock_activation_days[species])
                target = int(self.config.livestock_targets[species])
                if snapshot.clock.day < activation_day or int(counts.get(species, 0)) >= target:
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

            # Seed restocking for staggered cohorts
            active_by_crop: Counter[str] = Counter()
            for position, planned_crop in ANTIGRAVITY_CROP_PLAN.items():
                tile = self._tile(farm, position)
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    active_by_crop[str(tile.get("crop", planned_crop))] += 1
            seed_costs = {"MELON": 80.0, "STRAWBERRY": 100.0, "WHEAT": 10.0}
            for crop in ("STRAWBERRY", "MELON", "WHEAT"):
                eligible_slots = sum(
                    1
                    for position, planned_crop in ANTIGRAVITY_CROP_PLAN.items()
                    if planned_crop == crop
                    and snapshot.clock.day >= ANTIGRAVITY_COHORT_OFFSET[position]
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

    def _materialize_requests(
        self, snapshot: CodexSnapshot, result: dict[str, Any]
    ) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        positions = self._positions(snapshot.farm)
        unit_actions = [result.get("farmer", ["PASS"]), *(result.get("hands", []) or [])]
        for worker_id, action in enumerate(unit_actions):
            if not action or worker_id >= len(positions):
                continue
            opcode = str(action[0])
            normalized = "MOVE" if opcode in MOVE_ACTIONS else opcode
            self.action_requests_by_opcode[normalized] += 1
            self.daily_requested[snapshot.clock.day][normalized] += 1
            if opcode == "PASS":
                continue
            position = positions[worker_id]
            records.append(
                {
                    "step": snapshot.clock.step,
                    "day": snapshot.clock.day,
                    "worker_id": worker_id,
                    "role": self._role_for(worker_id),
                    "opcode": opcode,
                    "normalized": normalized,
                    "position": position,
                    "target": tuple(self._commitments.get(worker_id, {}).get("target", position)),
                    "action": list(action),
                }
            )
        for order in result.get("market", []) or []:
            if not order:
                continue
            kind = str(order[0])
            item = str(order[1]) if len(order) > 1 else "UNKNOWN"
            units = int(order[2]) if len(order) > 2 else 1
            self.market_requested_units[f"{kind}:{item}"] += units
        return records

    def _attribute_execution(
        self, previous: CodexSnapshot, current: CodexSnapshot
    ) -> None:
        p_farm = previous.farm
        c_farm = current.farm
        p_priv = previous.private
        c_priv = current.private
        day = previous.clock.day

        # Track completed actions and productions
        for position in ANTIGRAVITY_CROP_POSITIONS:
            p_tile = self._tile(p_farm, position)
            c_tile = self._tile(c_farm, position)
            if not isinstance(p_tile, dict) or not isinstance(c_tile, dict):
                continue
            if not p_tile.get("watered_today", False) and c_tile.get("watered_today", False):
                self.daily_completed[day]["WATER"] += 1
                self.daily_due_completed[day].add(f"WATER:{position[0]}:{position[1]}")
            if int(p_tile.get("yield_units", 0)) > int(c_tile.get("yield_units", 0)):
                crop = str(p_tile.get("crop", "CROP"))
                harvested = int(p_tile.get("yield_units", 0)) - int(c_tile.get("yield_units", 0))
                self.production_units[crop] += harvested
                self.daily_completed[day]["HARVEST"] += 1
                self.daily_due_completed[day].add(f"HARVEST:{position[0]}:{position[1]}")

        for position in ANTIGRAVITY_PASTURE_POSITIONS:
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
            for position in ANTIGRAVITY_PASTURE_POSITIONS:
                p_tile = self._tile(p_farm, position)
                c_tile = self._tile(c_farm, position)
                if (
                    isinstance(p_tile, dict)
                    and p_tile.get("animal")
                    and (not isinstance(c_tile, dict) or not c_tile.get("animal"))
                ):
                    self.animal_escapes += 1

        # Track fertilizer application
        for position in ANTIGRAVITY_CROP_POSITIONS:
            p_tile = self._tile(p_farm, position)
            c_tile = self._tile(c_farm, position)
            if isinstance(p_tile, dict) and isinstance(c_tile, dict):
                if int(p_tile.get("fertilized_until_day", -1)) < int(c_tile.get("fertilized_until_day", -1)):
                    self.production_units["FERTILIZER_APPLIED"] += 1
                    self.daily_completed[day]["FERTILIZE"] += 1

    def act(
        self,
        observation: dict[str, Any],
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Produce deterministic action dictionary."""
        try:
            snapshot = CodexObservationAdapter.parse(
                observation,
                configuration or {"episodeSteps": self.episode_steps, "turnsPerDay": self.turns_per_day},
                fallback_turns_per_day=self.turns_per_day,
                fallback_episode_steps=self.episode_steps,
            )
            if self._previous_snapshot is not None:
                self._attribute_execution(self._previous_snapshot, snapshot)

            self._maybe_replan_global(snapshot)
            unit_actions = self.decide_unit_actions(snapshot)
            market_orders = self.decide_market_orders(snapshot)
            farmer_action = unit_actions[0] if unit_actions else ["PASS"]
            hands_actions = unit_actions[1:] if len(unit_actions) > 1 else []

            result = {
                "farmer": farmer_action,
                "hands": hands_actions,
                "market": market_orders,
            }
            self._pending_requests = self._materialize_requests(snapshot, result)
            self._previous_snapshot = snapshot
            self._last_action = result
            self.final_money = float(snapshot.farm.get("money", 0.0))
            return result
        except Exception as exc:
            self.error_count += 1
            self.fallback_count += 1
            self.last_exception = f"{type(exc).__name__}: {exc}"
            return dict(_SAFE_PASS)

    def telemetry_snapshot(self) -> dict[str, Any]:
        """Produce comprehensive telemetry dictionary."""
        productive = sum(
            self.action_requests_by_opcode[op] for op in PRODUCTIVE_ACTIONS
        )
        moves = self.action_requests_by_opcode["MOVE"]
        passes = self.action_requests_by_opcode["PASS"]
        move_per_prod = round(moves / max(1, productive), 4)
        due_total = sum(len(items) for items in self.daily_due.values())
        due_completed = sum(len(items) for items in self.daily_due_completed.values())
        on_time_ratio = round(due_completed / max(1, due_total), 4)

        return {
            "MILK_units": int(self.production_units["MILK"]),
            "WOOL_units": int(self.production_units["WOOL"]),
            "MELON_units": int(self.production_units["MELON"]),
            "STRAWBERRY_units": int(self.production_units["STRAWBERRY"]),
            "WHEAT_consumed": int(self.action_requests_by_opcode["FEED"]),
            "WHEAT_sold": int(self.market_requested_units["SELL:WHEAT"]),
            "fertilizer_collected": int(self.production_units["FERTILIZER_COLLECTED"]),
            "fertilizer_applied": int(self.production_units["FERTILIZER_APPLIED"]),
            "crop_revenue": float(
                self.production_units["MELON"] * 250
                + self.production_units["STRAWBERRY"] * 120
                + self.production_units["WHEAT"] * 25
            ),
            "livestock_revenue": float(
                self.production_units["MILK"] * 160
                + self.production_units["WOOL"] * 200
            ),
            "market_trading_contribution": 0.0,
            "productive_actions": productive,
            "MOVE_actions": moves,
            "PASS_actions": passes,
            "MOVE_PER_PRODUCTIVE_ACTION": move_per_prod,
            "PRODUCTIVE_UTILIZATION": round(productive / max(1, moves + productive + passes), 4),
            "PRODUCTIVE_UTILIZATION_FINAL": round(productive / max(1, moves + productive + passes), 4),
            "ON_TIME_CROP_SERVICE_RATIO": on_time_ratio,
            "HARD_DEADLINE_MISSES": self.hard_deadline_misses,
            "ANIMAL_ESCAPE": self.animal_escapes,
            "RETARGET_COUNT": self.retarget_count,
            "RETARGET_COUNT_PER_WORKER_DAY": round(self.retarget_count / 30.0, 4),
            "TARGET_DWELL_TIME": round(self.target_dwell_total / max(1, self.target_dwell_count), 2),
            "DUPLICATE_ASSIGNMENTS": self.duplicate_assignments,
            "ROLE_CHANGES": self.role_changes,
            "CROSS_ZONE_ASSISTS": self.cross_zone_assists,
            "GLOBAL_REPLANS": self.global_replan_count,
            "LOCAL_REPLANS": self.local_replan_count,
        }

# ==========================================
# --- Antigravity Dual Q0+Q1 Policy ---
# ==========================================
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

# ==========================================
# --- Agent Factory & Kaggle Entrypoint ---
# ==========================================
class AntigravityC2_75K_Agent:
    """Antigravity C2 75K Tournament Candidate Agent."""

    def __init__(
        self,
        config: Any = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        self.config = config or AntigravityC2_75K_Config.load()
        self.policy = AntigravityDualQPolicy(config=self.config, run_context=run_context)
        self.antigravity_75k_instance = self.policy
        self.last_exception: str | None = None
        self.error_count: int = 0
        self.fallback_count: int = 0

    def act(
        self,
        observation: dict[str, Any],
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.policy.act(observation, configuration=configuration)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            return self.act(observation, configuration=configuration)
        except Exception as exc:
            self.last_exception = f"{type(exc).__name__}: {exc}"
            self.error_count += 1
            self.fallback_count += 1
            return {"farmer": ["PASS"], "hands": [], "market": []}


def create_agent(run_context: dict[str, Any] | None = None) -> AntigravityC2_75K_Agent:
    return AntigravityC2_75K_Agent(run_context=run_context)


_agent_factory: Callable[[dict[str, Any], Any], dict[str, Any]] | None = None
_episode_sequence = 0


def agent(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
    """Kaggle entry point for Antigravity 75K routine candidate."""
    global _agent_factory, _episode_sequence
    step = int(observation.get("step", 0))
    if step == 0 or _agent_factory is None:
        _episode_sequence += 1
        player = int(observation.get("player", 0))
        _agent_factory = create_agent(
            run_context={
                "run_id": "antigravity-kaggle-runtime",
                "episode_id": f"antigravity-episode-{_episode_sequence:06d}",
                "seed": None,
                "opponent_id": "KAGGLE_UNOBSERVED",
                "player_position": player,
            }
        )
    return _agent_factory(observation, configuration)
