"""Copilot E18 economic recovery V2.

This variant keeps the repair hypothesis narrow and explicit:
1) force early hiring when the workforce is empty or under target;
2) prioritize harvest/water/plant tasks on managed tiles;
3) keep the action loop simple enough that productive work can be observed in
   the engine before any regime or opponent-reactive logic is introduced.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "COPILOT-E18.5-ECONOMIC-RECOVERY-V2"
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "docs"
    / "model_specs"
    / "copilot"
    / "e18"
    / "configs"
    / "COPILOT_E18_5_ECONOMIC_RECOVERY_V2.json"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


@dataclass(frozen=True)
class CopilotE18EconomicRecoveryV2Config:
    candidate_id: str
    model_spec_version: str
    family: str
    preferred_crop: str
    hire_target: int
    early_hire_days: int
    turns_per_day: int
    episode_steps: int

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "CopilotE18EconomicRecoveryV2Config":
        config = cls(
            candidate_id=str(payload["candidate_id"]),
            model_spec_version=str(payload["model_spec_version"]),
            family=str(payload.get("family", "ADAPTIVE_CROP")),
            preferred_crop=str(payload.get("preferred_crop", "WHEAT")).upper(),
            hire_target=int(payload.get("hire_target", 2)),
            early_hire_days=int(payload.get("early_hire_days", 4)),
            turns_per_day=int(payload.get("turns_per_day", 24)),
            episode_steps=int(payload.get("episode_steps", 720)),
        )
        if config.candidate_id != "COPILOT_E18_5_ECONOMIC_RECOVERY_V2":
            raise ValueError("unexpected candidate_id")
        if config.model_spec_version != POLICY_VERSION:
            raise ValueError("unexpected model_spec_version")
        if config.hire_target <= 0:
            raise ValueError("hire_target must be positive")
        return config


def load_copilot_e18_economic_recovery_v2_config(
    path: Path | str | None = None,
) -> CopilotE18EconomicRecoveryV2Config:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return CopilotE18EconomicRecoveryV2Config.from_mapping(payload)


def _manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class CopilotE18EconomicRecoveryV2Policy:
    def __init__(self, config=None, *, run_context: dict[str, Any] | None = None) -> None:
        self.config = config or load_copilot_e18_economic_recovery_v2_config()
        self.run_context = deepcopy(run_context or {})
        self.model_spec_version = self.config.model_spec_version
        self.technical_errors = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.telemetry = {"hire_day": None, "last_hypothesis": "hire-first-economic-loop"}

    def _crop_score(self, crop: str) -> int:
        crop_name = str(crop).upper()
        score = {"WHEAT": 4, "CARROT": 5, "POTATO": 5, "ONION": 5, "BEET": 6}.get(crop_name, 3)
        return score

    def _all_tasks(self, farm: dict[str, Any], day: int) -> list[tuple[int, tuple[int, int], str, str]]:
        tasks: list[tuple[int, tuple[int, int], str, str]] = []
        tiles = farm.get("tiles", []) or []
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict):
                    continue
                kind = str(tile.get("kind", "")).upper()
                if kind == "PLANT":
                    crop = str(tile.get("crop", self.config.preferred_crop)).upper()
                    planted_day = int(tile.get("planted_day", day))
                    age = max(0, day - planted_day)
                    maturity = max(1, int(tile.get("maturity_days", 2)))
                    if age >= maturity and tile.get("yield_units", 0) > 0:
                        tasks.append((0, (x, y), "HARVEST", crop))
                    elif not tile.get("watered_today", False):
                        tasks.append((10, (x, y), "WATER", crop))
                elif kind == "WEED":
                    tasks.append((30, (x, y), "DIG", "DIG"))
                elif kind == "EMPTY":
                    tasks.append((40, (x, y), "PLANT", self.config.preferred_crop))
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
            market: list[list[str]] = []
            money = float(farm.get("money", 0.0) or 0.0)
            hands = list(farm.get("hands", []) or [])
            day = int(snapshot.clock.day)
            hour = int(snapshot.clock.hour)
            desired_hands = self.config.hire_target if day < self.config.early_hire_days else max(1, self.config.hire_target - 1)
            if hour == 0 and len(hands) < desired_hands and money >= 1.0:
                market.append(["HIRE"])
                self.telemetry["hire_day"] = day

            tasks = self._all_tasks(farm, day)
            farmer_pos = tuple(farm.get("farmer", [0, 0]))
            hand_positions = [tuple(position) for position in hands]
            farmer_action = ["PASS"]
            hand_actions: list[list[str]] = []
            used: set[tuple[int, int]] = set()

            if tasks:
                chosen_farmer = min(tasks, key=lambda item: _manhattan(farmer_pos, item[1]))
                if _manhattan(farmer_pos, chosen_farmer[1]) <= 3:
                    farmer_action = self._unit_action(farmer_pos, chosen_farmer[1], chosen_farmer[2], chosen_farmer[3])
                    used.add(chosen_farmer[1])

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


def create_copilot_e18_economic_recovery_v2(*, config_path: str | Path | None = None, run_context: dict[str, Any] | None = None):
    config = load_copilot_e18_economic_recovery_v2_config(config_path)
    policy = CopilotE18EconomicRecoveryV2Policy(config=config, run_context=run_context)
    return policy


__all__ = [
    "CopilotE18EconomicRecoveryV2Config",
    "CopilotE18EconomicRecoveryV2Policy",
    "DEFAULT_CONFIG_PATH",
    "POLICY_VERSION",
    "create_copilot_e18_economic_recovery_v2",
    "load_copilot_e18_economic_recovery_v2_config",
]
