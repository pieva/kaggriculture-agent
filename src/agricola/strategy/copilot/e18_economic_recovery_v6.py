from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "COPILOT-E18.10-ECONOMIC-RECOVERY-V6"
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "docs"
    / "model_specs"
    / "copilot"
    / "e18"
    / "configs"
    / "COPILOT_E18_10_ECONOMIC_RECOVERY_V6.json"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}

CROP_TABLE = {
    "WHEAT": {"seed": 10, "first_yield_day": 2, "max_yield_day": 4},
    "CARROT": {"seed": 20, "first_yield_day": 2, "max_yield_day": 3},
    "TOMATO": {"seed": 50, "first_yield_day": 8, "max_yield_day": 8},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10},
    "MELON": {"seed": 80, "first_yield_day": 10, "max_yield_day": 12},
}

ANIMAL_TABLE = {
    "COW": {"cost": 200},
    "SHEEP": {"cost": 100},
    "GOOSE": {"cost": 80},
}


@dataclass(frozen=True)
class CopilotE18EconomicRecoveryV6Config:
    candidate_id: str
    model_spec_version: str
    family: str
    preferred_crop: str
    hire_target: int
    early_hire_days: int
    seed_batch: int
    turns_per_day: int
    episode_steps: int
    cash_buffer: int
    livestock_day: int
    livestock_target: int

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "CopilotE18EconomicRecoveryV6Config":
        config = cls(
            candidate_id=str(payload["candidate_id"]),
            model_spec_version=str(payload["model_spec_version"]),
            family=str(payload.get("family", "BALANCED_LIVESTOCK")),
            preferred_crop=str(payload.get("preferred_crop", "CARROT")).upper(),
            hire_target=int(payload.get("hire_target", 3)),
            early_hire_days=int(payload.get("early_hire_days", 4)),
            seed_batch=int(payload.get("seed_batch", 3)),
            turns_per_day=int(payload.get("turns_per_day", 24)),
            episode_steps=int(payload.get("episode_steps", 720)),
            cash_buffer=int(payload.get("cash_buffer", 400)),
            livestock_day=int(payload.get("livestock_day", 8)),
            livestock_target=int(payload.get("livestock_target", 2)),
        )
        if config.candidate_id != "COPILOT_E18_10_ECONOMIC_RECOVERY_V6":
            raise ValueError("unexpected candidate_id")
        if config.model_spec_version != POLICY_VERSION:
            raise ValueError("unexpected model_spec_version")
        return config


def load_copilot_e18_economic_recovery_v6_config(path: Path | str | None = None) -> CopilotE18EconomicRecoveryV6Config:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return CopilotE18EconomicRecoveryV6Config.from_mapping(payload)


def _manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _task_action(from_pos: tuple[int, int], target: tuple[int, int], verb: str, crop: str) -> list[str]:
    if from_pos == target:
        if verb in {"HARVEST", "WATER", "DIG", "BUILD_PASTURE"}:
            return [verb]
        return ["PLANT", crop]
    dx = target[0] - from_pos[0]
    dy = target[1] - from_pos[1]
    if abs(dx) >= abs(dy):
        return ["EAST" if dx > 0 else "WEST"]
    return ["SOUTH" if dy > 0 else "NORTH"]


