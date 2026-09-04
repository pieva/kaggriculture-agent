"""Late E17 6-6-2 research candidates produced in the Copilot workstream.

The frozen Codex V2 source stays byte-identical to its Kaggle bundle. These
classes are local, non-promoted research overlays and are not submissions.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    DEFAULT_TOPOLOGY_662_CONFIG_PATH,
    CodexE17TopologyCap662Agent,
    _farm,
    _pasture_livestock_resources,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_V3_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/configs/CODEX_E17_3_TOPOLOGY_CAP_662_V3.json"
)
DEFAULT_V4_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/configs/CODEX_E17_3_TOPOLOGY_CAP_662_V4.json"
)
_PASTURE_LIVESTOCK = frozenset({"COW", "SHEEP"})
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def _load_candidate_config(
    path: Path | str,
    *,
    allowed_ids: frozenset[str],
) -> dict[str, Any]:
    candidate = json.loads(Path(path).read_text(encoding="utf-8"))
    if candidate.get("candidate_id") not in allowed_ids:
        raise ValueError(f"unexpected candidate_id: {candidate.get('candidate_id')!r}")
    baseline = json.loads(DEFAULT_TOPOLOGY_662_CONFIG_PATH.read_text(encoding="utf-8"))
    invariant_keys = (
        "base_policy",
        "quadrant_pasture_caps",
        "q2_pasture_cap",
        "pasture_fill_target",
        "pasture_targets",
        "blocked_v4d_pasture_targets",
        "reclaimed_crop_targets",
        "q2_reclaimed_crop_targets",
        "allow_q2_zero_future_variant",
    )
    for key in invariant_keys:
        if candidate.get(key) != baseline.get(key):
            raise ValueError(f"candidate changes frozen 6-6-2 invariant {key!r}")
    return candidate


class CodexE17TopologyCap662V3Agent(CodexE17TopologyCap662Agent):
    """Service-gated 6-6-2 variant from the Copilot tournament diagnosis."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy: Callable[..., dict[str, Any]] | None = None,
    ) -> None:
        candidate_config = _load_candidate_config(
            config_path or DEFAULT_V3_CONFIG_PATH,
            allowed_ids=frozenset(
                {
                    "CODEX_E17_3_TOPOLOGY_FILL_662_V3",
                    "CODEX_E17_3_TOPOLOGY_FILL_662_V4",
                }
            ),
        )
        super().__init__(
            run_context=run_context,
            config_path=DEFAULT_TOPOLOGY_662_CONFIG_PATH,
            base_policy=base_policy,
        )
        self.config = candidate_config
        self.candidate_id = "CODEX_E17_3_TOPOLOGY_FILL_662_V3"
        self.model_spec_version = "CODEX-E17.3-TOPOLOGY-FILL-662-V3"
        self.market_guard_weeds = int(self.config.get("market_regime_guard_weeds", 18))
        self.service_guard_empty_targets = int(
            self.config.get("service_guard_empty_targets", 2)
        )
        self.market_buy_animal_cut = float(
            self.config.get("market_buy_animal_cut", 0.5)
        )
        self.service_guard_activations = 0

    def _market_regime(self, observation: dict[str, Any]) -> str:
        farm = _farm(observation)
        weeds = sum(
            1
            for row in farm.get("tiles", []) or []
            for tile in row
            if isinstance(tile, dict) and tile.get("kind") == "WEED"
        )
        unlocked = len(farm.get("unlocked_quadrants", []) or [])
        if unlocked < 3:
            return "growth"
        if (
            weeds >= self.market_guard_weeds
            or self.latest_empty_target_pastures >= self.service_guard_empty_targets
        ):
            return "service_guard"
        return "balanced"

    def _apply_service_guard(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        if self._market_regime(observation) != "service_guard":
            return
        self.service_guard_activations += 1
        adjusted: list[Any] = []
        for order in action.get("market", []) or []:
            if not (
                isinstance(order, list)
                and len(order) >= 3
                and str(order[0]) == "BUY_ANIMAL"
                and str(order[1]) in _PASTURE_LIVESTOCK
            ):
                adjusted.append(order)
                continue
            requested = max(0, int(order[2]))
            if requested <= 1:
                adjusted.append(order)
                continue
            scaled = max(1, round(requested * self.market_buy_animal_cut))
            adjusted.append([*order[:2], scaled, *order[3:]])
        action["market"] = adjusted

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        self._apply_service_guard(action, observation)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        snapshot = super().telemetry_snapshot()
        snapshot["service_guard_activations"] = self.service_guard_activations
        return snapshot


class CodexE17TopologyCap662V4Agent(CodexE17TopologyCap662V3Agent):
    """Late early-herd prototype; technically testable but not benchmarked."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy: Callable[..., dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            run_context=run_context,
            config_path=config_path or DEFAULT_V4_CONFIG_PATH,
            base_policy=base_policy,
        )
        self.candidate_id = "CODEX_E17_3_TOPOLOGY_FILL_662_V4"
        self.model_spec_version = "CODEX-E17.3-TOPOLOGY-FILL-662-V4"
        self.early_livestock_activation_day = int(
            self.config.get("early_livestock_activation_day", 6)
        )
        self.early_livestock_cutoff_day = int(
            self.config.get("early_livestock_cutoff_day", 12)
        )
        self.early_livestock_cap = int(self.config.get("early_livestock_cap", 3))
        self.early_livestock_cash_floor = float(
            self.config.get("early_livestock_cash_floor", 1500.0)
        )
        self.early_livestock_batch_size = int(
            self.config.get("early_livestock_batch_size", 2)
        )
        self.early_livestock_activations = 0
        self.early_livestock_units = 0

    def _early_livestock_order(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        day = int(observation.get("day", 0))
        if not (
            self.early_livestock_activation_day
            <= day
            <= self.early_livestock_cutoff_day
        ):
            return
        farm = _farm(observation)
        if len(farm.get("unlocked_quadrants", []) or []) < 2:
            return
        current = _pasture_livestock_resources(observation)
        if current >= self.early_livestock_cap:
            return
        money = float(farm.get("money", 0.0) or 0.0)
        if money < self.early_livestock_cash_floor:
            return
        if self._market_regime(observation) == "service_guard":
            return
        planted = sum(
            1
            for row in farm.get("tiles", []) or []
            for tile in row
            if isinstance(tile, dict) and tile.get("kind") == "PLANT"
        )
        if planted <= 0 and self.latest_target_pastures_built < 2:
            return
        existing_orders = sum(
            max(0, int(order[2]))
            for order in action.get("market", []) or []
            if isinstance(order, list)
            and len(order) >= 3
            and str(order[0]) == "BUY_ANIMAL"
            and str(order[1]) in _PASTURE_LIVESTOCK
        )
        remaining = max(0, self.early_livestock_cap - current - existing_orders)
        if remaining <= 0:
            return
        species = next(
            (
                str(item)
                for item in self.config.get(
                    "early_livestock_species_priority", ["SHEEP", "COW"]
                )
                if str(item) in _PASTURE_LIVESTOCK
            ),
            "SHEEP",
        )
        quantity = min(self.early_livestock_batch_size, remaining)
        if quantity <= 0:
            return
        action.setdefault("market", []).append(["BUY_ANIMAL", species, quantity])
        self.early_livestock_activations += 1
        self.early_livestock_units += quantity

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        self._early_livestock_order(action, observation)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        snapshot = super().telemetry_snapshot()
        snapshot.update(
            {
                "early_livestock_activations": self.early_livestock_activations,
                "early_livestock_units": self.early_livestock_units,
            }
        )
        return snapshot


def create_codex_e17_topology_cap_662_v3(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy: Callable[..., dict[str, Any]] | None = None,
):
    instance = CodexE17TopologyCap662V3Agent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )
    return _wrap_candidate(instance, version=3)


def create_codex_e17_topology_cap_662_v4(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy: Callable[..., dict[str, Any]] | None = None,
):
    instance = CodexE17TopologyCap662V4Agent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )
    return _wrap_candidate(instance, version=4)


def _wrap_candidate(
    instance: CodexE17TopologyCap662V3Agent,
    *,
    version: int,
):
    def policy(
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            setattr(policy, f"codex_e17_topology_662_v{version}_last_error", None)
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            setattr(
                policy,
                f"codex_e17_topology_662_v{version}_last_error",
                instance.last_exception,
            )
            return deepcopy(_SAFE_PASS)

    setattr(policy, f"codex_e17_topology_662_v{version}_instance", instance)
    setattr(policy, f"codex_e17_topology_662_v{version}_last_error", None)
    policy.__name__ = f"codex_e17_3_topology_fill_662_v{version}_policy"
    return policy


__all__ = [
    "DEFAULT_V3_CONFIG_PATH",
    "DEFAULT_V4_CONFIG_PATH",
    "CodexE17TopologyCap662V3Agent",
    "CodexE17TopologyCap662V4Agent",
    "create_codex_e17_topology_cap_662_v3",
    "create_codex_e17_topology_cap_662_v4",
]
