#!/usr/bin/env python3
"""Run the sequential E18.4 V2 locality/task-aging development gate."""

from __future__ import annotations

import csv
import json
import statistics
import sys
from collections import Counter
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
from agricola.strategy.codex.codex_e18_state_driven_772_v2 import (
    create_codex_e18_state_driven_772_v2,
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
    / "E18_4_STATE_DRIVEN_772_V2_DEV_GATE.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
OUTPUT_REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_4_STATE_DRIVEN_772_V2_DEV_GATE_REPORT_IT.md"
)
CANDIDATE = "CODEX_E18_4_STATE_DRIVEN_772_V2"
CONTROL = "CODEX_E18_2_CONTROL"
PARTICIPANTS = (CANDIDATE, CONTROL)


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-4-V2-GATE-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-4-V2-GATE-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_codex_e18_state_driven_772_v2(run_context=context)
        return policy, policy.codex_e18_state_driven_v2_instance
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
        metrics["route_thrashing_violations"] = int(
            telemetry["route_thrashing_violations"]
        )
        metrics["pass_on_actionable_violations"] = int(
            telemetry["pass_on_actionable_violations"]
        )
        metrics["cross_cluster_transfers"] = sum(
            int(value) for value in telemetry["cross_cluster_transfers"].values()
        )
        metrics["ownership_changes"] = len(telemetry["ownership_changes"])
        metrics["aged_task_observations"] = telemetry["aged_task_observations"]
        metrics["home_cluster_counts"] = dict(
            Counter(telemetry["home_clusters"].values())
        )
        metrics["cross_cluster_transfer_reasons"] = telemetry[
            "cross_cluster_transfers"
        ]
    else:
        metrics["target_pastures_by_quadrant"] = {"Q0": 7, "Q1": 7, "Q2": 5}
        metrics["route_thrashing_violations"] = 0
        metrics["pass_on_actionable_violations"] = 0
        metrics["cross_cluster_transfers"] = 0
        metrics["ownership_changes"] = 0
        metrics["aged_task_observations"] = {}
        metrics["home_cluster_counts"] = {}
        metrics["cross_cluster_transfer_reasons"] = {}
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
        "productive_actions",
        "move_actions",
        "pass_actions",
        "move_per_productive",
        "crop_tile_days_d21_d30",
        "unwatered_tile_days_d21_d30",
        "weed_tile_days_d21_d30",
        "harvested_units_total",
        "mean_units_per_harvest",
        "abandoned_crop_count",
        "final_empty_target_pastures",
        "route_thrashing_violations",
        "pass_on_actionable_violations",
        "cross_cluster_transfers",
        "ownership_changes",
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
            "technical_errors": sum(int(row["technical_errors"]) for row in rows),
            "fallbacks": sum(int(row["fallbacks"]) for row in rows),
            "verified_livestock_losses": sum(
                int(row["verified_livestock_losses"]) for row in rows
            ),
            **{f"{field}_mean": _mean(rows, field) for field in fields},
        }
    return result


