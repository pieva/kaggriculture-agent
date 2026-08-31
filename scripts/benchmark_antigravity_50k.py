#!/usr/bin/env python3
"""Run the preregistered compact-Q0 Antigravity 50K performance benchmark."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.antigravity.agent_c2_50k import (
    MODEL_SPEC_VERSION,
    create_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = REPO_ROOT / "results" / "model_spec_c2" / "antigravity"
DEFAULT_CSV = RESULT_DIR / "ANTIGRAVITY_50K_RESULTS.csv"
DEFAULT_JSON = RESULT_DIR / "ANTIGRAVITY_50K_RESULTS.json"

PHASE_B_SEEDS = (26090101, 26090102, 26090103)
PHASE_A_C_SEEDS = (1838889274, 1619968655, 710418712)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def inert_policy(
    observation: dict[str, Any], configuration: Any = None
) -> dict[str, Any]:
    del observation, configuration
    return dict(SAFE_PASS)


def _final_counts(farm: dict[str, Any]) -> dict[str, int]:
    counts = {
        "active_crops": 0,
        "pastures": 0,
        "animals": 0,
        "cows": 0,
        "sheep": 0,
        "owned_tiles": 0,
    }
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if tile != "LOCKED":
                counts["owned_tiles"] += 1
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "PLANT":
                counts["active_crops"] += 1
            if tile.get("kind") == "PASTURE":
                counts["pastures"] += 1
            if tile.get("animal"):
                counts["animals"] += 1
                if tile.get("animal") == "COW":
                    counts["cows"] += 1
                elif tile.get("animal") == "SHEEP":
                    counts["sheep"] += 1
    return counts


def run_episode(*, seed: int, seat: int, sequence: int) -> dict[str, Any]:
    episode_agent = create_agent(
        run_context={
            "run_id": "antigravity-compact-q0-50k-20260831",
            "episode_id": f"antigravity-50k-{sequence:04d}",
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
    instance = episode_agent.antigravity_50k_instance
    telemetry = instance.telemetry_snapshot()
    status = str(terminal.get("status", "UNKNOWN"))
    final_money = float(farm.get("money", 0.0))
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
        "milk_units": int(telemetry["MILK_units"]),
        "wool_units": int(telemetry["WOOL_units"]),
        "melon_units": int(telemetry["MELON_units"]),
        "strawberry_units": int(telemetry["STRAWBERRY_units"]),
        "total_crop_units": int(telemetry["MELON_units"]) + int(telemetry["STRAWBERRY_units"]),
        "wheat_consumed": int(telemetry["WHEAT_consumed"]),
        "wheat_sold": int(telemetry["WHEAT_sold"]),
        "fertilizer_collected": int(telemetry["fertilizer_collected"]),
        "fertilizer_applied": int(telemetry["fertilizer_applied"]),
        "crop_revenue": float(telemetry["crop_revenue"]),
        "livestock_revenue": float(telemetry["livestock_revenue"]),
        "market_trading_contribution": float(telemetry["market_trading_contribution"]),
        "productive_actions": int(telemetry["productive_actions"]),
        "move_actions": int(telemetry["MOVE_actions"]),
        "pass_actions": int(telemetry["PASS_actions"]),
        "move_per_productive_action": telemetry["MOVE_PER_PRODUCTIVE_ACTION"],
        "productive_utilization": float(telemetry["PRODUCTIVE_UTILIZATION"]),
        "productive_utilization_final": float(telemetry["PRODUCTIVE_UTILIZATION_FINAL"]),
        "on_time_crop_service_ratio": float(telemetry["ON_TIME_CROP_SERVICE_RATIO"]),
        "hard_deadline_misses": int(telemetry["HARD_DEADLINE_MISSES"]),
        "animal_escapes": int(telemetry["ANIMAL_ESCAPE"]),
        "retarget_count": int(telemetry["RETARGET_COUNT"]),
        "retarget_per_worker_day": float(telemetry["RETARGET_COUNT_PER_WORKER_DAY"]),
        "target_dwell_time": float(telemetry["TARGET_DWELL_TIME"]),
        "duplicate_assignments": int(telemetry["DUPLICATE_ASSIGNMENTS"]),
        "role_changes": int(telemetry["ROLE_CHANGES"]),
        "cross_zone_assists": int(telemetry["CROSS_ZONE_ASSISTS"]),
        "interrupts_by_reason": json.dumps(telemetry.get("INTERRUPTS_BY_REASON", {}), sort_keys=True),
        "activation_records": json.dumps(telemetry.get("activation_records", []), sort_keys=True),
        **_final_counts(farm),
        "technical_pass": (
            status == "DONE"
            and instance.error_count == 0
            and instance.fallback_count == 0
        ),
    }


def _mean(rows: list[dict[str, Any]], field: str) -> float:
    return statistics.fmean(float(row[field]) for row in rows)


def aggregate(rows: list[dict[str, Any]], seeds: tuple[int, ...], phase: str) -> dict[str, Any]:
    scores = [float(row["final_money"]) for row in rows]
    mean_money = statistics.fmean(scores)
    if mean_money < 50_000:
        gate = "FAILURE"
    elif mean_money <= 56_772:
        gate = "MATERIAL_IMPROVEMENT_BELOW_LUCCC"
    elif mean_money < 61_118:
        gate = "LUCCC_BEATEN"
    else:
        gate = "CODEX_V7_1_MATCHED_OR_BEATEN"
    return {
        "phase": phase,
        "episode_count": len(rows),
        "seeds": list(seeds),
        "seats": sorted(list({int(row["seat"]) for row in rows})),
        "opponent": "INERT_PASS_POLICY",
        "model_spec_version": MODEL_SPEC_VERSION,
        "final_money_mean": round(mean_money, 2),
        "final_money_median": round(statistics.median(scores), 2),
        "final_money_std": round(statistics.pstdev(scores), 2) if len(scores) > 1 else 0.0,
        "final_money_min": round(min(scores), 2),
        "final_money_max": round(max(scores), 2),
        "milk_mean": round(_mean(rows, "milk_units"), 2),
        "wool_mean": round(_mean(rows, "wool_units"), 2),
        "melon_mean": round(_mean(rows, "melon_units"), 2),
        "strawberry_mean": round(_mean(rows, "strawberry_units"), 2),
        "total_crop_units_mean": round(_mean(rows, "total_crop_units"), 2),
        "fertilizer_collected_mean": round(_mean(rows, "fertilizer_collected"), 2),
        "fertilizer_applied_mean": round(_mean(rows, "fertilizer_applied"), 2),
        "productive_utilization_mean": round(_mean(rows, "productive_utilization"), 4),
        "move_per_productive_action_mean": round(_mean(rows, "move_per_productive_action"), 4),
        "retarget_per_worker_day_mean": round(_mean(rows, "retarget_per_worker_day"), 4),
        "on_time_crop_service_ratio_mean": round(_mean(rows, "on_time_crop_service_ratio"), 4),
        "hard_deadline_misses_total": sum(int(row["hard_deadline_misses"]) for row in rows),
        "animal_escapes_total": sum(int(row["animal_escapes"]) for row in rows),
        "crop_revenue_mean": round(_mean(rows, "crop_revenue"), 2),
        "livestock_revenue_mean": round(_mean(rows, "livestock_revenue"), 2),
        "technical_pass": all(bool(row["technical_pass"]) for row in rows),
        "economic_gate": gate,
        "delta_vs_ag_pure_horti_43837_33": round(mean_money - 43837.33, 2),
        "delta_vs_ag_q0_3x3_routine_39695_33": round(mean_money - 39695.33, 2),
        "delta_vs_luccc_56772": round(mean_money - 56772.0, 2),
        "delta_vs_codex_v7_1_61118_83": round(mean_money - 61118.83, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["a", "b", "c", "all"], default="b")
    parser.add_argument("--csv", type=Path, default=None)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()

    phase = args.phase.upper()
    if phase == "B":
        seeds = PHASE_B_SEEDS
        seats = (0, 1)
        csv_path = args.csv or DEFAULT_CSV
        json_path = args.json or DEFAULT_JSON
    elif phase == "A":
        seeds = PHASE_A_C_SEEDS
        seats = (0,)
        csv_path = args.csv or (RESULT_DIR / "ANTIGRAVITY_50K_PHASE_A_RESULTS.csv")
        json_path = args.json or (RESULT_DIR / "ANTIGRAVITY_50K_PHASE_A_RESULTS.json")
    elif phase == "C":
        seeds = PHASE_A_C_SEEDS
        seats = (0, 1)
        csv_path = args.csv or (RESULT_DIR / "ANTIGRAVITY_50K_PHASE_C_RESULTS.csv")
        json_path = args.json or (RESULT_DIR / "ANTIGRAVITY_50K_PHASE_C_RESULTS.json")
    else:  # ALL
        seeds = PHASE_B_SEEDS
        seats = (0, 1)
        csv_path = args.csv or DEFAULT_CSV
        json_path = args.json or DEFAULT_JSON

    print(f"=== Running Antigravity 50K Benchmark (Phase {phase}) ===")
    print(f"Seeds: {seeds}, Seats: {seats}")

    rows: list[dict[str, Any]] = []
    sequence = 0
    for seed in seeds:
        for seat in seats:
            sequence += 1
            row = run_episode(seed=seed, seat=seat, sequence=sequence)
            rows.append(row)
            print(
                f"[{sequence}/{len(seeds)*len(seats)}] seed={seed} seat={seat} "
                f"money=${row['final_money']:,.2f} milk={row['milk_units']} wool={row['wool_units']} "
                f"melon={row['melon_units']} straw={row['strawberry_units']} escapes={row['animal_escapes']} "
                f"moves/prod={row['move_per_productive_action']:.3f} status={row['status']}"
            )

    summary = aggregate(rows, seeds, phase)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(
        json.dumps(
            {
                "protocol": f"ANTIGRAVITY_COMPACT_Q0_50K_PHASE_{phase}",
                "post_hoc_tuning": False,
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
    print("\n=== AGGREGATE SUMMARY ===")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"\nWrote CSV: {csv_path}")
    print(f"Wrote JSON: {json_path}")
    return 0 if summary["technical_pass"] and summary["final_money_mean"] >= 50000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
