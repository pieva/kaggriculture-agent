#!/usr/bin/env python3
"""Run the dual-quadrant Antigravity 75K performance benchmark."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.antigravity.agent_c2_75k import (
    DUAL_MODEL_SPEC_VERSION,
    create_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = REPO_ROOT / "results" / "model_spec_c2" / "antigravity"
DEFAULT_CSV = RESULT_DIR / "ANTIGRAVITY_75K_RESULTS.csv"
DEFAULT_JSON = RESULT_DIR / "ANTIGRAVITY_75K_RESULTS.json"

PHASE_B_SEEDS = (26090101, 26090102, 26090103)
PHASE_A_C_SEEDS = (1838889274, 1619968655, 710418712)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def inert_policy(
    observation: dict[str, Any], configuration: Any = None
) -> dict[str, Any]:
    del observation, configuration
    return dict(SAFE_PASS)


def _quadrant_counts(farm: dict[str, Any]) -> dict[str, int]:
    counts = {
        "q0_active_crops": 0,
        "q1_active_crops": 0,
        "q2_active_crops": 0,
        "q0_animals": 0,
        "q1_animals": 0,
        "q2_animals": 0,
        "q0_cows": 0,
        "q0_sheep": 0,
        "q1_cows": 0,
        "q1_sheep": 0,
        "owned_tiles": 0,
    }
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row):
            if tile != "LOCKED":
                counts["owned_tiles"] += 1
            if not isinstance(tile, dict):
                continue
            module = "q0" if x < 5 and y < 5 else "q1" if x >= 5 and y < 5 else "q2" if x < 5 and y >= 5 else None
            if module is None:
                continue
            if tile.get("kind") == "PLANT":
                counts[f"{module}_active_crops"] += 1
            animal = tile.get("animal")
            if animal:
                counts[f"{module}_animals"] += 1
                if animal == "COW":
                    counts[f"{module}_cows"] += 1
                elif animal == "SHEEP":
                    counts[f"{module}_sheep"] += 1
    return counts


def run_episode(*, seed: int, seat: int, sequence: int) -> dict[str, Any]:
    episode_agent = create_agent(
        run_context={
            "run_id": "antigravity-dual-q0-q1-75k-20260831",
            "episode_id": f"antigravity-75k-{sequence:04d}",
            "seed": seed,
            "opponent_id": "INERT_PASS_POLICY",
            "player_position": seat,
        }
    )
    agents = [episode_agent, inert_policy] if seat == 0 else [inert_policy, episode_agent]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    terminal = env.steps[-1][seat]
    observation = terminal.get("observation", {}) or {}
    farms = observation.get("farms", []) or []
    farm = farms[seat] if seat < len(farms) else {}
    instance = episode_agent.antigravity_75k_instance
    telemetry = instance.telemetry_snapshot()
    status = str(terminal.get("status", "UNKNOWN"))
    final_money = float(farm.get("money", 0.0))
    q_counts = _quadrant_counts(farm)

    return {
        "episode_sequence": sequence,
        "seed": seed,
        "seat": seat,
        "opponent": "INERT_PASS_POLICY",
        "status": status,
        "final_money": final_money,
        "technical_error_count": instance.error_count,
        "technical_fallback_count": instance.fallback_count,
        "last_exception": instance.last_exception,
        "milk_units": int(telemetry.get("MILK_units", 0)),
        "wool_units": int(telemetry.get("WOOL_units", 0)),
        "melon_units": int(telemetry.get("MELON_units", 0)),
        "strawberry_units": int(telemetry.get("STRAWBERRY_units", 0)),
        "total_crop_units": int(telemetry.get("MELON_units", 0)) + int(telemetry.get("STRAWBERRY_units", 0)),
        "fertilizer_collected": int(telemetry.get("fertilizer_collected", 0)),
        "fertilizer_applied": int(telemetry.get("fertilizer_applied", 0)),
        "animal_escapes": int(telemetry.get("ANIMAL_ESCAPE", 0)),
        "wheat_consumed": int(telemetry.get("WHEAT_consumed", 0)),
        "productive_actions": int(telemetry.get("productive_actions", 0)),
        "move_actions": int(telemetry.get("MOVE_actions", 0)),
        "pass_actions": int(telemetry.get("PASS_actions", 0)),
        "move_per_productive_action": float(telemetry.get("MOVE_PER_PRODUCTIVE_ACTION", 0.0)),
        "hard_deadline_misses": int(telemetry.get("HARD_DEADLINE_MISSES", 0)),
        "crop_revenue": float(telemetry.get("crop_revenue", 0.0)),
        "livestock_revenue": float(telemetry.get("livestock_revenue", 0.0)),
        "owned_quadrants": 2 if q_counts["owned_tiles"] >= 50 else 1,
        "q0_active_crops": q_counts["q0_active_crops"],
        "q1_active_crops": q_counts["q1_active_crops"],
        "q0_animals": q_counts["q0_animals"],
        "q1_animals": q_counts["q1_animals"],
        "q0_cows": q_counts["q0_cows"],
        "q0_sheep": q_counts["q0_sheep"],
        "q1_cows": q_counts["q1_cows"],
        "q1_sheep": q_counts["q1_sheep"],
        "q1_activation_day": instance.q1_activation_day,
    }


def aggregate_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    final_moneys = [float(r["final_money"]) for r in rows]
    return {
        "candidate_version": DUAL_MODEL_SPEC_VERSION,
        "episode_count": len(rows),
        "seeds": sorted({int(r["seed"]) for r in rows}),
        "seats": sorted({int(r["seat"]) for r in rows}),
        "final_money_mean": statistics.mean(final_moneys),
        "final_money_median": statistics.median(final_moneys),
        "final_money_min": min(final_moneys),
        "final_money_max": max(final_moneys),
        "final_money_std": statistics.stdev(final_moneys) if len(final_moneys) > 1 else 0.0,
        "animal_escapes_total": sum(int(r["animal_escapes"]) for r in rows),
        "hard_deadline_misses_total": sum(int(r["hard_deadline_misses"]) for r in rows),
        "milk_mean": statistics.mean(float(r["milk_units"]) for r in rows),
        "wool_mean": statistics.mean(float(r["wool_units"]) for r in rows),
        "melon_mean": statistics.mean(float(r["melon_units"]) for r in rows),
        "strawberry_mean": statistics.mean(float(r["strawberry_units"]) for r in rows),
        "total_crop_units_mean": statistics.mean(float(r["total_crop_units"]) for r in rows),
        "move_per_productive_action_mean": statistics.mean(float(r["move_per_productive_action"]) for r in rows),
        "crop_revenue_mean": statistics.mean(float(r["crop_revenue"]) for r in rows),
        "livestock_revenue_mean": statistics.mean(float(r["livestock_revenue"]) for r in rows),
        "q1_activation_day_mean": statistics.mean(float(r["q1_activation_day"] or 0) for r in rows),
        "technical_pass": all(r["status"] == "DONE" and r["technical_error_count"] == 0 for r in rows),
    }


def run_benchmark(seeds: tuple[int, ...], protocol_name: str, csv_path: Path, json_path: Path) -> dict[str, Any]:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    sequence = 0

    print(f"\n{'='*75}")
    print(f"RUNNING BENCHMARK: {protocol_name}")
    print(f"Seeds: {seeds} | Seats: (0, 1) | Total Episodes: {len(seeds)*2}")
    print(f"{'='*75}\n")

    for seed in seeds:
        for seat in (0, 1):
            sequence += 1
            print(f"Running Episode {sequence}/6: Seed {seed} | Seat {seat} ...", end=" ", flush=True)
            result = run_episode(seed=seed, seat=seat, sequence=sequence)
            rows.append(result)
            print(f"DONE | Money: ${result['final_money']:,.2f} | Milk: {result['milk_units']} | Wool: {result['wool_units']} | Melon: {result['melon_units']} | Straw: {result['strawberry_units']} | Escapes: {result['animal_escapes']}")

    aggregate = aggregate_rows(rows)

    # Write CSV
    if rows:
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    # Write JSON
    payload = {
        "protocol": protocol_name,
        "post_hoc_seed_selection": False,
        "aggregate": aggregate,
        "rows": rows,
        "TOURNAMENT_AUTHORIZED": "NO",
        "KAGGLE_AUTHORIZED": "NO",
    }
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)

    print(f"\n{'-'*75}")
    print(f"BENCHMARK SUMMARY ({protocol_name})")
    print(f"Mean Final Money:   ${aggregate['final_money_mean']:,.2f}")
    print(f"Median Final Money: ${aggregate['final_money_median']:,.2f}")
    print(f"Min / Max Money:    ${aggregate['final_money_min']:,.2f} / ${aggregate['final_money_max']:,.2f}")
    print(f"Animal Escapes:     {aggregate['animal_escapes_total']}")
    print(f"Milk / Wool Mean:   {aggregate['milk_mean']:.2f} / {aggregate['wool_mean']:.2f}")
    print(f"Crop Units Mean:    {aggregate['total_crop_units_mean']:.2f} (Melon: {aggregate['melon_mean']:.2f}, Straw: {aggregate['strawberry_mean']:.2f})")
    print(f"Technical Pass:     {aggregate['technical_pass']}")
    print(f"{'='*75}\n")

    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Antigravity 75K dual-quadrant benchmark.")
    parser.add_argument("--phase", choices=["b", "c", "all"], default="b", help="Benchmark phase to execute.")
    args = parser.parse_args()

    if args.phase in ("b", "all"):
        run_benchmark(
            PHASE_B_SEEDS,
            "ANTIGRAVITY_75K_DUAL_Q_PHASE_B",
            RESULT_DIR / "ANTIGRAVITY_75K_RESULTS.csv",
            RESULT_DIR / "ANTIGRAVITY_75K_RESULTS.json",
        )
    if args.phase in ("c", "all"):
        run_benchmark(
            PHASE_A_C_SEEDS,
            "ANTIGRAVITY_75K_DUAL_Q_PHASE_C",
            RESULT_DIR / "ANTIGRAVITY_75K_PHASE_C_RESULTS.csv",
            RESULT_DIR / "ANTIGRAVITY_75K_PHASE_C_RESULTS.json",
        )
