#!/usr/bin/env python3
"""Frozen post-3Q closure tournament with explicit provenance gates."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[1]
FREEZE_DIR = (
    ROOT
    / "results"
    / "model_spec_c2"
    / "post_3q_closure_tournament"
    / "freeze"
)
FROZEN = {
    "ANTIGRAVITY": FREEZE_DIR / "submission_antigravity_v4.py",
    "CODEX": FREEZE_DIR / "submission_codex_v9.py",
    "COPILOT": FREEZE_DIR / "submission_copilot_v2.py",
}
EXPECTED_SHA256 = {
    "ANTIGRAVITY": "5786AC521DDC0931539032ED1A4D642F75846911A078E8E8E82535C7F4757872",
    "CODEX": "AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421",
    "COPILOT": "DABD7FEFBBBC36396AEE04BD883CE0770D4B96D1312BB3CE009E051AC3C20A94",
}
RESULT_DIR = ROOT / "results" / "model_spec_c2" / "post_3q_closure_tournament"
RESULT_JSON = RESULT_DIR / "POST_3Q_CLOSURE_TOURNAMENT_RESULTS.json"
RESULT_CSV = RESULT_DIR / "POST_3Q_CLOSURE_TOURNAMENT_RESULTS.csv"

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


def _load_frozen_module(name: str):
    path = FROZEN[name]
    spec = importlib.util.spec_from_file_location(
        f"post_3q_closure_{name.lower()}", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FROZEN_MODULES = {name: _load_frozen_module(name) for name in FROZEN}


def _verify_freeze() -> dict[str, str]:
    observed = {
        name: hashlib.sha256(path.read_bytes()).hexdigest().upper()
        for name, path in FROZEN.items()
    }
    if observed != EXPECTED_SHA256:
        raise RuntimeError(f"frozen candidate hash mismatch: {observed}")
    routine_hashes = {
        str(FROZEN_MODULES[name].ROUTINE_SHA256) for name in FROZEN_MODULES
    }
    if routine_hashes != {
        "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"
    }:
        raise RuntimeError(f"unexpected routine provenance: {routine_hashes}")
    return observed


def _agent(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {"seed": seed, "seat": seat, "player_position": seat}
    if name in FROZEN_MODULES:
        instance = FROZEN_MODULES[name].create_agent(run_context=context)
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
    frozen_hashes = _verify_freeze()
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
        "protocol": "POST_3Q_CLOSURE_THREE_WAY_FROZEN_V1",
        "seeds": list(SEEDS),
        "seat_balanced": True,
        "post_hoc_selection": False,
        "strategic_independence_gate": "FAIL",
        "strategic_independence_reason": (
            "Antigravity V4 and Copilot V2 reuse Codex V9 ROUTINE_ACTIONS "
            "with the same routine SHA-256; results are closing replication, "
            "not independent agent attribution."
        ),
        "routine_sha256": {
            name: str(FROZEN_MODULES[name].ROUTINE_SHA256) for name in FROZEN_MODULES
        },
        "frozen_model_versions": {
            name: str(FROZEN_MODULES[name].MODEL_SPEC_VERSION)
            for name in FROZEN_MODULES
        },
        "frozen_file_sha256": frozen_hashes,
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
