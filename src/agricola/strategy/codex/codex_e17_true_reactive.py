"""E17 Codex market-regime adaptation over the frozen guarded candidate.

Unlike the V1 emergency-only guard, this candidate can change emitted market
orders in normal gameplay when observed prices, liquidity, feed coverage, or
deferred inventory cross preregistered bounds.  Unit routing and the frozen V9
routine remain untouched so the first experiment changes one causal family.
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
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    create_codex_e17_reactive_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_TRUE_REACTIVE_CONFIG_PATH = (
    REPO_ROOT
    / "experiments"
    / "e17"
    / "configs"
    / "codex"
    / "CODEX_E17_1_TRUE_REACTIVE_V2.json"
)
TRUE_REACTIVE_MODEL_SPEC_VERSION = "CODEX-E17.1-TRUE-REACTIVE-V2"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def load_true_reactive_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load and validate the bounded market-regime configuration."""

    config_path = Path(path) if path is not None else DEFAULT_TRUE_REACTIVE_CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E17_1_TRUE_REACTIVE_V2",
        "model_spec_version": TRUE_REACTIVE_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E17.1-3Q-REACTIVE-GUARDED-V1",
        "causal_family": "MARKET_REGIME_ADAPTATION",
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    for key in (
        "turns_per_day",
        "episode_steps",
        "emergency_cash_floor",
        "feed_reserve_per_animal",
        "max_deferral_steps",
        "max_opportunistic_sale_units",
    ):
        if int(config.get(key, -1)) < 0:
            raise ValueError(f"{key} must be non-negative")
    for key in (
        "low_output_price_ratio",
        "high_output_price_ratio",
        "wheat_scarcity_price_ratio",
        "price_recovery_ratio",
        "shed_pressure_ratio",
    ):
        if float(config.get(key, 0.0)) <= 0:
            raise ValueError(f"{key} must be positive")
    if not 0 < float(config["shed_pressure_ratio"]) <= 1:
        raise ValueError("shed_pressure_ratio must be in (0, 1]")
    if not config.get("reference_prices") or not config.get("sellable_products"):
        raise ValueError("reference prices and sellable products are required")
    return deepcopy(config)


def _market_orders(action: dict[str, Any]) -> list[Any]:
    market = action.get("market", [])
    return list(market) if isinstance(market, list) else []


def _private_item_total(private: dict[str, Any], item: str) -> int:
    total = int((private.get("shed", {}) or {}).get(item, 0) or 0)
    for inventory in private.get("inventories", []) or []:
        if isinstance(inventory, dict):
            total += int(inventory.get(item, 0) or 0)
    return total


def _active_animal_count(farm: dict[str, Any]) -> int:
    return sum(
        1
        for row in farm.get("tiles", []) or []
        for tile in row
        if isinstance(tile, dict) and tile.get("animal")
    )


def _shed_total(private: dict[str, Any]) -> int:
    return sum(int(value or 0) for value in (private.get("shed", {}) or {}).values())


def _sell_quantity(orders: list[Any], item: str) -> int:
    return sum(
        max(0, int(order[2]))
        for order in orders
        if isinstance(order, list) and len(order) >= 3 and order[:2] == ["SELL", item]
    )


