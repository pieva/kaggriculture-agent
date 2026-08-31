#!/usr/bin/env python3
"""Run the one-shot preregistered compact-Q0 Codex performance experiment."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.codex_c2 import MODEL_SPEC_VERSION, create_agent

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = REPO_ROOT / "results" / "model_spec_c2" / "codex"
DEFAULT_CSV = RESULT_DIR / "CODEX_COMPACT_Q0_ROUTINE_RESULTS.csv"
DEFAULT_JSON = RESULT_DIR / "CODEX_COMPACT_Q0_ROUTINE_RESULTS.json"
TECHNICAL_EVIDENCE = RESULT_DIR / "CODEX_COMPACT_Q0_ROUTINE_TECHNICAL_SMOKE.json"
SEEDS = (26090101, 26090102, 26090103)
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
            "run_id": "codex-compact-q0-preregistered-20260831",
            "episode_id": f"codex-compact-q0-{sequence:04d}",
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
    instance = episode_agent.codex_c2_instance
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
        "interrupts_by_reason": json.dumps(telemetry["INTERRUPTS_BY_REASON"], sort_keys=True),
        "activation_records": json.dumps(telemetry["activation_records"], sort_keys=True),
        **_final_counts(farm),
        "technical_pass": (
            status == "DONE"
            and instance.error_count == 0
            and instance.fallback_count == 0
        ),
    }


def _mean(rows: list[dict[str, Any]], field: str) -> float:
    return statistics.fmean(float(row[field]) for row in rows)


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scores = [float(row["final_money"]) for row in rows]
    mean_money = statistics.fmean(scores)
    if mean_money < 50_000:
        gate = "FAILURE"
    elif mean_money <= 56_772:
        gate = "MATERIAL_IMPROVEMENT_BELOW_LUCCC"
    elif mean_money < 80_000:
        gate = "LUCCC_BEATEN"
    else:
        gate = "PROJECT_TARGET_MET"
    return {
        "episode_count": len(rows),
        "seeds": list(SEEDS),
        "seats": [0, 1],
        "opponent": "INERT_PASS_POLICY",
        "model_spec_version": MODEL_SPEC_VERSION,
        "final_money_mean": mean_money,
        "final_money_median": statistics.median(scores),
        "final_money_std": statistics.pstdev(scores),
        "final_money_min": min(scores),
        "final_money_max": max(scores),
        "milk_mean": _mean(rows, "milk_units"),
        "wool_mean": _mean(rows, "wool_units"),
        "melon_mean": _mean(rows, "melon_units"),
        "strawberry_mean": _mean(rows, "strawberry_units"),
        "productive_utilization_mean": _mean(rows, "productive_utilization"),
        "productive_utilization_final_mean": _mean(rows, "productive_utilization_final"),
        "move_per_productive_action_mean": _mean(rows, "move_per_productive_action"),
        "retarget_per_worker_day_mean": _mean(rows, "retarget_per_worker_day"),
        "on_time_crop_service_ratio_mean": _mean(rows, "on_time_crop_service_ratio"),
        "hard_deadline_misses_total": sum(int(row["hard_deadline_misses"]) for row in rows),
        "animal_escapes_total": sum(int(row["animal_escapes"]) for row in rows),
        "crop_revenue_mean": _mean(rows, "crop_revenue"),
        "livestock_revenue_mean": _mean(rows, "livestock_revenue"),
        "technical_pass": all(bool(row["technical_pass"]) for row in rows),
        "economic_gate": gate,
        "delta_vs_codex_v6_9851": mean_money - 9851.0,
        "delta_vs_ag_q0_3x3_37997_67": mean_money - 37997.67,
        "delta_vs_luccc_56772": mean_money - 56772.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    args = parser.parse_args()
    if not TECHNICAL_EVIDENCE.exists():
        raise SystemExit("technical verification evidence is missing")
    technical = json.loads(TECHNICAL_EVIDENCE.read_text(encoding="utf-8"))
    if not bool(technical.get("technical_pass")):
        raise SystemExit("technical verification did not pass")

    rows: list[dict[str, Any]] = []
    sequence = 0
    for seed in SEEDS:
        for seat in (0, 1):
            sequence += 1
            row = run_episode(seed=seed, seat=seat, sequence=sequence)
            rows.append(row)
            print(
                f"[{sequence}/6] seed={seed} seat={seat} "
                f"money={row['final_money']:.2f} status={row['status']}"
            )
    summary = aggregate(rows)
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    args.json.write_text(
        json.dumps(
            {
                "protocol": "CODEX_COMPACT_Q0_ROUTINE_PREREGISTERED",
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
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"wrote {args.csv}")
    print(f"wrote {args.json}")
    return 0 if summary["technical_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
