"""E18.11 exact-7-7-0 recovery of provably infeasible local commands.

E18.10 V2 remains authoritative.  When its final command cannot execute on
the worker's current live, dry crop, this overlay can replace four known local
opcodes with WATER.  MOVE, PASS, valid commands, shed access and trajectories
are immutable.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _SAFE_PASS,
    _farm,
    _inventories,
    _positions,
    _store_unit_actions,
    _tile,
    _unit_actions,
)
from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    CodexE18770WaterBeforeDigGuardV2Agent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_770_INVALID_COMMAND_WATER_RECOVERY_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_11_770_INVALID_COMMAND_WATER_RECOVERY_V1.json"
)
E18_770_INVALID_COMMAND_WATER_RECOVERY_MODEL_SPEC_VERSION = (
    "CODEX-E18.11-770-INVALID-COMMAND-WATER-RECOVERY-V1"
)


def load_e18_770_invalid_command_water_recovery_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_INVALID_COMMAND_WATER_RECOVERY_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_11_770_INVALID_COMMAND_WATER_RECOVERY_V1",
        "model_spec_version": (
            E18_770_INVALID_COMMAND_WATER_RECOVERY_MODEL_SPEC_VERSION
        ),
        "base_policy": "CODEX-E18.10-770-WATER-BEFORE-DIG-GUARD-V2",
        "causal_family": "INFEASIBLE_LOCAL_COMMAND_TO_IN_PLACE_WATER",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "activation_day": 0,
        "service_end_day": 28,
        "replaceable_infeasible_opcodes": [
            "FERTILIZE",
            "HARVEST",
            "PLACE",
            "PLANT",
        ],
        "excluded_shared_logistics_targets": [
            [4, 4],
            [5, 4],
            [4, 5],
            [5, 5],
        ],
        "allowed_override": (
            "KNOWN_INFEASIBLE_LOCAL_COMMAND_TO_WATER_ONLY"
        ),
        "require_live_crop": True,
        "require_zero_yield": True,
        "require_unwatered": True,
        "deduplicate_water_by_target": True,
        "allow_worker_rerouting": False,
        "provider_trajectory_mutation": False,
        "market_mutation": False,
        "worker_count_mutation": False,
        "livestock_cap_mutation": False,
        "public_features_only": True,
        "private_inventory_used_for_local_feasibility_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    return deepcopy(config)


class CodexE18770InvalidCommandWaterRecoveryAgent(
    CodexE18770WaterBeforeDigGuardV2Agent
):
    """Turn only known, locally infeasible provider work into WATER."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_11_config = (
            load_e18_770_invalid_command_water_recovery_config(config_path)
        )
        self.candidate_id = str(self.e18_11_config["candidate_id"])
        self.model_spec_version = (
            E18_770_INVALID_COMMAND_WATER_RECOVERY_MODEL_SPEC_VERSION
        )
        self.replaceable_opcodes = frozenset(
            str(value)
            for value in self.e18_11_config["replaceable_infeasible_opcodes"]
        )
        self.excluded_shared_logistics_targets = frozenset(
            tuple(value)
            for value in self.e18_11_config[
                "excluded_shared_logistics_targets"
            ]
        )
        self.infeasible_local_to_water: Counter[str] = Counter()
        self.infeasible_local_water_batches = 0
        self.feasible_provider_overrides = 0
        self.worker_route_mutations = 0

    @staticmethod
    def _known_command_is_infeasible(
        command: list[Any],
        *,
        inventory: dict[str, Any],
    ) -> bool:
        opcode = str(command[0])
        if opcode == "FERTILIZE":
            return int(inventory.get("FERTILIZER", 0) or 0) <= 0
        return opcode in {"HARVEST", "PLACE", "PLANT"}

    def _apply_invalid_command_water_recovery(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        day = int(observation.get("day", 0))
        if not (
            int(self.e18_11_config["activation_day"])
            <= day
            <= int(self.e18_11_config["service_end_day"])
        ):
            return
        farm = _farm(observation)
        positions = _positions(farm)
        commands = _unit_actions(action, len(positions))
        inventories = _inventories(
            observation.get("private", {}) or {}, len(positions)
        )
        claimed = {
            positions[worker]
            for worker, command in enumerate(commands)
            if worker < len(positions) and command == ["WATER"]
        }
        changed = False
        for worker, command in enumerate(commands):
            if not command:
                continue
            opcode = str(command[0])
            position = positions[worker]
            tile = _tile(farm, position)
            if not (
                opcode in self.replaceable_opcodes
                and position not in self.excluded_shared_logistics_targets
                and position not in claimed
                and isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and int(tile.get("yield_units", 0) or 0) <= 0
                and not bool(tile.get("watered_today", False))
                and self._known_command_is_infeasible(
                    command, inventory=inventories[worker]
                )
            ):
                continue
            commands[worker] = ["WATER"]
            claimed.add(position)
            self.infeasible_local_to_water[opcode] += 1
            changed = True
        if changed:
            self.infeasible_local_water_batches += 1
            _store_unit_actions(action, commands)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        self._apply_invalid_command_water_recovery(action, observation)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "INFEASIBLE_LOCAL_COMMAND_TO_IN_PLACE_WATER",
            "infeasible_local_to_water": dict(self.infeasible_local_to_water),
            "infeasible_local_to_water_total": sum(
                self.infeasible_local_to_water.values()
            ),
            "infeasible_local_water_batches": (
                self.infeasible_local_water_batches
            ),
            "feasible_provider_overrides": self.feasible_provider_overrides,
            "worker_route_mutations": self.worker_route_mutations,
            "market_mutation": False,
            "worker_count_mutation": False,
            "livestock_cap_mutation": False,
        }


def create_codex_e18_770_invalid_command_water_recovery(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770InvalidCommandWaterRecoveryAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_invalid_command_water_recovery_last_error = (
                None
            )
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_invalid_command_water_recovery_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_invalid_command_water_recovery_instance = instance
    policy.codex_e18_770_invalid_command_water_recovery_last_error = None
    policy.__name__ = (
        "codex_e18_11_770_invalid_command_water_recovery_policy"
    )
    return policy


__all__ = [
    "DEFAULT_E18_770_INVALID_COMMAND_WATER_RECOVERY_CONFIG_PATH",
    "E18_770_INVALID_COMMAND_WATER_RECOVERY_MODEL_SPEC_VERSION",
    "CodexE18770InvalidCommandWaterRecoveryAgent",
    "create_codex_e18_770_invalid_command_water_recovery",
    "load_e18_770_invalid_command_water_recovery_config",
]
