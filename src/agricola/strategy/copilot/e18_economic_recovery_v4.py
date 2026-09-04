"""Copilot E18 economic recovery V4.

This revision is intentionally grounded in the project's already-working
multi-tile ROI strategy families. The improvement hypothesis is narrow and
operational: before adding opponent-reactive logic, Copilot must follow a
verified harvest/plant/water loop with explicit seed buying and selling.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "COPILOT-E18.7-ECONOMIC-RECOVERY-V4"
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "docs"
    / "model_specs"
    / "copilot"
    / "e18"
    / "configs"
    / "COPILOT_E18_7_ECONOMIC_RECOVERY_V4.json"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
CROP_TABLE = {
    "WHEAT": {"seed": 10, "max_yield_day": 4},
    "CARROT": {"seed": 20, "max_yield_day": 3},
    "POTATO": {"seed": 25, "max_yield_day": 4},
    "ONION": {"seed": 30, "max_yield_day": 4},
    "BEET": {"seed": 35, "max_yield_day": 5},
}
MANAGED_TILES = (
    (4, 4), (4, 3), (3, 4), (3, 3),
    (4, 2), (3, 2), (2, 4), (2, 3), (2, 2),
)


@dataclass(frozen=True)
class CopilotE18EconomicRecoveryV4Config:
    candidate_id: str
    model_spec_version: str
    family: str
    preferred_crop: str
    hire_target: int
    early_hire_days: int
    turns_per_day: int
    episode_steps: int
    seed_buffer: int

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "CopilotE18EconomicRecoveryV4Config":
        config = cls(
            candidate_id=str(payload["candidate_id"]),
            model_spec_version=str(payload["model_spec_version"]),
            family=str(payload.get("family", "ADAPTIVE_CROP")),
            preferred_crop=str(payload.get("preferred_crop", "WHEAT")).upper(),
            hire_target=int(payload.get("hire_target", 2)),
            early_hire_days=int(payload.get("early_hire_days", 4)),
            turns_per_day=int(payload.get("turns_per_day", 24)),
            episode_steps=int(payload.get("episode_steps", 720)),
            seed_buffer=int(payload.get("seed_buffer", 2)),
        )
        if config.candidate_id != "COPILOT_E18_7_ECONOMIC_RECOVERY_V4":
            raise ValueError("unexpected candidate_id")
        if config.model_spec_version != POLICY_VERSION:
            raise ValueError("unexpected model_spec_version")
        return config


def load_copilot_e18_economic_recovery_v4_config(path: Path | str | None = None) -> CopilotE18EconomicRecoveryV4Config:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return CopilotE18EconomicRecoveryV4Config.from_mapping(payload)


def _manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _crop_roi(crop_name: str, sell_price: float) -> float:
    crop = CROP_TABLE.get(str(crop_name).upper(), {"seed": 10, "max_yield_day": 4})
    seed_cost = float(crop["seed"])
    return (sell_price * 2.0 - seed_cost) / max(1.0, float(crop["max_yield_day"]))


class CopilotE18EconomicRecoveryV4Policy:
    def __init__(self, config=None, *, run_context: dict[str, Any] | None = None) -> None:
        self.config = config or load_copilot_e18_economic_recovery_v4_config()
        self.run_context = deepcopy(run_context or {})
        self.model_spec_version = self.config.model_spec_version
        self.technical_errors = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.telemetry = {"hire_day": None, "last_hypothesis": "roi-verified-throughput"}

    def _inventory_count(self, farm: dict[str, Any], observation: dict[str, Any], crop: str) -> int:
        inventory = farm.get("inventory") if isinstance(farm.get("inventory"), dict) else None
        if inventory is None:
            inventory = observation.get("private", {}).get("inventory", {})
        if isinstance(inventory, dict):
            return int(inventory.get(str(crop).upper(), 0) or 0)
        return 0

    def _select_crop(self, observation: dict[str, Any], farm: dict[str, Any]) -> str:
        market = observation.get("market", {}) or {}
        sell_prices = market.get("prices", {}) if isinstance(market, dict) else {}
        if isinstance(sell_prices, dict):
            sell_price = max([float(price) for price in sell_prices.values()] or [12.0])
        else:
            sell_price = 12.0
        best_crop = self.config.preferred_crop
        best_score = -10**9
        for crop in CROP_TABLE:
            score = _crop_roi(crop, sell_price)
            if score > best_score:
                best_score = score
                best_crop = crop
        return best_crop

    def _tasks(self, farm: dict[str, Any], day: int, crop: str) -> list[tuple[int, tuple[int, int], str, str]]:
        tasks: list[tuple[int, tuple[int, int], str, str]] = []
        tiles = farm.get("tiles", []) or []
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict):
                    continue
                kind = str(tile.get("kind", "")).upper()
                if kind == "PLANT":
                    plant_crop = str(tile.get("crop", crop)).upper()
                    planted_day = int(tile.get("planted_day", day))
                    age = max(0, day - planted_day)
                    maturity = max(1, int(tile.get("maturity_days", 2)))
                    if age >= maturity and tile.get("yield_units", 0) > 0:
                        tasks.append((0, (x, y), "HARVEST", plant_crop))
                    elif not tile.get("watered_today", False):
                        tasks.append((10, (x, y), "WATER", plant_crop))
                elif kind == "WEED":
                    tasks.append((30, (x, y), "DIG", "DIG"))
                elif kind == "EMPTY":
                    tasks.append((40, (x, y), "PLANT", crop))
        tasks.sort(key=lambda item: (item[0], item[1][1], item[1][0]))
        return tasks

    def _unit_action(self, from_pos: tuple[int, int], target: tuple[int, int], verb: str, crop: str) -> list[str]:
        if from_pos == target:
            if verb == "PLANT":
                return ["PLANT", crop]
            if verb == "DIG":
                return ["DIG"]
            return [verb]
        if from_pos[0] < target[0]:
            return ["EAST"]
        if from_pos[0] > target[0]:
            return ["WEST"]
        if from_pos[1] < target[1]:
            return ["SOUTH"]
        if from_pos[1] > target[1]:
            return ["NORTH"]
        return ["PASS"]

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
            market: list[list[str | int]] = []
            money = float(farm.get("money", 0.0) or 0.0)
            hands = list(farm.get("hands", []) or [])
            day = int(snapshot.clock.day)
            hour = int(snapshot.clock.hour)
            crop = self._select_crop(observation, farm)
            target_hands = self.config.hire_target if day < self.config.early_hire_days else max(1, self.config.hire_target - 1)
            if hour == 0 and len(hands) < target_hands and money >= 1.0:
                market.append(["HIRE"])
                self.telemetry["hire_day"] = day

            seed_count = self._inventory_count(farm, observation, crop)
            empty_tiles = 0
            tiles = farm.get("tiles", []) or []
            for row in tiles:
                for tile in row:
                    if isinstance(tile, dict) and str(tile.get("kind", "")).upper() == "EMPTY":
                        empty_tiles += 1
            if empty_tiles > 0 and money >= 1:
                needed = max(0, empty_tiles + self.config.seed_buffer - seed_count)
                if needed > 0:
                    market.append(["BUY_SEED", crop, max(1, needed)])

            for product in ["WHEAT", "CARROT", "POTATO", "ONION", "BEET"]:
                product_count = self._inventory_count(farm, observation, product)
                if product_count > 0:
                    market.append(["SELL", product, product_count])

            tasks = self._tasks(farm, day, crop)
            farmer_pos = tuple(farm.get("farmer", [0, 0]))
            hand_positions = [tuple(position) for position in hands]
            farmer_action = ["PASS"]
            hand_actions: list[list[str]] = []
            used: set[tuple[int, int]] = set()

            if tasks:
                farmer_task = min(tasks, key=lambda item: _manhattan(farmer_pos, item[1]))
                if _manhattan(farmer_pos, farmer_task[1]) <= 3:
                    farmer_action = self._unit_action(farmer_pos, farmer_task[1], farmer_task[2], farmer_task[3])
                    used.add(farmer_task[1])
                for hand_pos in hand_positions:
                    remaining = [task for task in tasks if task[1] not in used]
                    if not remaining:
                        break
                    candidate = min(remaining, key=lambda item: _manhattan(hand_pos, item[1]))
                    hand_actions.append(self._unit_action(hand_pos, candidate[1], candidate[2], candidate[3]))
                    used.add(candidate[1])

            return {"farmer": farmer_action, "hands": hand_actions, "market": market}
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


def create_copilot_e18_economic_recovery_v4(*, config_path: str | Path | None = None, run_context: dict[str, Any] | None = None):
    config = load_copilot_e18_economic_recovery_v4_config(config_path)
    policy = CopilotE18EconomicRecoveryV4Policy(config=config, run_context=run_context)
    return policy


__all__ = [
    "CopilotE18EconomicRecoveryV4Config",
    "CopilotE18EconomicRecoveryV4Policy",
    "DEFAULT_CONFIG_PATH",
    "POLICY_VERSION",
    "create_copilot_e18_economic_recovery_v4",
    "load_copilot_e18_economic_recovery_v4_config",
]
