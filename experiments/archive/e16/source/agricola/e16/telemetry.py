"""Exact engine-level event ledger and E16 state telemetry."""

from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict
from contextlib import AbstractContextManager
from copy import deepcopy
from itertools import pairwise
from types import TracebackType
from typing import Any, Self

LEDGER_REQUIRED_FIELDS = {
    "design_id",
    "stage",
    "cell_id",
    "episode_id",
    "seed",
    "treatment_seat",
    "player",
    "seat",
    "actor_role",
    "step",
    "day",
    "hour",
    "actor_or_order_id",
    "actor_or_order_type",
    "unit_index",
    "target_tile_or_commodity",
    "requested_payload",
    "engine_applied_payload",
    "executed_payload",
    "success",
    "failure_or_noop_reason",
    "requested_quantity",
    "executed_quantity",
    "displayed_price_at_request",
    "realized_price",
    "realized_value",
    "cash_flow_category",
    "cash_before",
    "cash_after",
    "relevant_state_before",
    "relevant_state_after",
    "provenance",
    "treatment_build_sha256",
    "opponent_sha256",
    "engine_version",
    "configuration_sha256",
    "quadrants_owned",
    "execution_status",
    "lifecycle_statuses",
    "attribution_status",
}


def _plain(value: Any) -> Any:
    if isinstance(value, dict) or hasattr(value, "items"):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _owned_quadrants(farm: Any) -> int:
    raw = farm.get("unlocked_quadrants", ["NW"])
    return len(raw) if isinstance(raw, list) else int(raw)


def _actor_snapshot(engine: Any, farm: Any, private: Any, idx: int) -> dict[str, Any]:
    position = engine._farmer_position(farm, idx)
    inventory = private.get("inventories", [])
    actor_inventory = inventory[idx] if idx < len(inventory) else {}
    tile = None
    if position is not None:
        tile = farm["tiles"][position[1]][position[0]]
    return {
        "position": _plain(position),
        "inventory": _plain(actor_inventory),
        "tile": _plain(tile),
        "shed": _plain(private.get("shed", {})),
        "seeds": _plain(private.get("seeds", {})),
        "money": float(farm.get("money", 0.0)),
    }


