#!/usr/bin/env python3
"""Codex-only E18.3 topology ablation against the frozen E18.2 control.

Each fixed geometry is evaluated on the seven preregistered development seeds
in both seats.  The experiment deliberately excludes peer agents, holdout
seeds, final-confirmation seeds, and Kaggle evidence.
"""

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
    DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH,
    create_codex_e18_capacity_governed_v4d,
)
from agricola.strategy.codex.codex_e18_labor_conserving_topology_ablation import (
    DEFAULT_E18_LABOR_CONSERVING_CONFIG_PATH,
    TOPOLOGY_MODES,
    create_codex_e18_labor_conserving_topology,
)
from experiments.e17.tools.common import (
    run_e17_three_agent_development_tournament_v2 as base,
)
from experiments.e18.tools.common import analyze_episode_105080066 as replay_analysis
from experiments.e18.tools.common import (
    run_e18_dynamic_architecture_tournament_v1 as prior,
)
from experiments.e18.tools.common import (
    run_e18_four_agent_reactive_tournament_v2 as common,
)

MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_labor_conserving_topology_ablation.py"
)
CONTROL_SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_capacity_governed_v4d.py"
)

CONTROL = "CODEX_E18_2_CONTROL"
ARMS = {
    f"CODEX_E18_3_{mode.replace('-', '')}": mode for mode in TOPOLOGY_MODES
}
PARTICIPANTS = (*ARMS, CONTROL)
PAIRS = tuple((arm, CONTROL) for arm in ARMS)
TARGET_MONEY = 100_000.0


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-3-ABLATION-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-3-ABLATION-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name in ARMS:
        policy = create_codex_e18_labor_conserving_topology(
            topology_mode=ARMS[name], run_context=context
        )
        return policy, policy.codex_e18_labor_conserving_instance
    if name == CONTROL:
        policy = create_codex_e18_capacity_governed_v4d(run_context=context)
        return policy, policy.codex_e18_capacity_governed_instance
    raise ValueError(name)


def _farm_surface(farm: dict[str, Any]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            kind = str(tile.get("kind", ""))
            if kind == "PLANT":
                counts["crops"] += 1
                if not bool(tile.get("watered_today", False)):
                    counts["unwatered"] += 1
                if int(tile.get("consecutive_unwatered", 0) or 0) > 0:
                    counts["water_stressed"] += 1
            elif kind == "WEED":
                counts["weeds"] += 1
    return counts


def _lifecycle_metrics(env: Any, seat: int) -> dict[str, Any]:
    daily: list[dict[str, float]] = []
    for state in env.steps:
        observation = state[seat].get("observation", {}) or {}
        if int(observation.get("hour", -1)) != 23:
            continue
        farm = base._farm(state, seat)
        surface = _farm_surface(farm)
        daily.append(
            {
                "display_day": int(observation.get("day", 0)) + 1,
                "money": float(farm.get("money", 0.0) or 0.0),
                "crops": float(surface["crops"]),
                "unwatered": float(surface["unwatered"]),
                "water_stressed": float(surface["water_stressed"]),
                "weeds": float(surface["weeds"]),
            }
        )
    late = [row for row in daily if row["display_day"] >= 21]
    money_by_day = {int(row["display_day"]): row["money"] for row in daily}
    return {
        "crop_tile_days_total": sum(row["crops"] for row in daily),
        "crop_tile_days_d21_d30": sum(row["crops"] for row in late),
        "unwatered_tile_days_total": sum(row["unwatered"] for row in daily),
        "unwatered_tile_days_d21_d30": sum(row["unwatered"] for row in late),
        "water_stressed_tile_days_total": sum(
            row["water_stressed"] for row in daily
        ),
        "weed_tile_days_total": sum(row["weeds"] for row in daily),
        "weed_tile_days_d21_d30": sum(row["weeds"] for row in late),
        "money_d22": money_by_day.get(22),
        "money_d30": money_by_day.get(30),
        "money_gain_d22_d30": (
            money_by_day[30] - money_by_day[22]
            if 22 in money_by_day and 30 in money_by_day
            else None
        ),
    }


def _pasture_profile(farm: dict[str, Any]) -> dict[str, dict[str, int]]:
    result = {
        quadrant: {"built": 0, "filled": 0}
        for quadrant in ("Q0", "Q1", "Q2")
    }
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict) or tile.get("kind") != "PASTURE":
                continue
            quadrant = replay_analysis._quadrant(x, y)
            result[quadrant]["built"] += 1
            if tile.get("animal"):
                result[quadrant]["filled"] += 1
    return result


