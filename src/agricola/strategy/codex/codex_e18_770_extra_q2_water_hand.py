"""E18.15 exact-7-7-0 extra Q2 WATER hand.

E18.10 V2 remains authoritative for its farmer and twelve hands.  From D15
through D19 this treatment appends at most one daily HIRE and assigns only the
thirteenth hand to a nearest/sticky Q2 WATER task.  Existing worker commands
are never changed.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _SAFE_PASS,
    _farm,
    _positions,
    _store_unit_actions,
    _tile,
    _unit_actions,
)
from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    CodexE18770WaterBeforeDigGuardV2Agent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_770_EXTRA_Q2_WATER_HAND_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_15_770_EXTRA_Q2_WATER_HAND_V1.json"
)
E18_770_EXTRA_Q2_WATER_HAND_MODEL_SPEC_VERSION = (
    "CODEX-E18.15-770-EXTRA-Q2-WATER-HAND-V1"
)


def load_e18_770_extra_q2_water_hand_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_EXTRA_Q2_WATER_HAND_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_15_770_EXTRA_Q2_WATER_HAND_V1",
        "model_spec_version": E18_770_EXTRA_Q2_WATER_HAND_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.10-770-WATER-BEFORE-DIG-GUARD-V2",
        "causal_family": "ONE_EXTRA_DAILY_Q2_WATER_HAND",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "activation_day": 14,
        "end_day": 18,
        "target_hands": 13,
        "max_extra_hires_per_day": 1,
        "hire_operating_cash_floor": 3000.0,
        "service_quadrant": "Q2",
        "service_opcode": "WATER",
        "exclude_targets": [[4, 5]],
        "water_live_crop_only": True,
        "provider_workers_authoritative": True,
        "market_mutation": "APPEND_ONE_HIRE_ONLY",
        "worker_count_mutation": True,
        "livestock_cap_mutation": False,
        "crop_calendar_mutation": False,
        "public_features_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    return deepcopy(config)


def _distance(left: tuple[int, int], right: tuple[int, int]) -> int:
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def _move(position: tuple[int, int], target: tuple[int, int]) -> list[str]:
    if position[0] < target[0]:
        return ["EAST"]
    if position[0] > target[0]:
        return ["WEST"]
    if position[1] < target[1]:
        return ["SOUTH"]
    if position[1] > target[1]:
        return ["NORTH"]
    return ["PASS"]


class CodexE18770ExtraQ2WaterHandAgent(
    CodexE18770WaterBeforeDigGuardV2Agent
):
    """Add one late daily hand without touching any provider-owned worker."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_15_config = load_e18_770_extra_q2_water_hand_config(
            config_path
        )
        self.candidate_id = str(self.e18_15_config["candidate_id"])
        self.model_spec_version = (
            E18_770_EXTRA_Q2_WATER_HAND_MODEL_SPEC_VERSION
        )
        self.excluded_targets = frozenset(
            tuple(value) for value in self.e18_15_config["exclude_targets"]
        )
        self.extra_hire_requested_days: set[int] = set()
        self.extra_hire_orders = 0
        self.extra_worker_water_actions = 0
        self.extra_worker_move_actions = 0
        self.extra_worker_pass_actions = 0
        self.extra_worker_assignment_switches = 0
        self.provider_worker_overrides = 0
        self.extra_worker_target: tuple[int, int] | None = None
        self.max_observed_hands = 0

    @staticmethod
    def _max_market_orders(configuration: Any) -> int:
        if isinstance(configuration, dict):
            return int(configuration.get("maxMarketOrdersPerTurn", 10) or 10)
        return int(getattr(configuration, "maxMarketOrdersPerTurn", 10) or 10)

    def _append_extra_hire(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        configuration: Any,
    ) -> None:
        day = int(observation.get("day", 0))
        if not (
            int(self.e18_15_config["activation_day"])
            <= day
            <= int(self.e18_15_config["end_day"])
        ):
            return
        farm = _farm(observation)
        hands = len(farm.get("hands", []) or [])
        self.max_observed_hands = max(self.max_observed_hands, hands)
        if (
            day in self.extra_hire_requested_days
            or hands >= int(self.e18_15_config["target_hands"])
            or float(farm.get("money", 0.0) or 0.0)
            < float(self.e18_15_config["hire_operating_cash_floor"])
        ):
            return
        market = action.setdefault("market", [])
        if len(market) >= self._max_market_orders(configuration):
            return
        market.append(["HIRE"])
        self.extra_hire_requested_days.add(day)
        self.extra_hire_orders += 1

    def _water_targets(
        self,
        observation: dict[str, Any],
        positions: list[tuple[int, int]],
        actions: list[list[Any]],
        extra_worker: int,
    ) -> list[tuple[int, int]]:
        farm = _farm(observation)
        reserved = {
            positions[worker]
            for worker, command in enumerate(actions)
            if worker != extra_worker
            and worker < len(positions)
            and command == ["WATER"]
        }
        targets = []
        for y, row in enumerate(farm.get("tiles", []) or []):
            if y < 5:
                continue
            for x, tile in enumerate(row):
                target = (x, y)
                if (
                    x >= 5
                    or target in self.excluded_targets
                    or target in reserved
                    or not isinstance(tile, dict)
                    or tile.get("kind") != "PLANT"
                    or int(tile.get("yield_units", 0) or 0) > 0
                    or bool(tile.get("watered_today", False))
                ):
                    continue
                targets.append(target)
        return targets

    def _dispatch_extra_worker(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        day = int(observation.get("day", 0))
        if not (
            int(self.e18_15_config["activation_day"])
            <= day
            <= int(self.e18_15_config["end_day"])
        ):
            self.extra_worker_target = None
            return
        farm = _farm(observation)
        positions = _positions(farm)
        extra_worker = int(self.e18_15_config["target_hands"])
        if extra_worker >= len(positions):
            return
        actions = _unit_actions(action, len(positions))
        before_provider = deepcopy(actions[:extra_worker])
        targets = self._water_targets(
            observation, positions, actions, extra_worker
        )
        previous = self.extra_worker_target
        if previous not in targets:
            self.extra_worker_target = min(
                targets,
                key=lambda target: (
                    int(
                        not bool(
                            (_tile(farm, target) or {}).get(
                                "consecutive_unwatered", 0
                            )
                        )
                    ),
                    _distance(positions[extra_worker], target),
                    target,
                ),
                default=None,
            )
        if previous != self.extra_worker_target and self.extra_worker_target is not None:
            self.extra_worker_assignment_switches += 1
        target = self.extra_worker_target
        if target is None:
            actions[extra_worker] = ["PASS"]
            self.extra_worker_pass_actions += 1
        elif positions[extra_worker] == target:
            actions[extra_worker] = ["WATER"]
            self.extra_worker_water_actions += 1
            self.extra_worker_target = None
        else:
            actions[extra_worker] = _move(positions[extra_worker], target)
            self.extra_worker_move_actions += 1
        if actions[:extra_worker] != before_provider:
            self.provider_worker_overrides += 1
        _store_unit_actions(action, actions)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        self._append_extra_hire(action, observation, configuration)
        self._dispatch_extra_worker(action, observation)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "ONE_EXTRA_DAILY_Q2_WATER_HAND",
            "extra_hire_orders": self.extra_hire_orders,
            "extra_hire_requested_days": sorted(
                self.extra_hire_requested_days
            ),
            "extra_worker_water_actions": self.extra_worker_water_actions,
            "extra_worker_move_actions": self.extra_worker_move_actions,
            "extra_worker_pass_actions": self.extra_worker_pass_actions,
            "extra_worker_assignment_switches": (
                self.extra_worker_assignment_switches
            ),
            "provider_worker_overrides": self.provider_worker_overrides,
            "max_observed_hands": self.max_observed_hands,
            "worker_count_mutation": True,
            "market_mutation": "APPEND_ONE_HIRE_ONLY",
            "livestock_cap_mutation": False,
            "crop_calendar_mutation": False,
        }


def create_codex_e18_770_extra_q2_water_hand(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770ExtraQ2WaterHandAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_extra_q2_water_hand_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_extra_q2_water_hand_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_extra_q2_water_hand_instance = instance
    policy.codex_e18_770_extra_q2_water_hand_last_error = None
    policy.__name__ = "codex_e18_15_770_extra_q2_water_hand_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_EXTRA_Q2_WATER_HAND_CONFIG_PATH",
    "E18_770_EXTRA_Q2_WATER_HAND_MODEL_SPEC_VERSION",
    "CodexE18770ExtraQ2WaterHandAgent",
    "create_codex_e18_770_extra_q2_water_hand",
    "load_e18_770_extra_q2_water_hand_config",
]
