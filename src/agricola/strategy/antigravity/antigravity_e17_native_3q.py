"""Antigravity E17.0 native three-quadrant crop-first baseline.

The policy is intentionally simple and deterministic. It owns three quadrants,
avoids animals entirely during E17.0 baseline construction, and uses only
agent-local planning logic so the provenance and routine fingerprint are
independent from Codex/Copilot.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.e17_ledger import canonical_sha256
from agricola.core.state import CROPS


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONFIG_PATH = (
    REPO_ROOT
    / "experiments"
    / "e17"
    / "configs"
    / "antigravity"
    / "ANTIGRAVITY_E17_0_NATIVE_3Q_BASELINE_CONFIG.json"
)
E17_NATIVE_MODEL_SPEC_VERSION = "ANTIGRAVITY-E17.0-NATIVE-3Q-CROP-FIRST-V1"
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
MOVE_OPCODES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})
PRODUCTIVE_OPCODES = frozenset({"DIG", "PLANT", "WATER", "HARVEST"})


def load_e17_native_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("candidate_id") != "ANTIGRAVITY_E17_0_NATIVE_3Q_BASELINE":
        raise ValueError("unexpected E17 native candidate_id")
    if config.get("model_spec_version") != E17_NATIVE_MODEL_SPEC_VERSION:
        raise ValueError("unexpected E17 native model_spec_version")
    if int(config.get("quadrants_owned_target", 0)) != 3:
        raise ValueError("E17 native baseline requires three quadrants")
    return deepcopy(config)


def _farm(observation: dict[str, Any]) -> dict[str, Any]:
    player = int(observation.get("player", 0))
    farms = observation.get("farms", []) or []
    return farms[player] if 0 <= player < len(farms) and isinstance(farms[player], dict) else {}


def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
    x, y = position
    tiles = farm.get("tiles", []) or []
    if 0 <= y < len(tiles) and isinstance(tiles[y], list) and 0 <= x < len(tiles[y]):
        return tiles[y][x]
    return "LOCKED"


def _quadrant(position: tuple[int, int]) -> str:
    x, y = position
    if x < 5 and y < 5:
        return "Q0"
    if x >= 5 and y < 5:
        return "Q1"
    if x < 5 and y >= 5:
        return "Q2"
    return "Q3"


def _manhattan_step(origin: tuple[int, int], target: tuple[int, int]) -> list[str]:
    ox, oy = origin
    tx, ty = target
    if ox < tx:
        return ["EAST"]
    if ox > tx:
        return ["WEST"]
    if oy < ty:
        return ["SOUTH"]
    if oy > ty:
        return ["NORTH"]
    return ["PASS"]


class AntigravityE17NativeThreeQPolicy:
    """Deterministic 3Q baseline with native crop planning."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
    ) -> None:
        context = deepcopy(run_context or {})
        self.config = deepcopy(config or load_e17_native_config())
        self.candidate_id = "ANTIGRAVITY_E17_0_NATIVE_3Q_BASELINE"
        self.model_spec_version = E17_NATIVE_MODEL_SPEC_VERSION
        self.run_id = str(context.get("run_id", "antigravity-e17-native"))
        self.episode_id = str(context.get("episode_id", "antigravity-e17-native-episode"))
        self.seed = context.get("seed")
        self.player_position = context.get("player_position")
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.final_money = 0.0
        self.q1_activation_day: int | None = None
        self.q2_activation_day: int | None = None
        self.max_hands = 0
        self.max_quadrants = 1
        self.max_active_animals = 0
        self.max_active_crops = 0
        self.action_counts: Counter[str] = Counter()
        self.sale_requests: Counter[str] = Counter()
        self.production_units: Counter[str] = Counter()
        self._last_day: int | None = None
        self._last_animal_count = 0
        self.routine_hash = canonical_sha256(
            {
                "unlock_days": {
                    "q1": self.config["q1_unlock_day"],
                    "q2": self.config["q2_unlock_day"],
                },
                "quadrant_crops": self.config["quadrant_crops"],
                "target_tiles": self.config["target_tiles"],
                "sell_threshold": self.config["sell_threshold"],
            }
        )

    def _observe_state(self, observation: dict[str, Any]) -> dict[str, Any]:
        farm = _farm(observation)
        day = int(observation.get("day", 0))
        quadrants = len(farm.get("unlocked_quadrants", []) or [])
        hands = len(farm.get("hands", []) or [])
        animals = 0
        crops = 0
        for row in farm.get("tiles", []) or []:
            if not isinstance(row, list):
                continue
            for item in row:
                if isinstance(item, dict):
                    if item.get("animal"):
                        animals += 1
                    if item.get("kind") == "PLANT":
                        crops += 1
        if self._last_day is not None and day > self._last_day:
            escaped = max(0, self._last_animal_count - animals)
            self.production_units["DERIVED_ESCAPE"] += escaped
        self._last_day = day
        self._last_animal_count = animals
        self.final_money = float(farm.get("money", 0.0))
        self.max_hands = max(self.max_hands, hands)
        self.max_quadrants = max(self.max_quadrants, quadrants)
        self.max_active_animals = max(self.max_active_animals, animals)
        self.max_active_crops = max(self.max_active_crops, crops)
        if quadrants >= 2 and self.q1_activation_day is None:
            self.q1_activation_day = day
        if quadrants >= 3 and self.q2_activation_day is None:
            self.q2_activation_day = day
        return farm

    def _assigned_crop(self, position: tuple[int, int]) -> str:
        quadrant = _quadrant(position)
        return str(self.config["quadrant_crops"].get(quadrant, self.config["default_crop"]))

    def _harvestable(self, tile: dict[str, Any], day: int) -> bool:
        if int(tile.get("yield_units", 0)) > 0:
            return True
        crop = str(tile.get("crop", self.config["default_crop"]))
        planted_day = int(tile.get("planted_day", day))
        max_yield_day = int(CROPS.get(crop, CROPS[self.config["default_crop"]])["max_yield_day"])
        return day - planted_day >= max_yield_day

    def _owned_quadrants(self, farm: dict[str, Any]) -> set[str]:
        unlocked = farm.get("unlocked_quadrants", []) or []
        names: set[str] = set()
        for entry in unlocked:
            value = str(entry).upper()
            if value in {"NW", "Q0"}:
                names.add("Q0")
            elif value in {"NE", "Q1"}:
                names.add("Q1")
            elif value in {"SW", "Q2"}:
                names.add("Q2")
            elif value in {"SE", "Q3"}:
                names.add("Q3")
        if not names:
            names.add("Q0")
        return names

    def _market_order(self, observation: dict[str, Any], farm: dict[str, Any]) -> list[list[Any]]:
        day = int(observation.get("day", 0))
        money = float(farm.get("money", 0.0))
        owned = self._owned_quadrants(farm)
        shed = (observation.get("private", {}) or {}).get("shed", {}) or {}
        seeds = (observation.get("private", {}) or {}).get("seeds", {}) or {}

        for crop in self.config["sell_priority"]:
            quantity = int(shed.get(crop, 0))
            threshold = int(self.config["sell_threshold"].get(crop, 1))
            if quantity >= threshold or (day >= 27 and quantity > 0):
                self.sale_requests[crop] += quantity
                return [["SELL", crop, quantity]]

        if "Q1" not in owned and day >= int(self.config["q1_unlock_day"]) and money >= float(self.config["q1_min_cash"]):
            return [["BUY_LAND"]]
        if "Q2" not in owned and day >= int(self.config["q2_unlock_day"]) and money >= float(self.config["q2_min_cash"]):
            return [["BUY_LAND"]]

        needed_crop = self.config["seed_buy_priority"][min(len(owned) - 1, len(self.config["seed_buy_priority"]) - 1)]
        desired = int(self.config["seed_target_stock"].get(needed_crop, 1))
        current = int(seeds.get(needed_crop, 0))
        cost = float(CROPS[needed_crop]["seed"])
        if current < desired and money >= cost:
            return [["BUY_SEED", needed_crop, desired - current]]

        return []

    def _target_positions(self, farm: dict[str, Any]) -> list[tuple[int, int]]:
        owned = self._owned_quadrants(farm)
        positions: list[tuple[int, int]] = []
        for quadrant in ("Q0", "Q1", "Q2"):
            if quadrant in owned:
                positions.extend(tuple(pos) for pos in self.config["target_tiles"][quadrant])
        return positions

    def _farmer_action(self, observation: dict[str, Any], farm: dict[str, Any]) -> list[str]:
        day = int(observation.get("day", 0))
        farmer_position = tuple(farm.get("farmer", [4, 4]))
        seeds = (observation.get("private", {}) or {}).get("seeds", {}) or {}
        current_tile = _tile(farm, farmer_position)
        crop_here = self._assigned_crop(farmer_position)

        if isinstance(current_tile, dict) and current_tile.get("kind") == "WEED":
            return ["DIG"]
        if isinstance(current_tile, dict) and current_tile.get("kind") == "PLANT":
            if self._harvestable(current_tile, day):
                return ["HARVEST"]
            if not current_tile.get("watered_today", False):
                return ["WATER"]
        if current_tile is None and int(seeds.get(crop_here, 0)) > 0 and farmer_position in self._target_positions(farm):
            return ["PLANT", crop_here]

        harvest_targets: list[tuple[int, int]] = []
        water_targets: list[tuple[int, int]] = []
        dig_targets: list[tuple[int, int]] = []
        plant_targets: list[tuple[int, int]] = []

        for position in self._target_positions(farm):
            tile = _tile(farm, position)
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                dig_targets.append(position)
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                if self._harvestable(tile, day):
                    harvest_targets.append(position)
                elif not tile.get("watered_today", False):
                    water_targets.append(position)
            elif tile is None and int(seeds.get(self._assigned_crop(position), 0)) > 0:
                plant_targets.append(position)

        for targets, command in (
            (dig_targets, "DIG"),
            (harvest_targets, "HARVEST"),
            (water_targets, "WATER"),
            (plant_targets, "PLANT"),
        ):
            if not targets:
                continue
            target = min(
                targets,
                key=lambda pos: (
                    abs(pos[0] - farmer_position[0]) + abs(pos[1] - farmer_position[1]),
                    pos[1],
                    pos[0],
                ),
            )
            if target == farmer_position:
                if command == "PLANT":
                    return ["PLANT", self._assigned_crop(target)]
                return [command]
            return _manhattan_step(farmer_position, target)
        return ["PASS"]

    def _attribute_action(self, action: dict[str, Any]) -> None:
        opcode = str((action.get("farmer") or ["PASS"])[0])
        self.action_counts[opcode] += 1

    def __call__(self, observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        del configuration
        farm = self._observe_state(observation)
        action = {
            "farmer": self._farmer_action(observation, farm),
            "hands": [],
            "market": self._market_order(observation, farm),
        }
        self._attribute_action(action)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        productive = sum(self.action_counts[opcode] for opcode in PRODUCTIVE_OPCODES)
        moves = sum(self.action_counts[opcode] for opcode in MOVE_OPCODES)
        return {
            "agent_version": self.model_spec_version,
            "routine_sha256": self.routine_hash,
            "FINAL_MONEY": self.final_money,
            "Q1_activation_day": self.q1_activation_day,
            "Q2_activation_day": self.q2_activation_day,
            "productive_actions": productive,
            "MOVE_actions": moves,
            "PASS_actions": int(self.action_counts["PASS"]),
            "MOVE_PER_PRODUCTIVE_ACTION": moves / productive if productive else None,
            "ANIMAL_ESCAPE": int(self.production_units["DERIVED_ESCAPE"]),
            "max_hands": self.max_hands,
            "max_quadrants": self.max_quadrants,
            "max_active_animals": self.max_active_animals,
            "max_active_crops": self.max_active_crops,
            "sale_requests": dict(self.sale_requests),
            "action_requests_by_opcode": dict(self.action_counts),
        }


def create_e17_native_agent(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    config = load_e17_native_config(config_path)
    instance = AntigravityE17NativeThreeQPolicy(run_context=run_context, config=config)

    def policy(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.antigravity_e17_native_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.antigravity_e17_native_last_error = instance.last_exception
            return deepcopy(SAFE_PASS)

    policy.antigravity_e17_native_instance = instance
    policy.antigravity_e17_native_last_error = None
    policy.__name__ = "antigravity_e17_native_3q_policy"
    return policy


__all__ = [
    "AntigravityE17NativeThreeQPolicy",
    "E17_NATIVE_MODEL_SPEC_VERSION",
    "create_e17_native_agent",
    "load_e17_native_config",
]
