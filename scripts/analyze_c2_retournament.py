#!/usr/bin/env python3
"""Enrich frozen C2 retournament artifacts from the nine recorded replays."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = REPO_ROOT / "results" / "model_spec_c2" / "retournament"
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
SIDES = ((0, "p0"), (1, "p1"))
ORIGINAL_MEANS = {"antigravity": 3000.0, "codex": 16846.5, "copilot": 3000.0}


def instantiate_candidate(key: str) -> Callable[[dict[str, Any], Any], dict[str, Any]]:
    if key == "antigravity":
        from agricola.strategy.antigravity.agent_c2 import AntigravityC2Agent

        return AntigravityC2Agent()
    if key == "codex":
        from agricola.strategy.codex_c2 import create_agent

        return create_agent()
    if key == "copilot":
        from agricola.strategy.copilot.agent_c2 import CopilotC2Agent

        return CopilotC2Agent()
    raise ValueError(f"unknown candidate key: {key}")


def _farm(agent_step: dict[str, Any], seat: int) -> dict[str, Any]:
    observation = agent_step.get("observation", {}) or {}
    farms = observation.get("farms", []) or []
    return farms[seat] if seat < len(farms) and isinstance(farms[seat], dict) else {}


def _private(agent_step: dict[str, Any]) -> dict[str, Any]:
    private = (agent_step.get("observation", {}) or {}).get("private", {}) or {}
    return private if isinstance(private, dict) else {}


def _positions(farm: dict[str, Any]) -> tuple[tuple[int, int], ...]:
    raw = [farm.get("farmer", [4, 4]), *(farm.get("hands", []) or [])]
    return tuple(tuple(int(value) for value in position) for position in raw)


def _tile_state(farm: dict[str, Any]) -> dict[str, int]:
    state = {"active": 0, "watered": 0, "pastures": 0, "cows": 0, "weeds": 0, "yield": 0}
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            if kind == "PLANT":
                state["active"] += 1
                state["watered"] += int(bool(tile.get("watered_today", False)))
            elif kind == "PASTURE":
                state["pastures"] += 1
                state["cows"] += int(tile.get("animal") == "COW")
            elif kind == "WEED":
                state["weeds"] += 1
            state["yield"] += int(tile.get("yield_units", 0) or 0)
    return state


def _inventory_state(private: dict[str, Any]) -> tuple[dict[str, int], dict[str, int], int]:
    shed = private.get("shed", {}) if isinstance(private.get("shed", {}), dict) else {}
    seeds = private.get("seeds", {}) if isinstance(private.get("seeds", {}), dict) else {}
    goods: defaultdict[str, int] = defaultdict(int)
    for item, amount in shed.items():
        goods[str(item)] += int(amount or 0)
    for inventory in private.get("inventories", []) or []:
        if isinstance(inventory, dict):
            for item, amount in inventory.items():
                goods[str(item)] += int(amount or 0)
    clean_seeds = {str(item): int(amount or 0) for item, amount in seeds.items()}
    return dict(goods), clean_seeds, sum(goods.values())


def _ops(action: dict[str, Any]) -> tuple[list[str], list[str]]:
    unit_ops: list[str] = []
    raw_units = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
    for unit_action in raw_units:
        if isinstance(unit_action, list) and unit_action:
            opcode = str(unit_action[0]).upper()
            unit_ops.append("MOVE" if opcode in MOVES else opcode)
    market_ops = [
        str(order[0]).upper()
        for order in action.get("market", []) or []
        if isinstance(order, list) and order
    ]
    return unit_ops, market_ops


def _snapshot(agent_step: dict[str, Any], seat: int) -> dict[str, Any]:
    observation = agent_step.get("observation", {}) or {}
    farm = _farm(agent_step, seat)
    private = _private(agent_step)
    tiles = _tile_state(farm)
    goods, seeds, goods_total = _inventory_state(private)
    quadrants = farm.get("unlocked_quadrants", []) or []
    return {
        **tiles,
        "money": float(farm.get("money", 0.0)),
        "positions": _positions(farm),
        "workforce": 1 + len(farm.get("hands", []) or []),
        "quadrants": len(quadrants) if isinstance(quadrants, list) else int(quadrants),
        "goods": goods,
        "goods_total": goods_total,
        "seeds": seeds,
        "seed_total": sum(seeds.values()),
        "prices": dict((observation.get("market", {}) or {}).get("prices", {}) or {}),
        "day": int(observation.get("day", 0)),
        "step": int(observation.get("step", 0)),
    }


def _replay_actions(
    steps: list[Any], seat: int, key: str, configuration: dict[str, Any]
) -> dict[str, Any]:
    candidate = instantiate_candidate(key)
    outer_errors = 0
    outer_fallbacks = 0
    exceptions: list[str] = []
    mismatches: list[int] = []
    for index in range(len(steps) - 1):
        observation = deepcopy(steps[index][seat].get("observation", {}) or {})
        # Kaggle replay JSON stores the shared step only on P0, while the live
        # runner injects it into each callable observation.
        observation.setdefault("step", index)
        try:
            produced = candidate(observation, configuration)
        except Exception as exc:  # noqa: BLE001 - tournament boundary audit
            outer_errors += 1
            outer_fallbacks += 1
            exceptions.append(f"{type(exc).__name__}: {exc}")
            produced = deepcopy(SAFE_PASS)
        recorded = steps[index + 1][seat].get("action", {}) or {}
        if produced != recorded:
            mismatches.append(index + 1)

    instance = getattr(candidate, "codex_c2_instance", candidate)
    internal_errors = int(getattr(instance, "error_count", 0) or 0)
    if hasattr(instance, "fallback_count"):
        internal_fallbacks = int(getattr(instance, "fallback_count", 0) or 0)
    elif key == "antigravity":
        internal_fallbacks = internal_errors
    else:
        internal_fallbacks = 0
    last_exception = getattr(instance, "last_exception", None)
    return {
        "decisions_replayed": len(steps) - 1,
        "action_mismatch_count": len(mismatches),
        "first_action_mismatch_steps": mismatches[:10],
        "error_count": internal_errors + outer_errors,
        "fallback_count": internal_fallbacks + outer_fallbacks,
        "last_exception": str(last_exception) if last_exception else (exceptions[-1] if exceptions else None),
        "verified": not mismatches and not internal_errors and not outer_errors,
    }


def analyze_player(
    steps: list[Any], seat: int, key: str, configuration: dict[str, Any]
) -> dict[str, Any]:
    unit_actions: Counter[str] = Counter()
    market_orders: Counter[str] = Counter()
    effects: Counter[str] = Counter()
    active: list[int] = []
    money: list[float] = []
    quadrants: list[int] = []
    workforce: list[int] = []
    first_revenue_step: int | None = None
    first_cash_gain_step: int | None = None
    gross_sell_value = 0.0
    previous: dict[str, Any] | None = None

    for index, joint_step in enumerate(steps):
        agent_step = joint_step[seat]
        action = agent_step.get("action", {}) or {}
        unit_ops, market_ops = _ops(action)
        unit_actions.update(unit_ops)
        market_orders.update(market_ops)
        current = _snapshot(agent_step, seat)
        active.append(current["active"])
        money.append(current["money"])
        quadrants.append(current["quadrants"])
        workforce.append(current["workforce"])

        if previous is not None:
            if "MOVE" in unit_ops and current["positions"] != previous["positions"]:
                effects["MOVE"] += 1
            if "PLANT" in unit_ops and current["active"] > previous["active"]:
                effects["PLANT"] += 1
            if "WATER" in unit_ops and current["watered"] > previous["watered"]:
                effects["WATER"] += 1
            if "HARVEST" in unit_ops and (
                current["active"] < previous["active"]
                or current["yield"] < previous["yield"]
                or current["goods_total"] > previous["goods_total"]
            ):
                effects["HARVEST"] += 1
            if "DIG" in unit_ops and (
                current["weeds"] < previous["weeds"]
                or current["active"] < previous["active"]
            ):
                effects["DIG"] += 1
            if "BUY_SEED" in market_ops and current["seed_total"] > previous["seed_total"]:
                effects["BUY_SEED"] += 1
            if "BUY_LAND" in market_ops and current["quadrants"] > previous["quadrants"]:
                effects["BUY_LAND"] += 1
            if "HIRE" in market_ops and current["workforce"] > previous["workforce"]:
                effects["HIRE"] += 1

            sell_orders = [
                order
                for order in action.get("market", []) or []
                if isinstance(order, list) and order and str(order[0]).upper() == "SELL"
            ]
            sell_effect = False
            for order in sell_orders:
                if len(order) < 3:
                    continue
                product = str(order[1])
                quantity = int(order[2] or 0)
                price = float(previous["prices"].get(product, 0.0) or 0.0)
                gross_sell_value += quantity * price
                if current["goods"].get(product, 0) < previous["goods"].get(product, 0):
                    sell_effect = True
            if sell_orders and (sell_effect or current["money"] > previous["money"]):
                effects["SELL"] += 1
                if first_revenue_step is None:
                    first_revenue_step = index
            if current["money"] > previous["money"] and first_cash_gain_step is None:
                first_cash_gain_step = index
        previous = current

    status = str(steps[-1][seat].get("status", "UNKNOWN"))
    replay_audit = _replay_actions(steps, seat, key, configuration)
    return {
        "completion": status == "DONE" and len(steps) == 720,
        "status": status,
        "steps": len(steps),
        "error_count": replay_audit["error_count"],
        "fallback_count": replay_audit["fallback_count"],
        "action_replay_audit": replay_audit,
        "action_dispatch": dict(sorted(unit_actions.items())),
        "market_dispatch": dict(sorted(market_orders.items())),
        "state_transition_effects": dict(sorted(effects.items())),
        "active_surface": {
            "mean": statistics.fmean(active),
            "max": max(active),
            "final": active[-1],
        },
        "economic_effect": {
            "initial_cash": money[0],
            "minimum_cash": min(money),
            "final_cash": money[-1],
            "first_revenue_step": first_revenue_step,
            "first_cash_gain_step": first_cash_gain_step,
            "gross_sell_value_at_observed_prices": gross_sell_value,
        },
        "land": {
            "max_quadrants": max(quadrants),
            "final_quadrants": quadrants[-1],
        },
        "workforce": {
            "mean": statistics.fmean(workforce),
            "max": max(workforce),
            "final": workforce[-1],
        },
    }


def _mean(values: list[float | int | None]) -> float | None:
    present = [float(value) for value in values if value is not None]
    return statistics.fmean(present) if present else None


def aggregate(payload: dict[str, Any]) -> dict[str, Any]:
    by_candidate: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    records = {key: {"wins": 0, "losses": 0, "ties": 0} for key in ORIGINAL_MEANS}

    for match in payload["match_results"]:
        replay_path = DEFAULT_RESULTS / "raw" / match["match_id"] / "replay.json"
        replay = json.loads(replay_path.read_text(encoding="utf-8"))
        steps = replay["steps"]
        configuration = replay.get("configuration", {}) or {}
        for seat, side in SIDES:
            key = match[side]["key"]
            enhanced = analyze_player(steps, seat, key, configuration)
            match[side]["telemetry_enhanced"] = enhanced
            by_candidate[key].append(
                {"score": float(match[side]["final_money"]), **enhanced}
            )

        p0_key = match["p0"]["key"]
        p1_key = match["p1"]["key"]
        p0_score = float(match["p0"]["final_money"])
        p1_score = float(match["p1"]["final_money"])
        if p0_score > p1_score:
            records[p0_key]["wins"] += 1
            records[p1_key]["losses"] += 1
        elif p1_score > p0_score:
            records[p1_key]["wins"] += 1
            records[p0_key]["losses"] += 1
        else:
            records[p0_key]["ties"] += 1
            records[p1_key]["ties"] += 1

        raw_summary_path = DEFAULT_RESULTS / "raw" / match["match_id"] / "summary.json"
        raw_summary_path.write_text(json.dumps(match, indent=2) + "\n", encoding="utf-8")

    summary: dict[str, Any] = {}
    for key, episodes in by_candidate.items():
        scores = [episode["score"] for episode in episodes]
        dispatch_keys = (
            "PLANT", "WATER", "HARVEST", "DIG", "MOVE", "PASS"
        )
        market_keys = ("BUY_SEED", "SELL", "BUY_LAND", "HIRE")
        effect_keys = (
            "PLANT", "WATER", "HARVEST", "DIG", "MOVE", "BUY_SEED", "SELL", "BUY_LAND", "HIRE"
        )
        original = ORIGINAL_MEANS[key]
        mean_score = statistics.fmean(scores)
        summary[key] = {
            "name": payload["summary_statistics"][key]["name"],
            "matches_played": len(episodes),
            "record": records[key],
            "mean_money": mean_score,
            "median_money": statistics.median(scores),
            "sample_std_money_ddof_1": statistics.stdev(scores),
            "min_money": min(scores),
            "max_money": max(scores),
            "completion_count": sum(int(episode["completion"]) for episode in episodes),
            "completion_rate": statistics.fmean(int(episode["completion"]) for episode in episodes),
            "error_count": sum(episode["error_count"] for episode in episodes),
            "fallback_count": sum(episode["fallback_count"] for episode in episodes),
            "action_replay_mismatch_count": sum(
                episode["action_replay_audit"]["action_mismatch_count"] for episode in episodes
            ),
            "active_surface": {
                "mean": _mean([episode["active_surface"]["mean"] for episode in episodes]),
                "max": max(episode["active_surface"]["max"] for episode in episodes),
                "mean_final": _mean([episode["active_surface"]["final"] for episode in episodes]),
                "final_by_episode": [episode["active_surface"]["final"] for episode in episodes],
            },
            "mean_action_dispatch": {
                opcode: _mean([episode["action_dispatch"].get(opcode, 0) for episode in episodes])
                for opcode in dispatch_keys
            },
            "mean_market_dispatch": {
                opcode: _mean([episode["market_dispatch"].get(opcode, 0) for episode in episodes])
                for opcode in market_keys
            },
            "mean_market_orders": _mean(
                [sum(episode["market_dispatch"].values()) for episode in episodes]
            ),
            "mean_state_transition_effects": {
                opcode: _mean([episode["state_transition_effects"].get(opcode, 0) for episode in episodes])
                for opcode in effect_keys
            },
            "first_revenue_step": {
                "mean": _mean([episode["economic_effect"]["first_revenue_step"] for episode in episodes]),
                "min": min(episode["economic_effect"]["first_revenue_step"] for episode in episodes),
                "max": max(episode["economic_effect"]["first_revenue_step"] for episode in episodes),
                "by_episode": [episode["economic_effect"]["first_revenue_step"] for episode in episodes],
            },
            "cash": {
                "minimum_observed": min(episode["economic_effect"]["minimum_cash"] for episode in episodes),
                "mean_episode_minimum": _mean([episode["economic_effect"]["minimum_cash"] for episode in episodes]),
            },
            "land": {
                "max_quadrants": max(episode["land"]["max_quadrants"] for episode in episodes),
                "mean_final_quadrants": _mean([episode["land"]["final_quadrants"] for episode in episodes]),
            },
            "workforce": {
                "max": max(episode["workforce"]["max"] for episode in episodes),
                "mean_episode_peak": _mean([episode["workforce"]["max"] for episode in episodes]),
                "mean_effective": _mean([episode["workforce"]["mean"] for episode in episodes]),
            },
            "original_c2_mean_money": original,
            "delta_vs_original": mean_score - original,
            "delta_percent_vs_original": (mean_score - original) / original * 100.0,
        }
    return summary


def write_csv(path: Path, summary: dict[str, Any]) -> None:
    fields = [
        "candidate", "matches", "wins", "losses", "ties", "mean_money", "median_money",
        "sample_std_ddof_1", "min_money", "max_money", "completion_rate", "error_count",
        "fallback_count", "action_replay_mismatches", "active_mean", "active_max", "active_final_mean",
        "plant_dispatch_mean", "water_dispatch_mean", "harvest_dispatch_mean", "dig_dispatch_mean",
        "move_dispatch_mean", "market_orders_mean", "buy_seed_mean", "sell_mean", "buy_land_mean",
        "hire_mean", "first_revenue_step_mean", "minimum_cash", "max_quadrants", "workforce_max",
        "workforce_mean_effective", "original_mean", "delta_absolute", "delta_percent",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in summary.values():
            record = item["record"]
            actions = item["mean_action_dispatch"]
            market = item["mean_market_dispatch"]
            writer.writerow({
                "candidate": item["name"], "matches": item["matches_played"],
                "wins": record["wins"], "losses": record["losses"], "ties": record["ties"],
                "mean_money": item["mean_money"], "median_money": item["median_money"],
                "sample_std_ddof_1": item["sample_std_money_ddof_1"], "min_money": item["min_money"],
                "max_money": item["max_money"], "completion_rate": item["completion_rate"],
                "error_count": item["error_count"], "fallback_count": item["fallback_count"],
                "action_replay_mismatches": item["action_replay_mismatch_count"],
                "active_mean": item["active_surface"]["mean"], "active_max": item["active_surface"]["max"],
                "active_final_mean": item["active_surface"]["mean_final"],
                "plant_dispatch_mean": actions["PLANT"], "water_dispatch_mean": actions["WATER"],
                "harvest_dispatch_mean": actions["HARVEST"], "dig_dispatch_mean": actions["DIG"],
                "move_dispatch_mean": actions["MOVE"],
                "market_orders_mean": item["mean_market_orders"],
                "buy_seed_mean": market["BUY_SEED"], "sell_mean": market["SELL"],
                "buy_land_mean": market["BUY_LAND"], "hire_mean": market["HIRE"],
                "first_revenue_step_mean": item["first_revenue_step"]["mean"],
                "minimum_cash": item["cash"]["minimum_observed"],
                "max_quadrants": item["land"]["max_quadrants"], "workforce_max": item["workforce"]["max"],
                "workforce_mean_effective": item["workforce"]["mean_effective"],
                "original_mean": item["original_c2_mean_money"], "delta_absolute": item["delta_vs_original"],
                "delta_percent": item["delta_percent_vs_original"],
            })


def main() -> int:
    global DEFAULT_RESULTS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args()
    DEFAULT_RESULTS = args.results_dir.resolve()

    json_path = DEFAULT_RESULTS / "aggregated_results.json"
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if len(payload.get("match_results", [])) != 9:
        raise RuntimeError("expected exactly nine frozen retournament matches")
    payload["protocol"] = "MODEL_SPEC_C2_RETOURNAMENT_FROZEN_V2"
    payload["instrumentation"] = {
        "engine_run": "neutral runner derived from scripts/run_c2_tournament.py",
        "post_hoc_state_analysis": "scripts/analyze_c2_retournament.py",
        "action_replay": "719 decisions per candidate/episode reproduced from preceding observations",
        "candidate_behavior_changed": False,
    }
    payload["summary_statistics"] = aggregate(payload)
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_csv(DEFAULT_RESULTS / "aggregated_results.csv", payload["summary_statistics"])

    failures = [
        f"{key}: errors={item['error_count']}, fallbacks={item['fallback_count']}, "
        f"mismatches={item['action_replay_mismatch_count']}, completion={item['completion_rate']}"
        for key, item in payload["summary_statistics"].items()
        if item["error_count"]
        or item["fallback_count"]
        or item["action_replay_mismatch_count"]
        or item["completion_rate"] != 1.0
    ]
    print(json.dumps(payload["summary_statistics"], indent=2))
    if failures:
        print("AUDIT FAILURES:")
        print("\n".join(failures))
        return 1
    print("ACTION_REPLAY_AND_TELEMETRY_AUDIT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
