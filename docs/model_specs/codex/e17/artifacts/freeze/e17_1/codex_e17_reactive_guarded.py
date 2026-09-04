"""E17.1 reactive guard layered over the frozen Codex V9 3Q routine.

The V9 action remains the default provider.  This module changes it only for
one causal family: animal feed serviceability under observed WHEAT scarcity or
critical hunger.  Every changed batch is retained in an auditable override
record; the frozen V9 source and the Kaggle submission are never mutated.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import (
    CodexObservationAdapter,
    stable_payload_hash,
)
from agricola.strategy.codex.codex_3q_mixed_high_density import create_v9_agent

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_REACTIVE_CONFIG_PATH = (
    REPO_ROOT
    / "experiments"
    / "e17"
    / "configs"
    / "codex"
    / "CODEX_E17_1_3Q_REACTIVE_GUARDED_V1.json"
)
REACTIVE_MODEL_SPEC_VERSION = "CODEX-E17.1-3Q-REACTIVE-GUARDED-V1"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def load_reactive_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load the bounded E17.1 guard configuration."""

    config_path = Path(path) if path is not None else DEFAULT_REACTIVE_CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("candidate_id") != "CODEX_E17_1_3Q_REACTIVE_GUARDED_V1":
        raise ValueError("unexpected E17.1 candidate_id")
    if config.get("model_spec_version") != REACTIVE_MODEL_SPEC_VERSION:
        raise ValueError("unexpected E17.1 model_spec_version")
    if config.get("base_policy") != "CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY":
        raise ValueError("E17.1 must use the frozen Codex V9 as default provider")
    if config.get("causal_family") != "WHEAT_FEED_SERVICEABILITY":
        raise ValueError("E17.1 is restricted to WHEAT/feed serviceability")
    for key in (
        "turns_per_day",
        "episode_steps",
        "feed_reserve_rounds",
        "critical_unfed_threshold",
        "max_extra_wheat_per_step",
        "operating_cash_floor",
    ):
        if int(config.get(key, -1)) < 0:
            raise ValueError(f"{key} must be non-negative")
    if int(config["turns_per_day"]) <= 0 or int(config["episode_steps"]) <= 0:
        raise ValueError("clock dimensions must be positive")
    return deepcopy(config)


def _unit_actions(action: dict[str, Any]) -> list[list[Any]]:
    return [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]


def _wheat_total(private: dict[str, Any]) -> int:
    total = int((private.get("shed", {}) or {}).get("WHEAT", 0) or 0)
    for inventory in private.get("inventories", []) or []:
        if isinstance(inventory, dict):
            total += int(inventory.get("WHEAT", 0) or 0)
    return total


def _market_quantity(action: dict[str, Any], opcode: str, item: str) -> int:
    total = 0
    for order in action.get("market", []) or []:
        if isinstance(order, list) and len(order) >= 3 and order[:2] == [opcode, item]:
            try:
                total += max(0, int(order[2]))
            except (TypeError, ValueError):
                continue
    return total


