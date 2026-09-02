#!/usr/bin/env python3
"""Development-only competitive mirror: Codex reactive versus frozen V9."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.codex.codex_3q_mixed_high_density import create_v9_agent
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    create_codex_e17_reactive_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUTPUT_PATH = (
    REPO_ROOT
    / "experiments/e17/artifacts/derived/codex/E17_1_COMPETITIVE_DEVELOPMENT_METRICS.json"
)


def _animal_count(observation: dict[str, Any], seat: int) -> int:
    farms = observation.get("farms", []) or []
    if seat >= len(farms):
        return 0
    return sum(
        1
        for row in farms[seat].get("tiles", []) or []
        for tile in row
        if isinstance(tile, dict) and tile.get("animal")
    )


def _derived_escapes(steps: list[Any], seat: int) -> int:
    last_day = None
    last_count = 0
    escapes = 0
    for state in steps:
        observation = state[seat].get("observation", {}) or {}
        day = int(observation.get("day", 0))
        count = _animal_count(observation, seat)
        if last_day is not None and day > last_day:
            escapes += max(0, last_count - count)
        last_day = day
        last_count = count
    return escapes


def run_matrix(seeds: list[int]) -> dict[str, Any]:
    rows = []
    for seed in seeds:
        for reactive_seat in (0, 1):
            context = {
                "run_id": f"E17-1-COMP-S{seed}-P{reactive_seat}",
                "episode_id": f"E17-1-COMP-S{seed}-P{reactive_seat}",
                "seed": seed,
                "player_position": reactive_seat,
            }
            reactive = create_codex_e17_reactive_agent(run_context=context)
            control = create_v9_agent(
                run_context={**context, "player_position": 1 - reactive_seat}
            )
            agents = [reactive, control] if reactive_seat == 0 else [control, reactive]
            env = make(
                "kaggriculture",
                configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
                debug=True,
            )
            env.run(agents)
            terminal = env.steps[-1]
            reactive_reward = float(terminal[reactive_seat].get("reward") or 0.0)
            control_reward = float(terminal[1 - reactive_seat].get("reward") or 0.0)
            instance = reactive.codex_e17_instance
            telemetry = instance.telemetry_snapshot()
            row = {
                "seed": seed,
                "reactive_seat": reactive_seat,
                "reactive_reward": reactive_reward,
                "control_reward": control_reward,
                "reward_delta": reactive_reward - control_reward,
                "reactive_status": terminal[reactive_seat].get("status"),
                "control_status": terminal[1 - reactive_seat].get("status"),
                "reactive_errors": instance.error_count
                + instance.base_policy.codex_v9_instance.error_count,
                "control_errors": control.codex_v9_instance.error_count,
                "override_batches": telemetry["reactive_override_batches"],
                "override_reasons": telemetry["reactive_override_reasons"],
                "detected_unfilled_wheat_units": telemetry[
                    "detected_unfilled_wheat_units"
                ],
                "reactive_derived_escapes": _derived_escapes(
                    env.steps, reactive_seat
                ),
                "control_derived_escapes": _derived_escapes(
                    env.steps, 1 - reactive_seat
                ),
            }
            rows.append(row)
            print(
                f"seed={seed} seat={reactive_seat} reactive={reactive_reward:.0f} "
                f"control={control_reward:.0f} delta={row['reward_delta']:+.0f} "
                f"overrides={row['override_batches']}",
                flush=True,
            )

    rewards = [row["reactive_reward"] for row in rows]
    controls = [row["control_reward"] for row in rows]
    metrics = {
        "schema_version": "E17_1_CODEX_COMPETITIVE_DEVELOPMENT_V1",
        "epistemic_role": "DEVELOPMENT_ONLY",
        "participants": [
            "CODEX-E17.1-3Q-REACTIVE-GUARDED-V1",
            "CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY",
        ],
        "seeds": seeds,
        "seats": [0, 1],
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "runs": len(rows),
        "reactive_mean": statistics.mean(rewards),
        "control_mean": statistics.mean(controls),
        "mean_matched_delta": statistics.mean(
            row["reward_delta"] for row in rows
        ),
        "wins": sum(row["reward_delta"] > 0 for row in rows),
        "ties": sum(row["reward_delta"] == 0 for row in rows),
        "losses": sum(row["reward_delta"] < 0 for row in rows),
        "override_batches": sum(row["override_batches"] for row in rows),
        "detected_unfilled_wheat_units": sum(
            row["detected_unfilled_wheat_units"] for row in rows
        ),
        "reactive_derived_escapes": sum(
            row["reactive_derived_escapes"] for row in rows
        ),
        "technical_errors": sum(
            row["reactive_errors"] + row["control_errors"] for row in rows
        ),
        "results": rows,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(metrics, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return metrics


def main(argv: list[str] | None = None) -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=manifest["seed_policy"]["development"],
    )
    args = parser.parse_args(argv)
    forbidden = set(manifest["seed_policy"]["holdout"]["seeds"]) | set(
        manifest["seed_policy"]["final_confirmation"]["seeds"]
    )
    if forbidden.intersection(args.seeds):
        raise SystemExit("holdout/final seeds are forbidden in development")
    metrics = run_matrix(args.seeds)
    print(json.dumps({key: metrics[key] for key in (
        "runs", "reactive_mean", "control_mean", "mean_matched_delta",
        "wins", "ties", "losses", "override_batches",
        "detected_unfilled_wheat_units", "reactive_derived_escapes",
        "technical_errors",
    )}, indent=2, sort_keys=True))
    return 0 if metrics["technical_errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
