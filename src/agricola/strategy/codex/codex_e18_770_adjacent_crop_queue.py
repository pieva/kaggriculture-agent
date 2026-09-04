"""E18.8 exact-7-7-0 adjacent crop queue for provider-idle workers.

E18.6 remains the complete provider. This overlay changes only provider PASS:
it may execute an in-place crop service or take one same-quadrant step toward
an adjacent HARVEST/WATER task. A one-step mission survives only while the
provider keeps the worker idle; every provider non-PASS remains authoritative.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.state import CROPS
from agricola.strategy.codex.codex_e17_reactive_service_routing_core import (
    _distance,
    _move,
)
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _SAFE_PASS,
    _farm,
    _inventories,
    _positions,
    _quadrant,
    _store_unit_actions,
    _tile,
    _unit_actions,
)
from agricola.strategy.codex.codex_e18_concentrated_770_throughput import (
    CodexE18Concentrated770ThroughputAgent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_770_ADJACENT_CROP_QUEUE_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_8_770_ADJACENT_CROP_QUEUE_V1.json"
)
E18_770_ADJACENT_CROP_QUEUE_MODEL_SPEC_VERSION = (
    "CODEX-E18.8-770-ADJACENT-CROP-QUEUE-V1"
)
_MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})


def load_e18_770_adjacent_crop_queue_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_ADJACENT_CROP_QUEUE_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_8_770_ADJACENT_CROP_QUEUE_V1",
        "model_spec_version": E18_770_ADJACENT_CROP_QUEUE_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.6-CONCENTRATED-770-THROUGHPUT-V1",
        "causal_family": "PASS_TO_SAME_QUADRANT_ADJACENT_CROP_QUEUE",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "local_service_opcodes": ["HARVEST", "WATER"],
        "local_service_priority": ["HARVEST", "WATER"],
        "max_assignment_distance": 1,
        "max_workers_per_quadrant_per_turn": 1,
        "sticky_until_service_or_provider_reclaim": True,
        "require_empty_inventory_for_harvest": True,
        "allow_plant": False,
        "allow_dig": False,
        "allow_cross_quadrant_routing": False,
        "provider_non_pass_authoritative": True,
        "market_mutation": False,
        "calendar_mutation": False,
        "worker_count_mutation": False,
        "livestock_cap_mutation": False,
        "public_features_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    if int(config.get("local_service_activation_day", 0)) < 1:
        raise ValueError("local service activation must be a positive day")
    if int(config.get("water_terminal_passthrough_day", -1)) > 28:
        raise ValueError("water service must preserve the terminal day")
    return deepcopy(config)


class CodexE18770AdjacentCropQueueAgent(
    CodexE18Concentrated770ThroughputAgent
):
    """Route provider-idle workers to an adjacent same-quadrant crop task."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_8_config = load_e18_770_adjacent_crop_queue_config(config_path)
        self.candidate_id = str(self.e18_8_config["candidate_id"])
        self.model_spec_version = E18_770_ADJACENT_CROP_QUEUE_MODEL_SPEC_VERSION
        self.adjacent_missions: dict[int, tuple[tuple[int, int], str]] = {}
        self.adjacent_queue_commands: Counter[str] = Counter()
        self.adjacent_queue_assignments = 0
        self.adjacent_queue_completions = 0
        self.adjacent_queue_cancellations = 0
        self.adjacent_queue_batches = 0
        self.adjacent_queue_candidates = 0
        self.adjacent_inventory_blocks = 0
        self.non_pass_overrides = 0
        self.cross_quadrant_routes = 0
        self.max_observed_assignment_distance = 0

    def _crop_tasks(
        self, observation: dict[str, Any]
    ) -> list[tuple[int, tuple[int, int], str]]:
        farm = _farm(observation)
        day = int(observation.get("day", 0))
        priority = {
            opcode: rank
            for rank, opcode in enumerate(
                self.e18_8_config["local_service_priority"]
            )
        }
        tasks: list[tuple[int, tuple[int, int], str]] = []
        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                    continue
                crop = str(tile.get("crop", ""))
                mature = day - int(tile.get("planted_day", day)) >= int(
                    CROPS.get(crop, {}).get("first_yield_day", 10**6)
                )
                if mature and int(tile.get("yield_units", 0) or 0) > 0:
                    tasks.append((priority["HARVEST"], (x, y), "HARVEST"))
                elif (
                    day < int(
                        self.e18_8_config["water_terminal_passthrough_day"]
                    )
                    and not bool(tile.get("watered_today", False))
                ):
                    tasks.append((priority["WATER"], (x, y), "WATER"))
        return tasks

    def _task_valid(
        self,
        observation: dict[str, Any],
        target: tuple[int, int],
        opcode: str,
        inventory: dict[str, Any],
    ) -> bool:
        tile = _tile(_farm(observation), target)
        if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
            return False
        day = int(observation.get("day", 0))
        if opcode == "HARVEST":
            crop = str(tile.get("crop", ""))
            mature = day - int(tile.get("planted_day", day)) >= int(
                CROPS.get(crop, {}).get("first_yield_day", 10**6)
            )
            empty = not any(int(value or 0) > 0 for value in inventory.values())
            if not empty:
                self.adjacent_inventory_blocks += 1
            return mature and int(tile.get("yield_units", 0) or 0) > 0 and empty
        return (
            opcode == "WATER"
            and day
            < int(self.e18_8_config["water_terminal_passthrough_day"])
            and not bool(tile.get("watered_today", False))
        )

    def _apply_adjacent_queue(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        if int(observation.get("day", 0)) < int(
            self.e18_8_config["local_service_activation_day"]
        ):
            return
        positions = _positions(_farm(observation))
        actions = _unit_actions(action, len(positions))
        inventories = _inventories(
            observation.get("private", {}) or {}, len(positions)
        )
        changed = False
        reserved: set[tuple[int, int]] = set()
        quadrant_counts: Counter[str] = Counter()

        for worker, mission in list(self.adjacent_missions.items()):
            if worker >= len(actions) or actions[worker] != ["PASS"]:
                self.adjacent_queue_cancellations += 1
                del self.adjacent_missions[worker]
                continue
            target, opcode = mission
            if not self._task_valid(
                observation, target, opcode, inventories[worker]
            ):
                self.adjacent_queue_cancellations += 1
                del self.adjacent_missions[worker]
                continue
            if _quadrant(positions[worker]) != _quadrant(target):
                self.cross_quadrant_routes += 1
                del self.adjacent_missions[worker]
                continue
            if positions[worker] == target:
                actions[worker] = [opcode]
                self.adjacent_queue_commands[opcode] += 1
                self.adjacent_queue_completions += 1
                quadrant_counts[_quadrant(target)] += 1
                reserved.add(target)
                del self.adjacent_missions[worker]
                changed = True
            else:
                actions[worker] = _move(positions[worker], target)
                self.adjacent_queue_commands[str(actions[worker][0])] += 1
                quadrant_counts[_quadrant(target)] += 1
                reserved.add(target)
                changed = True

        claimed = {
            positions[worker]
            for worker, command in enumerate(actions)
            if command and command[0] not in {"PASS", *_MOVES}
        }
        tasks = self._crop_tasks(observation)
        candidates: list[
            tuple[int, int, int, int, tuple[int, int], str]
        ] = []
        max_distance = int(self.e18_8_config["max_assignment_distance"])
        for worker, command in enumerate(actions):
            if command != ["PASS"] or worker in self.adjacent_missions:
                continue
            for priority, target, opcode in tasks:
                distance = _distance(positions[worker], target)
                if (
                    distance <= max_distance
                    and target not in claimed
                    and target not in reserved
                    and _quadrant(positions[worker]) == _quadrant(target)
                    and self._task_valid(
                        observation, target, opcode, inventories[worker]
                    )
                ):
                    candidates.append(
                        (priority, distance, target[1], target[0], target, opcode)
                    )
                    break
        self.adjacent_queue_candidates += len(candidates)
        limit = int(self.e18_8_config["max_workers_per_quadrant_per_turn"])
        for worker, command in enumerate(actions):
            if command != ["PASS"]:
                continue
            worker_candidates = [
                candidate
                for candidate in candidates
                if candidate[4] not in reserved
                and _distance(positions[worker], candidate[4]) <= max_distance
                and _quadrant(positions[worker]) == _quadrant(candidate[4])
            ]
            if not worker_candidates:
                continue
            priority, distance, _y, _x, target, opcode = min(worker_candidates)
            del priority
            quadrant = _quadrant(target)
            if quadrant_counts[quadrant] >= limit:
                continue
            if command != ["PASS"]:
                self.non_pass_overrides += 1
                continue
            self.max_observed_assignment_distance = max(
                self.max_observed_assignment_distance, distance
            )
            self.adjacent_queue_assignments += 1
            quadrant_counts[quadrant] += 1
            reserved.add(target)
            if distance == 0:
                actions[worker] = [opcode]
                self.adjacent_queue_commands[opcode] += 1
                self.adjacent_queue_completions += 1
            else:
                actions[worker] = _move(positions[worker], target)
                self.adjacent_queue_commands[str(actions[worker][0])] += 1
                self.adjacent_missions[worker] = (target, opcode)
            changed = True
        if changed:
            self.adjacent_queue_batches += 1
            _store_unit_actions(action, actions)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        self._apply_adjacent_queue(action, observation)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "PASS_TO_SAME_QUADRANT_ADJACENT_CROP_QUEUE",
            "adjacent_queue_commands": dict(self.adjacent_queue_commands),
            "adjacent_queue_assignments": self.adjacent_queue_assignments,
            "adjacent_queue_completions": self.adjacent_queue_completions,
            "adjacent_queue_cancellations": self.adjacent_queue_cancellations,
            "adjacent_queue_batches": self.adjacent_queue_batches,
            "adjacent_queue_candidates": self.adjacent_queue_candidates,
            "adjacent_inventory_blocks": self.adjacent_inventory_blocks,
            "non_pass_overrides": self.non_pass_overrides,
            "cross_quadrant_routes": self.cross_quadrant_routes,
            "max_observed_assignment_distance": (
                self.max_observed_assignment_distance
            ),
            "market_mutation": False,
            "calendar_mutation": False,
            "worker_count_mutation": False,
            "livestock_cap_mutation": False,
        }


def create_codex_e18_770_adjacent_crop_queue(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770AdjacentCropQueueAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_adjacent_crop_queue_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_adjacent_crop_queue_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_adjacent_crop_queue_instance = instance
    policy.codex_e18_770_adjacent_crop_queue_last_error = None
    policy.__name__ = "codex_e18_8_770_adjacent_crop_queue_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_ADJACENT_CROP_QUEUE_CONFIG_PATH",
    "E18_770_ADJACENT_CROP_QUEUE_MODEL_SPEC_VERSION",
    "CodexE18770AdjacentCropQueueAgent",
    "create_codex_e18_770_adjacent_crop_queue",
    "load_e18_770_adjacent_crop_queue_config",
]
