#!/usr/bin/env python3
"""Run the bounded real-engine service-peak preflight for Codex C2 V4."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.codex_c2 import create_agent

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "results"
    / "model_spec_c2"
    / "performance_iteration"
    / "CODEX_C2_V4_PREFLIGHT.json"
)
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


def inert_agent(
    observation: dict[str, Any], configuration: Any = None
) -> dict[str, Any]:
    del observation, configuration
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _farm_state(agent_step: dict[str, Any], seat: int) -> dict[str, Any]:
    observation = agent_step.get("observation", {}) or {}
    farms = observation.get("farms", []) or []
    return farms[seat] if seat < len(farms) else {}


def _tile_metrics(farm: dict[str, Any]) -> tuple[int, int, int, int]:
    active = watered = pastures = cows = 0
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "PLANT":
                active += 1
                watered += int(bool(tile.get("watered_today", False)))
            if tile.get("kind") == "PASTURE":
                pastures += 1
                cows += int(tile.get("animal") == "COW")
    return active, watered, pastures, cows


def _positions(farm: dict[str, Any]) -> tuple[tuple[int, int], ...]:
    raw = [farm.get("farmer", [4, 4]), *(farm.get("hands", []) or [])]
    return tuple(tuple(int(value) for value in position) for position in raw)


def _tile_at(farm: dict[str, Any], position: tuple[int, int]) -> Any:
    x, y = position
    tiles = farm.get("tiles", []) or []
    if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
        return tiles[y][x]
    return None


def _private_state(agent_step: dict[str, Any]) -> dict[str, Any]:
    private = (agent_step.get("observation", {}) or {}).get("private", {}) or {}
    return private if isinstance(private, dict) else {}


def summarize_run(env: Any, seat: int, episode_agent: Any) -> dict[str, Any]:
    unit_actions: Counter[str] = Counter()
    market_orders: Counter[str] = Counter()
    crop_plant_attempts: Counter[str] = Counter()
    effective_crop_harvests: Counter[str] = Counter()
    effective_crop_harvest_units: Counter[str] = Counter()
    ordered_sell_quantities: Counter[str] = Counter()
    observed_sell_drawdown: Counter[str] = Counter()
    wheat_harvest_events: list[dict[str, Any]] = []
    wheat_water_events: list[dict[str, Any]] = []
    wheat_plant_keys: set[tuple[int, int, int]] = set()
    wheat_ready_first_seen: dict[tuple[int, int, int], dict[str, Any]] = {}
    wheat_completions: dict[tuple[int, int, int], dict[str, Any]] = {}
    wheat_ready_trajectory: list[int] = []
    active_positions_by_day: dict[int, set[tuple[int, int]]] = defaultdict(set)
    watered_positions_by_day: dict[int, set[tuple[int, int]]] = defaultdict(set)
    player_values: set[int] = set()
    active_trajectory: list[int] = []
    watered_trajectory: list[int] = []
    pasture_trajectory: list[int] = []
    cow_trajectory: list[int] = []
    quadrant_trajectory: list[int] = []
    money_trajectory: list[float] = []
    plant_effect_steps: list[int] = []
    water_effect_steps: list[int] = []
    movement_effect_steps: list[int] = []
    sell_cash_gain_steps: list[int] = []
    active_transition_count = 0

    previous_agent_step: dict[str, Any] | None = None
    for index, joint_step in enumerate(env.steps):
        agent_step = joint_step[seat]
        observation = agent_step.get("observation", {}) or {}
        if "player" in observation:
            player_values.add(int(observation["player"]))
        farm = _farm_state(agent_step, seat)
        active, watered, pastures, cows = _tile_metrics(farm)
        positions = _positions(farm)
        quadrants = len(farm.get("unlocked_quadrants", []) or [])
        money = float(farm.get("money", 0.0))
        day = int(observation.get("day", 0))
        wheat_ready_now = 0

        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    active_positions_by_day[day].add((x, y))
                    if bool(tile.get("watered_today", False)):
                        watered_positions_by_day[day].add((x, y))
                    if tile.get("crop") == "WHEAT":
                        try:
                            planted_day = int(tile["planted_day"])
                            yield_units = int(tile["yield_units"])
                            deadline_step = int(tile["max_lifespan_step"])
                        except (KeyError, TypeError, ValueError):
                            continue
                        key = (x, y, planted_day)
                        wheat_plant_keys.add(key)
                        if yield_units > 0 and day - planted_day >= 4:
                            wheat_ready_now += 1
                            wheat_ready_first_seen.setdefault(
                                key,
                                {
                                    "position": [x, y],
                                    "planted_day": planted_day,
                                    "ready_step": index,
                                    "deadline_step": deadline_step,
                                    "ready_yield": yield_units,
                                },
                            )

        wheat_ready_trajectory.append(wheat_ready_now)

        active_trajectory.append(active)
        watered_trajectory.append(watered)
        pasture_trajectory.append(pastures)
        cow_trajectory.append(cows)
        quadrant_trajectory.append(quadrants)
        money_trajectory.append(money)

        action = agent_step.get("action", {}) or {}
        farmer_action = action.get("farmer", ["PASS"])
        hands_actions = action.get("hands", []) or []
        all_unit_actions = [farmer_action, *hands_actions]
        previous_farm = (
            _farm_state(previous_agent_step, seat)
            if previous_agent_step is not None
            else {}
        )
        actor_positions = (
            _positions(previous_farm)
            if previous_agent_step is not None
            else positions
        )
        step_unit_ops: set[str] = set()
        for actor_position, unit_action in zip(actor_positions, all_unit_actions):
            if not isinstance(unit_action, list) or not unit_action:
                continue
            opcode = str(unit_action[0]).upper()
            normalized = "MOVE" if opcode in MOVES else opcode
            unit_actions[normalized] += 1
            step_unit_ops.add(normalized)
            if opcode == "PLANT" and len(unit_action) >= 2:
                crop_plant_attempts[str(unit_action[1]).upper()] += 1

            if opcode == "WATER" and previous_agent_step is not None:
                tile = _tile_at(previous_farm, actor_position)
                next_tile = _tile_at(farm, actor_position)
                if isinstance(tile, dict) and tile.get("crop") == "WHEAT":
                    wheat_water_events.append(
                        {
                            "step": index,
                            "day": int(
                                (previous_agent_step.get("observation", {}) or {}).get(
                                    "day", 0
                                )
                            ),
                            "position": list(actor_position),
                            "planted_day": tile.get("planted_day"),
                            "yield_before": tile.get("yield_units"),
                            "yield_after": (
                                next_tile.get("yield_units")
                                if isinstance(next_tile, dict)
                                else None
                            ),
                        }
                    )

            if opcode == "HARVEST" and previous_agent_step is not None:
                tile = _tile_at(previous_farm, actor_position)
                next_tile = _tile_at(farm, actor_position)
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    crop = str(tile.get("crop", "UNKNOWN")).upper()
                    try:
                        current_yield = int(tile.get("yield_units", 0))
                        next_yield = (
                            int(next_tile.get("yield_units", 0))
                            if isinstance(next_tile, dict)
                            and next_tile.get("kind") == "PLANT"
                            and next_tile.get("crop") == tile.get("crop")
                            else 0
                        )
                    except (TypeError, ValueError):
                        current_yield = next_yield = 0
                    if current_yield > 0 and next_yield < current_yield:
                        effective_crop_harvests[crop] += 1
                        effective_crop_harvest_units[crop] += current_yield
                        if crop == "WHEAT":
                            try:
                                planted_day = int(tile["planted_day"])
                            except (KeyError, TypeError, ValueError):
                                planted_day = -1
                            key = (*actor_position, planted_day)
                            wheat_completions[key] = {
                                "step": index,
                                "yield": current_yield,
                            }
                            wheat_harvest_events.append(
                                {
                                    "step": index,
                                    "day": int(
                                        (
                                            previous_agent_step.get(
                                                "observation", {}
                                            )
                                            or {}
                                        ).get("day", 0)
                                    ),
                                    "position": list(actor_position),
                                    "planted_day": tile.get("planted_day"),
                                    "yield": current_yield,
                                    "watered_today": tile.get("watered_today"),
                                }
                            )

        step_market_ops: set[str] = set()
        step_sell_products: set[str] = set()
        for order in action.get("market", []) or []:
            if not isinstance(order, list) or not order:
                continue
            opcode = str(order[0]).upper()
            market_orders[opcode] += 1
            step_market_ops.add(opcode)
            if opcode == "SELL" and len(order) >= 3:
                product = str(order[1]).upper()
                step_sell_products.add(product)
                try:
                    ordered_sell_quantities[product] += int(order[2])
                except (TypeError, ValueError):
                    pass

        if previous_agent_step is not None:
            previous_active, previous_watered, _, _ = _tile_metrics(previous_farm)
            previous_positions = _positions(previous_farm)
            previous_money = float(previous_farm.get("money", 0.0))
            if active != previous_active:
                active_transition_count += 1
            if "PLANT" in step_unit_ops and active > previous_active:
                plant_effect_steps.append(index)
            if "WATER" in step_unit_ops and watered > previous_watered:
                water_effect_steps.append(index)
            if "MOVE" in step_unit_ops and positions != previous_positions:
                movement_effect_steps.append(index)
            if "SELL" in step_market_ops and money > previous_money:
                sell_cash_gain_steps.append(index)

            previous_shed = (
                _private_state(previous_agent_step).get("shed", {}) or {}
            )
            current_shed = _private_state(agent_step).get("shed", {}) or {}
            for product in step_sell_products:
                before = int(previous_shed.get(product, 0))
                after = int(current_shed.get(product, 0))
                if before > after:
                    observed_sell_drawdown[product] += before - after
        previous_agent_step = agent_step

    status = str(env.steps[-1][seat].get("status", "UNKNOWN"))
    instance = episode_agent.codex_c2_instance
    failures: list[str] = []
    if status != "DONE":
        failures.append(f"terminal status is {status}, expected DONE")
    if player_values != {seat}:
        failures.append(f"observation.player values {sorted(player_values)} do not bind to seat {seat}")
    if instance.error_count or instance.fallback_count:
        failures.append(
            f"agent errors/fallbacks are {instance.error_count}/{instance.fallback_count}"
        )
    if max(active_trajectory, default=0) < 8:
        failures.append("policy did not leave the initial state with at least eight active crops")
    if max(quadrant_trajectory, default=0) < 2:
        failures.append("gated second-quadrant expansion was not realized")
    if not plant_effect_steps:
        failures.append("PLANT emitted without an observed active-surface increase")
    if not water_effect_steps:
        failures.append("WATER emitted without an observed watered-state increase")
    if not movement_effect_steps:
        failures.append("MOVE emitted without an observed position transition")
    if unit_actions["HARVEST"] == 0:
        failures.append("no harvest occurred")
    if market_orders["BUY_SEED"] == 0:
        failures.append("no seed purchase occurred")
    if not sell_cash_gain_steps:
        failures.append("no SELL was paired with a positive cash transition")

    wheat_cohorts: Counter[int] = Counter(
        planted_day for _, _, planted_day in wheat_plant_keys
    )
    max_wheat_plant_cohort = max(wheat_cohorts.values(), default=0)
    peak_wheat_ready = max(wheat_ready_trajectory, default=0)
    terminal_step = len(env.steps) - 1
    deadline_evaluable = {
        key: event
        for key, event in wheat_ready_first_seen.items()
        if int(event["deadline_step"]) <= terminal_step
    }
    deadline_misses = sum(
        1
        for key, event in deadline_evaluable.items()
        if key not in wheat_completions
        or int(wheat_completions[key]["step"]) >= int(event["deadline_step"])
    )
    deadline_miss_rate = (
        deadline_misses / len(deadline_evaluable) if deadline_evaluable else 1.0
    )
    wheat_harvests = effective_crop_harvests["WHEAT"]
    wheat_harvests_ge3 = sum(
        1 for event in wheat_harvest_events if int(event["yield"]) >= 3
    )
    fraction_wheat_harvested_ge3 = (
        wheat_harvests_ge3 / wheat_harvests if wheat_harvests else 0.0
    )
    ready_to_completed_latency = [
        int(wheat_completions[key]["step"]) - int(event["ready_step"])
        for key, event in wheat_ready_first_seen.items()
        if key in wheat_completions
    ]

    if max_wheat_plant_cohort > 2:
        failures.append(
            f"max WHEAT plant cohort is {max_wheat_plant_cohort}, expected <= 2"
        )
    if peak_wheat_ready > 4:
        failures.append(
            f"peak simultaneous WHEAT ready is {peak_wheat_ready}, expected <= 4"
        )
    if deadline_miss_rate > 0.25:
        failures.append(
            f"WHEAT deadline miss rate is {deadline_miss_rate:.3f}, expected <= 0.25"
        )
    if fraction_wheat_harvested_ge3 < 0.80:
        failures.append(
            "fraction WHEAT harvested at yield >= 3 is "
            f"{fraction_wheat_harvested_ge3:.3f}, expected >= 0.80"
        )
    if effective_crop_harvests["MELON"] == 0:
        failures.append("no effective MELON harvest occurred")
    if observed_sell_drawdown["MELON"] == 0:
        failures.append("no effective MELON sale drawdown occurred")

    daily_water_coverage = {
        str(day): (
            len(watered_positions_by_day[day]) / len(active_positions)
            if active_positions
            else 1.0
        )
        for day, active_positions in sorted(active_positions_by_day.items())
    }
    total_unit_actions = sum(unit_actions.values())

    return {
        "seat": seat,
        "status": status,
        "steps_observed": len(env.steps),
        "player_values": sorted(player_values),
        "own_farm_binding_verified": player_values == {seat},
        "error_count": instance.error_count,
        "fallback_count": instance.fallback_count,
        "last_exception": instance.last_exception,
        "unit_actions": dict(sorted(unit_actions.items())),
        "market_orders": dict(sorted(market_orders.items())),
        "mechanism": {
            "crop_plant_attempts": dict(sorted(crop_plant_attempts.items())),
            "effective_crop_harvests": dict(
                sorted(effective_crop_harvests.items())
            ),
            "effective_crop_harvest_units": dict(
                sorted(effective_crop_harvest_units.items())
            ),
            "yield_per_effective_harvest": {
                crop: effective_crop_harvest_units[crop] / count
                for crop, count in sorted(effective_crop_harvests.items())
                if count
            },
            "ordered_sell_quantities": dict(
                sorted(ordered_sell_quantities.items())
            ),
            "observed_sell_drawdown": dict(sorted(observed_sell_drawdown.items())),
            "wheat_harvest_events": wheat_harvest_events,
            "wheat_water_events": wheat_water_events,
            "wheat_service_peak": {
                "effective_plant_cohort_by_day": {
                    str(day): count for day, count in sorted(wheat_cohorts.items())
                },
                "max_effective_plant_cohort": max_wheat_plant_cohort,
                "peak_simultaneous_economic_ready": peak_wheat_ready,
                "ready_trajectory": wheat_ready_trajectory,
                "ready_events": list(wheat_ready_first_seen.values()),
                "deadline_evaluable_count": len(deadline_evaluable),
                "deadline_miss_count": deadline_misses,
                "deadline_miss_rate": deadline_miss_rate,
                "ready_to_completed_latency": ready_to_completed_latency,
                "harvest_count": wheat_harvests,
                "harvest_yield_ge3_count": wheat_harvests_ge3,
                "fraction_harvested_at_yield_ge3": (
                    fraction_wheat_harvested_ge3
                ),
            },
            "daily_water_coverage": daily_water_coverage,
            "mean_daily_water_coverage": (
                sum(daily_water_coverage.values()) / len(daily_water_coverage)
                if daily_water_coverage
                else 1.0
            ),
            "movement_share": (
                unit_actions["MOVE"] / total_unit_actions
                if total_unit_actions
                else 0.0
            ),
        },
        "state_transitions": {
            "active_surface_changes": active_transition_count,
            "plant_effect_count": len(plant_effect_steps),
            "water_effect_count": len(water_effect_steps),
            "movement_effect_count": len(movement_effect_steps),
            "first_plant_effect_step": plant_effect_steps[0] if plant_effect_steps else None,
            "first_water_effect_step": water_effect_steps[0] if water_effect_steps else None,
            "first_movement_effect_step": movement_effect_steps[0] if movement_effect_steps else None,
        },
        "productive_state": {
            "max_active_surface": max(active_trajectory, default=0),
            "final_active_surface": active_trajectory[-1] if active_trajectory else 0,
            "max_quadrants": max(quadrant_trajectory, default=0),
            "max_pastures": max(pasture_trajectory, default=0),
            "max_cows": max(cow_trajectory, default=0),
        },
        "economic_cycle": {
            "initial_cash": money_trajectory[0] if money_trajectory else None,
            "final_cash": money_trajectory[-1] if money_trajectory else None,
            "min_cash": min(money_trajectory, default=None),
            "max_cash": max(money_trajectory, default=None),
            "first_sell_cash_gain_step": sell_cash_gain_steps[0] if sell_cash_gain_steps else None,
            "sell_cash_gain_count": len(sell_cash_gain_steps),
            "cycle_observed": bool(
                market_orders["BUY_SEED"]
                and plant_effect_steps
                and water_effect_steps
                and unit_actions["HARVEST"]
                and sell_cash_gain_steps
            ),
        },
        "failures": failures,
        "passed": not failures,
    }


def run_preflight(seed: int, steps: int) -> dict[str, Any]:
    runs: list[dict[str, Any]] = []
    for seat in (0, 1):
        episode_agent = create_agent()
        agents = (
            [episode_agent, inert_agent]
            if seat == 0
            else [inert_agent, episode_agent]
        )
        env = make(
            "kaggriculture",
            configuration={"seed": seed, "episodeSteps": steps},
            debug=True,
        )
        env.run(agents)
        runs.append(summarize_run(env, seat, episode_agent))

    failures = [
        f"P{run['seat']}: {failure}"
        for run in runs
        for failure in run["failures"]
    ]
    return {
        "protocol": "CODEX_C2_STAGGERED_HARVEST_SERVICE_PREFLIGHT_V4",
        "seed": seed,
        "episode_steps": steps,
        "opponent": "inert_agent",
        "runs": runs,
        "failures": failures,
        "passed": not failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=26083001)
    parser.add_argument("--steps", type=int, default=360)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    payload = run_preflight(args.seed, args.steps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
