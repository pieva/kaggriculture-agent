"""E18.13 exact-7-7-0 D20 critical FEED deadline.

The E18.10 V2 provider remains authoritative except when a worker is already
standing on a critical unfed animal with carried Wheat late on D20.  A final
MOVE is delayed once so FEED executes in place before the day boundary.
"""

from __future__ import annotations

import json
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
DEFAULT_E18_770_D20_CRITICAL_FEED_DEADLINE_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_13_770_D20_CRITICAL_FEED_DEADLINE_V1.json"
)
E18_770_D20_CRITICAL_FEED_DEADLINE_MODEL_SPEC_VERSION = (
    "CODEX-E18.13-770-D20-CRITICAL-FEED-DEADLINE-V1"
)
_MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})


def load_e18_770_d20_critical_feed_deadline_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_D20_CRITICAL_FEED_DEADLINE_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_13_770_D20_CRITICAL_FEED_DEADLINE_V1",
        "model_spec_version": (
            E18_770_D20_CRITICAL_FEED_DEADLINE_MODEL_SPEC_VERSION
        ),
        "base_policy": "CODEX-E18.10-770-WATER-BEFORE-DIG-GUARD-V2",
        "causal_family": "D20_IN_PLACE_CRITICAL_FEED_BEFORE_MOVE",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "activation_day": 19,
        "end_day": 19,
        "activation_hour": 20,
        "critical_unfed_threshold": 1,
        "allowed_override": "MOVE_TO_IN_PLACE_FEED_ONLY",
        "require_carried_wheat": True,
        "max_workers_per_target_per_turn": 1,
        "market_mutation": False,
        "worker_count_mutation": False,
        "livestock_cap_mutation": False,
        "crop_lifecycle_mutation": False,
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


class CodexE18770D20CriticalFeedDeadlineAgent(
    CodexE18770WaterBeforeDigGuardV2Agent
):
    """Execute one feasible critical FEED before a provider departure."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_13_config = load_e18_770_d20_critical_feed_deadline_config(
            config_path
        )
        self.candidate_id = str(self.e18_13_config["candidate_id"])
        self.model_spec_version = (
            E18_770_D20_CRITICAL_FEED_DEADLINE_MODEL_SPEC_VERSION
        )
        self.move_to_critical_feed_overrides = 0
        self.critical_feed_batches = 0
        self.infeasible_feed_overrides = 0
        self.non_move_overrides = 0

    def _apply_d20_critical_feed(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        day = int(observation.get("day", 0))
        hour = int(observation.get("hour", 0))
        if not (
            int(self.e18_13_config["activation_day"])
            <= day
            <= int(self.e18_13_config["end_day"])
            and hour >= int(self.e18_13_config["activation_hour"])
        ):
            return
        farm = _farm(observation)
        positions = _positions(farm)
        commands = _unit_actions(action, len(positions))
        inventories = _inventories(
            observation.get("private", {}) or {}, len(positions)
        )
        claimed: set[tuple[int, int]] = set()
        changed = False
        threshold = int(self.e18_13_config["critical_unfed_threshold"])
        for worker, command in enumerate(commands):
            if not command or str(command[0]) not in _MOVES:
                continue
            position = positions[worker]
            tile = _tile(farm, position)
            eligible = (
                position not in claimed
                and isinstance(tile, dict)
                and str(tile.get("animal", "")) in {"COW", "SHEEP"}
                and not bool(tile.get("fed_today", False))
                and int(tile.get("consecutive_unfed", 0) or 0) >= threshold
                and int(inventories[worker].get("WHEAT", 0) or 0) > 0
            )
            if not eligible:
                continue
            commands[worker] = ["FEED"]
            claimed.add(position)
            self.move_to_critical_feed_overrides += 1
            changed = True
        if changed:
            self.critical_feed_batches += 1
            _store_unit_actions(action, commands)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        self._apply_d20_critical_feed(action, observation)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "D20_IN_PLACE_CRITICAL_FEED_BEFORE_MOVE",
            "move_to_critical_feed_overrides": (
                self.move_to_critical_feed_overrides
            ),
            "critical_feed_batches": self.critical_feed_batches,
            "infeasible_feed_overrides": self.infeasible_feed_overrides,
            "non_move_overrides": self.non_move_overrides,
            "route_delay_commands": self.move_to_critical_feed_overrides,
            "market_mutation": False,
            "worker_count_mutation": False,
            "livestock_cap_mutation": False,
            "crop_lifecycle_mutation": False,
        }


def create_codex_e18_770_d20_critical_feed_deadline(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770D20CriticalFeedDeadlineAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_d20_critical_feed_deadline_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_d20_critical_feed_deadline_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_d20_critical_feed_deadline_instance = instance
    policy.codex_e18_770_d20_critical_feed_deadline_last_error = None
    policy.__name__ = "codex_e18_13_770_d20_critical_feed_deadline_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_D20_CRITICAL_FEED_DEADLINE_CONFIG_PATH",
    "E18_770_D20_CRITICAL_FEED_DEADLINE_MODEL_SPEC_VERSION",
    "CodexE18770D20CriticalFeedDeadlineAgent",
    "create_codex_e18_770_d20_critical_feed_deadline",
    "load_e18_770_d20_critical_feed_deadline_config",
]
