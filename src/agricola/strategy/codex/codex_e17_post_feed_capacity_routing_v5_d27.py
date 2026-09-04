"""E17.2 isolated D27 handoff ablation over the frozen V4D behavior."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4D_CONFIG_PATH,
    CodexE17BatchedClusterRoutingV4,
    load_v4_config,
)
from agricola.strategy.codex.codex_e17_reactive_service_routing_v3 import (
    _SAFE_PASS,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_V5_D27_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/configs/"
    / "CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V5_D27.json"
)
V5_D27_MODEL_SPEC_VERSION = (
    "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V5-D27"
)
V5_D27_CANDIDATE_ID = "CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V5_D27"
_METADATA_KEYS = {
    "candidate_id",
    "schema_version",
    "model_spec_version",
    "base_policy",
    "causal_family",
    "activation_day",
}


def load_v5_d27_config(path: Path | str | None = None) -> dict[str, Any]:
    """Validate that D27 changes only handoff timing from frozen V4D."""

    config_path = Path(path) if path is not None else DEFAULT_V5_D27_CONFIG_PATH
    overlay = json.loads(config_path.read_text(encoding="utf-8"))
    if overlay.get("candidate_id") != V5_D27_CANDIDATE_ID:
        raise ValueError("unexpected V5 D27 candidate_id")
    if overlay.get("model_spec_version") != V5_D27_MODEL_SPEC_VERSION:
        raise ValueError("model_spec_version does not match V5 D27 candidate")
    if int(overlay.get("activation_day", -1)) != 27:
        raise ValueError("V5 D27 must activate on day 27")
    if int(overlay.get("liquidation_day", -1)) != 29:
        raise ValueError("V5 D27 must preserve the D29 liquidation window")

    frozen_overlay = json.loads(DEFAULT_V4D_CONFIG_PATH.read_text(encoding="utf-8"))
    functional_overlay = {
        key: value for key, value in overlay.items() if key not in _METADATA_KEYS
    }
    frozen_functional = {
        key: value
        for key, value in frozen_overlay.items()
        if key not in _METADATA_KEYS
    }
    if functional_overlay != frozen_functional:
        raise ValueError("V5 D27 may change only activation day and metadata")

    config = load_v4_config(DEFAULT_V4D_CONFIG_PATH)
    config.update(overlay)
    return config


class CodexE17PostFeedCapacityRoutingV5D27(CodexE17BatchedClusterRoutingV4):
    """Frozen V4D behavior activated one day earlier."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
    ) -> None:
        super().__init__(
            run_context=run_context,
            config_path=DEFAULT_V4D_CONFIG_PATH,
        )
        self.config = load_v5_d27_config(config_path)
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = str(self.config["model_spec_version"])


def create_codex_e17_post_feed_capacity_routing_v5_d27(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    """Create the fail-closed isolated D27 ablation."""

    instance = CodexE17PostFeedCapacityRoutingV5D27(
        run_context=run_context,
        config_path=config_path,
    )

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_e17_batched_cluster_routing_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e17_batched_cluster_routing_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e17_batched_cluster_routing_instance = instance
    policy.codex_e17_batched_cluster_routing_last_error = None
    policy.__name__ = "codex_e17_2_post_feed_capacity_routing_v5_d27_policy"
    return policy


__all__ = [
    "DEFAULT_V5_D27_CONFIG_PATH",
    "V5_D27_CANDIDATE_ID",
    "V5_D27_MODEL_SPEC_VERSION",
    "CodexE17PostFeedCapacityRoutingV5D27",
    "create_codex_e17_post_feed_capacity_routing_v5_d27",
    "load_v5_d27_config",
]
