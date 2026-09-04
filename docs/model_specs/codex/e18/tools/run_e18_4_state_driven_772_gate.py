#!/usr/bin/env python3
"""Run the preregistered E18.4 state-driven 7-7-2 development gate."""

from __future__ import annotations

import csv
import json
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agricola.strategy.codex.codex_e18_capacity_governed_v4d import (
    create_codex_e18_capacity_governed_v4d,
)
from agricola.strategy.codex.codex_e18_state_driven_772 import (
    create_codex_e18_state_driven_772,
)
from docs.model_specs.codex.e18.tools import (
    run_e18_3_labor_conserving_topology_ablation as ablation,
)
from experiments.e17.tools.common import (
    run_e17_three_agent_development_tournament_v2 as base,
)
from experiments.e18.tools.common import analyze_episode_105080066 as replay
from experiments.e18.tools.common import (
    run_e18_dynamic_architecture_tournament_v1 as prior,
)

MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_4_STATE_DRIVEN_772_DEV_GATE_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
CANDIDATE = "CODEX_E18_4_STATE_DRIVEN_772"
CONTROL = "CODEX_E18_2_CONTROL"
PARTICIPANTS = (CANDIDATE, CONTROL)


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-4-GATE-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-4-GATE-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_codex_e18_state_driven_772(run_context=context)
        return policy, policy.codex_e18_state_driven_instance
    if name == CONTROL:
        policy = create_codex_e18_capacity_governed_v4d(run_context=context)
        return policy, policy.codex_e18_capacity_governed_instance
    raise ValueError(name)


def _seat_metrics(env: Any, seat: int, name: str, controller: Any) -> dict[str, Any]:
    metrics = base._seat_metrics(env, seat, "E18_GENERIC", controller)
    metrics.update(ablation._lifecycle_metrics(env, seat))
    metrics["verified_livestock_losses"] = prior._verified_livestock_losses(
        env, seat
    )
    farm = base._farm(env.steps[-1], seat)
    profile = ablation._pasture_profile(farm)
    metrics["final_pastures_by_quadrant"] = {
        quadrant: value["built"] for quadrant, value in profile.items()
    }
    metrics["final_filled_pastures_by_quadrant"] = {
        quadrant: value["filled"] for quadrant, value in profile.items()
    }
    execution = replay._execution_metrics(env.steps, seat)
    transitions = replay._transition_metrics(env.steps, seat)["counts"]
    metrics["harvested_units_total"] = int(execution["harvested_units_total"])
    metrics["harvest_events_total"] = int(sum(execution["harvest_events"].values()))
    metrics["mean_units_per_harvest"] = (
        metrics["harvested_units_total"] / metrics["harvest_events_total"]
        if metrics["harvest_events_total"]
        else 0.0
    )
    metrics["abandoned_crop_count"] = int(
        transitions.get("expired_to_weed", 0)
        + transitions.get("starved_to_weed", 0)
        + transitions.get("disappeared_without_observed_harvest", 0)
    )
    metrics["technical_errors"] = int(getattr(controller, "error_count", 0))
    metrics["fallbacks"] = int(getattr(controller, "fallback_count", 0))
    if name == CANDIDATE:
        telemetry = controller.telemetry_snapshot()
        metrics["target_pastures_by_quadrant"] = {"Q0": 7, "Q1": 7, "Q2": 2}
        metrics["execution_outcomes"] = telemetry["execution_outcomes"]
        metrics["market_execution_outcomes"] = telemetry[
            "market_execution_outcomes"
        ]
        metrics["routing_commands"] = int(telemetry["routing_commands"])
        metrics["service_commands"] = int(telemetry["service_commands"])
        metrics["sale_deferral_batches"] = int(
            telemetry["sale_deferral_batches"]
        )
    else:
        metrics["target_pastures_by_quadrant"] = {"Q0": 7, "Q1": 7, "Q2": 5}
    metrics["final_empty_target_pastures"] = sum(
        max(
            0,
            int(metrics["target_pastures_by_quadrant"][quadrant])
            - int(profile[quadrant]["filled"]),
        )
        for quadrant in ("Q0", "Q1", "Q2")
    )
    return metrics


def _run_match(seed: int, p0: str, p1: str) -> dict[str, Any]:
    policy0, controller0 = _factory(p0, seed, 0)
    policy1, controller1 = _factory(p1, seed, 1)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([policy0, policy1])
    metrics0 = _seat_metrics(env, 0, p0, controller0)
    metrics1 = _seat_metrics(env, 1, p1, controller1)
    winner = (
        p0
        if metrics0["money"] > metrics1["money"]
        else p1
        if metrics1["money"] > metrics0["money"]
        else "TIE"
    )
    return {
        "seed": seed,
        "p0": p0,
        "p1": p1,
        "winner": winner,
        "margin_p0": metrics0["money"] - metrics1["money"],
        "p0_metrics": metrics0,
        "p1_metrics": metrics1,
    }


def _run_spec(index: int, seed: int, p0: str, p1: str) -> tuple[int, dict[str, Any]]:
    return index, _run_match(seed, p0, p1)


def _records(matches: list[dict[str, Any]], participant: str) -> list[dict[str, Any]]:
    return [
        match[f"p{seat}_metrics"]
        for match in matches
        for seat in (0, 1)
        if match[f"p{seat}"] == participant
    ]


