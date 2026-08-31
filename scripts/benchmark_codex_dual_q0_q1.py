#!/usr/bin/env python3
"""Evaluate the isolated Codex V7.2 Q0+Q1 candidate on six canonical runs."""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.codex_dual_q0_q1 import (
    DUAL_MODEL_SPEC_VERSION,
    create_dual_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = REPO_ROOT / "results" / "model_spec_c2" / "codex"
RESULT_CSV = RESULT_DIR / "CODEX_V7_2_DUAL_Q_RESULTS.csv"
RESULT_JSON = RESULT_DIR / "CODEX_V7_2_DUAL_Q_RESULTS.json"
SEEDS = (26090101, 26090102, 26090103)
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
        "q0_animals": 0,
        "q1_animals": 0,
        "q0_cows": 0,
        "q0_sheep": 0,
        "q1_cows": 0,
        "q1_sheep": 0,
    }
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            module = "q0" if x < 5 and y < 5 else "q1" if x >= 5 and y < 5 else None
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
    episode_agent = create_dual_agent(
        run_context={
            "run_id": "codex-v7-2-dual-q-canonical",
            "episode_id": f"codex-dual-q-{sequence:04d}",
            "seed": seed,
            "opponent_id": "INERT_PASS_POLICY",
            "player_position": seat,
        }
    )
    agents = (
        [episode_agent, inert_policy]
        if seat == 0
        else [inert_policy, episode_agent]
    )
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
    instance = episode_agent.codex_dual_instance
    telemetry = instance.telemetry_snapshot()
    return {
        "episode_sequence": sequence,
        "seed": seed,
        "seat": seat,
        "status": str(terminal.get("status", "UNKNOWN")),
        "final_money": float(farm.get("money", 0.0)),
        "technical_error_count": instance.error_count,
        "technical_fallback_count": instance.fallback_count,
        "last_exception": instance.last_exception,
        "owned_quadrants": len(farm.get("unlocked_quadrants", []) or []),
        "q1_activation_day": telemetry["Q1_activation_day"],
        "q1_full_module_day": telemetry["Q1_full_module_day"],
        "q1_first_output_day": telemetry["Q1_first_output_day"],
        "q1_first_output_product": telemetry["Q1_first_output_product"],
        "milk_units": int(telemetry["MILK_units"]),
        "wool_units": int(telemetry["WOOL_units"]),
        "melon_units": int(telemetry["MELON_units"]),
        "strawberry_units": int(telemetry["STRAWBERRY_units"]),
        "q0_melon_units": int(telemetry["Q0_MELON_units"]),
        "q0_strawberry_units": int(telemetry["Q0_STRAWBERRY_units"]),
        "q1_melon_units": int(telemetry["Q1_MELON_units"]),
        "q1_strawberry_units": int(telemetry["Q1_STRAWBERRY_units"]),
        "q0_milk_units": int(telemetry["Q0_MILK_units"]),
        "q0_wool_units": int(telemetry["Q0_WOOL_units"]),
        "q1_milk_units": int(telemetry["Q1_MILK_units"]),
        "q1_wool_units": int(telemetry["Q1_WOOL_units"]),
        "crop_revenue": float(telemetry["crop_revenue"]),
        "livestock_revenue": float(telemetry["livestock_revenue"]),
        "wheat_consumed": int(telemetry["WHEAT_consumed"]),
        "fertilizer_collected": int(telemetry["fertilizer_collected"]),
        "fertilizer_applied": int(telemetry["fertilizer_applied"]),
        "productive_actions": int(telemetry["productive_actions"]),
        "move_actions": int(telemetry["MOVE_actions"]),
        "pass_actions": int(telemetry["PASS_actions"]),
        "move_per_productive_action": telemetry["MOVE_PER_PRODUCTIVE_ACTION"],
        "hard_deadline_misses": int(telemetry["HARD_DEADLINE_MISSES"]),
        "animal_escapes": int(telemetry["ANIMAL_ESCAPE"]),
        "activation_records": json.dumps(
            telemetry["Q1_activation_records"], sort_keys=True
        ),
        **_quadrant_counts(farm),
    }


