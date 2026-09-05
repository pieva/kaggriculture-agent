"""E18.17 synchronized late-crop controller for the exact 7-7-0 policy.

E18.16 remains authoritative for topology, livestock, FEED, market and worker
count.  The treatment is restricted to D21-D28 crop lifecycle decisions:
state-based PLANT admission, in-place HARVEST/WATER priority, and at most one
persistent HARVEST mission with explicit reservation and execution ack.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.state import CROPS
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _SAFE_PASS,
    _distance,
    _farm,
    _move,
    _positions,
    _shed_access,
    _store_unit_actions,
    _tile,
    _unit_actions,
)
from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    CodexE18770ExactCapCriticalFeedAgent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_770_SYNCHRONIZED_LATE_CROP_MISSION_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_17_770_SYNCHRONIZED_LATE_CROP_MISSION_V1.json"
)
E18_770_SYNCHRONIZED_LATE_CROP_MISSION_MODEL_SPEC_VERSION = (
    "CODEX-E18.17-770-SYNCHRONIZED-LATE-CROP-MISSION-V1"
)
_MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})


def load_e18_770_synchronized_late_crop_mission_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_SYNCHRONIZED_LATE_CROP_MISSION_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": (
            "CODEX_E18_17_770_SYNCHRONIZED_LATE_CROP_MISSION_V1"
        ),
        "model_spec_version": (
            E18_770_SYNCHRONIZED_LATE_CROP_MISSION_MODEL_SPEC_VERSION
        ),
        "base_policy": "CODEX-E18.16-770-EXACT-CAP-CRITICAL-FEED-V1",
        "causal_family": (
            "SYNCHRONIZED_LATE_CROP_ADMISSION_PRIORITY_AND_MISSION_ACK"
        ),
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "pasture_fill_target": 14,
        "livestock_resource_cap": 14,
        "activation_day": 20,
        "end_day": 27,
        "terminal_harvest_day": 28,
        "plant_payback_deadline_day": 30,
        "harvest_backlog_plant_block_threshold": 999,
        "water_stress_plant_block_threshold": 999,
        "weed_backlog_plant_block_threshold": 999,
        "local_priority_order": [
            "HARVEST_READY",
            "WATER_AT_RISK",
            "DIG_WEED",
            "PLANT",
        ],
        "local_override_opcodes": ["PASS"],
        "max_persistent_harvest_missions": 1,
        "max_harvest_route_distance": 0,
        "mission_workers": "ANY_UNIT_ON_TARGET_PROVIDER_PASS",
        "mission_provider_override_opcodes": ["PASS"],
        "exclude_shed_access": True,
        "preserve_market": True,
        "preserve_worker_count": True,
        "preserve_livestock_policy": True,
        "public_features_only": True,
        "private_inventory_used_for_mission_feasibility_only": False,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    return deepcopy(config)


class CodexE18770SynchronizedLateCropMissionAgent(
    CodexE18770ExactCapCriticalFeedAgent
):
    """Synchronize late crop admission and completion without new capacity."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_17_config = (
            load_e18_770_synchronized_late_crop_mission_config(config_path)
        )
        self.candidate_id = str(self.e18_17_config["candidate_id"])
        self.model_spec_version = (
            E18_770_SYNCHRONIZED_LATE_CROP_MISSION_MODEL_SPEC_VERSION
        )
        self.active_harvest_mission: dict[str, Any] | None = None
        self.pending_harvest_ack: dict[str, Any] | None = None
        self.latest_backlog: dict[str, int] = {}
        self.max_backlog: Counter[str] = Counter()
        self.plant_commands_seen = 0
        self.plant_commands_admitted = 0
        self.plant_commands_blocked = 0
        self.plant_blocks_by_reason: Counter[str] = Counter()
        self.local_harvest_overrides = 0
        self.local_water_overrides = 0
        self.local_dig_overrides = 0
        self.local_priority_batches = 0
        self.harvest_missions_started = 0
        self.provider_harvest_missions_adopted = 0
        self.harvest_missions_completed = 0
        self.harvest_missions_cancelled = 0
        self.harvest_mission_route_commands = 0
        self.harvest_mission_service_commands = 0
        self.harvest_mission_acknowledged = 0
        self.harvest_mission_service_retries = 0
        self.harvest_mission_pauses = 0
        self.provider_move_overrides = 0
        self.provider_non_move_overrides = 0

    def _active_window(self, observation: dict[str, Any]) -> bool:
        day = int(observation.get("day", 0))
        return (
            int(self.e18_17_config["activation_day"])
            <= day
            <= int(self.e18_17_config["end_day"])
        )

    @staticmethod
    def _crop_tiles(
        observation: dict[str, Any],
    ) -> list[tuple[tuple[int, int], dict[str, Any]]]:
        farm = _farm(observation)
        return [
            ((x, y), tile)
            for y, row in enumerate(farm.get("tiles", []) or [])
            for x, tile in enumerate(row)
            if isinstance(tile, dict) and tile.get("kind") == "PLANT"
        ]

    def _backlog(self, observation: dict[str, Any]) -> dict[str, int]:
        farm = _farm(observation)
        harvest_ready = 0
        water_at_risk = 0
        unwatered = 0
        weeds = 0
        for row in farm.get("tiles", []) or []:
            for tile in row:
                if not isinstance(tile, dict):
                    continue
                if tile.get("kind") == "WEED":
                    weeds += 1
                elif tile.get("kind") == "PLANT":
                    if int(tile.get("yield_units", 0) or 0) > 0:
                        harvest_ready += 1
                    if not bool(tile.get("watered_today", False)):
                        unwatered += 1
                        if int(tile.get("consecutive_unwatered", 0) or 0) > 0:
                            water_at_risk += 1
        backlog = {
            "harvest_ready": harvest_ready,
            "water_at_risk": water_at_risk,
            "unwatered": unwatered,
            "weeds": weeds,
        }
        self.latest_backlog = backlog
        for key, value in backlog.items():
            self.max_backlog[key] = max(self.max_backlog[key], value)
        return backlog

    def _observe_pending_ack(self, observation: dict[str, Any]) -> None:
        pending = self.pending_harvest_ack
        if pending is None:
            return
        if int(observation.get("step", 0)) <= int(pending["step"]):
            return
        target = tuple(pending["target"])
        tile = _tile(_farm(observation), target)
        after_yield = (
            int(tile.get("yield_units", 0) or 0)
            if isinstance(tile, dict) and tile.get("kind") == "PLANT"
            else -1
        )
        if after_yield < int(pending["before_yield"]):
            self.harvest_mission_acknowledged += 1
            self.harvest_missions_completed += 1
            self.active_harvest_mission = None
        else:
            self.harvest_mission_service_retries += 1
            self.harvest_missions_cancelled += 1
            self.active_harvest_mission = None
        self.pending_harvest_ack = None

    def _apply_local_priorities(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        if not self._active_window(observation):
            return
        farm = _farm(observation)
        positions = _positions(farm)
        commands = _unit_actions(action, len(positions))
        allowed = set(self.e18_17_config["local_override_opcodes"])
        excluded = (
            set(_shed_access(len(farm.get("tiles", []) or []) or 10))
            if bool(self.e18_17_config["exclude_shed_access"])
            else set()
        )
        claimed: set[tuple[int, int]] = set()
        for worker, command in enumerate(commands):
            if worker >= len(positions) or not command:
                continue
            position = positions[worker]
            tile = _tile(farm, position)
            opcode = str(command[0])
            if (
                opcode == "HARVEST"
                and isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and int(tile.get("yield_units", 0) or 0) > 0
            ) or (
                opcode == "WATER"
                and isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and not bool(tile.get("watered_today", False))
            ) or (
                opcode == "DIG"
                and isinstance(tile, dict)
                and tile.get("kind") == "WEED"
            ):
                claimed.add(position)
        changed = False
        for worker, command in enumerate(commands):
            if worker >= len(positions) or not command:
                continue
            opcode = str(command[0])
            if opcode not in allowed:
                continue
            position = positions[worker]
            if position in excluded:
                continue
            if position in claimed:
                continue
            tile = _tile(farm, position)
            desired: list[Any] | None = None
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                if int(tile.get("yield_units", 0) or 0) > 0:
                    desired = ["HARVEST"]
                elif (
                    not bool(tile.get("watered_today", False))
                    and int(tile.get("consecutive_unwatered", 0) or 0) > 0
                ):
                    desired = ["WATER"]
            elif isinstance(tile, dict) and tile.get("kind") == "WEED":
                desired = ["DIG"]
            if desired is None or command == desired:
                if desired is not None:
                    claimed.add(position)
                continue
            commands[worker] = desired
            claimed.add(position)
            changed = True
            if desired[0] == "HARVEST":
                self.local_harvest_overrides += 1
            elif desired[0] == "WATER":
                self.local_water_overrides += 1
            else:
                self.local_dig_overrides += 1
        if changed:
            self.local_priority_batches += 1
            _store_unit_actions(action, commands)

    def _ready_harvest_targets(
        self,
        observation: dict[str, Any],
    ) -> list[tuple[tuple[int, int], dict[str, Any]]]:
        return [
            (target, tile)
            for target, tile in self._crop_tiles(observation)
            if int(tile.get("yield_units", 0) or 0) > 0
        ]

    def _clear_invalid_mission(self, observation: dict[str, Any]) -> None:
        mission = self.active_harvest_mission
        if mission is None:
            return
        positions = _positions(_farm(observation))
        worker = int(mission["worker"])
        target = tuple(mission["target"])
        tile = _tile(_farm(observation), target)
        target_ready = (
            isinstance(tile, dict)
            and tile.get("kind") == "PLANT"
            and int(tile.get("yield_units", 0) or 0) > 0
        )
        if worker >= len(positions) or not target_ready:
            if self.pending_harvest_ack is None:
                self.harvest_missions_cancelled += 1
            self.active_harvest_mission = None
            self.pending_harvest_ack = None

    def _start_harvest_mission(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        if self.active_harvest_mission is not None:
            return
        farm = _farm(observation)
        positions = _positions(farm)
        commands = _unit_actions(action, len(positions))
        shed = (
            set(_shed_access(len(farm.get("tiles", []) or []) or 10))
            if bool(self.e18_17_config["exclude_shed_access"])
            else set()
        )
        fulfilled = {
            positions[worker]
            for worker, command in enumerate(commands)
            if worker < len(positions)
            and command
            and str(command[0]) == "HARVEST"
        }
        workers = [
            worker
            for worker in range(len(positions))
            if commands[worker] and str(commands[worker][0]) == "PASS"
            and positions[worker] not in shed
        ]
        candidates = [
            (target, tile)
            for target, tile in self._ready_harvest_targets(observation)
            if target not in shed and target not in fulfilled
        ]
        limit = int(self.e18_17_config["max_harvest_route_distance"])
        provider_owned = [
            (
                worker,
                positions[worker],
                str(_tile(farm, positions[worker]).get("crop", "")),
                int(
                    _tile(farm, positions[worker]).get("yield_units", 0)
                    or 0
                ),
            )
            for worker, command in enumerate(commands)
            if worker < len(positions)
            and command
            and str(command[0]) == "HARVEST"
            and positions[worker] not in shed
            and isinstance(_tile(farm, positions[worker]), dict)
            and _tile(farm, positions[worker]).get("kind") == "PLANT"
            and int(
                _tile(farm, positions[worker]).get("yield_units", 0) or 0
            )
            > 0
        ]
        if provider_owned:
            worker, target, crop, before_yield = min(provider_owned)
            self.active_harvest_mission = {
                "worker": worker,
                "target": list(target),
                "crop": crop,
                "created_step": int(observation.get("step", 0)),
                "provider_owned": True,
            }
            self.pending_harvest_ack = {
                "step": int(observation.get("step", 0)),
                "target": list(target),
                "before_yield": before_yield,
            }
            self.harvest_missions_started += 1
            self.provider_harvest_missions_adopted += 1
            return
        ranked = [
            (
                _distance(positions[worker], target),
                -int(tile.get("yield_units", 0) or 0),
                target[1],
                target[0],
                worker,
                target,
                str(tile.get("crop", "")),
            )
            for worker in workers
            for target, tile in candidates
            if _distance(positions[worker], target) <= limit
        ]
        if not ranked:
            return
        _distance_value, _yield_rank, _y, _x, worker, target, crop = min(ranked)
        self.active_harvest_mission = {
            "worker": worker,
            "target": list(target),
            "crop": crop,
            "created_step": int(observation.get("step", 0)),
        }
        self.harvest_missions_started += 1

    def _advance_harvest_mission(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        mission = self.active_harvest_mission
        if mission is None:
            return
        if self.pending_harvest_ack is not None:
            return
        farm = _farm(observation)
        positions = _positions(farm)
        commands = _unit_actions(action, len(positions))
        worker = int(mission["worker"])
        if worker >= len(positions):
            return
        target = tuple(mission["target"])
        position = positions[worker]
        opcode = str(commands[worker][0]) if commands[worker] else "PASS"
        if opcode != "PASS":
            self.harvest_mission_pauses += 1
            return
        original = list(commands[worker])
        if position == target:
            tile = _tile(farm, target)
            if not (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and int(tile.get("yield_units", 0) or 0) > 0
            ):
                return
            commands[worker] = ["HARVEST"]
            self.pending_harvest_ack = {
                "step": int(observation.get("step", 0)),
                "target": list(target),
                "before_yield": int(tile.get("yield_units", 0) or 0),
            }
            self.harvest_mission_service_commands += 1
        else:
            commands[worker] = _move(position, target)
            self.harvest_mission_route_commands += 1
        if original != commands[worker]:
            if opcode in _MOVES:
                self.provider_move_overrides += 1
            elif opcode != "PASS":
                self.provider_non_move_overrides += 1
        _store_unit_actions(action, commands)

    def _apply_plant_admission(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        backlog: dict[str, int],
    ) -> None:
        if not self._active_window(observation):
            return
        day = int(observation.get("day", 0))
        positions = _positions(_farm(observation))
        commands = _unit_actions(action, len(positions))
        changed = False
        for worker, command in enumerate(commands):
            if not command or str(command[0]) != "PLANT" or len(command) < 2:
                continue
            self.plant_commands_seen += 1
            crop = str(command[1])
            first_yield = int(CROPS.get(crop, {}).get("first_yield_day", 99))
            reasons = []
            if day + first_yield >= int(
                self.e18_17_config["plant_payback_deadline_day"]
            ):
                reasons.append("NO_PAYBACK_WINDOW")
            if backlog["harvest_ready"] >= int(
                self.e18_17_config[
                    "harvest_backlog_plant_block_threshold"
                ]
            ):
                reasons.append("HARVEST_BACKLOG")
            if backlog["water_at_risk"] >= int(
                self.e18_17_config[
                    "water_stress_plant_block_threshold"
                ]
            ):
                reasons.append("WATER_STRESS")
            if backlog["weeds"] >= int(
                self.e18_17_config["weed_backlog_plant_block_threshold"]
            ):
                reasons.append("WEED_BACKLOG")
            if not reasons:
                self.plant_commands_admitted += 1
                continue
            commands[worker] = ["PASS"]
            self.plant_commands_blocked += 1
            for reason in reasons:
                self.plant_blocks_by_reason[reason] += 1
            changed = True
        if changed:
            _store_unit_actions(action, commands)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        self._observe_pending_ack(observation)
        action = super().__call__(observation, configuration)
        if not self._active_window(observation):
            if self.active_harvest_mission is not None:
                self.harvest_missions_cancelled += 1
                self.active_harvest_mission = None
                self.pending_harvest_ack = None
            return action
        backlog = self._backlog(observation)
        self._clear_invalid_mission(observation)
        self._start_harvest_mission(action, observation)
        self._advance_harvest_mission(action, observation)
        self._apply_local_priorities(action, observation)
        self._apply_plant_admission(action, observation, backlog)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": (
                "SYNCHRONIZED_LATE_CROP_ADMISSION_PRIORITY_AND_MISSION_ACK"
            ),
            "latest_backlog": dict(self.latest_backlog),
            "max_backlog": dict(self.max_backlog),
            "plant_commands_seen": self.plant_commands_seen,
            "plant_commands_admitted": self.plant_commands_admitted,
            "plant_commands_blocked": self.plant_commands_blocked,
            "plant_blocks_by_reason": dict(self.plant_blocks_by_reason),
            "local_harvest_overrides": self.local_harvest_overrides,
            "local_water_overrides": self.local_water_overrides,
            "local_dig_overrides": self.local_dig_overrides,
            "local_priority_batches": self.local_priority_batches,
            "harvest_missions_started": self.harvest_missions_started,
            "provider_harvest_missions_adopted": (
                self.provider_harvest_missions_adopted
            ),
            "harvest_missions_completed": self.harvest_missions_completed,
            "harvest_missions_cancelled": self.harvest_missions_cancelled,
            "harvest_mission_route_commands": (
                self.harvest_mission_route_commands
            ),
            "harvest_mission_service_commands": (
                self.harvest_mission_service_commands
            ),
            "harvest_mission_acknowledged": (
                self.harvest_mission_acknowledged
            ),
            "harvest_mission_service_retries": (
                self.harvest_mission_service_retries
            ),
            "harvest_mission_pauses": self.harvest_mission_pauses,
            "provider_move_overrides": self.provider_move_overrides,
            "provider_non_move_overrides": self.provider_non_move_overrides,
            "active_harvest_mission": deepcopy(self.active_harvest_mission),
            "market_mutation": False,
            "worker_count_mutation": False,
            "livestock_cap_mutation": True,
            "crop_lifecycle_mutation": True,
        }


def create_codex_e18_770_synchronized_late_crop_mission(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770SynchronizedLateCropMissionAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_synchronized_late_crop_mission_last_error = (
                None
            )
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_synchronized_late_crop_mission_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_synchronized_late_crop_mission_instance = instance
    policy.codex_e18_770_synchronized_late_crop_mission_last_error = None
    policy.__name__ = "codex_e18_17_770_synchronized_late_crop_mission_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_SYNCHRONIZED_LATE_CROP_MISSION_CONFIG_PATH",
    "E18_770_SYNCHRONIZED_LATE_CROP_MISSION_MODEL_SPEC_VERSION",
    "CodexE18770SynchronizedLateCropMissionAgent",
    "create_codex_e18_770_synchronized_late_crop_mission",
    "load_e18_770_synchronized_late_crop_mission_config",
]
