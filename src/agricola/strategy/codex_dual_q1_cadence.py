"""Codex V7.3: one causal Q1 livestock-cadence change over V7.2."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex_dual_q0_q1 import CodexDualQAgent
from agricola.strategy.codex_lifecycle import CodexSnapshot

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CADENCE_CONFIG_PATH = (
    REPO_ROOT
    / "configs"
    / "model_spec_c2"
    / "CODEX_C2_DUAL_Q1_CADENCE_CONFIG.json"
)
CADENCE_MODEL_SPEC_VERSION = "CODEX-C2-V7.3-DUAL-Q1-CADENCE"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def load_cadence_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path) if path is not None else DEFAULT_CADENCE_CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("candidate_id") != "CODEX_C2_DUAL_Q1_CADENCE":
        raise ValueError("unexpected cadence candidate_id")
    if config.get("model_spec_version") != CADENCE_MODEL_SPEC_VERSION:
        raise ValueError("unexpected cadence model_spec_version")
    relief = config.get("q1_cadence_relief", {})
    if relief.get("worker_role") != "FERTILIZER_LOGISTICS_Q1":
        raise ValueError("Q1 cadence requires the local fertilizer worker")
    if relief.get("eligible_tasks") != ["ANIMAL_COLLECTION", "CARE"]:
        raise ValueError("Q1 cadence must remain limited to collection and care")
    if not relief.get("feed_ownership_unchanged"):
        raise ValueError("Q1 feed ownership must remain unchanged")
    if not relief.get("q0_ownership_unchanged"):
        raise ValueError("Q0 ownership must remain unchanged")
    return deepcopy(config)


class CodexDualQ1CadenceAgent(CodexDualQAgent):
    """Give W12 local Q1 collection/care relief after hard crop obligations."""

    def __init__(
        self,
        candidate_config: dict[str, Any] | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        config = deepcopy(candidate_config or load_cadence_config())
        super().__init__(config, run_context=run_context)
        self.candidate_id = "CODEX_C2_DUAL_Q1_CADENCE"
        self.model_spec_version = CADENCE_MODEL_SPEC_VERSION

    def _fertilizer_role_candidates(
        self,
        snapshot: CodexSnapshot,
        role: str,
        hard_crop_tasks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        base_candidates = super()._fertilizer_role_candidates(
            snapshot, role, hard_crop_tasks
        )
        if role != "FERTILIZER_LOGISTICS_Q1":
            return base_candidates
        q1_cadence = [
            {
                **task,
                "value": max(
                    130 if species == "COW" else 120,
                    int(task["value"]),
                ),
            }
            for species in ("COW", "SHEEP")
            for task in self._module_animal_tasks(snapshot, "Q1", species)
            if task["kind"] in {"ANIMAL_COLLECTION", "CARE"}
        ]
        return base_candidates + q1_cadence


def create_cadence_agent(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    instance = CodexDualQ1CadenceAgent(
        load_cadence_config(config_path),
        run_context=run_context,
    )

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_cadence_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_cadence_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_cadence_instance = instance
    policy.codex_cadence_last_error = None
    policy.__name__ = "codex_dual_q1_cadence_policy"
    return policy
