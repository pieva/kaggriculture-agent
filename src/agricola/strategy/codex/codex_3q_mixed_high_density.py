"""Codex V9.0 standalone-source 3Q high-density routine controller."""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_v9_routine_data import ROUTINE_ACTIONS, ROUTINE_SHA256

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_V9_CONFIG_PATH = (
    REPO_ROOT
    / "docs"
    / "model_specs"
    / "codex"
    / "configs"
    / "CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json"
)
V9_MODEL_SPEC_VERSION = "CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}

Q2_SHEEP_PASTURES: tuple[tuple[int, int], ...] = (
    (3, 5),
    (4, 5),
    (3, 6),
    (4, 6),
    (4, 7),
)
Q2_CROP_POSITIONS: tuple[tuple[int, int], ...] = tuple(
    (x, y)
    for y in range(5, 10)
    for x in range(5)
    if (x, y) not in set(Q2_SHEEP_PASTURES)
)


def load_v9_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load and validate the immutable V9 execution envelope."""

    config_path = Path(path) if path is not None else DEFAULT_V9_CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("candidate_id") != "CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY":
        raise ValueError("unexpected V9 candidate_id")
    if config.get("model_spec_version") != V9_MODEL_SPEC_VERSION:
        raise ValueError("unexpected V9 model_spec_version")
    if int(config.get("quadrants_owned", 0)) != 3:
        raise ValueError("V9 requires three quadrants")
    if int(config.get("workforce_total", 0)) != 13:
        raise ValueError("V9 requires farmer plus twelve hands")
    return deepcopy(config)


class CodexThreeQDistilledRoutineAgent:
    """Execute the frozen 719-step routine and collect passive telemetry."""

    PRODUCTIVE = frozenset(
        {
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
    )
    MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})

    def __init__(self, *, run_context: dict[str, Any] | None = None) -> None:
        context = deepcopy(run_context or {})
        self.candidate_id = "CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY"
        self.model_spec_version = V9_MODEL_SPEC_VERSION
        self.run_id = str(context.get("run_id", "codex-v9-distilled-routine"))
        self.episode_id = str(context.get("episode_id", "codex-v9-episode"))
        self.seed = context.get("seed")
        self.player_position = context.get("player_position")
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.final_money = 0.0
        self.q1_activation_day: int | None = None
        self.q2_activation_day: int | None = None
        self.q2_full_module_day: int | None = None
        self.q2_first_output_day: int | None = None
        self.animal_escapes = 0
        self.action_counts: Counter[str] = Counter()
        self.production_units: Counter[str] = Counter()
        self.sale_requests: Counter[str] = Counter()
        self.max_hands = 0
        self.max_quadrants = 1
        self.max_active_animals = 0
        self.max_active_crops = 0
        self._last_day: int | None = None
        self._last_animal_count = 0

    @staticmethod
    def _farm(observation: dict[str, Any]) -> dict[str, Any]:
        player = int(observation.get("player", 0))
        farms = observation.get("farms", []) or []
        return farms[player] if 0 <= player < len(farms) else {}

    @staticmethod
    def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
        x, y = position
        tiles = farm.get("tiles", []) or []
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return None

    def _observe_state(self, observation: dict[str, Any]) -> dict[str, Any]:
        farm = self._farm(observation)
        day = int(observation.get("day", 0))
        quadrants = len(farm.get("unlocked_quadrants", []) or [])
        hands = len(farm.get("hands", []) or [])
        animals = 0
        crops = 0
        q2_animals = 0
        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict):
                    continue
                if tile.get("animal"):
                    animals += 1
                    if x < 5 and y >= 5:
                        q2_animals += 1
                if tile.get("kind") == "PLANT":
                    crops += 1

        if self._last_day is not None and day > self._last_day:
            self.animal_escapes += max(0, self._last_animal_count - animals)
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
        if q2_animals >= 5 and self.q2_full_module_day is None:
            self.q2_full_module_day = day
        return farm

    def _attribute_action(
        self,
        observation: dict[str, Any],
        farm: dict[str, Any],
        action: dict[str, Any],
    ) -> None:
        positions = [
            tuple(farm.get("farmer", [4, 4])),
            *(tuple(position) for position in farm.get("hands", []) or []),
        ]
        unit_actions = [
            action.get("farmer", ["PASS"]),
            *(action.get("hands", []) or []),
        ]
        for worker_id, unit_action in enumerate(unit_actions):
            if not unit_action:
                continue
            opcode = str(unit_action[0])
            self.action_counts[opcode] += 1
            if opcode != "HARVEST" or worker_id >= len(positions):
                if opcode == "FEED":
                    self.production_units["WHEAT_CONSUMED"] += 1
                elif opcode == "COLLECT_FERTILIZER":
                    self.production_units["FERTILIZER_COLLECTED"] += 1
                continue
            tile = self._tile(farm, positions[worker_id])
            if not isinstance(tile, dict):
                continue
            units = int(tile.get("yield_units", 0))
            item = tile.get("crop")
            animal = tile.get("animal")
            if animal == "COW":
                item = "MILK"
            elif animal == "SHEEP":
                item = "WOOL"
            elif animal == "GOOSE":
                item = "EGG"
            if item and units > 0:
                self.production_units[str(item)] += units
                x, y = positions[worker_id]
                if x < 5 and y >= 5 and self.q2_first_output_day is None:
                    self.q2_first_output_day = int(observation.get("day", 0))

        for order in action.get("market", []) or []:
            if len(order) >= 3 and order[0] == "SELL":
                self.sale_requests[str(order[1])] += int(order[2])

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        del configuration
        step = int(observation.get("step", 0))
        farm = self._observe_state(observation)
        action = (
            deepcopy(ROUTINE_ACTIONS[step])
            if 0 <= step < len(ROUTINE_ACTIONS)
            else deepcopy(_SAFE_PASS)
        )
        if step == 195:
            for order in action.get("market", []) or []:
                if order[:2] == ["BUY_PRODUCT", "WHEAT"]:
                    order[2] = max(4, int(order[2]))
                    break
            action["market"] = [
                order
                for order in action.get("market", []) or []
                if order[:2] != ["BUY_ANIMAL", "COW"]
            ]
        self._attribute_action(observation, farm, action)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        productive = sum(self.action_counts[opcode] for opcode in self.PRODUCTIVE)
        moves = sum(self.action_counts[opcode] for opcode in self.MOVES)
        return {
            "agent_version": self.model_spec_version,
            "routine_sha256": ROUTINE_SHA256,
            "FINAL_MONEY": self.final_money,
            "Q1_activation_day": self.q1_activation_day,
            "Q1_full_module_day": None,
            "Q1_first_output_day": None,
            "Q2_activation_day": self.q2_activation_day,
            "Q2_full_module_day": self.q2_full_module_day,
            "Q2_first_output_day": self.q2_first_output_day,
            "Q2_activation_records": [],
            "MILK_units": int(self.production_units["MILK"]),
            "WOOL_units": int(self.production_units["WOOL"]),
            "MELON_units": int(self.production_units["MELON"]),
            "STRAWBERRY_units": int(self.production_units["STRAWBERRY"]),
            "WHEAT_sold": int(self.sale_requests["WHEAT"]),
            "WHEAT_consumed": int(self.production_units["WHEAT_CONSUMED"]),
            "fertilizer_collected": int(
                self.production_units["FERTILIZER_COLLECTED"]
            ),
            "productive_actions": productive,
            "MOVE_actions": moves,
            "PASS_actions": int(self.action_counts["PASS"]),
            "MOVE_PER_PRODUCTIVE_ACTION": (
                moves / productive if productive else None
            ),
            "ANIMAL_ESCAPE": self.animal_escapes,
            "max_hands": self.max_hands,
            "max_quadrants": self.max_quadrants,
            "max_active_animals": self.max_active_animals,
            "max_active_crops": self.max_active_crops,
            "sale_requests": dict(self.sale_requests),
            "action_requests_by_opcode": dict(self.action_counts),
        }


def create_v9_agent(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    """Create the fail-closed Kaggle-compatible V9 policy."""

    load_v9_config(config_path)
    instance = CodexThreeQDistilledRoutineAgent(run_context=run_context)

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_v9_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_v9_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_v9_instance = instance
    policy.codex_v9_last_error = None
    policy.__name__ = "codex_v9_3q_mixed_high_density_policy"
    return policy


__all__ = [
    "CodexThreeQDistilledRoutineAgent",
    "Q2_CROP_POSITIONS",
    "Q2_SHEEP_PASTURES",
    "V9_MODEL_SPEC_VERSION",
    "create_v9_agent",
    "load_v9_config",
]
