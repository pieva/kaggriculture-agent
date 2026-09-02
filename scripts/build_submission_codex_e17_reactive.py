#!/usr/bin/env python3
"""Build the standalone Codex E17.1 reactive Kaggle probe."""

from __future__ import annotations

import hashlib
import json
import pprint
from pathlib import Path

from agricola.strategy.codex.codex_v9_routine_data import (
    ROUTINE_ACTIONS,
    ROUTINE_SHA256,
)

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "submission" / "submission_codex_e17_reactive.py"
SOURCE = ROOT / "src" / "agricola" / "strategy" / "codex" / "codex_e17_reactive_guarded.py"
CONFIG = (
    ROOT
    / "experiments"
    / "e17"
    / "configs"
    / "codex"
    / "CODEX_E17_1_3Q_REACTIVE_GUARDED_V1.json"
)
FREEZE_MANIFEST = (
    ROOT
    / "experiments"
    / "e17"
    / "artifacts"
    / "freeze"
    / "codex"
    / "e17_1"
    / "E17_1_FREEZE_MANIFEST.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _verify_frozen_inputs() -> tuple[dict, dict]:
    manifest = json.loads(FREEZE_MANIFEST.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if manifest.get("status") != "FROZEN_FOR_REACTIVE_TOURNAMENT":
        raise RuntimeError("Codex E17.1 source is not frozen")
    if _sha256(SOURCE) != manifest["source_sha256"]:
        raise RuntimeError("Codex E17.1 source hash differs from the freeze manifest")
    if _sha256(CONFIG) != manifest["config_sha256"]:
        raise RuntimeError("Codex E17.1 config hash differs from the freeze manifest")
    return manifest, config


_TEMPLATE = '''"""Standalone Codex E17.1 3Q reactive guarded Kaggle probe.

The immutable V9 routine remains the default action provider.  The bounded
reactive layer intervenes only for observed WHEAT/feed serviceability risk.
This file is generated from frozen, hash-verified source and configuration.
"""

from collections import Counter
from copy import deepcopy

MODEL_SPEC_VERSION = "__MODEL_SPEC_VERSION__"
PARENT_MODEL_SPEC_VERSION = "CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY"
ROUTINE_SHA256 = "__ROUTINE_SHA256__"
FROZEN_SOURCE_SHA256 = "__SOURCE_SHA256__"
FROZEN_CONFIG_SHA256 = "__CONFIG_SHA256__"
REACTIVE_CONFIG = __REACTIVE_CONFIG__
ROUTINE_ACTIONS = __ROUTINE_ACTIONS__
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def _configuration_value(configuration, name, default):
    if isinstance(configuration, dict):
        return configuration.get(name, default)
    return getattr(configuration, name, default)


def _unit_actions(action):
    return [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]


def _wheat_total(private):
    total = int((private.get("shed", {}) or {}).get("WHEAT", 0) or 0)
    for inventory in private.get("inventories", []) or []:
        if isinstance(inventory, dict):
            total += int(inventory.get("WHEAT", 0) or 0)
    return total


def _market_quantity(action, opcode, item):
    total = 0
    for order in action.get("market", []) or []:
        if isinstance(order, list) and len(order) >= 3 and order[:2] == [opcode, item]:
            try:
                total += max(0, int(order[2]))
            except (TypeError, ValueError):
                continue
    return total


class CodexE17ReactiveStandaloneAgent:
    """Frozen V9 routine plus the bounded E17.1 WHEAT/feed guard."""

    def __init__(self):
        self.config = deepcopy(REACTIVE_CONFIG)
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception = None
        self.override_count = 0
        self.override_reasons = Counter()
        self.detected_unfilled_wheat_units = 0
        self._pending_wheat_buy = None

    @staticmethod
    def _base_action(step):
        action = (
            deepcopy(ROUTINE_ACTIONS[step])
            if 0 <= step < len(ROUTINE_ACTIONS)
            else deepcopy(SAFE_PASS)
        )
        if step == 195:
            for order in action.get("market", []) or []:
                if order[:2] == ["BUY_PRODUCT", "WHEAT"]:
                    order[2] = max(4, int(order[2]))
                    break
            action["market"] = [
                order
                for order in action.get("market", []) or []
                if order[:2] != ["BUY_ANIMAL", "COW"]
            ]
        return action

    @staticmethod
    def _animal_features(farm):
        animals = []
        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict) or not tile.get("animal"):
                    continue
                animals.append(
                    {
                        "position": (x, y),
                        "fed_today": bool(tile.get("fed_today", False)),
                        "consecutive_unfed": int(tile.get("consecutive_unfed", 0) or 0),
                    }
                )
        return animals

    @staticmethod
    def _positions_and_inventories(farm, private):
        positions = [
            tuple(farm.get("farmer", [4, 4])),
            *(tuple(value) for value in farm.get("hands", []) or []),
        ]
        inventories = [
            value if isinstance(value, dict) else {}
            for value in (private.get("inventories", []) or [])
        ]
        if len(inventories) < len(positions):
            inventories.extend({} for _ in range(len(positions) - len(inventories)))
        return positions, inventories

    @staticmethod
    def _scheduled_feed_positions(action, farm):
        positions = [
            tuple(farm.get("farmer", [4, 4])),
            *(tuple(value) for value in farm.get("hands", []) or []),
        ]
        return {
            positions[index]
            for index, unit_action in enumerate(_unit_actions(action))
            if index < len(positions) and unit_action and unit_action[0] == "FEED"
        }

    def _apply_critical_feed_overrides(self, action, farm, private, critical_positions):
        if not self.config["allow_critical_feed_override"] or not critical_positions:
            return []
        positions, inventories = self._positions_and_inventories(farm, private)
        actions = _unit_actions(action)
        reasons = []
        for worker_id, position in enumerate(positions):
            if worker_id >= len(actions) or position not in critical_positions:
                continue
            if int(inventories[worker_id].get("WHEAT", 0) or 0) <= 0:
                continue
            if actions[worker_id] and actions[worker_id][0] == "FEED":
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

    def _settle_previous_wheat_buy(self, wheat_total, step):
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

    def _remember_wheat_buy(self, action, wheat_total, step):
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
        action,
        active_animals,
        wheat_total,
        money,
        wheat_price,
        max_orders,
        detected_unfilled_wheat,
        critical_eod,
    ):
        if active_animals <= 0 or not (detected_unfilled_wheat or critical_eod):
            return []
        reasons = []
        feed_requests = sum(
            1
            for unit_action in _unit_actions(action)
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
            new_market = []
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

    def __call__(self, observation, configuration=None):
        step = int(observation["step"])
        if step == 0:
            self._pending_wheat_buy = None
        turns_per_day = int(
            _configuration_value(configuration, "turnsPerDay", self.config["turns_per_day"])
        )
        day = int(observation.get("day", step // turns_per_day))
        hour = int(observation.get("hour", step % turns_per_day))
        if step != day * turns_per_day + hour:
            raise ValueError("invalid observation clock")
        player = int(observation.get("player", 0))
        farms = observation.get("farms", []) or []
        farm = farms[player]
        private = observation.get("private", {}) or {}
        market_state = observation.get("market", {}) or {}

        baseline = self._base_action(step)
        action = deepcopy(baseline)
        animals = self._animal_features(farm)
        wheat_total = _wheat_total(private)
        detected_unfilled_wheat = self._settle_previous_wheat_buy(wheat_total, step)
        threshold = int(self.config["critical_unfed_threshold"])
        critical_positions = {
            entry["position"]
            for entry in animals
            if not entry["fed_today"] and entry["consecutive_unfed"] >= threshold
        }
        critical_positions.difference_update(self._scheduled_feed_positions(action, farm))
        uncovered_critical_count = len(critical_positions)
        reasons = []
        is_eod = hour == turns_per_day - 1
        if is_eod:
            reasons.extend(
                self._apply_critical_feed_overrides(
                    action, farm, private, critical_positions
                )
            )
        prices = market_state.get("prices", {}) or {}
        reasons.extend(
            self._apply_market_guard(
                action=action,
                active_animals=len(animals),
                wheat_total=wheat_total,
                money=float(farm.get("money", 0.0) or 0.0),
                wheat_price=float(prices.get("WHEAT", 1.0) or 1.0),
                max_orders=int(
                    _configuration_value(configuration, "maxMarketOrdersPerTurn", 10)
                ),
                detected_unfilled_wheat=detected_unfilled_wheat,
                critical_eod=is_eod and uncovered_critical_count > 0,
            )
        )
        self._remember_wheat_buy(action, wheat_total, step)
        if action != baseline:
            self.override_count += 1
            self.override_reasons.update(reasons or ["UNCLASSIFIED_OVERRIDE"])
        return action


def create_agent(run_context=None):
    del run_context
    instance = CodexE17ReactiveStandaloneAgent()

    def policy(observation, configuration=None):
        try:
            action = instance(observation, configuration)
            policy.codex_e17_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed Kaggle boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e17_last_error = instance.last_exception
            return deepcopy(SAFE_PASS)

    policy.codex_e17_instance = instance
    policy.codex_e17_last_error = None
    return policy


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)
'''


def build_submission_codex_e17_reactive(output_path: Path | str | None = None) -> Path:
    """Generate the separate E17.1 reactive probe without touching E17.0."""

    manifest, config = _verify_frozen_inputs()
    target = Path(output_path) if output_path is not None else TARGET
    body = (
        _TEMPLATE.replace("__MODEL_SPEC_VERSION__", manifest["policy_version"])
        .replace("__ROUTINE_SHA256__", ROUTINE_SHA256)
        .replace("__SOURCE_SHA256__", manifest["source_sha256"])
        .replace("__CONFIG_SHA256__", manifest["config_sha256"])
        .replace(
            "__REACTIVE_CONFIG__",
            pprint.pformat(config, width=100, sort_dicts=False),
        )
        .replace(
            "__ROUTINE_ACTIONS__",
            pprint.pformat(ROUTINE_ACTIONS, width=100, sort_dicts=False),
        )
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8", newline="\n")
    return target


def main() -> int:
    target = build_submission_codex_e17_reactive()
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
