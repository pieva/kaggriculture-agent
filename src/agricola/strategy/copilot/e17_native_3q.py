"""Native Copilot E17.0 three-quadrant baseline.

The controller is deliberately state-reactive and table-free. It consumes only
the shared observation contract, owns its task selection and path decisions, and
does not import another agent's routine, planner, dispatcher, or schedule.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import (
    CodexObservationAdapter,
    stable_payload_hash,
)

POLICY_VERSION = "COPILOT-E17.0-NATIVE-3Q-CROP-BASELINE-V1"
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "docs" / "model_specs" / "copilot" / "e17" / "configs"
    / "COPILOT_E17_0_NATIVE_3Q_V1.json"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
QUADRANT_ORDER = ("NW", "NE", "SW")
LAND_COSTS = (1000, 2000, 4000)
CROP_FIRST_YIELD_DAYS = {
    "WHEAT": 2,
    "CARROT": 2,
    "TOMATO": 8,
    "STRAWBERRY": 10,
    "MELON": 10,
}

NATIVE_POLICY_DESCRIPTOR = {
    "policy_version": POLICY_VERSION,
    "controller": "state-reactive-greedy-task-allocation",
    "task_priority": ["harvest", "water", "dig", "plant"],
    "path_rule": "deterministic-manhattan-x-then-y",
    "quadrant_rule": "balance-empty-tile-allocation-across-owned-NW-NE-SW",
    "action_table": False,
    "external_strategy_dependency": False,
}


def native_policy_fingerprint() -> str:
    """Return the agent-local algorithm fingerprint, not an action-table hash."""

    return stable_payload_hash(NATIVE_POLICY_DESCRIPTOR).upper()


@dataclass(frozen=True)
class NativeCopilotConfig:
    policy_id: str
    primary_crop: str
    target_quadrants: int
    target_hands_per_day: int
    land_cash_reserve: int
    seed_reorder_level: int
    seed_batch_quantity: int
    harvest_age_days: int
    terminal_harvest_day: int
    fallback_turns_per_day: int
    fallback_episode_steps: int
    max_market_orders_per_turn: int

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "NativeCopilotConfig":
        config = cls(
            policy_id=str(payload["policy_id"]),
            primary_crop=str(payload["primary_crop"]).upper(),
            target_quadrants=int(payload["target_quadrants"]),
            target_hands_per_day=int(payload["target_hands_per_day"]),
            land_cash_reserve=int(payload["land_cash_reserve"]),
            seed_reorder_level=int(payload["seed_reorder_level"]),
            seed_batch_quantity=int(payload["seed_batch_quantity"]),
            harvest_age_days=int(payload["harvest_age_days"]),
            terminal_harvest_day=int(payload["terminal_harvest_day"]),
            fallback_turns_per_day=int(payload["fallback_turns_per_day"]),
            fallback_episode_steps=int(payload["fallback_episode_steps"]),
            max_market_orders_per_turn=int(payload["max_market_orders_per_turn"]),
        )
        if config.policy_id != POLICY_VERSION:
            raise ValueError("config policy_id does not match the controller")
        if config.primary_crop not in CROP_FIRST_YIELD_DAYS:
            raise ValueError("unsupported primary_crop")
        if config.target_quadrants != 3:
            raise ValueError("the E17.0 Copilot baseline must own exactly 3 quadrants")
        if config.target_hands_per_day < 0:
            raise ValueError("target_hands_per_day must be non-negative")
        if config.seed_batch_quantity <= 0 or config.seed_reorder_level < 0:
            raise ValueError("seed configuration must be positive")
        return config


def load_native_config(path: Path | str = DEFAULT_CONFIG_PATH) -> NativeCopilotConfig:
    with Path(path).open("r", encoding="utf-8") as handle:
        return NativeCopilotConfig.from_mapping(json.load(handle))


def _quadrant(x: int, y: int, board_size: int) -> str:
    half = board_size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def _tile_at(tiles: list[list[Any]], position: tuple[int, int]) -> Any:
    x, y = position
    if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
        return tiles[y][x]
    return "LOCKED"


def _move_toward(source: tuple[int, int], target: tuple[int, int]) -> list[str]:
    sx, sy = source
    tx, ty = target
    if sx < tx:
        return ["EAST"]
    if sx > tx:
        return ["WEST"]
    if sy < ty:
        return ["SOUTH"]
    if sy > ty:
        return ["NORTH"]
    return ["PASS"]


class CopilotNativeThreeQPolicy:
    """Deterministic crop-only 3Q baseline driven by current state."""

    def __init__(self, config: NativeCopilotConfig | None = None):
        self.config = config or load_native_config()
        self.technical_errors = 0

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            return self.act(observation, configuration)
        except Exception:
            self.technical_errors += 1
            farm = {}
            if isinstance(observation, dict):
                player = int(observation.get("player", 0))
                farms = observation.get("farms", []) or []
                if 0 <= player < len(farms) and isinstance(farms[player], dict):
                    farm = farms[player]
            return {
                "farmer": ["PASS"],
                "hands": [["PASS"] for _ in farm.get("hands", [])],
                "market": [],
            }

    def act(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        snapshot = CodexObservationAdapter.parse(
            observation,
            configuration,
            fallback_turns_per_day=self.config.fallback_turns_per_day,
            fallback_episode_steps=self.config.fallback_episode_steps,
        )
        farm = snapshot.farm
        private = snapshot.private
        tiles = farm.get("tiles", []) or []
        board_size = int(snapshot.configuration_snapshot["boardSize"])
        unlocked = tuple(farm.get("unlocked_quadrants", ["NW"]) or ["NW"])
        positions = [tuple(farm.get("farmer", [4, 4]))]
        positions.extend(tuple(pos) for pos in farm.get("hands", []) or [])
        seed_budget = int((private.get("seeds", {}) or {}).get(self.config.primary_crop, 0))
        actions = self._allocate_unit_actions(
            positions=positions,
            tiles=tiles,
            unlocked=unlocked,
            board_size=board_size,
            day=snapshot.clock.day,
            seed_budget=seed_budget,
        )
        market = self._market_orders(
            farm=farm,
            private=private,
            hour=snapshot.clock.hour,
            unlocked_count=len(unlocked),
        )
        return {"farmer": actions[0], "hands": actions[1:], "market": market}

    def _task_for_tile(self, tile: Any, day: int) -> tuple[int, list[str]] | None:
        if tile is None:
            return 3, ["PLANT", self.config.primary_crop]
        if not isinstance(tile, dict):
            return None
        if tile.get("kind") == "WEED":
            return 2, ["DIG"]
        if tile.get("kind") != "PLANT":
            return None
        crop = str(tile.get("crop", ""))
        age = day - int(tile.get("planted_day", day))
        first_yield = CROP_FIRST_YIELD_DAYS.get(crop, self.config.harvest_age_days)
        ready = int(tile.get("yield_units", 0)) > 0 and (
            age >= max(first_yield, self.config.harvest_age_days)
            or day >= self.config.terminal_harvest_day
        )
        if ready:
            return 0, ["HARVEST"]
        if not bool(tile.get("watered_today", False)):
            return 1, ["WATER"]
        return None

    def _allocate_unit_actions(
        self,
        *,
        positions: list[tuple[int, int]],
        tiles: list[list[Any]],
        unlocked: tuple[str, ...],
        board_size: int,
        day: int,
        seed_budget: int,
    ) -> list[list[str]]:
        tasks: list[tuple[int, tuple[int, int], list[str], str]] = []
        active_by_quadrant = {name: 0 for name in QUADRANT_ORDER}
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                quadrant = _quadrant(x, y, board_size)
                if quadrant not in unlocked or quadrant not in active_by_quadrant:
                    continue
                if tile is not None:
                    active_by_quadrant[quadrant] += 1
                task = self._task_for_tile(tile, day)
                if task is not None:
                    tasks.append((task[0], (x, y), task[1], quadrant))

        claimed: set[tuple[int, int]] = set()
        assigned_empty = {name: 0 for name in QUADRANT_ORDER}
        unit_actions: list[list[str]] = []
        available_seeds = seed_budget
        quadrant_rank = {name: index for index, name in enumerate(QUADRANT_ORDER)}

        for position in positions:
            current_task = self._task_for_tile(_tile_at(tiles, position), day)
            if current_task is not None and position not in claimed:
                priority, command = current_task
                if command[0] != "PLANT" or available_seeds > 0:
                    claimed.add(position)
                    if command[0] == "PLANT":
                        available_seeds -= 1
                    unit_actions.append(command)
                    continue

            available = [task for task in tasks if task[1] not in claimed]
            if not available:
                unit_actions.append(["PASS"])
                continue

            def task_key(item: tuple[int, tuple[int, int], list[str], str]):
                priority, target, _command, quadrant = item
                distance = abs(position[0] - target[0]) + abs(position[1] - target[1])
                balance = (
                    active_by_quadrant[quadrant] + assigned_empty[quadrant]
                    if priority == 3
                    else 0
                )
                return (
                    priority,
                    balance,
                    distance,
                    quadrant_rank[quadrant],
                    target[1],
                    target[0],
                )

            priority, target, command, quadrant = min(available, key=task_key)
            claimed.add(target)
            if priority == 3:
                assigned_empty[quadrant] += 1
            if target == position and command[0] == "PLANT":
                if available_seeds <= 0:
                    unit_actions.append(["PASS"])
                else:
                    available_seeds -= 1
                    unit_actions.append(command)
            elif target == position:
                unit_actions.append(command)
            else:
                unit_actions.append(_move_toward(position, target))

        return unit_actions or [["PASS"]]

    def _market_orders(
        self,
        *,
        farm: dict[str, Any],
        private: dict[str, Any],
        hour: int,
        unlocked_count: int,
    ) -> list[list[Any]]:
        orders: list[list[Any]] = []
        shed = private.get("shed", {}) or {}
        crop_quantity = int(shed.get(self.config.primary_crop, 0))
        if crop_quantity > 0:
            orders.append(["SELL", self.config.primary_crop, crop_quantity])

        money = float(farm.get("money", 0.0))
        if unlocked_count < self.config.target_quadrants:
            land_cost = LAND_COSTS[unlocked_count - 1]
            if money >= land_cost + self.config.land_cash_reserve:
                orders.append(["BUY_LAND"])

        hands = farm.get("hands", []) or []
        if hour == 0 and len(hands) < self.config.target_hands_per_day:
            missing = self.config.target_hands_per_day - len(hands)
            orders.extend([["HIRE"] for _ in range(missing)])

        seeds = private.get("seeds", {}) or {}
        if int(seeds.get(self.config.primary_crop, 0)) <= self.config.seed_reorder_level:
            orders.append(
                ["BUY_SEED", self.config.primary_crop, self.config.seed_batch_quantity]
            )
        return orders[: self.config.max_market_orders_per_turn]


def create_native_agent(
    config_path: Path | str = DEFAULT_CONFIG_PATH,
) -> CopilotNativeThreeQPolicy:
    return CopilotNativeThreeQPolicy(load_native_config(config_path))


def agent(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
    """Stateless Kaggle-compatible entry point for smoke use."""

    return create_native_agent()(observation, configuration)


__all__ = [
    "CopilotNativeThreeQPolicy",
    "DEFAULT_CONFIG_PATH",
    "NATIVE_POLICY_DESCRIPTOR",
    "NativeCopilotConfig",
    "POLICY_VERSION",
    "create_native_agent",
    "load_native_config",
    "native_policy_fingerprint",
]
