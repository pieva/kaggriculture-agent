#!/usr/bin/env python3
"""Run the non-qualifying E17 reactive three-way development exhibition."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import sys
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.claude.e17_reactive_3q_v2 import (
    create_claude_e17_agent_v2,
)
from agricola.strategy.codex.codex_3q_mixed_high_density import create_v9_agent
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    create_codex_e17_reactive_agent,
)
from agricola.strategy.codex.codex_v9_routine_data import ROUTINE_SHA256

ROOT = Path(__file__).resolve().parents[4]
MANIFEST = ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
CODEX_REACTIVE_FREEZE = (
    ROOT
    / "docs/model_specs/codex/e17/artifacts/freeze/e17_1/E17_1_FREEZE_MANIFEST.json"
)
CLAUDE_V2_FREEZE = (
    ROOT
    / "docs/model_specs/claude/e17/artifacts/freeze/e17_1_v2/E17_1_V2_FREEZE_MANIFEST.json"
)
V9_SOURCE = ROOT / "src/agricola/strategy/codex/codex_3q_mixed_high_density.py"
V9_CONFIG = (
    ROOT
    / "docs/model_specs/codex/configs/"
    / "CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json"
)
DEFAULT_JSON = (
    ROOT
    / "experiments/e17/artifacts/derived/common/"
    / "E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION.json"
)
DEFAULT_CSV = (
    ROOT
    / "experiments/e17/artifacts/derived/common/"
    / "E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION.csv"
)
EXPECTED_ROUTINE_SHA256 = (
    "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"
)
PARTICIPANTS = ("CODEX_V9", "CODEX_REACTIVE", "CLAUDE_V2")
PAIRS = (
    ("CODEX_V9", "CODEX_REACTIVE"),
    ("CODEX_V9", "CLAUDE_V2"),
    ("CODEX_REACTIVE", "CLAUDE_V2"),
)
MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})
PRODUCTIVE = frozenset(
    {
        "PLANT",
        "WATER",
        "HARVEST",
        "DIG",
        "BUILD_PASTURE",
        "BUILD_COOP",
        "FEED",
        "CARE",
        "COLLECT_FERTILIZER",
        "FERTILIZE",
    }
)
HANDLING = frozenset({"PICKUP", "PLACE"})
QUADRANTS = {
    "Q0_NW": (range(5), range(5)),
    "Q1_NE": (range(5, 10), range(5)),
    "Q2_SW": (range(5), range(5, 10)),
    "Q3_SE": (range(5, 10), range(5, 10)),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _verify_provenance() -> dict[str, Any]:
    common = _load_json(MANIFEST)
    codex = _load_json(CODEX_REACTIVE_FREEZE)
    claude = _load_json(CLAUDE_V2_FREEZE)
    if codex.get("status") != "FROZEN_FOR_REACTIVE_TOURNAMENT":
        raise RuntimeError("Codex reactive freeze is not admissible")
    if claude.get("status") != "FROZEN_WITH_FAILED_GATES":
        raise RuntimeError("Claude V2 status changed; review the exhibition protocol")
    codex_source = ROOT / codex["source_path"]
    codex_config = ROOT / codex["config_path"]
    claude_source = ROOT / claude["source"]["path"]
    claude_config = ROOT / claude["config"]["path"]
    observed = {
        "codex_reactive_source": _sha256(codex_source),
        "codex_reactive_config": _sha256(codex_config),
        "claude_v2_source": _sha256(claude_source),
        "claude_v2_config": _sha256(claude_config),
        "codex_v9_source": _sha256(V9_SOURCE),
        "codex_v9_config": _sha256(V9_CONFIG),
        "codex_v9_routine": ROUTINE_SHA256,
    }
    expected = {
        "codex_reactive_source": codex["source_sha256"],
        "codex_reactive_config": codex["config_sha256"],
        "claude_v2_source": claude["source"]["sha256"],
        "claude_v2_config": claude["config"]["sha256"],
        "codex_v9_source": common["opponents"]["codex_v9_freeze"][
            "source_sha256"
        ],
        "codex_v9_config": common["opponents"]["codex_v9_freeze"][
            "config_sha256"
        ],
        "codex_v9_routine": EXPECTED_ROUTINE_SHA256,
    }
    if observed != expected:
        raise RuntimeError(f"candidate provenance mismatch: {observed}")
    return {
        "observed_sha256": observed,
        "codex_reactive_freeze_status": codex["status"],
        "claude_v2_freeze_status": claude["status"],
        "claude_v2_gate_status": claude["gate_status"],
    }


def _factory(name: str, seed: int, seat: int) -> tuple[Callable[..., Any], Any]:
    context = {
        "run_id": f"E17-DEV-EXHIBITION-S{seed}-P{seat}-{name}",
        "episode_id": f"E17-DEV-EXHIBITION-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == "CODEX_V9":
        policy = create_v9_agent(run_context=context)
        return policy, policy.codex_v9_instance
    if name == "CODEX_REACTIVE":
        policy = create_codex_e17_reactive_agent(run_context=context)
        return policy, policy.codex_e17_instance
    if name == "CLAUDE_V2":
        policy = create_claude_e17_agent_v2(run_context=context)
        return policy, policy
    raise ValueError(name)


def _farm_from_state(state: list[Any], seat: int) -> dict[str, Any]:
    observation = state[seat].get("observation", {}) or {}
    farms = observation.get("farms", []) or []
    return farms[seat] if seat < len(farms) else {}


def _animal_counts(farm: dict[str, Any]) -> Counter[str]:
    return Counter(
        str(tile["animal"])
        for row in farm.get("tiles", []) or []
        for tile in row
        if isinstance(tile, dict) and tile.get("animal")
    )


def _crop_counts(farm: dict[str, Any]) -> Counter[str]:
    return Counter(
        str(tile.get("crop") or "UNKNOWN")
        for row in farm.get("tiles", []) or []
        for tile in row
        if isinstance(tile, dict) and tile.get("kind") == "PLANT"
    )


def _quadrant_profile(farm: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tiles = farm.get("tiles", []) or []
    result: dict[str, dict[str, Any]] = {}
    for name, (xs, ys) in QUADRANTS.items():
        usage: Counter[str] = Counter()
        crops: Counter[str] = Counter()
        animals: Counter[str] = Counter()
        for y in ys:
            for x in xs:
                tile = tiles[y][x] if y < len(tiles) and x < len(tiles[y]) else None
                if not isinstance(tile, dict):
                    usage["NON_PRODUCTIVE"] += 1
                    continue
                if tile.get("animal"):
                    species = str(tile["animal"])
                    animals[species] += 1
                    usage["ANIMAL"] += 1
                elif tile.get("kind") == "PLANT":
                    crop = str(tile.get("crop") or "UNKNOWN")
                    crops[crop] += 1
                    usage["CROP"] += 1
                elif tile.get("kind") in {"PASTURE", "COOP"}:
                    usage["EMPTY_LIVESTOCK_TILE"] += 1
                else:
                    usage["NON_PRODUCTIVE"] += 1
        result[name] = {
            "usage": dict(sorted(usage.items())),
            "crops": dict(sorted(crops.items())),
            "animals": dict(sorted(animals.items())),
        }
    return result


def _seat_metrics(env: Any, seat: int, controller: Any) -> dict[str, Any]:
    action_counts: Counter[str] = Counter()
    market_counts: Counter[str] = Counter()
    q1_activation_day = None
    q2_activation_day = None
    peak_hands = 0
    peak_crops = 0
    peak_animals = 0
    peak_quadrants = 0
    escapes = 0
    previous_day = None
    previous_animal_count = 0

    for state in env.steps:
        record = state[seat]
        observation = record.get("observation", {}) or {}
        farm = _farm_from_state(state, seat)
        day = int(observation.get("day", 0))
        quadrants = len(farm.get("unlocked_quadrants", []) or [])
        hands = len(farm.get("hands", []) or [])
        crops = sum(_crop_counts(farm).values())
        animals = sum(_animal_counts(farm).values())
        if previous_day is not None and day > previous_day:
            escapes += max(0, previous_animal_count - animals)
        previous_day = day
        previous_animal_count = animals
        if quadrants >= 2 and q1_activation_day is None:
            q1_activation_day = day
        if quadrants >= 3 and q2_activation_day is None:
            q2_activation_day = day
        peak_hands = max(peak_hands, hands)
        peak_crops = max(peak_crops, crops)
        peak_animals = max(peak_animals, animals)
        peak_quadrants = max(peak_quadrants, quadrants)

        action = record.get("action", {}) or {}
        commands = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
        for command in commands:
            if command:
                action_counts[str(command[0])] += 1
        for order in action.get("market", []) or []:
            if order:
                item = str(order[1]) if len(order) >= 2 else "NONE"
                quantity = int(order[2]) if len(order) >= 3 else 1
                market_counts[f"{order[0]}:{item}"] += quantity

    terminal = env.steps[-1][seat]
    farm = _farm_from_state(env.steps[-1], seat)
    crops = _crop_counts(farm)
    animals = _animal_counts(farm)
    productive = sum(action_counts[name] for name in PRODUCTIVE)
    handling = sum(action_counts[name] for name in HANDLING)
    moves = sum(action_counts[name] for name in MOVES)
    error_count = int(
        getattr(controller, "error_count", getattr(controller, "technical_errors", 0))
    )
    fallback_count = int(getattr(controller, "fallback_count", 0))
    return {
        "status": str(terminal.get("status", "UNKNOWN")),
        "money": float(farm.get("money", 0.0) or 0.0),
        "q1_activation_day": q1_activation_day,
        "q2_activation_day": q2_activation_day,
        "final_quadrants": len(farm.get("unlocked_quadrants", []) or []),
        "peak_quadrants": peak_quadrants,
        "peak_hands": peak_hands,
        "peak_crops": peak_crops,
        "peak_animals": peak_animals,
        "animal_escapes": escapes,
        "final_crops": dict(sorted(crops.items())),
        "final_animals": dict(sorted(animals.items())),
        "final_quadrant_profile": _quadrant_profile(farm),
        "move_actions": moves,
        "productive_actions": productive,
        "handling_actions": handling,
        "pass_actions": int(action_counts["PASS"]),
        "move_per_productive": moves / productive if productive else None,
        "action_counts": dict(sorted(action_counts.items())),
        "market_counts": dict(sorted(market_counts.items())),
        "technical_errors": error_count,
        "fallbacks": fallback_count,
        "reactive_override_batches": int(getattr(controller, "override_count", 0)),
        "detected_unfilled_wheat_units": int(
            getattr(controller, "detected_unfilled_wheat_units", 0)
        ),
    }


def _run_match(seed: int, p0: str, p1: str) -> dict[str, Any]:
    policy0, controller0 = _factory(p0, seed, 0)
    policy1, controller1 = _factory(p1, seed, 1)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run([policy0, policy1])
    metrics0 = _seat_metrics(env, 0, controller0)
    metrics1 = _seat_metrics(env, 1, controller1)
    if metrics0["money"] > metrics1["money"]:
        winner = p0
    elif metrics1["money"] > metrics0["money"]:
        winner = p1
    else:
        winner = "TIE"
    return {
        "seed": seed,
        "p0": p0,
        "p1": p1,
        "winner": winner,
        "margin_p0": metrics0["money"] - metrics1["money"],
        "p0_metrics": metrics0,
        "p1_metrics": metrics1,
    }


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    standings: dict[str, dict[str, Any]] = {}
    for participant in PARTICIPANTS:
        rows: list[dict[str, Any]] = []
        scores: list[float] = []
        seat_scores: dict[int, list[float]] = {0: [], 1: []}
        wins = losses = ties = 0
        for match in matches:
            if match["p0"] == participant:
                seat = 0
                metrics = match["p0_metrics"]
            elif match["p1"] == participant:
                seat = 1
                metrics = match["p1_metrics"]
            else:
                continue
            rows.append(metrics)
            scores.append(float(metrics["money"]))
            seat_scores[seat].append(float(metrics["money"]))
            if match["winner"] == participant:
                wins += 1
            elif match["winner"] == "TIE":
                ties += 1
            else:
                losses += 1
        standings[participant] = {
            "rank_basis": "wins_then_mean_money",
            "matches": len(rows),
            "wins": wins,
            "ties": ties,
            "losses": losses,
            "win_rate": wins / len(rows) if rows else 0.0,
            "money_mean": statistics.fmean(scores) if scores else 0.0,
            "money_median": statistics.median(scores) if scores else 0.0,
            "money_min": min(scores) if scores else 0.0,
            "money_max": max(scores) if scores else 0.0,
            "money_population_stddev": statistics.pstdev(scores) if scores else 0.0,
            "seat0_money_mean": statistics.fmean(seat_scores[0]) if seat_scores[0] else 0.0,
            "seat1_money_mean": statistics.fmean(seat_scores[1]) if seat_scores[1] else 0.0,
            "three_quadrant_runs": sum(row["peak_quadrants"] >= 3 for row in rows),
            "animal_escapes_total": sum(row["animal_escapes"] for row in rows),
            "technical_errors": sum(row["technical_errors"] for row in rows),
            "fallbacks": sum(row["fallbacks"] for row in rows),
            "reactive_override_batches": sum(
                row["reactive_override_batches"] for row in rows
            ),
            "detected_unfilled_wheat_units": sum(
                row["detected_unfilled_wheat_units"] for row in rows
            ),
            "q1_activation_day_median": statistics.median(
                row["q1_activation_day"]
                for row in rows
                if row["q1_activation_day"] is not None
            ),
            "q2_activation_day_median": statistics.median(
                row["q2_activation_day"]
                for row in rows
                if row["q2_activation_day"] is not None
            ) if any(row["q2_activation_day"] is not None for row in rows) else None,
            "peak_hands_max": max(row["peak_hands"] for row in rows),
            "move_per_productive_mean": statistics.fmean(
                row["move_per_productive"]
                for row in rows
                if row["move_per_productive"] is not None
            ),
        }
    return standings


def _head_to_head(matches: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for first, second in PAIRS:
        selected = [
            match
            for match in matches
            if {match["p0"], match["p1"]} == {first, second}
        ]
        first_wins = sum(match["winner"] == first for match in selected)
        second_wins = sum(match["winner"] == second for match in selected)
        ties = sum(match["winner"] == "TIE" for match in selected)
        deltas = []
        for match in selected:
            if match["p0"] == first:
                deltas.append(
                    match["p0_metrics"]["money"] - match["p1_metrics"]["money"]
                )
            else:
                deltas.append(
                    match["p1_metrics"]["money"] - match["p0_metrics"]["money"]
                )
        result[f"{first}_vs_{second}"] = {
            f"{first}_wins": first_wins,
            f"{second}_wins": second_wins,
            "ties": ties,
            f"{first}_mean_money_delta": statistics.fmean(deltas),
        }
    return result


def _write_csv(path: Path, matches: list[dict[str, Any]]) -> None:
    rows = []
    for match in matches:
        row = {
            "seed": match["seed"],
            "p0": match["p0"],
            "p1": match["p1"],
            "p0_money": match["p0_metrics"]["money"],
            "p1_money": match["p1_metrics"]["money"],
            "winner": match["winner"],
            "margin_p0": match["margin_p0"],
            "p0_q1_day": match["p0_metrics"]["q1_activation_day"],
            "p1_q1_day": match["p1_metrics"]["q1_activation_day"],
            "p0_q2_day": match["p0_metrics"]["q2_activation_day"],
            "p1_q2_day": match["p1_metrics"]["q2_activation_day"],
            "p0_peak_hands": match["p0_metrics"]["peak_hands"],
            "p1_peak_hands": match["p1_metrics"]["peak_hands"],
            "p0_escapes": match["p0_metrics"]["animal_escapes"],
            "p1_escapes": match["p1_metrics"]["animal_escapes"],
            "p0_overrides": match["p0_metrics"]["reactive_override_batches"],
            "p1_overrides": match["p1_metrics"]["reactive_override_batches"],
        }
        rows.append(row)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(seeds: list[int], output_json: Path, output_csv: Path) -> dict[str, Any]:
    provenance = _verify_provenance()
    matches = []
    total = len(seeds) * len(PAIRS) * 2
    for seed in seeds:
        for first, second in PAIRS:
            for p0, p1 in ((first, second), (second, first)):
                match = _run_match(seed, p0, p1)
                matches.append(match)
                print(
                    f"[{len(matches):02d}/{total:02d}] seed={seed} "
                    f"{p0}={match['p0_metrics']['money']:.0f} "
                    f"{p1}={match['p1_metrics']['money']:.0f} "
                    f"winner={match['winner']}",
                    flush=True,
                )
    payload = {
        "schema_version": "E17_REACTIVE_THREE_WAY_DEV_EXHIBITION_V1",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "official_tournament_admission": "BLOCKED_CLAUDE_V2_FAILED_GATES",
        "participants": list(PARTICIPANTS),
        "seeds": seeds,
        "seat_balanced": True,
        "post_hoc_seed_removal": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "provenance": provenance,
        "matches": matches,
        "standings": _aggregate(matches),
        "head_to_head": _head_to_head(matches),
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _write_csv(output_csv, matches)
    return payload


def main(argv: list[str] | None = None) -> int:
    common = _load_json(MANIFEST)
    development = list(common["seed_policy"]["development"])
    forbidden = set(common["seed_policy"]["holdout"]["seeds"]) | set(
        common["seed_policy"]["final_confirmation"]["seeds"]
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=development)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args(argv)
    if not set(args.seeds).issubset(set(development)):
        raise SystemExit("only preregistered development seeds are permitted")
    if forbidden.intersection(args.seeds):
        raise SystemExit("holdout/final-confirmation seed access is forbidden")
    payload = run(args.seeds, args.output_json, args.output_csv)
    print(json.dumps(payload["standings"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