def _mean(rows: list[dict[str, Any]], field: str) -> float:
    return statistics.fmean(float(row[field]) for row in rows)


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scores = [float(row["final_money"]) for row in rows]
    q1_days = [
        float(row["q1_activation_day"])
        for row in rows
        if row["q1_activation_day"] is not None
    ]
    full_days = [
        float(row["q1_full_module_day"])
        for row in rows
        if row["q1_full_module_day"] is not None
    ]
    first_output_days = [
        float(row["q1_first_output_day"])
        for row in rows
        if row["q1_first_output_day"] is not None
    ]
    return {
        "candidate_version": DUAL_MODEL_SPEC_VERSION,
        "episode_count": len(rows),
        "seeds": list(SEEDS),
        "seats": [0, 1],
        "final_money_mean": statistics.fmean(scores),
        "final_money_median": statistics.median(scores),
        "final_money_min": min(scores),
        "final_money_max": max(scores),
        "final_money_std": statistics.pstdev(scores),
        "delta_vs_v7_1": statistics.fmean(scores) - 61118.833333333336,
        "q1_activation_day_mean": statistics.fmean(q1_days) if q1_days else None,
        "q1_full_module_day_mean": statistics.fmean(full_days) if full_days else None,
        "q1_first_output_day_mean": (
            statistics.fmean(first_output_days) if first_output_days else None
        ),
        "milk_mean": _mean(rows, "milk_units"),
        "wool_mean": _mean(rows, "wool_units"),
        "melon_mean": _mean(rows, "melon_units"),
        "strawberry_mean": _mean(rows, "strawberry_units"),
        "q0_crop_units_mean": _mean(rows, "q0_melon_units")
        + _mean(rows, "q0_strawberry_units"),
        "q1_crop_units_mean": _mean(rows, "q1_melon_units")
        + _mean(rows, "q1_strawberry_units"),
        "total_crop_units_mean": _mean(rows, "melon_units")
        + _mean(rows, "strawberry_units"),
        "crop_revenue_mean": _mean(rows, "crop_revenue"),
        "livestock_revenue_mean": _mean(rows, "livestock_revenue"),
        "productive_actions_mean": _mean(rows, "productive_actions"),
        "move_actions_mean": _mean(rows, "move_actions"),
        "pass_actions_mean": _mean(rows, "pass_actions"),
        "move_per_productive_action_mean": _mean(
            rows, "move_per_productive_action"
        ),
        "animal_escapes_total": sum(int(row["animal_escapes"]) for row in rows),
        "hard_deadline_misses_total": sum(
            int(row["hard_deadline_misses"]) for row in rows
        ),
        "technical_pass": all(
            row["status"] == "DONE"
            and int(row["technical_error_count"]) == 0
            and int(row["technical_fallback_count"]) == 0
            for row in rows
        ),
    }


def main() -> int:
    rows: list[dict[str, Any]] = []
    sequence = 0
    for seed in SEEDS:
        for seat in (0, 1):
            sequence += 1
            row = run_episode(seed=seed, seat=seat, sequence=sequence)
            rows.append(row)
            print(
                f"[{sequence}/6] seed={seed} seat={seat} "
                f"money={row['final_money']:.2f} "
                f"q1_day={row['q1_activation_day']} "
                f"escapes={row['animal_escapes']}"
            )
    summary = aggregate(rows)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    with RESULT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    RESULT_JSON.write_text(
        json.dumps(
            {
                "protocol": "CODEX_V7_2_DUAL_Q_CANONICAL",
                "post_hoc_seed_selection": False,
                "rows": rows,
                "aggregate": summary,
                "TOURNAMENT_AUTHORIZED": "NO",
                "KAGGLE_AUTHORIZED": "NO",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"wrote {RESULT_CSV}")
    print(f"wrote {RESULT_JSON}")
    return 0 if summary["technical_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
