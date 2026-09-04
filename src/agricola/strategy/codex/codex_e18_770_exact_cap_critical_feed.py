"""E18.16 coherent livestock safety for the exact 7-7-0 topology.

The candidate combines the two causally diagnosed halves of the same defect:
fourteen COW/SHEEP resources for fourteen pasture slots, plus the single D20
in-place FEED that prevents a filled pasture from being lost at the boundary.
Crop lifecycle, worker count, and all other provider decisions remain frozen.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _SAFE_PASS,
    _pasture_livestock_resources,
)
from agricola.strategy.codex.codex_e18_770_d20_critical_feed_deadline import (
    CodexE18770D20CriticalFeedDeadlineAgent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_770_EXACT_CAP_CRITICAL_FEED_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1.json"
)
E18_770_EXACT_CAP_CRITICAL_FEED_MODEL_SPEC_VERSION = (
    "CODEX-E18.16-770-EXACT-CAP-CRITICAL-FEED-V1"
)


def load_e18_770_exact_cap_critical_feed_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_EXACT_CAP_CRITICAL_FEED_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1",
        "model_spec_version": E18_770_EXACT_CAP_CRITICAL_FEED_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.10-770-WATER-BEFORE-DIG-GUARD-V2",
        "causal_family": "COHERENT_14_SLOT_LIVESTOCK_SAFETY",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "pasture_fill_target": 14,
        "livestock_resource_cap": 14,
        "in_transit_buffer": 0,
        "critical_feed_activation_day": 19,
        "critical_feed_end_day": 19,
        "critical_feed_activation_hour": 20,
        "critical_unfed_threshold": 1,
        "market_mutation": "BUY_ANIMAL_CLAMP_ONLY",
        "worker_route_mutation": "ONE_D20_MOVE_DELAYED_FOR_FEED_ONLY",
        "worker_count_mutation": False,
        "crop_lifecycle_mutation": False,
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


class CodexE18770ExactCapCriticalFeedAgent(
    CodexE18770D20CriticalFeedDeadlineAgent
):
    """Remove the surplus animal and protect the fourteenth occupied slot."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_16_config = load_e18_770_exact_cap_critical_feed_config(
            config_path
        )
        self.candidate_id = str(self.e18_16_config["candidate_id"])
        self.model_spec_version = (
            E18_770_EXACT_CAP_CRITICAL_FEED_MODEL_SPEC_VERSION
        )
        exact_cap = int(self.e18_16_config["livestock_resource_cap"])
        self.livestock_resource_cap = exact_cap
        self.config["pre_q2_livestock_resource_cap"] = exact_cap
        self.config["livestock_resource_cap"] = exact_cap
        self.max_observed_livestock_resources = 0

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        self.max_observed_livestock_resources = max(
            self.max_observed_livestock_resources,
            _pasture_livestock_resources(observation),
        )
        return super().__call__(observation, configuration)

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "COHERENT_14_SLOT_LIVESTOCK_SAFETY",
            "livestock_resource_cap": self.livestock_resource_cap,
            "in_transit_buffer": 0,
            "max_observed_livestock_resources": (
                self.max_observed_livestock_resources
            ),
            "market_mutation": "BUY_ANIMAL_CLAMP_ONLY",
            "livestock_cap_mutation": True,
            "worker_count_mutation": False,
            "crop_lifecycle_mutation": False,
        }


def create_codex_e18_770_exact_cap_critical_feed(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770ExactCapCriticalFeedAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_exact_cap_critical_feed_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_exact_cap_critical_feed_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_exact_cap_critical_feed_instance = instance
    policy.codex_e18_770_exact_cap_critical_feed_last_error = None
    policy.__name__ = "codex_e18_16_770_exact_cap_critical_feed_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_EXACT_CAP_CRITICAL_FEED_CONFIG_PATH",
    "E18_770_EXACT_CAP_CRITICAL_FEED_MODEL_SPEC_VERSION",
    "CodexE18770ExactCapCriticalFeedAgent",
    "create_codex_e18_770_exact_cap_critical_feed",
    "load_e18_770_exact_cap_critical_feed_config",
]