class CodexE17ReactiveGuardedAgent:
    """State-reactive WHEAT/feed guard with immutable V9 defaults."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
    ) -> None:
        self.config = load_reactive_config(config_path)
        self.run_context = deepcopy(run_context or {})
        self.base_policy = create_v9_agent(run_context=self.run_context)
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = REACTIVE_MODEL_SPEC_VERSION
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.override_count = 0
        self.override_reasons: Counter[str] = Counter()
        self.override_records: list[dict[str, Any]] = []
        self.observation_count = 0
        self.detected_unfilled_wheat_units = 0
        self._pending_wheat_buy: dict[str, int] | None = None

    @staticmethod
    def _animal_features(farm: dict[str, Any]) -> dict[str, Any]:
        animals: list[dict[str, Any]] = []
        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict) or not tile.get("animal"):
                    continue
                animals.append(
                    {
                        "position": (x, y),
                        "animal": str(tile["animal"]),
                        "fed_today": bool(tile.get("fed_today", False)),
                        "consecutive_unfed": int(tile.get("consecutive_unfed", 0) or 0),
                    }
                )
        return {
            "animals": animals,
            "active_animals": len(animals),
        }

    @staticmethod
    def _positions_and_inventories(
        farm: dict[str, Any], private: dict[str, Any]
    ) -> tuple[list[tuple[int, int]], list[dict[str, Any]]]:
        positions = [
            tuple(farm.get("farmer", [4, 4])),
            *(tuple(value) for value in farm.get("hands", []) or []),
        ]
        raw_inventories = private.get("inventories", []) or []
        inventories = [
            value if isinstance(value, dict) else {} for value in raw_inventories
        ]
        if len(inventories) < len(positions):
            inventories.extend({} for _ in range(len(positions) - len(inventories)))
        return positions, inventories

    def _apply_critical_feed_overrides(
        self,
        action: dict[str, Any],
        farm: dict[str, Any],
        private: dict[str, Any],
        critical_positions: set[tuple[int, int]],
    ) -> list[str]:
        if not self.config["allow_critical_feed_override"] or not critical_positions:
            return []
        positions, inventories = self._positions_and_inventories(farm, private)
        actions = _unit_actions(action)
        reasons: list[str] = []
        for worker_id, position in enumerate(positions):
            if worker_id >= len(actions) or position not in critical_positions:
                continue
            inventory = inventories[worker_id]
            if int(inventory.get("WHEAT", 0) or 0) <= 0:
                continue
            unit_action = actions[worker_id]
            if unit_action and unit_action[0] == "FEED":
                continue
            if worker_id == 0:
                action["farmer"] = ["FEED"]
            else:
                hands = action.setdefault("hands", [])
                while len(hands) < worker_id:
                    hands.append(["PASS"])
                hands[worker_id - 1] = ["FEED"]
            reasons.append("CRITICAL_FEED_OVERRIDE")
            critical_positions.remove(position)
            if not critical_positions:
                break
        return reasons

    @staticmethod
    def _scheduled_feed_positions(
        action: dict[str, Any], farm: dict[str, Any]
    ) -> set[tuple[int, int]]:
        positions = [
            tuple(farm.get("farmer", [4, 4])),
            *(tuple(value) for value in farm.get("hands", []) or []),
        ]
        return {
            positions[index]
            for index, unit_action in enumerate(_unit_actions(action))
            if index < len(positions) and unit_action and unit_action[0] == "FEED"
        }

    def _settle_previous_wheat_buy(self, wheat_total: int, step: int) -> int:
        """Conservatively infer an unfilled WHEAT quantity from the next state.

        Requested FEED and WHEAT sales are subtracted even when they may have
        failed.  WHEAT harvests are not imputed.  Both choices bias the result
        against false claims of market non-execution.
        """

        pending = self._pending_wheat_buy
        self._pending_wheat_buy = None
        if not self.config["market_fill_tracking"] or pending is None:
            return 0
        if step <= pending["step"]:
            return 0
        expected_without_buy = max(
            0,
            pending["wheat_total"]
            - pending["feed_requests"]
            - pending["wheat_sell_requests"],
        )
        observed_gain = max(0, wheat_total - expected_without_buy)
        inferred_fill = min(pending["requested"], observed_gain)
        shortfall = max(0, pending["requested"] - inferred_fill)
        self.detected_unfilled_wheat_units += shortfall
        return shortfall

    def _remember_wheat_buy(
        self, action: dict[str, Any], *, wheat_total: int, step: int
    ) -> None:
        requested = _market_quantity(action, "BUY_PRODUCT", "WHEAT")
        if requested <= 0:
            self._pending_wheat_buy = None
            return
        self._pending_wheat_buy = {
            "step": step,
            "requested": requested,
            "wheat_total": wheat_total,
            "feed_requests": sum(
                1
                for unit_action in _unit_actions(action)
                if unit_action and unit_action[0] == "FEED"
            ),
            "wheat_sell_requests": _market_quantity(action, "SELL", "WHEAT"),
        }

    def _apply_market_guard(
        self,
        action: dict[str, Any],
        *,
        active_animals: int,
        wheat_total: int,
        money: float,
        wheat_price: float,
        max_orders: int,
        detected_unfilled_wheat: int,
        critical_eod: bool,
    ) -> list[str]:
        if active_animals <= 0 or not (detected_unfilled_wheat or critical_eod):
            return []
        reasons: list[str] = []
        feed_requests = sum(
            1 for unit_action in _unit_actions(action)
            if unit_action and unit_action[0] == "FEED"
        )
        target = active_animals * int(self.config["feed_reserve_rounds"])
        buys = _market_quantity(action, "BUY_PRODUCT", "WHEAT")
        sells = _market_quantity(action, "SELL", "WHEAT")
        projected = wheat_total - feed_requests + buys - sells
        shortfall = max(detected_unfilled_wheat, target - projected, 0)
        market = action.setdefault("market", [])

        if shortfall and sells and self.config["allow_wheat_sale_reduction"]:
            remaining = shortfall
            new_market: list[list[Any]] = []
            for order in market:
                if (
                    remaining > 0
                    and isinstance(order, list)
                    and len(order) >= 3
                    and order[:2] == ["SELL", "WHEAT"]
                ):
                    quantity = max(0, int(order[2]))
                    reduction = min(quantity, remaining)
                    quantity -= reduction
                    remaining -= reduction
                    if quantity > 0:
                        new_market.append([*order[:2], quantity, *order[3:]])
                    reasons.append("WHEAT_SALE_REDUCED")
                else:
                    new_market.append(order)
            action["market"] = market = new_market
            shortfall = remaining

        if shortfall:
            price = max(1.0, float(wheat_price or 1.0))
            spendable = max(0.0, float(money) - int(self.config["operating_cash_floor"]))
            affordable_total = int(spendable // price)
            existing_buys = _market_quantity(action, "BUY_PRODUCT", "WHEAT")
            affordable_extra = max(0, affordable_total - existing_buys)
            extra = min(
                shortfall,
                int(self.config["max_extra_wheat_per_step"]),
                affordable_extra,
            )
            if extra > 0:
                purchase_added = False
                for order in market:
                    if (
                        isinstance(order, list)
                        and len(order) >= 3
                        and order[:2] == ["BUY_PRODUCT", "WHEAT"]
                    ):
                        order[2] = int(order[2]) + extra
                        reasons.append("WHEAT_BUY_INCREASED")
                        purchase_added = True
                        break
                else:
                    if self.config["allow_market_buy_append"] and len(market) < max_orders:
                        market.append(["BUY_PRODUCT", "WHEAT", extra])
                        reasons.append("WHEAT_BUY_APPENDED")
                        purchase_added = True
                if purchase_added:
                    shortfall -= extra

        if shortfall and self.config["allow_animal_purchase_deferral"]:
            filtered = [
                order
                for order in market
                if not (
                    isinstance(order, list)
                    and len(order) >= 2
                    and order[0] == "BUY_ANIMAL"
                )
            ]
            if len(filtered) != len(market):
                action["market"] = filtered
                reasons.append("ANIMAL_PURCHASE_DEFERRED")
        return reasons

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        snapshot = CodexObservationAdapter.parse(
            observation,
            configuration,
            fallback_turns_per_day=int(self.config["turns_per_day"]),
            fallback_episode_steps=int(self.config["episode_steps"]),
        )
        baseline = self.base_policy(observation, configuration)
        action = deepcopy(baseline)
        features = self._animal_features(snapshot.farm)
        wheat_total = _wheat_total(snapshot.private)
        detected_unfilled_wheat = self._settle_previous_wheat_buy(
            wheat_total,
            snapshot.clock.step,
        )
        threshold = int(self.config["critical_unfed_threshold"])
        critical_positions = {
            entry["position"]
            for entry in features["animals"]
            if not entry["fed_today"] and entry["consecutive_unfed"] >= threshold
        }
        critical_animal_count = len(critical_positions)
        critical_positions.difference_update(
            self._scheduled_feed_positions(action, snapshot.farm)
        )
        uncovered_critical_count = len(critical_positions)
        reasons: list[str] = []
        if snapshot.clock.is_eod:
            reasons.extend(
                self._apply_critical_feed_overrides(
                    action,
                    snapshot.farm,
                    snapshot.private,
                    critical_positions,
                )
            )
        prices = snapshot.market.get("prices", {}) or {}
        reasons.extend(
            self._apply_market_guard(
                action,
                active_animals=int(features["active_animals"]),
                wheat_total=wheat_total,
                money=float(snapshot.farm.get("money", 0.0) or 0.0),
                wheat_price=float(prices.get("WHEAT", 1.0) or 1.0),
                max_orders=int(snapshot.configuration_snapshot["maxMarketOrdersPerTurn"]),
                detected_unfilled_wheat=detected_unfilled_wheat,
                critical_eod=snapshot.clock.is_eod and uncovered_critical_count > 0,
            )
        )
        self._remember_wheat_buy(
            action,
            wheat_total=wheat_total,
            step=snapshot.clock.step,
        )
        self.observation_count += 1
        if action != baseline:
            self.override_count += 1
            self.override_reasons.update(reasons or ["UNCLASSIFIED_OVERRIDE"])
            self.override_records.append(
                {
                    "step": snapshot.clock.step,
                    "day": snapshot.clock.day,
                    "hour": snapshot.clock.hour,
                    "state_id": snapshot.state_id,
                    "snapshot_fingerprint": snapshot.snapshot_fingerprint,
                    "active_animals": int(features["active_animals"]),
                    "critical_animals": critical_animal_count,
                    "uncovered_critical_animals": uncovered_critical_count,
                    "detected_unfilled_wheat": detected_unfilled_wheat,
                    "wheat_total": wheat_total,
                    "reasons": sorted(set(reasons)),
                    "baseline_action_sha256": stable_payload_hash(baseline),
                    "emitted_action_sha256": stable_payload_hash(action),
                }
            )
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = self.base_policy.codex_v9_instance.telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "base_agent_version": base["agent_version"],
            "observations": self.observation_count,
            "reactive_override_batches": self.override_count,
            "reactive_override_reasons": dict(self.override_reasons),
            "reactive_override_records": deepcopy(self.override_records),
            "detected_unfilled_wheat_units": self.detected_unfilled_wheat_units,
        }


def create_codex_e17_reactive_agent(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    """Create a fail-closed Kaggle-compatible E17.1 reactive policy."""

    instance = CodexE17ReactiveGuardedAgent(
        run_context=run_context,
        config_path=config_path,
    )

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_e17_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e17_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e17_instance = instance
    policy.codex_e17_last_error = None
    policy.__name__ = "codex_e17_1_3q_reactive_guarded_policy"
    return policy


__all__ = [
    "DEFAULT_REACTIVE_CONFIG_PATH",
    "REACTIVE_MODEL_SPEC_VERSION",
    "CodexE17ReactiveGuardedAgent",
    "create_codex_e17_reactive_agent",
    "load_reactive_config",
]
