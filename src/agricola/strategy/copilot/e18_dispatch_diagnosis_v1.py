"""Copilot E18 dispatch-diagnosis V1.

This version is intentionally diagnostic before corrective: it isolates the
root cause of the zero-hands failure by ensuring the initial hire gate fires
before any regime logic is considered.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "COPILOT-E18.3-DISPATCH-DIAGNOSIS-V1"
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "docs"
    / "model_specs"
    / "copilot"
    / "e18"
    / "configs"
    / "COPILOT_E18_3_DISPATCH_DIAGNOSIS_V1.json"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


@dataclass(frozen=True)
class CopilotE18DispatchDiagnosisConfig:
    candidate_id: str
    schema_version: str
    model_spec_version: str
    family: str
    primary_crop: str
    hire_cash_floor: int
    initial_hire_units: int
    max_market_orders_per_turn: int
    turns_per_day: int
    episode_steps: int

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> CopilotE18DispatchDiagnosisConfig:
        config = cls(
            candidate_id=str(payload["candidate_id"]),
            schema_version=str(payload["schema_version"]),
            model_spec_version=str(payload["model_spec_version"]),
            family=str(payload.get("family", "ADAPTIVE_CROP")),
            primary_crop=str(payload.get("primary_crop", "WHEAT")).upper(),
            hire_cash_floor=int(payload.get("hire_cash_floor", 400)),
            initial_hire_units=int(payload.get("initial_hire_units", 1)),
            max_market_orders_per_turn=int(payload.get("max_market_orders_per_turn", 2)),
            turns_per_day=int(payload.get("turns_per_day", 24)),
            episode_steps=int(payload.get("episode_steps", 720)),
        )
        if config.candidate_id != "COPILOT_E18_3_DISPATCH_DIAGNOSIS_V1":
            raise ValueError("unexpected candidate_id")
        if config.model_spec_version != POLICY_VERSION:
            raise ValueError("unexpected model_spec_version")
        if config.hire_cash_floor <= 0:
            raise ValueError("hire_cash_floor must be positive")
        return config


def load_copilot_e18_dispatch_diagnosis_v1_config(
    path: Path | str | None = None,
) -> CopilotE18DispatchDiagnosisConfig:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return CopilotE18DispatchDiagnosisConfig.from_mapping(payload)


def _tile_priority(tile: Any, day: int, crop: str) -> tuple[int, str, str | None]:
    if tile is None:
        return 2, "PLANT", crop
    if not isinstance(tile, dict):
        return 9, "PASS", None
    kind = str(tile.get("kind", "")).upper()
    if kind == "WEED":
        return 1, "DIG", "DIG"
    if kind != "PLANT":
        return 9, "PASS", None
    crop_name = str(tile.get("crop", crop)).upper()
    planted_day = int(tile.get("planted_day", day))
    age = max(0, day - planted_day)
    yield_units = int(tile.get("yield_units", 0) or 0)
    watered_today = bool(tile.get("watered_today", False))
    if yield_units > 0 and age >= 2:
        return 0, "HARVEST", crop_name
    if not watered_today and age <= 3:
        return 3, "WATER", "WATER"
    if age > 18 and yield_units == 0:
        return 1, "DIG", "DIG"
    return 4, "PLANT", crop_name


class CopilotE18DispatchDiagnosisV1Policy:
    """Zero-hands diagnosis and dispatch correction without regime logic."""

    def __init__(
        self,
        config: CopilotE18DispatchDiagnosisConfig | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        self.config = config or load_copilot_e18_dispatch_diagnosis_v1_config()
        self.run_context = deepcopy(run_context or {})
        self.candidate_id = self.config.candidate_id
        self.model_spec_version = self.config.model_spec_version
        self.technical_errors = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.diagnostic_reason = (
            "root_cause=missing_hire_dispatch_when_hands_empty; "
            "regime_logic_is_deferred_until_gate_0_passes"
        )
        self.last_hire_day: int | None = None

    def _hire_market_order(self, farm: dict[str, Any]) -> list[list[str]]:
        money = float(farm.get("money", 0.0) or 0.0)
        hands = farm.get("hands", []) or []
        if len(hands) > 0:
            return []
        if money < self.config.hire_cash_floor:
            return []
        return [["HIRE"]]

    def _task_scan(self, farm: dict[str, Any], day: int) -> list[tuple[int, tuple[int, int], str, str]]:
        tasks: list[tuple[int, tuple[int, int], str, str]] = []
        tiles = farm.get("tiles", []) or []
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                priority, verb, crop = _tile_priority(tile, day, self.config.primary_crop)
                if verb == "PASS":
                    continue
                tasks.append((priority, (x, y), verb, crop or self.config.primary_crop))
        tasks.sort(key=lambda item: (item[0], item[1][1], item[1][0]))
        return tasks

    def _move_toward(self, source: tuple[int, int], target: tuple[int, int]) -> list[str]:
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

    def _worker_allocation(
        self,
        farm: dict[str, Any],
        tasks: list[tuple[int, tuple[int, int], str, str]],
    ) -> tuple[list[str], list[list[str]]]:
        positions = [tuple(farm.get("farmer", [4, 4]))]
        positions.extend(tuple(position) for position in farm.get("hands", []) or [])
        farmer_action = ["PASS"]
        hand_actions: list[list[str]] = []
        if not tasks:
            return farmer_action, hand_actions
        for _, target, verb, crop in tasks:
            for index, position in enumerate(positions):
                if index >= len(positions):
                    break
                if index == 0:
                    if position == target:
                        farmer_action = [verb]
                        if verb == "PLANT":
                            farmer_action = ["PLANT", crop]
                        if verb == "HARVEST":
                            farmer_action = ["HARVEST"]
                        if verb == "WATER":
                            farmer_action = ["WATER"]
                        if verb == "DIG":
                            farmer_action = ["DIG"]
                        break
                    farmer_action = self._move_toward(position, target)
                    break
                if position == target:
                    hand_actions.append([verb] if verb != "PLANT" else ["PLANT", crop])
                    break
                hand_actions.append(self._move_toward(position, target))
                break
            if farmer_action != ["PASS"] or hand_actions:
                break
        return farmer_action, hand_actions

    def telemetry_snapshot(self) -> dict[str, Any]:
        return {
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "family": "ADAPTIVE_CROP",
            "diagnosis": self.diagnostic_reason,
            "last_hire_day": self.last_hire_day,
            "technical_errors": self.technical_errors,
            "fallbacks": self.fallback_count,
            "last_exception": self.last_exception,
        }

    def __call__(self, observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        try:
            snapshot = CodexObservationAdapter.parse(
                observation,
                configuration,
                fallback_turns_per_day=self.config.turns_per_day,
                fallback_episode_steps=self.config.episode_steps,
            )
            farm = snapshot.farm
            market = self._hire_market_order(farm)
            if market:
                self.last_hire_day = snapshot.clock.day
            tasks = self._task_scan(farm, snapshot.clock.day)
            farmer_action, hand_actions = self._worker_allocation(farm, tasks)
            action = {"farmer": farmer_action, "hands": hand_actions, "market": market}
            if not market and not farm.get("hands"):
                action["market"] = [["HIRE"]]
                self.last_hire_day = snapshot.clock.day
            return action
        except Exception as exc:  # noqa: BLE001 - explicit safe fallback path
            self.technical_errors += 1
            self.fallback_count += 1
            self.last_exception = f"{type(exc).__name__}: {exc}"
            return deepcopy(SAFE_PASS)


def create_copilot_e18_dispatch_diagnosis_v1(
    *,
    config_path: Path | str | None = None,
    run_context: dict[str, Any] | None = None,
) -> CopilotE18DispatchDiagnosisV1Policy:
    config = load_copilot_e18_dispatch_diagnosis_v1_config(config_path)
    return CopilotE18DispatchDiagnosisV1Policy(config=config, run_context=run_context)


def create_agent(
    *,
    config_path: Path | str | None = None,
    run_context: dict[str, Any] | None = None,
) -> CopilotE18DispatchDiagnosisV1Policy:
    return create_copilot_e18_dispatch_diagnosis_v1(config_path=config_path, run_context=run_context)


__all__ = [
    "DEFAULT_CONFIG_PATH",
    "POLICY_VERSION",
    "CopilotE18DispatchDiagnosisConfig",
    "CopilotE18DispatchDiagnosisV1Policy",
    "create_agent",
    "create_copilot_e18_dispatch_diagnosis_v1",
    "load_copilot_e18_dispatch_diagnosis_v1_config",
]