def _controller_metrics(name: str, controller: Any) -> dict[str, Any]:
    errors = int(getattr(controller, "error_count", 0))
    fallbacks = int(getattr(controller, "fallback_count", 0))
    if name == CONTROL:
        telemetry = controller.telemetry_snapshot()
        return {
            "technical_errors": errors,
            "fallbacks": fallbacks,
            "topology_mode": "7-7-5",
            "target_pastures_by_quadrant": {"Q0": 7, "Q1": 7, "Q2": 5},
            "released_workers_total": 0,
            "released_workers_without_work": int(
                telemetry.get("no_freed_work_violations", 0)
            ),
            "labor_handoff_batches": 0,
            "persistent_fill_batches": 0,
        }
    telemetry = controller.telemetry_snapshot()
    return {
        "technical_errors": errors,
        "fallbacks": fallbacks,
        "topology_mode": telemetry["topology_mode"],
        "target_pastures_by_quadrant": telemetry[
            "target_pastures_by_quadrant"
        ],
        "released_workers_total": int(telemetry["released_workers_total"]),
        "released_workers_without_work": int(
            telemetry["released_workers_without_work"]
        ),
        "labor_handoff_batches": int(telemetry["labor_handoff_batches"]),
        "persistent_fill_batches": int(telemetry["persistent_fill_batches"]),
    }


