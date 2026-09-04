"""E18.7 exact-7-7-0 PASS-to-in-place-crop-service treatment.

E18.6 remains the complete provider.  This overlay changes only a provider
PASS when the same worker can immediately HARVEST or WATER its current tile.
It never moves a worker, plants, digs, changes market orders, or changes the
7-7-0 topology.
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
DEFAULT_E18_770_IN_PLACE_SERVICE_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_7_770_IN_PLACE_CROP_SERVICE_V1.json"
)
E18_770_IN_PLACE_SERVICE_MODEL_SPEC_VERSION = (
    "CODEX-E18.7-770-IN-PLACE-CROP-SERVICE-V1"
)


def load_e18_770_in_place_service_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_IN_PLACE_SERVICE_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_7_770_IN_PLACE_CROP_SERVICE_V1",
        "model_spec_version": E18_770_IN_PLACE_SERVICE_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.6-CONCENTRATED-770-THROUGHPUT-V1",
        "causal_family": "PASS_TO_IN_PLACE_EXISTING_CROP_SERVICE",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "local_service_opcodes": ["HARVEST", "WATER"],
        "local_service_priority": ["HARVEST", "WATER"],
        "max_service_distance": 0,
        "max_workers_per_quadrant_per_turn": 1,
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


class CodexE18770InPlaceCropServiceAgent(
    CodexE18Concentrated770ThroughputAgent
):
    """Replace only safe in-place PASS actions with existing-crop service."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_7_config = load_e18_770_in_place_service_config(config_path)
        self.candidate_id = str(self.e18_7_config["candidate_id"])
        self.model_spec_version = E18_770_IN_PLACE_SERVICE_MODEL_SPEC_VERSION
        self.in_place_service_commands: Counter[str] = Counter()
        self.in_place_service_batches = 0
        self.in_place_service_candidates = 0
        self.in_place_inventory_blocks = 0
        self.non_pass_overrides = 0
        self.cross_quadrant_routes = 0
        self.max_observed_service_distance = 0

    def _service_command(
        self,
        observation: dict[str, Any],
        position: tuple[int, int],
        inventory: dict[str, Any],
    ) -> list[str] | None:
        tile = _tile(_farm(observation), position)
        if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
            return None
        day = int(observation.get("day", 0))
        crop = str(tile.get("crop", ""))
        mature = day - int(tile.get("planted_day", day)) >= int(
            CROPS.get(crop, {}).get("first_yield_day", 10**6)
        )
        if mature and int(tile.get("yield_units", 0) or 0) > 0:
            if bool(
                self.e18_7_config["require_empty_inventory_for_harvest"]
            ) and any(int(value or 0) > 0 for value in inventory.values()):
                self.in_place_inventory_blocks += 1
                return None
            return ["HARVEST"]
        if (
            day < int(self.e18_7_config["water_terminal_passthrough_day"])
            and not bool(tile.get("watered_today", False))
        ):
            return ["WATER"]
        return None

    def _replace_in_place_passes(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        if int(observation.get("day", 0)) < int(
            self.e18_7_config["local_service_activation_day"]
        ):
            return
        positions = _positions(_farm(observation))
        actions = _unit_actions(action, len(positions))
        inventories = _inventories(
            observation.get("private", {}) or {}, len(positions)
        )
        claimed = {
            positions[worker]
            for worker, command in enumerate(actions)
            if command and command[0] not in {"PASS", "NORTH", "SOUTH", "EAST", "WEST"}
        }
        candidates: list[tuple[int, str, int, list[str]]] = []
        priority = {
            opcode: rank
            for rank, opcode in enumerate(
                self.e18_7_config["local_service_priority"]
            )
        }
        for worker, command in enumerate(actions):
            if command != ["PASS"] or positions[worker] in claimed:
                continue
            service = self._service_command(
                observation, positions[worker], inventories[worker]
            )
            if service is None:
                continue
            candidates.append(
                (priority[service[0]], _quadrant(positions[worker]), worker, service)
            )
        self.in_place_service_candidates += len(candidates)
        quadrant_counts: Counter[str] = Counter()
        changed = False
        limit = int(self.e18_7_config["max_workers_per_quadrant_per_turn"])
        for _priority, quadrant, worker, service in sorted(candidates):
            if quadrant_counts[quadrant] >= limit:
                continue
            if actions[worker] != ["PASS"]:
                self.non_pass_overrides += 1
                continue
            actions[worker] = service
            quadrant_counts[quadrant] += 1
            self.in_place_service_commands[service[0]] += 1
            changed = True
        if changed:
            self.in_place_service_batches += 1
            _store_unit_actions(action, actions)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        self._replace_in_place_passes(action, observation)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "PASS_TO_IN_PLACE_EXISTING_CROP_SERVICE",
            "in_place_service_commands": dict(self.in_place_service_commands),
            "in_place_service_batches": self.in_place_service_batches,
            "in_place_service_candidates": self.in_place_service_candidates,
            "in_place_inventory_blocks": self.in_place_inventory_blocks,
            "non_pass_overrides": self.non_pass_overrides,
            "cross_quadrant_routes": self.cross_quadrant_routes,
            "max_observed_service_distance": self.max_observed_service_distance,
            "market_mutation": False,
            "calendar_mutation": False,
            "worker_count_mutation": False,
            "livestock_cap_mutation": False,
        }


def create_codex_e18_770_in_place_crop_service(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770InPlaceCropServiceAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_in_place_service_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_in_place_service_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_in_place_service_instance = instance
    policy.codex_e18_770_in_place_service_last_error = None
    policy.__name__ = "codex_e18_7_770_in_place_crop_service_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_IN_PLACE_SERVICE_CONFIG_PATH",
    "E18_770_IN_PLACE_SERVICE_MODEL_SPEC_VERSION",
    "CodexE18770InPlaceCropServiceAgent",
    "create_codex_e18_770_in_place_crop_service",
    "load_e18_770_in_place_service_config",
]
