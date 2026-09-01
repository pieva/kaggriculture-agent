#!/usr/bin/env python3
"""Canonical six-run verification for the Codex V8.0 3Q candidate."""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.codex_3q_elastic import (
    THREE_Q_MODEL_SPEC_VERSION,
    create_3q_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = REPO_ROOT / "results" / "model_spec_c2" / "codex"
RESULT_CSV = RESULT_DIR / "CODEX_V8_0_3Q_RESULTS.csv"
RESULT_JSON = RESULT_DIR / "CODEX_V8_0_3Q_RESULTS.json"
V73_RESULT_JSON = RESULT_DIR / "CODEX_V7_3_Q1_CADENCE_RESULTS.json"
SEEDS = (26090101, 26090102, 26090103)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def inert_policy(
    observation: dict[str, Any], configuration: Any = None
) -> dict[str, Any]:
    del observation, configuration
    return dict(SAFE_PASS)


def _mean(rows: list[dict[str, Any]], field: str) -> float:
    return statistics.fmean(float(row[field]) for row in rows)


def _optional_mean(rows: list[dict[str, Any]], field: str) -> float | None:
    values = [float(row[field]) for row in rows if row[field] is not None]
    return statistics.fmean(values) if values else None


def run_episode(*, seed: int, seat: int, sequence: int) -> dict[str, Any]:
    episode_agent = create_3q_agent(
        run_context={
            "run_id": "codex-v8-0-3q-canonical",
            "episode_id": f"codex-v8-3q-{sequence:04d}",
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
    farm = (observation.get("farms", []) or [])[seat]
    instance = episode_agent.codex_3q_instance
    telemetry = instance.telemetry_snapshot()
    service = telemetry["quadrant_livestock_service"]
    trajectory = telemetry["quadrant_state_trajectory"]
    q0_crop = int(telemetry["Q0_MELON_units"]) + int(
        telemetry["Q0_STRAWBERRY_units"]
    )
    q1_crop = int(telemetry["Q1_MELON_units"]) + int(
        telemetry["Q1_STRAWBERRY_units"]
    )
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
        "q2_activation_day": telemetry["Q2_activation_day"],
        "q2_full_module_day": telemetry["Q2_full_module_day"],
        "q2_first_output_day": telemetry["Q2_first_output_day"],
        "q2_first_output_product": telemetry["Q2_first_output_product"],
        "q2_max_active_animals": max(
            (int(row.get("q2_active_animals", 0)) for row in trajectory),
            default=0,
        ),
        "q2_milk_units": int(telemetry["Q2_MILK_units"]),
        "q2_wool_units": int(telemetry["Q2_WOOL_units"]),
        "q0_crop_units": q0_crop,
        "q1_crop_units": q1_crop,
        "milk_units": int(telemetry["MILK_units"]),
        "wool_units": int(telemetry["WOOL_units"]),
        "melon_units": int(telemetry["MELON_units"]),
        "strawberry_units": int(telemetry["STRAWBERRY_units"]),
        "fertilizer_collected": int(telemetry["fertilizer_collected"]),
        "productive_actions": int(telemetry["productive_actions"]),
        "move_actions": int(telemetry["MOVE_actions"]),
        "pass_actions": int(telemetry["PASS_actions"]),
        "move_per_productive_action": telemetry["MOVE_PER_PRODUCTIVE_ACTION"],
        "hard_deadline_misses": int(telemetry["HARD_DEADLINE_MISSES"]),
        "animal_escapes": int(telemetry["ANIMAL_ESCAPE"]),
        "q2_cow_feed_actions": int(service.get("Q2_COW_FEED", 0)),
        "q2_sheep_feed_actions": int(service.get("Q2_SHEEP_FEED", 0)),
        "q2_cow_harvest_actions": int(service.get("Q2_COW_HARVEST", 0)),
        "q2_sheep_harvest_actions": int(service.get("Q2_SHEEP_HARVEST", 0)),
        "q2_activation_records": json.dumps(
            telemetry["Q2_activation_records"], sort_keys=True
        ),
    }


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scores = [float(row["final_money"]) for row in rows]
    q0_crop = _mean(rows, "q0_crop_units")
    q1_crop = _mean(rows, "q1_crop_units")
    q2_output = _mean(rows, "q2_milk_units") + _mean(rows, "q2_wool_units")
    delta = statistics.fmean(scores) - 78036.16666666667
    q0_regression = max(0.0, (137.16666666666666 - q0_crop) / 137.16666666666666)
    q1_regression = max(0.0, (85.83333333333333 - q1_crop) / 85.83333333333333)
    technical_pass = all(
        row["status"] == "DONE"
        and int(row["technical_error_count"]) == 0
        and int(row["technical_fallback_count"]) == 0
        for row in rows
    )
    escapes = sum(int(row["animal_escapes"]) for row in rows)
    move_ratio = _mean(rows, "move_per_productive_action")
    central_gate = (
        technical_pass
        and statistics.fmean(scores) >= 90000
        and min(scores) >= 82000
        and delta >= 12000
        and q0_regression <= 0.03
        and q1_regression <= 0.03
        and escapes == 0
        and move_ratio <= 3.30
    )
    return {
        "candidate_version": THREE_Q_MODEL_SPEC_VERSION,
        "episode_count": len(rows),
        "seeds": list(SEEDS),
        "seats": [0, 1],
        "final_money_mean": statistics.fmean(scores),
        "final_money_median": statistics.median(scores),
        "final_money_min": min(scores),
        "final_money_max": max(scores),
        "final_money_std": statistics.pstdev(scores),
        "delta_vs_v7_3": delta,
        "q2_observed_net_contribution_mean": delta,
        "q2_activation_day_mean": _optional_mean(rows, "q2_activation_day"),
        "q2_full_module_day_mean": _optional_mean(rows, "q2_full_module_day"),
        "q2_first_output_day_mean": _optional_mean(rows, "q2_first_output_day"),
        "q2_max_active_animals_mean": _mean(rows, "q2_max_active_animals"),
        "q2_milk_units_mean": _mean(rows, "q2_milk_units"),
        "q2_wool_units_mean": _mean(rows, "q2_wool_units"),
        "q2_output_units_mean": q2_output,
        "q0_crop_units_mean": q0_crop,
        "q1_crop_units_mean": q1_crop,
        "q0_crop_regression": q0_regression,
        "q1_crop_regression": q1_regression,
        "milk_mean": _mean(rows, "milk_units"),
        "wool_mean": _mean(rows, "wool_units"),
        "fertilizer_collected_mean": _mean(rows, "fertilizer_collected"),
        "move_per_productive_action_mean": move_ratio,
        "animal_escapes_total": escapes,
        "hard_deadline_misses_total": sum(
            int(row["hard_deadline_misses"]) for row in rows
        ),
        "technical_pass": technical_pass,
        "minimum_gate_pass": (
            technical_pass
            and statistics.fmean(scores) >= 88000
            and min(scores) >= 78000
            and delta > 0
            and q0_regression <= 0.03
            and q1_regression <= 0.03
            and escapes == 0
            and move_ratio <= 3.50
        ),
        "central_gate_pass": central_gate,
    }


def main() -> int:
    baseline = json.loads(V73_RESULT_JSON.read_text(encoding="utf-8"))
    v73_scores = {
        (int(row["seed"]), int(row["seat"])): float(row["final_money"])
        for row in baseline["rows"]
    }
    rows: list[dict[str, Any]] = []
    sequence = 0
    for seed in SEEDS:
        for seat in (0, 1):
            sequence += 1
            row = run_episode(seed=seed, seat=seat, sequence=sequence)
            row["v7_3_final_money"] = v73_scores[(seed, seat)]
            row["paired_delta_vs_v7_3"] = (
                float(row["final_money"]) - v73_scores[(seed, seat)]
            )
            rows.append(row)
            print(
                f"[{sequence}/6] seed={seed} seat={seat} "
                f"money={row['final_money']:.2f} "
                f"delta_v73={row['paired_delta_vs_v7_3']:+.2f} "
                f"q2={row['q2_milk_units'] + row['q2_wool_units']} "
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
                "protocol": "CODEX_V8_0_3Q_CANONICAL",
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
