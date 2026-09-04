"""E18.5 fixed-topology 6-6-2 ablation over the E18.4 V2 dispatcher."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_reactive_service_routing_core import (
    _positions,
)
from agricola.strategy.codex.codex_e17_reactive_service_routing_v3 import _SAFE_PASS
from agricola.strategy.codex.codex_e18_state_driven_772_v2 import (
    DEFAULT_E18_STATE_DRIVEN_V2_CONFIG_PATH,
    CodexE18StateDriven772V2Agent,
    load_e18_state_driven_v2_config,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_STATE_DRIVEN_662_ABLATION_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1.json"
)
E18_STATE_DRIVEN_662_ABLATION_MODEL_SPEC_VERSION = (
    "CODEX-E18.5-STATE-DRIVEN-662-TOPOLOGY-ABLATION-V1"
)
_REMOVED_772_TARGETS = {(3, 2), (6, 2)}


def load_e18_state_driven_662_ablation_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    """Load the ablation and prove topology is its only policy mutation."""

    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_STATE_DRIVEN_662_ABLATION_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1",
        "schema_version": "e18.codex.state_driven_662_topology_ablation.v1",
        "model_spec_version": E18_STATE_DRIVEN_662_ABLATION_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.4-STATE-DRIVEN-772-V2",
        "causal_family": "STATE_DRIVEN_V2_DISPATCHER_FIXED_TOPOLOGY_662_ABLATION",
        "public_features_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")

    control = load_e18_state_driven_v2_config(
        DEFAULT_E18_STATE_DRIVEN_V2_CONFIG_PATH
    )
    allowed_changes = {
        "candidate_id",
        "schema_version",
        "model_spec_version",
        "base_policy",
        "causal_family",
        "pasture_targets",
        "pasture_livestock_cap",
    }
    for key, value in control.items():
        if key not in allowed_changes and config.get(key) != value:
            raise ValueError(f"662 ablation changed frozen V2 field {key!r}")

    control_targets = {tuple(value) for value in control["pasture_targets"]}
    targets = {tuple(value) for value in config.get("pasture_targets", [])}
    if control_targets - targets != _REMOVED_772_TARGETS:
        raise ValueError("662 ablation must remove only the canonical Q0/Q1 targets")
    q0 = sum(x < 5 and y < 5 for x, y in targets)
    q1 = sum(x >= 5 and y < 5 for x, y in targets)
    q2 = sum(x < 5 and y >= 5 for x, y in targets)
    if len(targets) != 14 or (q0, q1, q2) != (6, 6, 2):
        raise ValueError("ablation pasture target must be exactly 6-6-2")
    if int(config.get("pasture_livestock_cap", 0)) != 14:
        raise ValueError("6-6-2 ablation requires livestock cap 14")
    return deepcopy(config)


class CodexE18StateDriven662AblationAgent(CodexE18StateDriven772V2Agent):
    """Use the unchanged V2 dispatcher on fourteen fixed pasture targets."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.config = load_e18_state_driven_662_ablation_config(config_path)
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = E18_STATE_DRIVEN_662_ABLATION_MODEL_SPEC_VERSION
        self.bootstrap_topology_vetoes = 0

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        if int(observation.get("day", 0)) >= int(self.config["activation_day"]):
            return action
        player = int(observation.get("player", 0) or 0)
        farms = observation.get("farms", []) or []
        farm = farms[player] if player < len(farms) else {}
        positions = _positions(farm)
        commands = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
        for worker_id, position in enumerate(positions):
            if worker_id >= len(commands) or position not in _REMOVED_772_TARGETS:
                continue
            if commands[worker_id] and commands[worker_id][0] == "BUILD_PASTURE":
                commands[worker_id] = ["PASS"]
                self.bootstrap_topology_vetoes += 1
        action["farmer"] = commands[0] if commands else ["PASS"]
        action["hands"] = commands[1:]
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        telemetry = super().telemetry_snapshot()
        return {
            **telemetry,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "topology_mode": "6-6-2",
            "pasture_target_count": 14,
            "pasture_livestock_cap": 14,
            "topology_only_ablation": True,
            "bootstrap_topology_vetoes": self.bootstrap_topology_vetoes,
        }


def create_codex_e18_state_driven_662_ablation(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    """Create the fail-closed E18.5 6-6-2 development ablation."""

    instance = CodexE18StateDriven662AblationAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_state_driven_662_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_state_driven_662_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_state_driven_662_instance = instance
    policy.codex_e18_state_driven_662_last_error = None
    policy.__name__ = "codex_e18_5_state_driven_662_ablation_policy"
    return policy


__all__ = [
    "DEFAULT_E18_STATE_DRIVEN_662_ABLATION_CONFIG_PATH",
    "E18_STATE_DRIVEN_662_ABLATION_MODEL_SPEC_VERSION",
    "CodexE18StateDriven662AblationAgent",
    "create_codex_e18_state_driven_662_ablation",
    "load_e18_state_driven_662_ablation_config",
]
