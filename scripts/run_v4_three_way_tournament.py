#!/usr/bin/env python3
"""Frozen 42-match 3Q tournament: Antigravity V4, Codex V9, and Copilot."""

from __future__ import annotations

import csv
import importlib.util
import json
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agricola.strategy.antigravity.agent_c2_3q_v4 import (
    create_agent as create_antigravity_v4,
)
from agricola.strategy.copilot.three_quadrant import (
    CopilotThreeQPolicy,
)

CODEX_FROZEN = (
    ROOT
    / "docs"
    / "governance"
    / "history"
    / "model_spec_c2"
    / "codex"
    / "freeze"
    / "submission_codex_v9_tournament.py"
)
RESULT_DIR = ROOT / "docs" / "governance" / "history" / "model_spec_c2" / "antigravity"
RESULT_JSON = RESULT_DIR / "ANTIGRAVITY_V4_0_THREE_WAY_TOURNAMENT_RESULTS.json"
RESULT_CSV = RESULT_DIR / "ANTIGRAVITY_V4_0_THREE_WAY_TOURNAMENT_RESULTS.csv"

SEEDS = (
    26090101,
    26090102,
    26090103,
    1838889274,
    1619968655,
    710418712,
    562040596,
)
PAIRS = (
    ("ANTIGRAVITY", "CODEX"),
    ("ANTIGRAVITY", "COPILOT"),
    ("CODEX", "COPILOT"),
)
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
PRODUCTIVE = {
    "PLANT",
    "WATER",
    "HARVEST",
    "DIG",
    "BUILD_PASTURE",
    "FEED",
    "CARE",
    "COLLECT_FERTILIZER",
    "FERTILIZE",
}
HANDLING = {"PICKUP", "PLACE"}


def _load_codex_module():
    spec = importlib.util.spec_from_file_location("codex_v9_tournament_frozen", CODEX_FROZEN)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {CODEX_FROZEN}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CODEX_MODULE = _load_codex_module()


