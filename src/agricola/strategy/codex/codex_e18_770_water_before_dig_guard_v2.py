"""E18.10 V2 safe PASS-only WATER-before-DIG lifecycle guard.

E18.9 first suppresses speculative DIG. This post-provider overlay then
converts only an emitted PASS to WATER when that worker is already standing
on an unwatered live Strawberry in the protected rotation window. Provider
non-PASS commands and every trajectory remain authoritative.
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
from agricola.strategy.codex.codex_e18_770_live_crop_rotation_guard import (
    CodexE18770LiveCropRotationGuardAgent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_770_WATER_BEFORE_DIG_GUARD_V2_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_10_770_WATER_BEFORE_DIG_GUARD_V2.json"
)
E18_770_WATER_BEFORE_DIG_GUARD_V2_MODEL_SPEC_VERSION = (
    "CODEX-E18.10-770-WATER-BEFORE-DIG-GUARD-V2"
)


def load_e18_770_water_before_dig_guard_v2_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_WATER_BEFORE_DIG_GUARD_V2_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_10_770_WATER_BEFORE_DIG_GUARD_V2",
        "model_spec_version": E18_770_WATER_BEFORE_DIG_GUARD_V2_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.9-770-LIVE-CROP-ROTATION-GUARD-V1",
        "causal_family": "PROVIDER_PASS_TO_PROTECTED_LIVE_CROP_IN_PLACE_WATER",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "guard_activation_day": 20,
        "guard_end_day": 23,
        "guarded_targets": [[3, 5], [4, 5], [3, 6], [4, 6], [4, 7]],
        "excluded_shared_logistics_targets": [[4, 5]],
        "guarded_crop": "STRAWBERRY",
        "allowed_override": "PASS_TO_WATER_ONLY",
        "max_workers_per_target_per_turn": 1,
        "provider_non_pass_authoritative": True,
        "allow_worker_rerouting": False,
        "provider_trajectory_mutation": False,
        "market_mutation": False,
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
    return deepcopy(config)


class CodexE18770WaterBeforeDigGuardV2Agent(
    CodexE18770LiveCropRotationGuardAgent
):
    """Apply WATER only to a provider-idle worker already on a guarded crop."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_10_v2_config = load_e18_770_water_before_dig_guard_v2_config(
            config_path
        )
        self.candidate_id = str(self.e18_10_v2_config["candidate_id"])
        self.model_spec_version = (
            E18_770_WATER_BEFORE_DIG_GUARD_V2_MODEL_SPEC_VERSION
        )
        self.guarded_targets = frozenset(
            tuple(value) for value in self.e18_10_v2_config["guarded_targets"]
        )
        self.excluded_shared_logistics_targets = frozenset(
            tuple(value)
            for value in self.e18_10_v2_config[
                "excluded_shared_logistics_targets"
            ]
        )
        self.live_crop_dig_tasks_converted_to_water = 0
        self.water_guard_active_batches = 0
        self.provider_pass_to_water_overrides = 0
        self.provider_non_pass_overrides = 0

    def _apply_pass_only_water(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        day = int(observation.get("day", 0))
        if not (
            int(self.e18_10_v2_config["guard_activation_day"])
            <= day
            <= int(self.e18_10_v2_config["guard_end_day"])
        ):
            return
        farm = _farm(observation)
        positions = _positions(farm)
        actions = _unit_actions(action, len(positions))
        claimed: set[tuple[int, int]] = set()
        changed = False
        for worker, command in enumerate(actions):
            position = positions[worker]
            tile = _tile(farm, position)
            eligible = (
                command == ["PASS"]
                and position in self.guarded_targets
                and position not in self.excluded_shared_logistics_targets
                and position not in claimed
                and isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and str(tile.get("crop", ""))
                == str(self.e18_10_v2_config["guarded_crop"])
                and int(tile.get("yield_units", 0) or 0) <= 0
                and not bool(tile.get("watered_today", False))
            )
            if not eligible:
                continue
            actions[worker] = ["WATER"]
            claimed.add(position)
            self.live_crop_dig_tasks_converted_to_water += 1
            self.provider_pass_to_water_overrides += 1
            changed = True
        if changed:
            self.water_guard_active_batches += 1
            _store_unit_actions(action, actions)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        self._apply_pass_only_water(action, observation)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "PROVIDER_PASS_TO_PROTECTED_LIVE_CROP_WATER",
            "live_crop_dig_tasks_converted_to_water": (
                self.live_crop_dig_tasks_converted_to_water
            ),
            "water_guard_active_batches": self.water_guard_active_batches,
            "provider_pass_to_water_overrides": (
                self.provider_pass_to_water_overrides
            ),
            "worker_route_mutations": 0,
            "provider_non_pass_overrides": self.provider_non_pass_overrides,
            "market_mutation": False,
            "worker_count_mutation": False,
            "livestock_cap_mutation": False,
        }


def create_codex_e18_770_water_before_dig_guard_v2(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770WaterBeforeDigGuardV2Agent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_water_before_dig_guard_v2_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_water_before_dig_guard_v2_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_water_before_dig_guard_v2_instance = instance
    policy.codex_e18_770_water_before_dig_guard_v2_last_error = None
    policy.__name__ = "codex_e18_10_770_water_before_dig_guard_v2_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_WATER_BEFORE_DIG_GUARD_V2_CONFIG_PATH",
    "E18_770_WATER_BEFORE_DIG_GUARD_V2_MODEL_SPEC_VERSION",
    "CodexE18770WaterBeforeDigGuardV2Agent",
    "create_codex_e18_770_water_before_dig_guard_v2",
    "load_e18_770_water_before_dig_guard_v2_config",
]