class EngineEventLedger(AbstractContextManager["EngineEventLedger"]):
    """Wrap mutating engine functions and record their actual effects.

    The wrappers call the original engine functions exactly once. They observe
    mutation at the point it occurs, before town consumption and daily refresh
    can obscure attribution.
    """

    def __init__(self, metadata: dict[str, Any]):
        self.metadata = deepcopy(metadata)
        self.events: list[dict[str, Any]] = []
        self._originals: dict[str, Any] = {}
        self._farm_players: dict[int, int] = {}
        self._state: Any = None
        self._market_requests: dict[int, list[dict[str, Any]]] | None = None
        self._expected_players = 0
        self._current_unit_player = -1
        self._unit_blocks_seen = 0

    def __enter__(self) -> Self:
        from kaggle_environments.envs.kaggriculture import kaggriculture as engine

        self.engine = engine
        for name in (
            "_initialize",
            "_apply_unit_action",
            "_process_market",
            "_commit_unit",
            "_do_hire",
            "_do_buy_land",
        ):
            self._originals[name] = getattr(engine, name)

        def initialize(state: Any, env: Any) -> Any:
            result = self._originals["_initialize"](state, env)
            self._register_state(state)
            self._reset_unit_cycle()
            return result

        def apply_unit_action(
            farm: Any,
            private: Any,
            idx: int,
            action: Any,
            board_size: int,
            day: int,
            turns_per_day: int,
            shed_capacity: int = 100,
        ) -> Any:
            player = self._bind_unit_player(idx)
            requested = self._raw_unit_request(player, idx, action)
            applied = _plain(action)
            before = _actor_snapshot(engine, farm, private, idx)
            result = self._originals["_apply_unit_action"](
                farm,
                private,
                idx,
                action,
                board_size,
                day,
                turns_per_day,
                shed_capacity,
            )
            after = _actor_snapshot(engine, farm, private, idx)
            changed = before != after
            op = (
                requested[0]
                if isinstance(requested, list) and requested
                else "MALFORMED"
            )
            final_status = (
                "executed" if changed else ("no_op" if op == "PASS" else "failed")
            )
            reason = (
                None
                if changed
                else self._unit_failure_reason(requested, action, before)
            )
            self.events.append(
                self._base_event(
                    player=player,
                    actor_id=f"unit:{idx}",
                    actor_type="farmer" if idx == 0 else "farm_hand",
                    unit_index=idx,
                    target=self._unit_target(requested, before),
                    requested=requested,
                    applied=applied,
                    executed=applied if changed else None,
                    success=changed,
                    reason=reason,
                    requested_quantity=1,
                    executed_quantity=1 if changed else 0,
                    displayed_price=None,
                    realized_price=None,
                    realized_value=None,
                    cash_category="none",
                    cash_before=before["money"],
                    cash_after=after["money"],
                    state_before=before,
                    state_after=after,
                    status=final_status,
                )
            )
            return result

        def process_market(state: Any, env: Any) -> Any:
            self._validate_unit_cycle()
            self._register_state(state)
            self._begin_market(state, env)
            result = self._originals["_process_market"](state, env)
            self._finish_market(state)
            self._reset_unit_cycle()
            return result

        def commit_unit(
            op: str,
            item: str,
            price: float,
            farm: Any,
            private: Any,
            market: Any,
            shed_capacity: int = 100,
        ) -> bool:
            before_cash = float(farm.get("money", 0.0))
            before_private = _plain(private)
            ok = self._originals["_commit_unit"](
                op, item, price, farm, private, market, shed_capacity
            )
            if ok:
                self._record_market_unit(
                    self._market_player(farm),
                    op,
                    item,
                    float(price),
                    before_cash,
                    float(farm.get("money", 0.0)),
                    before_private,
                    _plain(private),
                )
            return ok

        def do_hire(farm: Any, private: Any, board_size: int, mult: int = 1) -> Any:
            before_cash = float(farm.get("money", 0.0))
            before_count = len(farm.get("hands", []))
            result = self._originals["_do_hire"](farm, private, board_size, mult)
            if len(farm.get("hands", [])) > before_count:
                self._record_market_unit(
                    self._market_player(farm),
                    "HIRE",
                    None,
                    before_cash - float(farm.get("money", 0.0)),
                    before_cash,
                    float(farm.get("money", 0.0)),
                    {"hands": before_count},
                    {"hands": len(farm.get("hands", []))},
                )
            return result

        def do_buy_land(farm: Any, board_size: int) -> Any:
            before_cash = float(farm.get("money", 0.0))
            before_count = _owned_quadrants(farm)
            result = self._originals["_do_buy_land"](farm, board_size)
            if _owned_quadrants(farm) > before_count:
                self._record_market_unit(
                    self._market_player(farm),
                    "BUY_LAND",
                    None,
                    before_cash - float(farm.get("money", 0.0)),
                    before_cash,
                    float(farm.get("money", 0.0)),
                    {"quadrants_owned": before_count},
                    {"quadrants_owned": _owned_quadrants(farm)},
                )
            return result

        engine._initialize = initialize
        engine._apply_unit_action = apply_unit_action
        engine._process_market = process_market
        engine._commit_unit = commit_unit
        engine._do_hire = do_hire
        engine._do_buy_land = do_buy_land
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        for name, original in self._originals.items():
            setattr(self.engine, name, original)
        self._market_requests = None
        return False

    def _register_state(self, state: Any) -> None:
        self._state = state
        if not state:
            return
        self._expected_players = len(state)
        farms = state[0].observation.get("farms", [])
        self._farm_players = {id(farm): player for player, farm in enumerate(farms)}

    def _reset_unit_cycle(self) -> None:
        self._current_unit_player = -1
        self._unit_blocks_seen = 0

    def _bind_unit_player(self, unit_index: int) -> int:
        if self._expected_players <= 0:
            raise RuntimeError("unit attribution requested before state registration")
        if unit_index == 0:
            self._current_unit_player += 1
            self._unit_blocks_seen += 1
        elif self._current_unit_player < 0:
            raise RuntimeError("farm-hand action precedes its player farmer block")
        if not 0 <= self._current_unit_player < self._expected_players:
            raise RuntimeError("unit player cycle exceeds registered players")
        return self._current_unit_player

    def _validate_unit_cycle(self) -> None:
        if self._unit_blocks_seen != self._expected_players:
            raise RuntimeError(
                "unit player cycle does not contain exactly one block per player"
            )

    def _market_player(self, farm: Any) -> int:
        player = self._farm_players.get(id(farm))
        if player is None:
            raise RuntimeError("market farm cannot be attributed to a player")
        return player

    def _step_context(self) -> tuple[int, int, int]:
        if self._state is None or not self._state:
            return 0, 0, 0
        obs = self._state[0].observation
        step = int(obs.get("step", 0))
        day = int(obs.get("day", step // 24))
        hour = int(obs.get("hour", step % 24))
        return step, day, hour

    def _raw_unit_request(self, player: int, idx: int, fallback: Any) -> Any:
        if self._state is None or player < 0 or player >= len(self._state):
            return _plain(fallback)
        action = self._state[player].action
        if not isinstance(action, dict):
            return ["PASS"]
        if idx == 0:
            return _plain(action.get("farmer", ["PASS"]))
        hands = action.get("hands", [])
        if isinstance(hands, list) and idx - 1 < len(hands):
            return _plain(hands[idx - 1])
        return ["PASS"]

    @staticmethod
    def _unit_target(action: Any, before: dict[str, Any]) -> Any:
        if not isinstance(action, list) or not action:
            return before.get("position")
        if (
            action[0] in {"BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL"}
            and len(action) > 1
        ):
            return action[1]
        return before.get("position")

    @staticmethod
    def _unit_failure_reason(
        requested: Any, applied: Any, before: dict[str, Any]
    ) -> str:
        if not isinstance(requested, list) or not requested:
            return "malformed_action"
        if requested[0] == "PASS":
            return "explicit_pass"
        if requested != _plain(applied) and requested[0] == "PLANT":
            return "atomic_seed_validation_rejection"
        if before.get("position") is None:
            return "actor_not_active"
        return "engine_illegal_or_unsatisfied_precondition"

    def _begin_market(self, state: Any, env: Any) -> None:
        max_orders = max(1, int(env.configuration.get("maxMarketOrdersPerTurn", 10)))
        obs = state[0].observation
        prices = obs.market.get("prices", {})
        requests: dict[int, list[dict[str, Any]]] = {}
        for player, item in enumerate(state):
            action = item.action if isinstance(item.action, dict) else {}
            raw_orders = action.get("market", []) if isinstance(action, dict) else []
            raw_orders = raw_orders if isinstance(raw_orders, list) else []
            player_requests = []
            for index, raw in enumerate(raw_orders):
                valid, op, commodity, quantity = self._parse_market_order(raw)
                displayed = None
                if commodity is not None:
                    displayed = prices.get(commodity)
                if op == "BUY_SEED" and commodity in self.engine.CROPS:
                    displayed = self.engine.CROPS[commodity]["seed"]
                elif op == "BUY_ANIMAL" and commodity in self.engine.ANIMALS:
                    displayed = self.engine.ANIMALS[commodity]["cost"]
                elif op == "HIRE":
                    displayed = self.engine._hire_cost(
                        obs.farms[player].get("hires_today", 0)
                    )
                elif op == "BUY_LAND":
                    extra = _owned_quadrants(obs.farms[player]) - 1
                    displayed = (
                        self.engine.LAND_PRICES[extra]
                        if extra < len(self.engine.LAND_PRICES)
                        else None
                    )
                player_requests.append(
                    {
                        "index": index,
                        "raw": _plain(raw),
                        "valid": valid and index < max_orders,
                        "op": op,
                        "commodity": commodity,
                        "requested_quantity": quantity,
                        "remaining": quantity,
                        "executions": [],
                        "displayed": float(displayed)
                        if displayed is not None
                        else None,
                        "cash_before": float(obs.farms[player].get("money", 0.0)),
                        "state_before": {
                            "shed": _plain(item.observation.private.get("shed", {})),
                            "seeds": _plain(item.observation.private.get("seeds", {})),
                            "hands": len(obs.farms[player].get("hands", [])),
                            "quadrants_owned": _owned_quadrants(obs.farms[player]),
                        },
                        "failure": "order_limit_rejection"
                        if index >= max_orders
                        else (None if valid else "malformed_order"),
                    }
                )
            requests[player] = player_requests
        self._market_requests = requests

    @staticmethod
    def _parse_market_order(raw: Any) -> tuple[bool, str | None, str | None, int]:
        if not isinstance(raw, list) or not raw:
            return False, None, None, 0
        op = raw[0]
        if op in {"HIRE", "BUY_LAND"}:
            return True, op, None, 1
        if op not in {"BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL"} or len(raw) < 3:
            return False, op, raw[1] if len(raw) > 1 else None, 0
        try:
            quantity = int(raw[2])
        except (TypeError, ValueError):
            return False, op, raw[1], 0
        return quantity > 0, op, raw[1], max(0, quantity)

    def _record_market_unit(
        self,
        player: int,
        op: str,
        item: str | None,
        price: float,
        cash_before: float,
        cash_after: float,
        state_before: Any,
        state_after: Any,
    ) -> None:
        if self._market_requests is None or player not in self._market_requests:
            return
        for request in self._market_requests[player]:
            if (
                request["valid"]
                and request["op"] == op
                and request["commodity"] == item
                and request["remaining"] > 0
            ):
                request["executions"].append(
                    {
                        "price": float(price),
                        "cash_before": cash_before,
                        "cash_after": cash_after,
                        "state_before": state_before,
                        "state_after": state_after,
                    }
                )
                request["remaining"] -= 1
                return

    def _finish_market(self, state: Any) -> None:
        if self._market_requests is None:
            return
        obs = state[0].observation
        for player, requests in self._market_requests.items():
            farm = obs.farms[player]
            private = state[player].observation.private
            for request in requests:
                executions = request["executions"]
                executed_quantity = len(executions)
                requested_quantity = int(request["requested_quantity"])
                if executed_quantity == requested_quantity and requested_quantity > 0:
                    status = "executed"
                elif executed_quantity > 0:
                    status = "partially_executed"
                else:
                    status = "failed"
                if status == "failed" and request["failure"] is None:
                    request["failure"] = (
                        "insufficient_cash_inventory_capacity_or_eligibility"
                    )
                prices = [entry["price"] for entry in executions]
                realized_value = sum(prices)
                category = self._cash_category(request["op"], request["commodity"])
                self.events.append(
                    self._base_event(
                        player=player,
                        actor_id=f"market:{request['index']}",
                        actor_type="market_order",
                        unit_index=None,
                        target=request["commodity"] or request["op"],
                        requested=request["raw"],
                        applied=request["raw"],
                        executed={
                            "type": request["op"],
                            "item": request["commodity"],
                            "quantity": executed_quantity,
                        }
                        if executed_quantity
                        else None,
                        success=executed_quantity > 0,
                        reason=request["failure"]
                        if status == "failed"
                        else (
                            "quantity_shortfall"
                            if status == "partially_executed"
                            else None
                        ),
                        requested_quantity=requested_quantity,
                        executed_quantity=executed_quantity,
                        displayed_price=request["displayed"],
                        realized_price=(realized_value / executed_quantity)
                        if executed_quantity
                        else None,
                        realized_value=realized_value if executed_quantity else None,
                        cash_category=category,
                        cash_before=executions[0]["cash_before"]
                        if executions
                        else request["cash_before"],
                        cash_after=float(farm.get("money", 0.0))
                        if not executions
                        else executions[-1]["cash_after"],
                        state_before=request["state_before"],
                        state_after={
                            "shed": _plain(private.get("shed", {})),
                            "seeds": _plain(private.get("seeds", {})),
                            "hands": len(farm.get("hands", [])),
                            "quadrants_owned": _owned_quadrants(farm),
                        },
                        status=status,
                    )
                )
        self._market_requests = None

    @staticmethod
    def _cash_category(op: str | None, commodity: str | None) -> str:
        if op == "SELL":
            return (
                "livestock_product_revenue"
                if commodity in {"MILK", "WOOL", "EGG"}
                else "crop_product_revenue"
            )
        if op == "BUY_ANIMAL":
            return "livestock_acquisition_cost"
        if op == "BUY_PRODUCT" and commodity == "WHEAT":
            return "feed_cost"
        if op == "BUY_SEED":
            return "seed_cost"
        if op == "HIRE":
            return "workforce_cost"
        if op == "BUY_LAND":
            return "land_cost"
        return "other"

    def _base_event(
        self,
        *,
        player: int,
        actor_id: str,
        actor_type: str,
        unit_index: int | None,
        target: Any,
        requested: Any,
        applied: Any,
        executed: Any,
        success: bool,
        reason: str | None,
        requested_quantity: int,
        executed_quantity: int,
        displayed_price: float | None,
        realized_price: float | None,
        realized_value: float | None,
        cash_category: str,
        cash_before: float,
        cash_after: float,
        state_before: Any,
        state_after: Any,
        status: str,
    ) -> dict[str, Any]:
        if not 0 <= player < self._expected_players:
            raise RuntimeError(f"event has unattributable player: {player}")
        step, day, hour = self._step_context()
        statuses = ["requested"]
        if status not in {"failed"} or executed_quantity > 0:
            statuses.append("accepted")
        statuses.append(status)
        quadrants = (
            state_after.get("quadrants_owned")
            if isinstance(state_after, dict)
            else None
        )
        if quadrants is None and self._state is not None and player >= 0:
            quadrants = _owned_quadrants(self._state[0].observation.farms[player])
        event = {
            **self.metadata,
            "player": player,
            "seat": player,
            "actor_role": "treatment"
            if player == int(self.metadata["treatment_seat"])
            else "opponent",
            "step": step,
            "day": day,
            "hour": hour,
            "actor_or_order_id": f"{self.metadata['episode_id']}:{step}:{player}:{actor_id}",
            "actor_or_order_type": actor_type,
            "unit_index": unit_index,
            "target_tile_or_commodity": _plain(target),
            "requested_payload": _plain(requested),
            "engine_applied_payload": _plain(applied),
            "executed_payload": _plain(executed),
            "success": bool(success),
            "failure_or_noop_reason": reason,
            "requested_quantity": requested_quantity,
            "executed_quantity": executed_quantity,
            "displayed_price_at_request": displayed_price,
            "realized_price": realized_price,
            "realized_value": realized_value,
            "cash_flow_category": cash_category,
            "cash_before": cash_before,
            "cash_after": cash_after,
            "relevant_state_before": _plain(state_before),
            "relevant_state_after": _plain(state_after),
            "provenance": "kaggriculture_engine_mutation_wrapper_v2",
            "quadrants_owned": quadrants,
            "execution_status": status,
            "lifecycle_statuses": statuses,
            "attribution_status": "attributed",
        }
        missing = LEDGER_REQUIRED_FIELDS - set(event)
        if missing:
            raise RuntimeError(f"ledger event missing fields: {sorted(missing)}")
        return event


def detect_t0(env_steps: list[Any], treatment_seat: int) -> int | None:
    previous = 1
    for step_data in env_steps:
        if treatment_seat >= len(step_data):
            continue
        obs = step_data[treatment_seat].get("observation", {})
        farms = obs.get("farms", [])
        if treatment_seat >= len(farms):
            continue
        current = _owned_quadrants(farms[treatment_seat])
        if previous < 2 <= current:
            return int(obs.get("step", 0))
        previous = current
    return None


def _median(values: list[float]) -> float:
    return float(statistics.median(values)) if values else 0.0


def derive_episode_telemetry(
    env_steps: list[Any],
    ledger: list[dict[str, Any]],
    treatment_seat: int,
    cell_config: dict[str, Any],
    episode_steps: int,
) -> dict[str, Any]:
    """Derive audit metrics without treating terminal inventory as cash."""

    t0_step = detect_t0(env_steps, treatment_seat)
    day_needs: dict[int, set[tuple[int, int]]] = defaultdict(set)
    daily_active: dict[int, list[int]] = defaultdict(list)
    daily_herd: dict[int, list[int]] = defaultdict(list)
    daily_pasture: dict[int, list[int]] = defaultdict(list)
    state_rows: list[dict[str, Any]] = []
    active_positions_by_step: list[tuple[int, set[tuple[int, int]]]] = []
    final_obs: dict[str, Any] = {}

    for step_data in env_steps:
        if treatment_seat >= len(step_data):
            continue
        obs = step_data[treatment_seat].get("observation", {})
        farms = obs.get("farms", [])
        if treatment_seat >= len(farms):
            continue
        farm = farms[treatment_seat]
        day = int(obs.get("day", 0))
        active = herd = pasture = occupied = fed = harvest_ready = surviving = 0
        active_positions: set[tuple[int, int]] = set()
        for y, row in enumerate(farm.get("tiles", [])):
            for x, tile in enumerate(row):
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    active += 1
                    active_positions.add((x, y))
                    day_needs[day].add((x, y))
                    if int(tile.get("consecutive_unwatered", 0)) < 2:
                        surviving += 1
                    if int(tile.get("yield_units", 0)) > 0:
                        harvest_ready += 1
                if isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                    pasture += 1
                    if tile.get("animal"):
                        occupied += 1
                        herd += 1
                        fed += int(bool(tile.get("fed_today", False)))
        daily_active[day].append(active)
        daily_herd[day].append(herd)
        daily_pasture[day].append(pasture)
        worker_capacity = 1 + len(farm.get("hands", []))
        state_rows.append(
            {
                "step": int(obs.get("step", 0)),
                "day": day,
                "hour": int(obs.get("hour", 0)),
                "assigned_crop_target": int(cell_config["crop_working_set_target"]),
                "achieved_crop_surface": active,
                "assigned_watering_priority": float(
                    cell_config["watering_dispatch_priority"]
                ),
                "assigned_herd_target": int(cell_config["livestock_headcount_target"]),
                "achieved_herd": herd,
                "assigned_pasture_target": int(
                    cell_config["pasture_allocation_target"]
                ),
                "achieved_pasture": pasture,
                "workforce_state": len(farm.get("hands", [])),
                "worker_capacity": worker_capacity,
                "pasture_occupancy": occupied / pasture if pasture else 0.0,
                "feed_demand": herd,
                "feed_coverage": fed / herd if herd else 1.0,
                "active_crop_surface": active,
                "surviving_crop_surface": surviving,
                "harvest_ready_surface": harvest_ready,
            }
        )
        active_positions_by_step.append((int(obs.get("step", 0)), active_positions))
        final_obs = obs

    successful_water = {
        (int(event["day"]), tuple(event["target_tile_or_commodity"]))
        for event in ledger
        if event["player"] == treatment_seat
        and event.get("attribution_status") == "attributed"
        and event["actor_or_order_type"] != "market_order"
        and isinstance(event.get("engine_applied_payload"), list)
        and event["engine_applied_payload"]
        and event["engine_applied_payload"][0] == "WATER"
        and event["execution_status"] == "executed"
    }
    daily_water_rates: dict[int, float] = {}
    for day, needs in day_needs.items():
        effects = sum((day, position) in successful_water for position in needs)
        daily_water_rates[day] = effects / len(needs) if needs else 0.0

    t0_day = None
    if t0_step is not None:
        t0_day = next(
            (row["day"] for row in state_rows if row["step"] == t0_step), t0_step // 24
        )
    steady_start_day = (t0_day + 3) if t0_day is not None else 10**9
    steady_end_step = max(0, episode_steps - int(cell_config["endgame_shutdown_steps"]))
    steady_days = sorted(
        {
            row["day"]
            for row in state_rows
            if row["day"] >= steady_start_day and row["step"] < steady_end_step
        }
    )
    productive_days = [day for day in steady_days if day_needs.get(day)]
    steady_water_rates = [daily_water_rates.get(day, 0.0) for day in productive_days]
    daily_need_denominators = {day: len(day_needs[day]) for day in productive_days}
    daily_successful_effects = {
        day: sum((day, position) in successful_water for position in day_needs[day])
        for day in productive_days
    }
    watering_need_denominator = sum(daily_need_denominators.values())
    successful_watering_effects = sum(daily_successful_effects.values())
    watering_execution_rate = (
        successful_watering_effects / watering_need_denominator
        if watering_need_denominator
        else 0.0
    )
    daily_attainment = {
        day: (
            _median([float(value) for value in values])
            / int(cell_config["crop_working_set_target"])
        )
        for day, values in daily_active.items()
    }
    continuity = (
        sum(rate >= 0.50 for rate in steady_water_rates) / len(steady_water_rates)
        if steady_water_rates
        else 0.0
    )
    if not 0.0 <= watering_execution_rate <= 1.0:
        raise RuntimeError("watering_execution_rate is outside [0, 1]")
    if not 0.0 <= continuity <= 1.0:
        raise RuntimeError("watering_continuity is outside [0, 1]")

    actor_events = [
        event
        for event in ledger
        if event["player"] == treatment_seat
        and event["actor_or_order_type"] != "market_order"
    ]
    failed_actor = sum(
        event["execution_status"] in {"failed", "no_op"} for event in actor_events
    )
    successful_removals = {
        (int(event["step"]), tuple(event["target_tile_or_commodity"]))
        for event in actor_events
        if event["execution_status"] == "executed"
        and isinstance(event["requested_payload"], list)
        and event["requested_payload"]
        and event["requested_payload"][0] in {"HARVEST", "DIG"}
    }
    crop_losses = 0
    for (previous_step, previous), (_, current) in pairwise(active_positions_by_step):
        for position in previous - current:
            if (previous_step, position) not in successful_removals:
                crop_losses += 1
    transit = [
        event
        for event in actor_events
        if isinstance(event["requested_payload"], list)
        and event["requested_payload"]
        and event["requested_payload"][0] in {"NORTH", "SOUTH", "EAST", "WEST"}
    ]
    necessary_transit = sum(
        bool(event.get("relevant_state_before", {}).get("inventory") or {})
        for event in transit
    )
    avoidable_transit = len(transit) - necessary_transit

    cash_flow: dict[str, float] = defaultdict(float)
    for event in ledger:
        if (
            event["player"] != treatment_seat
            or event["actor_or_order_type"] != "market_order"
        ):
            continue
        value = float(event["realized_value"] or 0.0)
        sign = (
            1.0
            if event["requested_payload"] and event["requested_payload"][0] == "SELL"
            else -1.0
        )
        cash_flow[event["cash_flow_category"]] += sign * value

    product_collected: dict[str, int] = defaultdict(int)
    product_stored: dict[str, int] = defaultdict(int)
    product_sold: dict[str, int] = defaultdict(int)
    purchase_steps: list[int] = []
    activation_steps: list[int] = []
    for event in ledger:
        if event["player"] != treatment_seat:
            continue
        payload = event.get("requested_payload")
        op = payload[0] if isinstance(payload, list) and payload else None
        if event["actor_or_order_type"] == "market_order":
            if op == "SELL" and len(payload) > 1:
                product_sold[payload[1]] += int(event["executed_quantity"])
            if op == "BUY_ANIMAL" and len(payload) > 1 and payload[1] == "COW":
                purchase_steps.extend(
                    [int(event["step"])] * int(event["executed_quantity"])
                )
            continue
        if event["execution_status"] != "executed":
            continue
        before = event.get("relevant_state_before", {})
        after = event.get("relevant_state_after", {})
        if op == "HARVEST":
            before_inventory = before.get("inventory", {}) or {}
            after_inventory = after.get("inventory", {}) or {}
            for item in set(before_inventory) | set(after_inventory):
                delta = int(after_inventory.get(item, 0)) - int(
                    before_inventory.get(item, 0)
                )
                if delta > 0:
                    product_collected[item] += delta
        if op in {"DROP", "PLACE"}:
            before_shed = before.get("shed", {}) or {}
            after_shed = after.get("shed", {}) or {}
            for item in set(before_shed) | set(after_shed):
                delta = int(after_shed.get(item, 0)) - int(before_shed.get(item, 0))
                if delta > 0:
                    product_stored[item] += delta
        if op == "PLACE" and len(payload) > 1 and payload[1] == "COW":
            activation_steps.append(int(event["step"]))

    activation_lags = [
        activation - purchase
        for purchase, activation in zip(
            sorted(purchase_steps), sorted(activation_steps)
        )
        if activation >= purchase
    ]

    final_farm = {}
    final_private = {}
    final_prices = {}
    if final_obs:
        final_farm = final_obs.get("farms", [])[treatment_seat]
        final_private = final_obs.get("private", {}) or {}
        final_prices = (final_obs.get("market", {}) or {}).get("prices", {}) or {}
    terminal_inventory = dict(final_private.get("shed", {}) or {})
    for inventory in final_private.get("inventories", []) or []:
        for item, quantity in (inventory or {}).items():
            terminal_inventory[item] = terminal_inventory.get(item, 0) + quantity
    unsold_quantity = sum(int(quantity) for quantity in terminal_inventory.values())
    unsold_estimate = sum(
        float(final_prices.get(item, 0.0)) * int(quantity)
        for item, quantity in terminal_inventory.items()
    )
    daily_serviced = {
        day: sum((day, position) in successful_water for position in needs)
        for day, needs in day_needs.items()
    }

    return {
        "t0_step": t0_step,
        "opening_failure": t0_step is None,
        "policy_realization_failure": t0_step is None,
        "steady_window": {
            "start_day": None if t0_step is None else steady_start_day,
            "end_step_exclusive": steady_end_step,
        },
        "watering_need_denominator": watering_need_denominator,
        "successful_watering_effects": successful_watering_effects,
        "watering_metric_status": "OBSERVED"
        if watering_need_denominator
        else "NO_STEADY_PRODUCTIVE_DAYS",
        "steady_productive_day_count": len(productive_days),
        "daily_watering_need_denominator": daily_need_denominators,
        "daily_successful_watering_effects": daily_successful_effects,
        "watering_execution_rate_formula": "sum(unique successful treatment crop-day WATER effects) / sum(unique treatment crop-day watering needs)",
        "watering_continuity_formula": "productive days with daily watering_execution_rate >= 0.50 / productive days",
        "serviced_crop_surface": _median(
            [float(daily_serviced.get(day, 0)) for day in productive_days]
        ),
        "watering_execution_rate": watering_execution_rate,
        "watering_continuity": continuity,
        "crop_target_attainment": _median(
            [daily_attainment[day] for day in steady_days if day in daily_attainment]
        ),
        "daily_watering_execution_rate": daily_water_rates,
        "daily_crop_target_attainment": daily_attainment,
        "pasture_occupancy": _median([row["pasture_occupancy"] for row in state_rows]),
        "feed_coverage": _median([row["feed_coverage"] for row in state_rows]),
        "action_failure_rate": failed_actor / len(actor_events)
        if actor_events
        else 0.0,
        "realized_cash_flow_by_category": dict(cash_flow),
        "livestock_acquisition_cost": -cash_flow.get("livestock_acquisition_cost", 0.0),
        "feed_cost": -cash_flow.get("feed_cost", 0.0),
        "livestock_service_cost": 0.0,
        "livestock_product_realized_value": cash_flow.get(
            "livestock_product_revenue", 0.0
        ),
        "purchase_to_activation_lag": activation_lags,
        "median_purchase_to_activation_lag": _median(
            [float(value) for value in activation_lags]
        ),
        "active_crop_surface": state_rows[-1]["active_crop_surface"]
        if state_rows
        else 0,
        "surviving_crop_surface": state_rows[-1]["surviving_crop_surface"]
        if state_rows
        else 0,
        "harvest_ready_surface": state_rows[-1]["harvest_ready_surface"]
        if state_rows
        else 0,
        "crop_losses": crop_losses,
        "product_generated": dict(product_collected),
        "product_collected": dict(product_collected),
        "product_stored": dict(product_stored),
        "product_sold": dict(product_sold),
        "worker_capacity": max(
            (row["worker_capacity"] for row in state_rows), default=0
        ),
        "worker_utilization": 1.0
        - (
            sum(event["execution_status"] == "no_op" for event in actor_events)
            / len(actor_events)
            if actor_events
            else 0.0
        ),
        "necessary_transit": necessary_transit,
        "avoidable_transit": avoidable_transit,
        "terminal_inventory_by_product": terminal_inventory,
        "terminal_unsold_inventory": terminal_inventory,
        "unsold_inventory_quantity": unsold_quantity,
        "unsold_inventory_value_estimate": unsold_estimate,
        "unsold_inventory_value_method": "terminal quantity multiplied by terminal displayed market price; non-cash observational estimate",
        "unsold_inventory_value_provenance": "terminal observation market.prices and private inventories",
        "final_money_observational_only": float(final_farm.get("money", 0.0))
        if final_farm
        else 0.0,
        "state_rows": state_rows,
    }


def validate_ledger_schema(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if not events:
        return ["event ledger is empty"]
    for index, event in enumerate(events):
        missing = LEDGER_REQUIRED_FIELDS - set(event)
        if missing:
            errors.append(f"event {index} missing {sorted(missing)}")
        if event.get("executed_quantity", 0) > event.get("requested_quantity", 0):
            errors.append(f"event {index} executes more than requested")
        if event.get("realized_price") is not None:
            expected = float(event["realized_price"]) * int(event["executed_quantity"])
            if not math.isclose(
                expected, float(event["realized_value"]), rel_tol=1e-9, abs_tol=1e-9
            ):
                errors.append(f"event {index} realized value does not reconcile")
    return errors


def write_jsonl(path: Any, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=True) + "\n")