def _seat_metrics(env: Any, seat: int, name: str, controller: Any) -> dict[str, Any]:
    metrics = base._seat_metrics(env, seat, "E18_GENERIC", controller)
    metrics.update(_controller_metrics(name, controller))
    metrics.update(_lifecycle_metrics(env, seat))
    metrics["verified_livestock_losses"] = prior._verified_livestock_losses(
        env, seat
    )
    metrics["animal_escapes"] = metrics["verified_livestock_losses"]
    farm = base._farm(env.steps[-1], seat)
    profile = _pasture_profile(farm)
    metrics["final_pastures_by_quadrant"] = {
        quadrant: value["built"] for quadrant, value in profile.items()
    }
    metrics["final_filled_pastures_by_quadrant"] = {
        quadrant: value["filled"] for quadrant, value in profile.items()
    }
    metrics["final_empty_target_pastures"] = sum(
        max(
            0,
            int(metrics["target_pastures_by_quadrant"][quadrant])
            - profile[quadrant]["filled"],
        )
        for quadrant in ("Q0", "Q1", "Q2")
    )
    transitions = replay_analysis._transition_metrics(env.steps, seat)["counts"]
    execution = replay_analysis._execution_metrics(env.steps, seat)
    metrics["crop_exit_counts"] = transitions
    metrics["abandoned_crop_count"] = int(
        transitions.get("expired_to_weed", 0)
        + transitions.get("starved_to_weed", 0)
        + transitions.get("disappeared_without_observed_harvest", 0)
    )
    metrics["harvested_units_total"] = int(execution["harvested_units_total"])
    metrics["harvested_wheat_units"] = int(
        execution["harvested_units"].get("WHEAT", 0)
    )
    events = execution["harvest_events"]
    metrics["harvest_events_total"] = int(sum(events.values()))
    metrics["mean_units_per_harvest"] = (
        metrics["harvested_units_total"] / metrics["harvest_events_total"]
        if metrics["harvest_events_total"]
        else 0.0
    )
    metrics["action_stream_hash"] = prior._action_stream_hash(env, seat)
    metrics["architecture_profile_hash"] = common._payload_hash(
        {
            "pastures": profile,
            "peak_crops": metrics["peak_crops"],
            "peak_animals": metrics["peak_animals"],
            "final_crops": metrics["final_crops"],
            "final_animals": metrics["final_animals"],
            "final_weeds": metrics["final_weeds"],
        }
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


def _records(
    matches: list[dict[str, Any]], participant: str, opponent: str | None = None
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for match in matches:
        for seat in (0, 1):
            if match[f"p{seat}"] != participant:
                continue
            if opponent is not None and match[f"p{1 - seat}"] != opponent:
                continue
            result.append(match[f"p{seat}_metrics"])
    return result


def _mean(records: list[dict[str, Any]], key: str) -> float:
    values = [float(record[key]) for record in records if record.get(key) is not None]
    return statistics.mean(values) if values else 0.0


MEAN_FIELDS = (
    "money",
    "peak_crops",
    "peak_animals",
    "final_crops",
    "final_animals",
    "final_weeds",
    "final_empty_target_pastures",
    "pass_actions",
    "productive_actions",
    "crop_tile_days_d21_d30",
    "unwatered_tile_days_d21_d30",
    "weed_tile_days_d21_d30",
    "money_gain_d22_d30",
    "abandoned_crop_count",
    "harvested_units_total",
    "harvested_wheat_units",
    "mean_units_per_harvest",
    "released_workers_total",
    "released_workers_without_work",
)


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    standings: dict[str, dict[str, Any]] = {}
    for participant in PARTICIPANTS:
        records = _records(matches, participant)
        money = [float(record["money"]) for record in records]
        standings[participant] = {
            "matches": len(records),
            "wins": sum(
                match["winner"] == participant
                for match in matches
                if participant in {match["p0"], match["p1"]}
            ),
            "money_median": statistics.median(money),
            "money_min": min(money),
            "money_max": max(money),
            "money_stdev": statistics.pstdev(money),
            "technical_errors": sum(int(row["technical_errors"]) for row in records),
            "fallbacks": sum(int(row["fallbacks"]) for row in records),
            "verified_livestock_losses": sum(
                int(row["verified_livestock_losses"]) for row in records
            ),
            "unique_action_streams": len(
                {row["action_stream_hash"] for row in records}
            ),
            "unique_architecture_profiles": len(
                {row["architecture_profile_hash"] for row in records}
            ),
            **{f"{field}_mean": _mean(records, field) for field in MEAN_FIELDS},
        }
    return standings


def _arm_gates(
    matches: list[dict[str, Any]], standings: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for arm, mode in ARMS.items():
        candidate = _records(matches, arm, CONTROL)
        control = _records(matches, CONTROL, arm)
        candidate_money = _mean(candidate, "money")
        control_money = _mean(control, "money")
        topology_exact = sum(
            row["final_pastures_by_quadrant"]
            == row["target_pastures_by_quadrant"]
            for row in candidate
        )
        checks = {
            "zero_technical_errors": standings[arm]["technical_errors"] == 0,
            "zero_fallbacks": standings[arm]["fallbacks"] == 0,
            "zero_verified_livestock_losses": standings[arm][
                "verified_livestock_losses"
            ]
            == 0,
            "exact_target_topology_all_matches": topology_exact == len(candidate),
            "mean_empty_target_pastures_at_most_one": _mean(
                candidate, "final_empty_target_pastures"
            )
            <= 1.0,
            "no_released_worker_to_pass": sum(
                int(row["released_workers_without_work"]) for row in candidate
            )
            == 0,
            "mean_money_at_least_100k": candidate_money >= TARGET_MONEY,
            "mean_money_not_below_control_minus_5pct": candidate_money
            >= control_money * 0.95,
            "late_unwatered_not_above_control_plus_10pct": _mean(
                candidate, "unwatered_tile_days_d21_d30"
            )
            <= _mean(control, "unwatered_tile_days_d21_d30") * 1.10,
            "abandoned_crops_not_above_control": _mean(
                candidate, "abandoned_crop_count"
            )
            <= _mean(control, "abandoned_crop_count"),
        }
        result[arm] = {
            "topology_mode": mode,
            "passed": all(checks.values()),
            "checks": checks,
            "exact_topology_matches": topology_exact,
            "candidate_money_mean": candidate_money,
            "control_money_mean": control_money,
            "money_delta": candidate_money - control_money,
            "money_percent_vs_control": (
                (candidate_money - control_money) / control_money * 100
                if control_money
                else 0.0
            ),
            "late_crop_tile_days_delta": _mean(
                candidate, "crop_tile_days_d21_d30"
            )
            - _mean(control, "crop_tile_days_d21_d30"),
            "late_unwatered_tile_days_delta": _mean(
                candidate, "unwatered_tile_days_d21_d30"
            )
            - _mean(control, "unwatered_tile_days_d21_d30"),
            "abandoned_crop_delta": _mean(candidate, "abandoned_crop_count")
            - _mean(control, "abandoned_crop_count"),
        }
    return result


def _write_csv(matches: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "seat",
        "participant",
        "opponent",
        "winner",
        *MEAN_FIELDS,
        "technical_errors",
        "fallbacks",
        "verified_livestock_losses",
        "final_pastures_by_quadrant",
        "final_filled_pastures_by_quadrant",
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
                        **{field: metrics.get(field) for field in MEAN_FIELDS},
                        "technical_errors": metrics["technical_errors"],
                        "fallbacks": metrics["fallbacks"],
                        "verified_livestock_losses": metrics[
                            "verified_livestock_losses"
                        ],
                        "final_pastures_by_quadrant": json.dumps(
                            metrics["final_pastures_by_quadrant"], sort_keys=True
                        ),
                        "final_filled_pastures_by_quadrant": json.dumps(
                            metrics["final_filled_pastures_by_quadrant"],
                            sort_keys=True,
                        ),
                    }
                )


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(seed) for seed in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps a reserved seed")
    specs: list[tuple[int, int, str, str]] = []
    for arm, control in PAIRS:
        for seed in seeds:
            for p0, p1 in ((arm, control), (control, arm)):
                specs.append((len(specs), seed, p0, p1))
    completed: dict[int, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(_run_spec, index, seed, p0, p1): (
                index,
                seed,
                p0,
                p1,
            )
            for index, seed, p0, p1 in specs
        }
        for future in as_completed(futures):
            index, seed, p0, p1 = futures[future]
            returned_index, match = future.result()
            if returned_index != index:
                raise RuntimeError("worker returned a mismatched matrix index")
            completed[index] = match
            print(
                f"[{len(completed):02d}/{len(specs)}] seed={seed} {p0} vs {p1} "
                f"winner={match['winner']} margin_p0={match['margin_p0']:.0f}",
                flush=True,
            )
    matches = [completed[index] for index in range(len(specs))]
    standings = _aggregate(matches)
    gates = _arm_gates(matches, standings)
    eligible = [arm for arm, gate in gates.items() if gate["passed"]]
    selected = max(
        eligible,
        key=lambda arm: standings[arm]["money_mean"],
        default=None,
    )
    payload = {
        "schema_version": "E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1",
        "date": "2026-09-03",
        "epistemic_role": "DEVELOPMENT_ONLY_CAUSAL_ABLATION",
        "participants": list(PARTICIPANTS),
        "pairs": [list(pair) for pair in PAIRS],
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "target_money": TARGET_MONEY,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_evidence_consumed": False,
        "peer_agents_excluded": True,
        "antigravity_excluded": True,
        "provenance": {
            "candidate_source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "candidate_source_sha256": common._sha256(SOURCE),
            "candidate_config": str(
                Path(DEFAULT_E18_LABOR_CONSERVING_CONFIG_PATH).relative_to(ROOT)
            ).replace("\\", "/"),
            "candidate_config_sha256": common._sha256(
                Path(DEFAULT_E18_LABOR_CONSERVING_CONFIG_PATH)
            ),
            "control_source": str(CONTROL_SOURCE.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "control_source_sha256": common._sha256(CONTROL_SOURCE),
            "control_config": str(
                Path(DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH).relative_to(ROOT)
            ).replace("\\", "/"),
            "control_config_sha256": common._sha256(
                Path(DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH)
            ),
        },
        "standings": standings,
        "arm_gates": gates,
        "selected_candidate": selected,
        "submission_authorized": selected is not None,
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv(matches)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    print(f"selected_candidate={selected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