class CopilotE18EconomicRecoveryV6Policy:
    def __init__(self, config=None, *, run_context: dict[str, Any] | None = None) -> None:
        self.config = config or load_copilot_e18_economic_recovery_v6_config()
        self.run_context = deepcopy(run_context or {})
        self.model_spec_version = self.config.model_spec_version
        self.technical_errors = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.telemetry = {
            "hire_day": None,
            "last_hypothesis": "fishbone-economic-recovery-with-livestock-gate",
        }

    def _best_crop(self, observation: dict[str, Any]) -> str:
        market = observation.get("market", {}) or {}
        prices = market.get("prices", {}) if isinstance(market, dict) else {}
        if not isinstance(prices, dict) or not prices:
            return self.config.preferred_crop
        best_crop = self.config.preferred_crop
        best_score = float("-inf")
        for crop, spec in CROP_TABLE.items():
            price = float(prices.get(crop, 0.0) or 0.0)
            first_day = float(spec.get("first_yield_day", 2))
            max_yield = float(spec.get("max_yield_day", 3))
            seed_cost = float(spec.get("seed", 20))
            score = (price * 2.0 - seed_cost) / max(1.0, first_day) + max_yield * 0.15
            if score > best_score:
                best_score = score
                best_crop = crop
        return best_crop

    def _count_animals(self, farm: dict[str, Any]) -> dict[str, int]:
        counts = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
        for row in farm.get("tiles", []) or []:
            for tile in row:
                if not isinstance(tile, dict):
                    continue
                if str(tile.get("kind", "")).upper() == "PASTURE":
                    animal = str(tile.get("animal", "")).upper()
                    if animal in counts:
                        counts[animal] += 1
        return counts

    def _empty_pastures(self, farm: dict[str, Any]) -> int:
        count = 0
        for row in farm.get("tiles", []) or []:
            for tile in row:
                if not isinstance(tile, dict):
                    continue
                if str(tile.get("kind", "")).upper() == "PASTURE" and not tile.get("animal"):
                    count += 1
        return count

    def __call__(self, observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        try:
            snapshot = CodexObservationAdapter.parse(
                observation,
                configuration,
                fallback_turns_per_day=self.config.turns_per_day,
                fallback_episode_steps=self.config.episode_steps,
            )
            farm = snapshot.farm
            private = snapshot.private
            market = snapshot.market
            prices = market.get("prices", {}) if isinstance(market, dict) else {}
            action = {"farmer": ["PASS"], "hands": [], "market": []}
            money = float(farm.get("money", 0.0) or 0.0)
            hour = int(snapshot.clock.hour)
            day = int(snapshot.clock.day)
            crop = self._best_crop(observation)
            farmer_pos = tuple(farm.get("farmer", [0, 0]))
            hands = [tuple(pos) for pos in farm.get("hands", []) or []]

            shed = private.get("shed", {}) if isinstance(private, dict) else {}
            if isinstance(shed, dict):
                for item, qty in sorted(shed.items()):
                    if qty > 0 and item in CROP_TABLE and item in prices:
                        action["market"].append(["SELL", item, int(qty)])

            if hour == 0 and len(hands) < self.config.hire_target and day < self.config.early_hire_days and money >= 1:
                action["market"].append(["HIRE"])
                self.telemetry["hire_day"] = day

            seeds = private.get("seeds", {}) if isinstance(private, dict) else {}
            seed_count = int((seeds or {}).get(crop, 0) or 0)
            seed_cost = int(CROP_TABLE.get(crop, {"seed": 20})["seed"])
            if seed_count < self.config.seed_batch and money >= max(seed_cost, self.config.cash_buffer * 0.2):
                action["market"].append(["BUY_SEED", crop, max(1, self.config.seed_batch - seed_count)])

            animals = self._count_animals(farm)
            empty_pastures = self._empty_pastures(farm)
            if (
                day >= self.config.livestock_day
                and empty_pastures > 0
                and money >= self.config.cash_buffer
                and sum(animals.values()) < self.config.livestock_target
            ):
                best_animal = "COW" if animals.get("COW", 0) == 0 else "SHEEP"
                if best_animal in ANIMAL_TABLE:
                    action["market"].append(["BUY_ANIMAL", best_animal, 1])

            tasks: list[tuple[int, tuple[int, int], str, str]] = []
            for y, row in enumerate(farm.get("tiles", []) or []):
                for x, tile in enumerate(row):
                    if isinstance(tile, dict):
                        kind = str(tile.get("kind", "")).upper()
                        if kind == "WEED":
                            tasks.append((0, (x, y), "DIG", "DIG"))
                        elif kind == "PLANT":
                            plant_crop = str(tile.get("crop", crop)).upper()
                            planted_day = int(tile.get("planted_day", day))
                            age = max(0, day - planted_day)
                            if tile.get("yield_units", 0) > 0 and age >= CROP_TABLE.get(plant_crop, {"first_yield_day": 2})["first_yield_day"]:
                                tasks.append((1, (x, y), "HARVEST", plant_crop))
                            elif not tile.get("watered_today", False):
                                tasks.append((2, (x, y), "WATER", plant_crop))
                    elif tile is None and seed_count > 0:
                        tasks.append((5, (x, y), "PLANT", crop))

            if tasks:
                selected = min(tasks, key=lambda item: (item[0], _manhattan(farmer_pos, item[1])))
                action["farmer"] = _task_action(farmer_pos, selected[1], selected[2], selected[3])

            used: set[tuple[int, int]] = set()
            if tasks:
                used.add(min(tasks, key=lambda item: _manhattan(farmer_pos, item[1]))[1])
            for hand_pos in hands:
                best_task = None
                best_score = None
                for task in tasks:
                    if task[1] in used:
                        continue
                    score = _manhattan(hand_pos, task[1])
                    if best_score is None or score < best_score:
                        best_task = task
                        best_score = score
                if best_task is not None:
                    used.add(best_task[1])
                    action["hands"].append(_task_action(hand_pos, best_task[1], best_task[2], best_task[3]))
            return action
        except Exception as exc:  # noqa: BLE001
            self.technical_errors += 1
            self.fallback_count += 1
            self.last_exception = f"{type(exc).__name__}: {exc}"
            return deepcopy(SAFE_PASS)

    def telemetry_snapshot(self) -> dict[str, Any]:
        return {
            "agent_version": self.model_spec_version,
            "candidate_id": self.config.candidate_id,
            "family": self.config.family,
            "hire_day": self.telemetry.get("hire_day"),
            "last_hypothesis": self.telemetry.get("last_hypothesis"),
            "technical_errors": self.technical_errors,
            "fallback_count": self.fallback_count,
            "last_exception": self.last_exception,
        }


def create_copilot_e18_economic_recovery_v6(*, config_path: str | Path | None = None, run_context: dict[str, Any] | None = None):
    config = load_copilot_e18_economic_recovery_v6_config(config_path)
    policy = CopilotE18EconomicRecoveryV6Policy(config=config, run_context=run_context)
    return policy


__all__ = [
    "CopilotE18EconomicRecoveryV6Config",
    "CopilotE18EconomicRecoveryV6Policy",
    "DEFAULT_CONFIG_PATH",
    "POLICY_VERSION",
    "create_copilot_e18_economic_recovery_v6",
    "load_copilot_e18_economic_recovery_v6_config",
]