def _gate_a(
    matches: list[dict[str, Any]], standings: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    rows = _records(matches, CANDIDATE)
    exact = sum(
        row["final_pastures_by_quadrant"] == {"Q0": 7, "Q1": 7, "Q2": 2}
        for row in rows
    )
    filled = sum(row["final_empty_target_pastures"] == 0 for row in rows)
    move = _mean(rows, "move_actions")
    productive = _mean(rows, "productive_actions")
    checks = {
        "move_actions_lte_e18_2": move <= 3584.6,
        "productive_actions_gte_95pct_e18_2": productive >= 2663.0,
        "move_per_productive_lte_1_28": (
            move / productive if productive else float("inf")
        )
        <= 1.28,
        "harvested_units_gte_95pct_e18_2": _mean(rows, "harvested_units_total")
        >= 571.3,
        "late_crop_tile_days_gte_95pct_e18_2": _mean(
            rows, "crop_tile_days_d21_d30"
        )
        >= 449.3,
        "mean_units_per_harvest_gte_3": _mean(rows, "mean_units_per_harvest")
        >= 3.0,
        "late_weed_tile_days_lte_110pct_e18_2": _mean(
            rows, "weed_tile_days_d21_d30"
        )
        <= 16.5,
        "zero_pass_on_actionable": sum(
            int(row["pass_on_actionable_violations"]) for row in rows
        )
        == 0,
        "zero_route_thrashing": sum(
            int(row["route_thrashing_violations"]) for row in rows
        )
        == 0,
        "exact_772_topology_all_matches": exact == len(rows),
        "all_16_target_pastures_filled": filled == len(rows),
        "zero_technical_errors": standings[CANDIDATE]["technical_errors"] == 0,
        "zero_fallbacks": standings[CANDIDATE]["fallbacks"] == 0,
        "zero_verified_livestock_losses": standings[CANDIDATE][
            "verified_livestock_losses"
        ]
        == 0,
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "exact_topology_matches": exact,
        "fully_filled_matches": filled,
    }


def _gate_b(matches: list[dict[str, Any]], gate_a: dict[str, Any]) -> dict[str, Any]:
    if not gate_a["passed"]:
        return {
            "evaluated": False,
            "passed": False,
            "blocked_by": "GATE_A",
            "checks": {},
        }
    candidate = _records(matches, CANDIDATE)
    control = _records(matches, CONTROL)
    deltas: list[float] = []
    ratios: list[float] = []
    for match in matches:
        candidate_metrics = (
            match["p0_metrics"] if match["p0"] == CANDIDATE else match["p1_metrics"]
        )
        control_metrics = (
            match["p0_metrics"] if match["p0"] == CONTROL else match["p1_metrics"]
        )
        deltas.append(candidate_metrics["money"] - control_metrics["money"])
        ratios.append(
            candidate_metrics["money"] / control_metrics["money"]
            if control_metrics["money"]
            else 0.0
        )
    checks = {
        "candidate_money_mean_gte_100k": _mean(candidate, "money") >= 100_000.0,
        "candidate_money_not_below_control": _mean(candidate, "money")
        >= _mean(control, "money"),
        "matched_nonnegative_at_least_10_of_14": sum(value >= 0 for value in deltas)
        >= 10,
        "no_episode_below_90pct_control": all(value >= 0.90 for value in ratios),
    }
    return {
        "evaluated": True,
        "passed": all(checks.values()),
        "checks": checks,
        "matched_nonnegative": sum(value >= 0 for value in deltas),
        "candidate_money_mean": _mean(candidate, "money"),
        "control_money_mean": _mean(control, "money"),
    }


def _write_csv(matches: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "seat",
        "participant",
        "opponent",
        "winner",
        "money",
        "productive_actions",
        "move_actions",
        "move_per_productive",
        "harvested_units_total",
        "mean_units_per_harvest",
        "crop_tile_days_d21_d30",
        "weed_tile_days_d21_d30",
        "final_empty_target_pastures",
        "route_thrashing_violations",
        "pass_on_actionable_violations",
        "verified_livestock_losses",
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


def _write_report(payload: dict[str, Any]) -> None:
    gate_a = payload["gate_a"]
    gate_b = payload["gate_b"]
    candidate = payload["standings"][CANDIDATE]
    control = payload["standings"][CONTROL]
    failed = [name for name, passed in gate_a["checks"].items() if not passed]
    report = f"""# E18.4 V2 — locality/task-aging development gate

## Decisione

**Gate A: {'PASS' if gate_a['passed'] else 'FAIL'}**. Gate B:
{'PASS' if gate_b['passed'] else 'FAIL' if gate_b['evaluated'] else 'NON ESEGUITO'}.
La candidata resta development-only; nessun upload Kaggle è autorizzato.

## Risultati principali

| KPI medio | V2 | E18.2 |
|---|---:|---:|
| Money | {candidate['money_mean']:.2f} | {control['money_mean']:.2f} |
| Move | {candidate['move_actions_mean']:.2f} | {control['move_actions_mean']:.2f} |
| Productive | {candidate['productive_actions_mean']:.2f} | {control['productive_actions_mean']:.2f} |
| Move/productive | {candidate['move_per_productive_mean']:.4f} | {control['move_per_productive_mean']:.4f} |
| Harvested units | {candidate['harvested_units_total_mean']:.2f} | {control['harvested_units_total_mean']:.2f} |
| Crop tile-days D21-D30 | {candidate['crop_tile_days_d21_d30_mean']:.2f} | {control['crop_tile_days_d21_d30_mean']:.2f} |
| Weed tile-days D21-D30 | {candidate['weed_tile_days_d21_d30_mean']:.2f} | {control['weed_tile_days_d21_d30_mean']:.2f} |

## Gate falliti

{chr(10).join(f'- `{name}`' for name in failed) if failed else '- Nessuno.'}

## Integrità

- match development: {payload['match_count']};
- holdout/final consumati: no/no;
- topologia 7-7-2 esatta: {gate_a['exact_topology_matches']}/{payload['match_count']};
- fill 16/16: {gate_a['fully_filled_matches']}/{payload['match_count']};
- errori/fallback/perdite: {candidate['technical_errors']}/{candidate['fallbacks']}/{candidate['verified_livestock_losses']}.
"""
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text(report, encoding="utf-8")


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
    gate_a = _gate_a(matches, standings)
    gate_b = _gate_b(matches, gate_a)
    payload = {
        "schema_version": "E18_4_STATE_DRIVEN_772_V2_DEV_GATE_V1",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "date": "2026-09-04",
        "participants": list(PARTICIPANTS),
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
        "standings": standings,
        "gate_a": gate_a,
        "gate_b": gate_b,
        "gate_c": {"evaluated": False, "blocked_by": "GATE_A_OR_B"},
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv(matches)
    _write_report(payload)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    print(f"wrote {OUTPUT_REPORT}")
    print(f"Gate A: {'PASS' if gate_a['passed'] else 'FAIL'}")
    print(
        "Gate B: "
        + (
            "PASS"
            if gate_b["passed"]
            else "FAIL"
            if gate_b["evaluated"]
            else "NOT RUN"
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