class CodexE17TrueReactiveAgent:
    """Bounded state-reactive market arbiter with an immutable default provider."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
    ) -> None:
        self.config = load_true_reactive_config(config_path)
        self.run_context = deepcopy(run_context or {})
        self.base_policy = create_codex_e17_reactive_agent(run_context=self.run_context)
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = TRUE_REACTIVE_MODEL_SPEC_VERSION
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.observation_count = 0
        self.override_count = 0
        self.regime_counts: Counter[str] = Counter()
        self.override_reasons: Counter[str] = Counter()
        self.override_records: list[dict[str, Any]] = []
        self.deferred_since: dict[str, int] = {}
        self._pending_record_index: int | None = None

    def _price_ratio(self, item: str, prices: dict[str, Any]) -> float:
        reference = float(self.config["reference_prices"].get(item, 0.0) or 0.0)
        current = float(prices.get(item, 0.0) or 0.0)
        return current / reference if reference > 0 and current > 0 else 1.0

    def _settle_previous_override(self, snapshot: Any) -> None:
        index = self._pending_record_index
        self._pending_record_index = None
        if index is None:
            return
        record = self.override_records[index]
        record["post_state"] = {
            "step": snapshot.clock.step,
            "cash": float(snapshot.farm.get("money", 0.0) or 0.0),
            "shed": deepcopy(snapshot.private.get("shed", {}) or {}),
            "snapshot_fingerprint": snapshot.snapshot_fingerprint,
        }
        record["outcome_evidence"] = (
            "Observed next-state delta; individual market-order attribution remains "
            "UNKNOWN when the emitted batch contains multiple orders."
        )

    def _feed_reserve(self, farm: dict[str, Any]) -> int:
        return _active_animal_count(farm) * int(self.config["feed_reserve_per_animal"])

    def _adapt_market(
        self,
        action: dict[str, Any],
        *,
        snapshot: Any,
    ) -> tuple[list[str], list[str], dict[str, Any]]:
        prices = snapshot.market.get("prices", {}) or {}
        private = snapshot.private
        farm = snapshot.farm
        money = float(farm.get("money", 0.0) or 0.0)
        shed_capacity = int(snapshot.configuration_snapshot["shedCapacity"])
        max_orders = int(snapshot.configuration_snapshot["maxMarketOrdersPerTurn"])
        shed_utilization = _shed_total(private) / max(1, shed_capacity)
        feed_reserve = self._feed_reserve(farm)
        wheat_total = _private_item_total(private, "WHEAT")
        terminal = snapshot.clock.is_terminal_action
        reasons: list[str] = []
        regimes: set[str] = set()
        retained_orders: list[Any] = []
        original_orders = _market_orders(action)

        for raw_order in original_orders:
            if not isinstance(raw_order, list) or len(raw_order) < 3:
                retained_orders.append(raw_order)
                continue
            opcode, item = raw_order[:2]
            if opcode != "SELL" or item not in self.config["reference_prices"]:
                retained_orders.append(raw_order)
                continue
            try:
                quantity = max(0, int(raw_order[2]))
            except (TypeError, ValueError):
                retained_orders.append(raw_order)
                continue
            if quantity <= 0:
                continue

            if (
                item == "WHEAT"
                and self.config["allow_wheat_reserve_protection"]
                and not terminal
            ):
                surplus = max(0, wheat_total - feed_reserve)
                protected_quantity = min(quantity, surplus)
                if protected_quantity < quantity:
                    reasons.append("WHEAT_RESERVE_PROTECTED")
                    regimes.add("INPUT_SCARCITY")
                quantity = protected_quantity
                if quantity <= 0:
                    continue

            item_ratio = self._price_ratio(str(item), prices)
            deferred_at = self.deferred_since.get(str(item))
            max_deferral_reached = (
                deferred_at is not None
                and snapshot.clock.step - deferred_at
                >= int(self.config["max_deferral_steps"])
            )
            may_defer = (
                self.config["allow_low_price_sale_deferral"]
                and not terminal
                and money >= float(self.config["emergency_cash_floor"])
                and shed_utilization < float(self.config["shed_pressure_ratio"])
                and item_ratio <= float(self.config["low_output_price_ratio"])
                and not max_deferral_reached
            )
            if may_defer:
                self.deferred_since.setdefault(str(item), snapshot.clock.step)
                reasons.append("LOW_PRICE_SALE_DEFERRED")
                regimes.add("OUTPUT_PRESSURE")
                continue

            retained_orders.append([*raw_order[:2], quantity, *raw_order[3:]])
            if item_ratio >= float(self.config["price_recovery_ratio"]):
                self.deferred_since.pop(str(item), None)

        action["market"] = retained_orders

        wheat_scarce = self._price_ratio("WHEAT", prices) >= float(
            self.config["wheat_scarcity_price_ratio"]
        )
        if wheat_scarce:
            regimes.add("INPUT_SCARCITY")
        planned_animals = sum(
            max(0, int(order[2]))
            for order in action["market"]
            if isinstance(order, list) and len(order) >= 3 and order[0] == "BUY_ANIMAL"
        )
        projected_feed_reserve = feed_reserve + planned_animals * int(
            self.config["feed_reserve_per_animal"]
        )
        feed_short = wheat_total < projected_feed_reserve
        if (
            wheat_scarce
            and feed_short
            and self.config["allow_scarcity_animal_deferral"]
            and not terminal
        ):
            filtered = [
                order
                for order in action["market"]
                if not (isinstance(order, list) and order and order[0] == "BUY_ANIMAL")
            ]
            if len(filtered) != len(action["market"]):
                action["market"] = filtered
                reasons.append("SCARCITY_ANIMAL_PURCHASE_DEFERRED")
                regimes.add("INPUT_SCARCITY")

        if (
            self.config["allow_high_price_opportunistic_sale"]
            and not terminal
            and len(action["market"]) < max_orders
        ):
            scheduled_items = {
                str(order[1])
                for order in action["market"]
                if isinstance(order, list) and len(order) >= 3 and order[0] == "SELL"
            }
            candidates: list[tuple[int, float, str, int, str]] = []
            shed = private.get("shed", {}) or {}
            for item in self.config["sellable_products"]:
                if item in scheduled_items:
                    continue
                quantity = int(shed.get(item, 0) or 0)
                if item == "WHEAT":
                    quantity = min(quantity, max(0, wheat_total - feed_reserve))
                if quantity <= 0:
                    continue
                item_ratio = self._price_ratio(item, prices)
                recovered_deferred = (
                    item in self.deferred_since
                    and item_ratio >= float(self.config["price_recovery_ratio"])
                )
                forced_release = (
                    item in self.deferred_since
                    and snapshot.clock.step - self.deferred_since[item]
                    >= int(self.config["max_deferral_steps"])
                )
                if (
                    item_ratio >= float(self.config["high_output_price_ratio"])
                    or recovered_deferred
                    or forced_release
                ):
                    candidates.append(
                        (
                            int(forced_release),
                            float(prices.get(item, 0.0) or 0.0),
                            item,
                            quantity,
                            "DEFERRED_SALE_RELEASED"
                            if forced_release
                            else "HIGH_PRICE_OPPORTUNISTIC_SALE",
                        )
                    )
            if candidates:
                _, _, item, available, sale_reason = max(candidates)
                quantity = min(
                    available,
                    int(self.config["max_opportunistic_sale_units"]),
                )
                action["market"].append(["SELL", item, quantity])
                self.deferred_since.pop(item, None)
                reasons.append(sale_reason)
                regimes.add(
                    "OUTPUT_RELEASE"
                    if sale_reason == "DEFERRED_SALE_RELEASED"
                    else "OUTPUT_OPPORTUNITY"
                )

        if money < float(self.config["emergency_cash_floor"]):
            regimes.add("LIQUIDITY_STRESS")
        if not regimes:
            regimes.add("NORMAL")
        facts = {
            "money": money,
            "shed_utilization": round(shed_utilization, 6),
            "active_animals": _active_animal_count(farm),
            "feed_reserve": feed_reserve,
            "planned_animals": planned_animals,
            "projected_feed_reserve": projected_feed_reserve,
            "wheat_total": wheat_total,
            "wheat_price_ratio": round(self._price_ratio("WHEAT", prices), 6),
            "deferred_items": dict(sorted(self.deferred_since.items())),
            "market_orders_before": len(original_orders),
            "market_orders_after": len(action["market"]),
        }
        return sorted(regimes), reasons, facts

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        snapshot = CodexObservationAdapter.parse(
            observation,
            configuration,
            fallback_turns_per_day=int(self.config["turns_per_day"]),
            fallback_episode_steps=int(self.config["episode_steps"]),
        )
        self._settle_previous_override(snapshot)
        provider_action = self.base_policy(observation, configuration)
        action = deepcopy(provider_action)
        regimes, reasons, facts = self._adapt_market(action, snapshot=snapshot)
        self.observation_count += 1
        self.regime_counts.update(regimes)
        if action != provider_action:
            self.override_count += 1
            self.override_reasons.update(reasons or ["UNCLASSIFIED_OVERRIDE"])
            record = {
                "step": snapshot.clock.step,
                "day": snapshot.clock.day,
                "hour": snapshot.clock.hour,
                "state_id": snapshot.state_id,
                "snapshot_fingerprint": snapshot.snapshot_fingerprint,
                "regimes": regimes,
                "reasons": sorted(set(reasons)),
                "facts": facts,
                "provider_action_sha256": stable_payload_hash(provider_action),
                "emitted_action_sha256": stable_payload_hash(action),
                "provider_market": deepcopy(provider_action.get("market", [])),
                "emitted_market": deepcopy(action.get("market", [])),
                "pre_state": {
                    "cash": float(snapshot.farm.get("money", 0.0) or 0.0),
                    "shed": deepcopy(snapshot.private.get("shed", {}) or {}),
                },
                "post_state": None,
                "outcome_evidence": "PENDING_NEXT_OBSERVATION",
            }
            self.override_records.append(record)
            self._pending_record_index = len(self.override_records) - 1
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        provider = self.base_policy.codex_e17_instance.telemetry_snapshot()
        return {
            **provider,
            "agent_version": self.model_spec_version,
            "base_agent_version": provider["agent_version"],
            "observations": self.observation_count,
            "true_reactive_override_batches": self.override_count,
            "true_reactive_override_reasons": dict(self.override_reasons),
            "market_regime_counts": dict(self.regime_counts),
            "true_reactive_override_records": deepcopy(self.override_records),
            "deferred_items_open": dict(sorted(self.deferred_since.items())),
        }


def create_codex_e17_true_reactive_agent(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    """Create a fail-closed Kaggle-compatible true-reactive policy."""

    instance = CodexE17TrueReactiveAgent(
        run_context=run_context,
        config_path=config_path,
    )

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_e17_true_reactive_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e17_true_reactive_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e17_true_reactive_instance = instance
    policy.codex_e17_true_reactive_last_error = None
    policy.__name__ = "codex_e17_1_true_reactive_v2_policy"
    return policy


__all__ = [
    "DEFAULT_TRUE_REACTIVE_CONFIG_PATH",
    "TRUE_REACTIVE_MODEL_SPEC_VERSION",
    "CodexE17TrueReactiveAgent",
    "create_codex_e17_true_reactive_agent",
    "load_true_reactive_config",
]
