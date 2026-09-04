"""E18.9 exact-7-7-0 guard against speculative live-crop rotation.

E18.6 remains authoritative. The only change removes its scheduled DIG task
when a reclaimed Q2 target still contains a live crop. WEED DIG, HARVEST,
WATER, worker trajectories, market orders, livestock and topology are intact.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _SAFE_PASS,
    _farm,
    _tile,
)
from agricola.strategy.codex.codex_e18_concentrated_770_throughput import (
    CodexE18Concentrated770ThroughputAgent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_770_LIVE_CROP_ROTATION_GUARD_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_9_770_LIVE_CROP_ROTATION_GUARD_V1.json"
)
E18_770_LIVE_CROP_ROTATION_GUARD_MODEL_SPEC_VERSION = (
    "CODEX-E18.9-770-LIVE-CROP-ROTATION-GUARD-V1"
)


def load_e18_770_live_crop_rotation_guard_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_LIVE_CROP_ROTATION_GUARD_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_9_770_LIVE_CROP_ROTATION_GUARD_V1",
        "model_spec_version": E18_770_LIVE_CROP_ROTATION_GUARD_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.6-CONCENTRATED-770-THROUGHPUT-V1",
        "causal_family": "SUPPRESS_SPECULATIVE_DIG_ON_LIVE_RECLAIMED_CROPS",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "guard_activation_day": 20,
        "guard_end_day": 23,
        "guarded_targets": [[3, 5], [4, 5], [3, 6], [4, 6], [4, 7]],
        "preserve_harvest": True,
        "preserve_water": True,
        "preserve_weed_dig": True,
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


class CodexE18770LiveCropRotationGuardAgent(
    CodexE18Concentrated770ThroughputAgent
):
    """Keep live reclaimed crops instead of scheduling a speculative DIG."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_9_config = load_e18_770_live_crop_rotation_guard_config(
            config_path
        )
        self.candidate_id = str(self.e18_9_config["candidate_id"])
        self.model_spec_version = (
            E18_770_LIVE_CROP_ROTATION_GUARD_MODEL_SPEC_VERSION
        )
        self.guarded_targets = frozenset(
            tuple(value) for value in self.e18_9_config["guarded_targets"]
        )
        self.live_crop_dig_tasks_suppressed = 0
        self.guard_active_batches = 0

    def _reclaimed_crop_tasks(
        self,
        observation: dict[str, Any],
    ) -> list[tuple[int, tuple[int, int], list[Any]]]:
        tasks = super()._reclaimed_crop_tasks(observation)
        farm = _farm(observation)
        kept: list[tuple[int, tuple[int, int], list[Any]]] = []
        suppressed = 0
        for priority, target, command in tasks:
            tile = _tile(farm, target)
            if (
                target in self.guarded_targets
                and command == ["DIG"]
                and isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
            ):
                suppressed += 1
                continue
            kept.append((priority, target, command))
        if suppressed:
            self.live_crop_dig_tasks_suppressed += suppressed
            self.guard_active_batches += 1
        return kept

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "SUPPRESS_SPECULATIVE_DIG_ON_LIVE_RECLAIMED_CROPS",
            "live_crop_dig_tasks_suppressed": (
                self.live_crop_dig_tasks_suppressed
            ),
            "guard_active_batches": self.guard_active_batches,
            "worker_route_mutations": 0,
            "provider_non_pass_overrides": 0,
            "market_mutation": False,
            "worker_count_mutation": False,
            "livestock_cap_mutation": False,
        }


def create_codex_e18_770_live_crop_rotation_guard(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770LiveCropRotationGuardAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_live_crop_rotation_guard_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_live_crop_rotation_guard_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_live_crop_rotation_guard_instance = instance
    policy.codex_e18_770_live_crop_rotation_guard_last_error = None
    policy.__name__ = "codex_e18_9_770_live_crop_rotation_guard_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_LIVE_CROP_ROTATION_GUARD_CONFIG_PATH",
    "E18_770_LIVE_CROP_ROTATION_GUARD_MODEL_SPEC_VERSION",
    "CodexE18770LiveCropRotationGuardAgent",
    "create_codex_e18_770_live_crop_rotation_guard",
    "load_e18_770_live_crop_rotation_guard_config",
]
