"""E18.12 exact-7-7-0 livestock resource cap.

E18.10 V2 is unchanged except that the animal resource cap equals the number
of pasture slots: fourteen.  This removes the unused in-transit buffer that
the topology-matched Top-3 profiles do not carry.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_topology_cap_662 import _SAFE_PASS
from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    CodexE18770WaterBeforeDigGuardV2Agent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_770_EXACT_LIVESTOCK_CAP_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_12_770_EXACT_LIVESTOCK_CAP_V1.json"
)
E18_770_EXACT_LIVESTOCK_CAP_MODEL_SPEC_VERSION = (
    "CODEX-E18.12-770-EXACT-LIVESTOCK-CAP-V1"
)


def load_e18_770_exact_livestock_cap_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_EXACT_LIVESTOCK_CAP_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_12_770_EXACT_LIVESTOCK_CAP_V1",
        "model_spec_version": E18_770_EXACT_LIVESTOCK_CAP_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.10-770-WATER-BEFORE-DIG-GUARD-V2",
        "causal_family": "EXACT_14_LIVESTOCK_RESOURCE_CAP",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "pasture_fill_target": 14,
        "livestock_resource_cap": 14,
        "in_transit_buffer": 0,
        "allow_worker_rerouting": False,
        "provider_trajectory_mutation": False,
        "crop_lifecycle_mutation": False,
        "market_mutation": "BUY_ANIMAL_CLAMP_ONLY",
        "worker_count_mutation": False,
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


class CodexE18770ExactLivestockCapAgent(
    CodexE18770WaterBeforeDigGuardV2Agent
):
    """Clamp COW/SHEEP resources to the fourteen available pastures."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_12_config = load_e18_770_exact_livestock_cap_config(
            config_path
        )
        self.candidate_id = str(self.e18_12_config["candidate_id"])
        self.model_spec_version = (
            E18_770_EXACT_LIVESTOCK_CAP_MODEL_SPEC_VERSION
        )
        exact_cap = int(self.e18_12_config["livestock_resource_cap"])
        self.livestock_resource_cap = exact_cap
        self.config["pre_q2_livestock_resource_cap"] = exact_cap
        self.config["livestock_resource_cap"] = exact_cap

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "EXACT_14_LIVESTOCK_RESOURCE_CAP",
            "livestock_resource_cap": self.livestock_resource_cap,
            "in_transit_buffer": 0,
            "worker_route_mutations": 0,
            "crop_lifecycle_mutation": False,
            "market_mutation": "BUY_ANIMAL_CLAMP_ONLY",
            "worker_count_mutation": False,
        }


def create_codex_e18_770_exact_livestock_cap(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770ExactLivestockCapAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_exact_livestock_cap_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_exact_livestock_cap_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_exact_livestock_cap_instance = instance
    policy.codex_e18_770_exact_livestock_cap_last_error = None
    policy.__name__ = "codex_e18_12_770_exact_livestock_cap_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_EXACT_LIVESTOCK_CAP_CONFIG_PATH",
    "E18_770_EXACT_LIVESTOCK_CAP_MODEL_SPEC_VERSION",
    "CodexE18770ExactLivestockCapAgent",
    "create_codex_e18_770_exact_livestock_cap",
    "load_e18_770_exact_livestock_cap_config",
]