def _agent(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {"seed": seed, "seat": seat, "player_position": seat}
    if name == "ANTIGRAVITY":
        instance = create_antigravity_v4(run_context=context)
        return instance, getattr(instance, "antigravity_v4_instance", instance)
    if name == "COPILOT":
        instance = CopilotThreeQPolicy(run_context=context)
        return instance.act, instance
    if name == "CODEX":
        instance = CODEX_MODULE.create_agent(run_context=context)
        return instance, instance
    raise ValueError(name)


def _active_counts(farm: dict[str, Any]) -> tuple[int, int, Counter[str]]:
    crops = 0
    animals: Counter[str] = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "PLANT":
                crops += 1
            if tile.get("animal"):
                animals[str(tile["animal"])] += 1
    return crops, sum(animals.values()), animals


def _animal_positions(farm: dict[str, Any]) -> set[tuple[int, int, str]]:
    return {
        (x, y, str(tile["animal"]))
        for y, row in enumerate(farm.get("tiles", []) or [])
        for x, tile in enumerate(row)
        if isinstance(tile, dict) and tile.get("animal")
    }


def _seat_metrics(env: Any, seat: int) -> dict[str, Any]:
    action_counts: Counter[str] = Counter()
    market_counts: Counter[str] = Counter()
    peak_hands = 0
    peak_crops = 0
    peak_animals = 0
    peak_quadrants = 0
    escapes = 0
    previous_day = None
    previous_animals: set[tuple[int, int, str]] = set()

    for state in env.steps:
        record = state[seat]
        observation = record.get("observation", {}) or {}
        farms = observation.get("farms", []) or []
        farm = farms[seat] if seat < len(farms) else {}
        day = int(observation.get("day", 0))
        crops, animals, _ = _active_counts(farm)
        current_animals = _animal_positions(farm)
        if previous_day is not None and day > previous_day:
            escapes += len(previous_animals - current_animals)
        previous_day = day
        previous_animals = current_animals
        peak_hands = max(peak_hands, len(farm.get("hands", []) or []))
        peak_crops = max(peak_crops, crops)
        peak_animals = max(peak_animals, animals)
        peak_quadrants = max(
            peak_quadrants, len(farm.get("unlocked_quadrants", []) or [])
        )

        action = record.get("action", {}) or {}
        unit_actions = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
        for unit_action in unit_actions:
            if unit_action:
                action_counts[str(unit_action[0])] += 1
        for order in action.get("market", []) or []:
            if order:
                quantity = int(order[2]) if len(order) >= 3 else 1
                item = str(order[1]) if len(order) >= 2 else "NONE"
                market_counts[f"{order[0]}:{item}"] += quantity

    terminal = env.steps[-1][seat]
    observation = terminal.get("observation", {}) or {}
    farm = observation["farms"][seat]
    crops, animals, species = _active_counts(farm)
    productive = sum(action_counts[opcode] for opcode in PRODUCTIVE)
    operational = productive + sum(action_counts[opcode] for opcode in HANDLING)
    moves = sum(action_counts[opcode] for opcode in MOVES)
    return {
        "status": str(terminal.get("status", "UNKNOWN")),
        "money": float(farm.get("money", 0.0)),
        "final_quadrants": len(farm.get("unlocked_quadrants", []) or []),
        "final_crops": crops,
        "final_animals": animals,
        "final_cows": int(species["COW"]),
        "final_sheep": int(species["SHEEP"]),
        "final_geese": int(species["GOOSE"]),
        "peak_quadrants": peak_quadrants,
        "peak_hands": peak_hands,
        "peak_crops": peak_crops,
        "peak_animals": peak_animals,
        "animal_escapes": escapes,
        "move_actions": moves,
        "productive_actions": productive,
        "operational_actions": operational,
        "pass_actions": int(action_counts["PASS"]),
        "move_per_productive": moves / productive if productive else None,
        "move_per_operational": moves / operational if operational else None,
        "action_counts": dict(action_counts),
        "market_counts": dict(market_counts),
    }


def run_match(seed: int, p0: str, p1: str) -> dict[str, Any]:
    fn0, obj0 = _agent(p0, seed, 0)
    fn1, obj1 = _agent(p1, seed, 1)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run([fn0, fn1])
    metrics0 = _seat_metrics(env, 0)
    metrics1 = _seat_metrics(env, 1)
    winner = p0 if metrics0["money"] > metrics1["money"] else p1 if metrics1["money"] > metrics0["money"] else "TIE"
    return {
        "seed": seed,
        "p0": p0,
        "p1": p1,
        "winner": winner,
        "margin_p0": metrics0["money"] - metrics1["money"],
        "p0_metrics": metrics0,
        "p1_metrics": metrics1,
        "p0_errors": int(getattr(obj0, "error_count", 0)),
        "p1_errors": int(getattr(obj1, "error_count", 0)),
        "p0_fallbacks": int(getattr(obj0, "fallback_count", 0)),
        "p1_fallbacks": int(getattr(obj1, "fallback_count", 0)),
    }


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, Any]:
    standings: dict[str, dict[str, Any]] = {}
    for name in ("ANTIGRAVITY", "COPILOT", "CODEX"):
        scores: list[float] = []
        wins = losses = ties = 0
        seat_scores = {0: [], 1: []}
        metrics: list[dict[str, Any]] = []
        errors = fallbacks = 0
        for match in matches:
            if match["p0"] == name:
                seat = 0
                own = match["p0_metrics"]
                errors += match["p0_errors"]
                fallbacks += match["p0_fallbacks"]
            elif match["p1"] == name:
                seat = 1
                own = match["p1_metrics"]
                errors += match["p1_errors"]
                fallbacks += match["p1_fallbacks"]
            else:
                continue
            scores.append(float(own["money"]))
            seat_scores[seat].append(float(own["money"]))
            metrics.append(own)
            if match["winner"] == name:
                wins += 1
            elif match["winner"] == "TIE":
                ties += 1
            else:
                losses += 1
        standings[name] = {
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "matches": len(scores),
            "win_rate": wins / len(scores) if scores else 0.0,
            "money_mean": statistics.fmean(scores) if scores else 0.0,
            "money_median": statistics.median(scores) if scores else 0.0,
            "money_min": min(scores) if scores else 0.0,
            "money_max": max(scores) if scores else 0.0,
            "seat0_money_mean": statistics.fmean(seat_scores[0]) if seat_scores[0] else 0.0,
            "seat1_money_mean": statistics.fmean(seat_scores[1]) if seat_scores[1] else 0.0,
            "animal_escapes_total": sum(int(row["animal_escapes"]) for row in metrics),
            "peak_hands_max": max(int(row["peak_hands"]) for row in metrics) if metrics else 0,
            "peak_crops_max": max(int(row["peak_crops"]) for row in metrics) if metrics else 0,
            "peak_animals_max": max(int(row["peak_animals"]) for row in metrics) if metrics else 0,
            "move_per_productive_mean": statistics.fmean(float(row["move_per_productive"]) for row in metrics) if metrics else 0.0,
            "move_per_operational_mean": statistics.fmean(float(row["move_per_operational"]) for row in metrics) if metrics else 0.0,
            "pass_actions_mean": statistics.fmean(float(row["pass_actions"]) for row in metrics) if metrics else 0.0,
            "productive_actions_mean": statistics.fmean(float(row["productive_actions"]) for row in metrics) if metrics else 0.0,
            "operational_actions_mean": statistics.fmean(float(row["operational_actions"]) for row in metrics) if metrics else 0.0,
            "errors": errors,
            "fallbacks": fallbacks,
        }
    return standings


def main() -> int:
    matches: list[dict[str, Any]] = []
    for seed in SEEDS:
        for first, second in PAIRS:
            for p0, p1 in ((first, second), (second, first)):
                match = run_match(seed, p0, p1)
                matches.append(match)
                print(
                    f"[{len(matches):02d}/42] seed={seed} {p0} "
                    f"{match['p0_metrics']['money']:.0f} - "
                    f"{match['p1_metrics']['money']:.0f} {p1} "
                    f"winner={match['winner']}"
                )

    standings = _aggregate(matches)
    payload = {
        "protocol": "ANTIGRAVITY_V4_0_3Q_THREE_WAY_FROZEN_V1",
        "seeds": list(SEEDS),
        "seat_balanced": True,
        "post_hoc_selection": False,
        "matches": matches,
        "standings": standings,
    }
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    flat_rows = [
        {
            "seed": match["seed"],
            "p0": match["p0"],
            "p1": match["p1"],
            "p0_money": match["p0_metrics"]["money"],
            "p1_money": match["p1_metrics"]["money"],
            "winner": match["winner"],
            "margin_p0": match["margin_p0"],
            "p0_quadrants": match["p0_metrics"]["final_quadrants"],
            "p1_quadrants": match["p1_metrics"]["final_quadrants"],
            "p0_peak_animals": match["p0_metrics"]["peak_animals"],
            "p1_peak_animals": match["p1_metrics"]["peak_animals"],
            "p0_peak_crops": match["p0_metrics"]["peak_crops"],
            "p1_peak_crops": match["p1_metrics"]["peak_crops"],
            "p0_escapes": match["p0_metrics"]["animal_escapes"],
            "p1_escapes": match["p1_metrics"]["animal_escapes"],
        }
        for match in matches
    ]
    with RESULT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat_rows[0]))
        writer.writeheader()
        writer.writerows(flat_rows)
    print(json.dumps(standings, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