def _mean(rows: list[dict[str, Any]], key: str) -> float:
    values = [float(row[key]) for row in rows if row.get(key) is not None]
    return statistics.mean(values) if values else 0.0


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    fields = (
        "money",
        "peak_crops",
        "peak_animals",
        "final_crops",
        "final_animals",
        "final_weeds",
        "productive_actions",
        "move_actions",
        "pass_actions",
        "crop_tile_days_d21_d30",
        "unwatered_tile_days_d21_d30",
        "weed_tile_days_d21_d30",
        "money_gain_d22_d30",
        "harvested_units_total",
        "mean_units_per_harvest",
        "abandoned_crop_count",
        "final_empty_target_pastures",
    )
    result: dict[str, dict[str, Any]] = {}
    for participant in PARTICIPANTS:
        rows = _records(matches, participant)
        money = [float(row["money"]) for row in rows]
        result[participant] = {
            "matches": len(rows),
            "wins": sum(match["winner"] == participant for match in matches),
            "money_median": statistics.median(money),
            "money_min": min(money),
            "money_max": max(money),
            "money_stdev": statistics.pstdev(money),
            "technical_errors": sum(int(row["technical_errors"]) for row in rows),
            "fallbacks": sum(int(row["fallbacks"]) for row in rows),
            "verified_livestock_losses": sum(
                int(row["verified_livestock_losses"]) for row in rows
            ),
            **{f"{field}_mean": _mean(rows, field) for field in fields},
        }
    return result


def _gate(
    matches: list[dict[str, Any]], standings: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    candidate = _records(matches, CANDIDATE)
    control = _records(matches, CONTROL)
    candidate_money = _mean(candidate, "money")
    control_money = _mean(control, "money")
    exact = sum(
        row["final_pastures_by_quadrant"] == {"Q0": 7, "Q1": 7, "Q2": 2}
        for row in candidate
    )
    filled = sum(row["final_empty_target_pastures"] == 0 for row in candidate)
    checks = {
        "zero_technical_errors": standings[CANDIDATE]["technical_errors"] == 0,
        "zero_fallbacks": standings[CANDIDATE]["fallbacks"] == 0,
        "zero_verified_livestock_losses": standings[CANDIDATE][
            "verified_livestock_losses"
        ]
        == 0,
        "exact_772_topology_all_matches": exact == len(candidate),
        "all_16_target_pastures_filled": filled == len(candidate),
        "money_mean_at_least_100k": candidate_money >= 100_000.0,
        "money_not_below_control_minus_10pct": candidate_money
        >= control_money * 0.90,
        "harvested_units_at_least_90pct_control": _mean(
            candidate, "harvested_units_total"
        )
        >= _mean(control, "harvested_units_total") * 0.90,
        "late_crop_tile_days_at_least_90pct_control": _mean(
            candidate, "crop_tile_days_d21_d30"
        )
        >= _mean(control, "crop_tile_days_d21_d30") * 0.90,
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "exact_topology_matches": exact,
        "fully_filled_matches": filled,
        "candidate_money_mean": candidate_money,
        "control_money_mean": control_money,
        "money_delta": candidate_money - control_money,
        "money_percent_vs_control": (
            (candidate_money - control_money) / control_money * 100
            if control_money
            else 0.0
        ),
    }


def _write_csv(matches: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "seat",
        "participant",
        "opponent",
        "winner",
        "money",
        "final_animals",
        "final_crops",
        "final_weeds",
        "final_empty_target_pastures",
        "verified_livestock_losses",
        "harvested_units_total",
        "crop_tile_days_d21_d30",
        "technical_errors",
        "fallbacks",
    ]
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for match in matches:
            for seat in (0, 1):
                metrics = match[f"p{seat}_metrics"]
                writer.writerow(
                    {
                        "seed": match["seed"],
                        "seat": seat,
                        "participant": match[f"p{seat}"],
                        "opponent": match[f"p{1 - seat}"],
                        "winner": match["winner"],
                        **{key: metrics.get(key) for key in fields[5:]},
                    }
                )


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    specs = [
        (index, seed, p0, p1)
        for index, (seed, (p0, p1)) in enumerate(
            (seed, seats)
            for seed in seeds
            for seats in ((CANDIDATE, CONTROL), (CONTROL, CANDIDATE))
        )
    ]
    completed: dict[int, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(_run_spec, index, seed, p0, p1): index
            for index, seed, p0, p1 in specs
        }
        for future in as_completed(futures):
            index, match = future.result()
            completed[index] = match
            print(
                f"[{len(completed):02d}/{len(specs)}] seed={match['seed']} "
                f"{match['p0']} vs {match['p1']} winner={match['winner']}",
                flush=True,
            )
    matches = [completed[index] for index in range(len(specs))]
    standings = _aggregate(matches)
    payload = {
        "schema_version": "E18_4_STATE_DRIVEN_772_DEV_GATE_V1",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "date": "2026-09-03",
        "participants": list(PARTICIPANTS),
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "antigravity_excluded": True,
        "standings": standings,
        "candidate_gate": _gate(matches, standings),
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv(matches)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
