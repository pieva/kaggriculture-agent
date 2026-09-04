"""Copilot E18 economic recovery V1.

This is a minimal, isolated repair that addresses the identified early-game
failure: when the workforce is empty the policy must hire and then enter a real
productive loop before any regime logic is considered.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "COPILOT-E18.4-ECONOMIC-RECOVERY-V1"
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "docs"
    / "model_specs"
    / "copilot"
    / "e18"
    / "configs"
    / "COPILOT_E18_4_ECONOMIC_RECOVERY_V1.json"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


@dataclass(frozen=True)
class CopilotE18EconomicRecoveryV1Config:
    candidate_id: str
    model_spec_version: str
    family: str
    preferred_crop: str
    hires_per_day: int
    turns_per_day: int
    episode_steps: int

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "CopilotE18EconomicRecoveryV1Config":
        config = cls(
            candidate_id=str(payload["candidate_id"]),
            model_spec_version=str(payload["model_spec_version"]),
            family=str(payload.get("family", "ADAPTIVE_CROP")),
            preferred_crop=str(payload.get("preferred_crop", "WHEAT")).upper(),
            hires_per_day=int(payload.get("hires_per_day", 1)),
            turns_per_day=int(payload.get("turns_per_day", 24)),
            episode_steps=int(payload.get("episode_steps", 720)),
        )
        if config.candidate_id != "COPILOT_E18_4_ECONOMIC_RECOVERY_V1":
            raise ValueError("unexpected candidate_id")
        if config.model_spec_version != POLICY_VERSION:
            raise ValueError("unexpected model_spec_version")
        if config.hires_per_day <= 0:
            raise ValueError("hires_per_day must be positive")
        return config


def load_copilot_e18_economic_recovery_v1_config(
    path: Path | str | None = None,
) -> CopilotE18EconomicRecoveryV1Config:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return CopilotE18EconomicRecoveryV1Config.from_mapping(payload)


def _manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class CopilotE18EconomicRecoveryV1Policy:
    def __init__(
        self,
        config: CopilotE18EconomicRecoveryV1Config | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        self.config = config or load_copilot_e18_economic_recovery_v1_config()
        self.run_context = deepcopy(run_context or {})
        self.model_spec_version = self.config.model_spec_version
        self.technical_errors = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.telemetry = {"hire_day": None, "last_regime": "EARLY_GROWTH"}

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
                    if age >= 2 and tile.get("yield_units", 0) > 0:
                        tasks.append((0, (x, y), "HARVEST", crop))
                    elif not tile.get("watered_today", False):
                        tasks.append((1, (x, y), "WATER", crop))
                elif kind == "WEED":
                    tasks.append((3, (x, y), "DIG", "DIG"))
                elif kind == "EMPTY":
                    tasks.append((5, (x, y), "PLANT", self.config.preferred_crop))
        tasks.sort(key=lambda item: (item[0], item[1][1], item[1][0]))
        return tasks

    def _unit_action(self, from_pos: tuple[int, int], target: tuple[int, int], verb: str, crop: str) -> list[str]:
        if from_pos == target:
            if verb == "PLANT":
                return ["PLANT", crop]
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
            hands = farm.get("hands", []) or []
            if snapshot.clock.hour == 0 and len(hands) == 0 and money >= 1:
                market.append(["HIRE"])
                self.telemetry["hire_day"] = snapshot.clock.day

            tasks = self._all_tasks(farm, snapshot.clock.day)
            farmer_pos = tuple(farm.get("farmer", [0, 0]))
            hand_positions = [tuple(position) for position in hands]
            farmer_action = ["PASS"]
            hand_actions: list[list[str]] = []
            unit_positions = [farmer_pos]
            unit_positions.extend(hand_positions)

            if tasks:
                used: set[tuple[int, int]] = set()
                if farmer_pos not in used:
                    best_task = min(tasks, key=lambda item: _manhattan(farmer_pos, item[1]))
                    task_target = best_task[1]
                    task_verb = best_task[2]
                    task_crop = best_task[3]
                    farmer_action = self._unit_action(farmer_pos, task_target, task_verb, task_crop)
                    used.add(task_target)

                for hand_pos in hand_positions:
                    if len(hand_actions) >= max(0, len(hands)):
                        break
                    remaining_tasks = [task for task in tasks if task[1] not in used]
                    if not remaining_tasks:
                        break
                    best_task = min(remaining_tasks, key=lambda item: _manhattan(hand_pos, item[1]))
                    task_target = best_task[1]
                    task_verb = best_task[2]
                    task_crop = best_task[3]
                    hand_actions.append(self._unit_action(hand_pos, task_target, task_verb, task_crop))
                    used.add(task_target)

            return {"farmer": farmer_action, "hands": hand_actions, "market": market}
        except Exception as exc:  # noqa: BLE001 - safe fallback path
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
            "last_regime": self.telemetry.get("last_regime"),
            "technical_errors": self.technical_errors,
            "fallback_count": self.fallback_count,
            "last_exception": self.last_exception,
        }


def create_copilot_e18_economic_recovery_v1(
    *,
    config_path: Path | str | None = None,
    run_context: dict[str, Any] | None = None,
) -> CopilotE18EconomicRecoveryV1Policy:
    config = load_copilot_e18_economic_recovery_v1_config(config_path)
    return CopilotE18EconomicRecoveryV1Policy(config=config, run_context=run_context)


def create_agent(
    *,
    config_path: Path | str | None = None,
    run_context: dict[str, Any] | None = None,
) -> CopilotE18EconomicRecoveryV1Policy:
    return create_copilot_e18_economic_recovery_v1(config_path=config_path, run_context=run_context)


__all__ = [
    "CopilotE18EconomicRecoveryV1Config",
    "CopilotE18EconomicRecoveryV1Policy",
    "DEFAULT_CONFIG_PATH",
    "POLICY_VERSION",
    "create_agent",
    "create_copilot_e18_economic_recovery_v1",
    "load_copilot_e18_economic_recovery_v1_config",
]
