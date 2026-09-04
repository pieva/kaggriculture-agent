#!/usr/bin/env python3
"""Run the topology-matched E18.8 adjacent crop queue development gate."""

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

from agricola.strategy.codex.codex_e18_770_adjacent_crop_queue import (
    DEFAULT_E18_770_ADJACENT_CROP_QUEUE_CONFIG_PATH,
    create_codex_e18_770_adjacent_crop_queue,
)
from agricola.strategy.codex.codex_e18_concentrated_770_throughput import (
    DEFAULT_E18_CONCENTRATED_770_CONFIG_PATH,
    create_codex_e18_concentrated_770_throughput,
)
from docs.model_specs.codex.e18.tools import (
    run_e18_7_770_in_place_crop_service_gate as prior,
)

MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
MATCHED_TOP3 = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_6_770_MATCHED_TOP3_GAP_ANALYSIS_2026_09_04.json"
)
E18_7_RESULT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_7_770_IN_PLACE_CROP_SERVICE_DEV_GATE_V1.json"
)
OUTPUT_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_8_770_ADJACENT_CROP_QUEUE_DEV_GATE_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_8_770_ADJACENT_CROP_QUEUE_DEV_GATE_REPORT_IT.md"
)
SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_770_adjacent_crop_queue.py"
)
CONTROL_SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_concentrated_770_throughput.py"
)

CANDIDATE = "CODEX_E18_8_770_ADJACENT_CROP_QUEUE"
CONTROL = "CODEX_E18_6_770_CONTROL"
PARTICIPANTS = (CANDIDATE, CONTROL)
EXPECTED_TOPOLOGY = {"Q0": 7, "Q1": 7, "Q2": 0}
MEAN_FIELDS = prior.MEAN_FIELDS


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-8-770-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-8-770-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_codex_e18_770_adjacent_crop_queue(run_context=context)
        return policy, policy.codex_e18_770_adjacent_crop_queue_instance
    if name == CONTROL:
        policy = create_codex_e18_concentrated_770_throughput(
            run_context=context
        )
        return policy, policy.codex_e18_concentrated_770_instance
    raise ValueError(name)


def _seat_metrics(
    env: Any,
    seat: int,
    name: str,
    controller: Any,
) -> dict[str, Any]:
    metrics = prior._seat_metrics(env, seat, name, controller)
    telemetry = controller.telemetry_snapshot()
    metrics.update(
        {
            "adjacent_queue_commands": telemetry.get(
                "adjacent_queue_commands", {}
            ),
            "adjacent_queue_assignments": int(
                telemetry.get("adjacent_queue_assignments", 0)
            ),
            "adjacent_queue_completions": int(
                telemetry.get("adjacent_queue_completions", 0)
            ),
            "adjacent_queue_cancellations": int(
                telemetry.get("adjacent_queue_cancellations", 0)
            ),
            "adjacent_queue_batches": int(
                telemetry.get("adjacent_queue_batches", 0)
            ),
            "adjacent_queue_candidates": int(
                telemetry.get("adjacent_queue_candidates", 0)
            ),
            "adjacent_inventory_blocks": int(
                telemetry.get("adjacent_inventory_blocks", 0)
            ),
            "max_observed_assignment_distance": int(
                telemetry.get("max_observed_assignment_distance", 0)
            ),
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


def _records(matches: list[dict[str, Any]], name: str) -> list[dict[str, Any]]:
    return [
        match[f"p{seat}_metrics"]
        for match in matches
        for seat in (0, 1)
        if match[f"p{seat}"] == name
    ]


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result = {}
    for name in PARTICIPANTS:
        rows = _records(matches, name)
        money = [float(row["money"]) for row in rows]
        result[name] = {
            "matches": len(rows),
            "wins": sum(match["winner"] == name for match in matches),
            "money_median": statistics.median(money),
            "money_min": min(money),
            "money_max": max(money),
            "technical_errors": sum(int(row["technical_errors"]) for row in rows),
            "fallbacks": sum(int(row["fallbacks"]) for row in rows),
            "verified_livestock_losses": sum(
                int(row["verified_livestock_losses"]) for row in rows
            ),
            **{
                f"{field}_mean": statistics.mean(float(row[field]) for row in rows)
                for field in MEAN_FIELDS
            },
        }
    return result


def _percent_delta(candidate: float, control: float) -> float:
    return 100.0 * (candidate - control) / control if control else 0.0


def _gates(
    matches: list[dict[str, Any]],
    standings: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    candidate_rows = _records(matches, CANDIDATE)
    control_rows = _records(matches, CONTROL)
    candidate = standings[CANDIDATE]
    control = standings[CONTROL]
    money_deltas = []
    for match in matches:
        seat = 0 if match["p0"] == CANDIDATE else 1
        candidate_money = float(match[f"p{seat}_metrics"]["money"])
        control_money = float(match[f"p{1 - seat}_metrics"]["money"])
        money_deltas.append(_percent_delta(candidate_money, control_money))
    exact_candidate = sum(
        row["final_pastures_by_quadrant"] == EXPECTED_TOPOLOGY
        and row["final_filled_pastures_total"] == 14
        for row in candidate_rows
    )
    exact_control = sum(
        row["final_pastures_by_quadrant"] == EXPECTED_TOPOLOGY
        and row["final_filled_pastures_total"] == 14
        for row in control_rows
    )
    gate_a_checks = {
        "exact_filled_770_candidate_all_matches": exact_candidate == 14,
        "exact_filled_770_control_all_matches": exact_control == 14,
        "zero_q2_pastures_candidate": all(
            int(row["max_observed_q2_pastures"]) == 0 for row in candidate_rows
        ),
        "zero_errors_and_fallbacks": (
            candidate["technical_errors"] == 0 and candidate["fallbacks"] == 0
        ),
        "zero_topology_breaches": all(
            int(row["topology_cap_breaches"]) == 0 for row in candidate_rows
        ),
        "treatment_activated_all_matches": all(
            int(row["adjacent_queue_batches"]) > 0 for row in candidate_rows
        ),
        "zero_non_pass_overrides": all(
            int(row["non_pass_overrides"]) == 0 for row in candidate_rows
        ),
        "zero_cross_quadrant_routes": all(
            int(row["cross_quadrant_routes"]) == 0 for row in candidate_rows
        ),
        "assignment_distance_at_most_one": all(
            int(row["max_observed_assignment_distance"]) <= 1
            for row in candidate_rows
        ),
        "non_queue_dimensions_frozen": all(
            not row["market_mutation"]
            and not row["calendar_mutation"]
            and not row["worker_count_mutation"]
            and not row["livestock_cap_mutation"]
            for row in candidate_rows
        ),
        "livestock_losses_not_above_control": candidate[
            "verified_livestock_losses"
        ]
        <= control["verified_livestock_losses"],
        "pass_at_least_5pct_lower": candidate["pass_actions_mean"]
        <= control["pass_actions_mean"] * 0.95,
        "crop_service_at_least_5pct_higher": candidate[
            "crop_service_actions_mean"
        ]
        >= control["crop_service_actions_mean"] * 1.05,
        "normalized_productive_at_least_3pct_higher": candidate[
            "normalized_productive_actions_mean"
        ]
        >= control["normalized_productive_actions_mean"] * 1.03,
        "move_not_above_control_plus_3pct": candidate["move_actions_mean"]
        <= control["move_actions_mean"] * 1.03,
        "normalized_ratio_not_worse": candidate[
            "normalized_move_per_productive_mean"
        ]
        <= control["normalized_move_per_productive_mean"],
        "harvest_events_at_least_5pct_higher": candidate[
            "harvest_events_total_mean"
        ]
        >= control["harvest_events_total_mean"] * 1.05,
        "harvested_units_at_least_5pct_higher": candidate[
            "harvested_units_total_mean"
        ]
        >= control["harvested_units_total_mean"] * 1.05,
        "late_unwatered_at_least_5pct_better": candidate[
            "late_unwatered_per_crop_tile_mean"
        ]
        <= control["late_unwatered_per_crop_tile_mean"] * 0.95,
        "money_not_below_control_minus_5pct": candidate["money_mean"]
        >= control["money_mean"] * 0.95,
        "worst_matched_money_delta_at_least_minus_10pct": min(money_deltas)
        >= -10.0,
    }
    gate_b_checks = {
        "pass_at_most_600": candidate["pass_actions_mean"] <= 600,
        "crop_service_at_least_1800": candidate["crop_service_actions_mean"]
        >= 1800,
        "move_at_most_3500": candidate["move_actions_mean"] <= 3500,
        "normalized_ratio_at_most_1_10": candidate[
            "normalized_move_per_productive_mean"
        ]
        <= 1.10,
        "late_crop_tile_days_at_least_500": candidate[
            "crop_tile_days_d21_d30_mean"
        ]
        >= 500,
        "late_unwatered_at_most_0_42": candidate[
            "late_unwatered_per_crop_tile_mean"
        ]
        <= 0.42,
        "harvest_events_at_least_300": candidate["harvest_events_total_mean"]
        >= 300,
    }
    return {
        "gate_a_causal": {
            "passed": all(gate_a_checks.values()),
            "checks": gate_a_checks,
        },
        "gate_b_top3_convergence": {
            "passed": all(gate_b_checks.values()),
            "checks": gate_b_checks,
            "promotion_required": False,
        },
        "exact_candidate_matches": exact_candidate,
        "exact_control_matches": exact_control,
        "mean_matched_money_delta_percent": statistics.mean(money_deltas),
        "worst_matched_money_delta_percent": min(money_deltas),
    }


def _write_csv(matches: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "seat",
        "participant",
        "opponent",
        "winner",
        *MEAN_FIELDS,
        "verified_livestock_losses",
        "technical_errors",
        "fallbacks",
        "final_pastures_by_quadrant",
        "adjacent_queue_commands",
        "adjacent_queue_assignments",
        "adjacent_queue_completions",
        "adjacent_queue_cancellations",
    ]
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
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
                        **{field: metrics[field] for field in MEAN_FIELDS},
                        "verified_livestock_losses": metrics[
                            "verified_livestock_losses"
                        ],
                        "technical_errors": metrics["technical_errors"],
                        "fallbacks": metrics["fallbacks"],
                        "final_pastures_by_quadrant": json.dumps(
                            metrics["final_pastures_by_quadrant"], sort_keys=True
                        ),
                        "adjacent_queue_commands": json.dumps(
                            metrics["adjacent_queue_commands"], sort_keys=True
                        ),
                        "adjacent_queue_assignments": metrics[
                            "adjacent_queue_assignments"
                        ],
                        "adjacent_queue_completions": metrics[
                            "adjacent_queue_completions"
                        ],
                        "adjacent_queue_cancellations": metrics[
                            "adjacent_queue_cancellations"
                        ],
                    }
                )


def _write_report(payload: dict[str, Any]) -> None:
    candidate = payload["standings"][CANDIDATE]
    control = payload["standings"][CONTROL]
    gates = payload["gates"]
    gate_a = gates["gate_a_causal"]
    gate_b = gates["gate_b_top3_convergence"]
    candidate_rows = _records(payload["matches"], CANDIDATE)

    def delta(field: str) -> float:
        return _percent_delta(candidate[f"{field}_mean"], control[f"{field}_mean"])

    total_assignments = sum(
        int(row["adjacent_queue_assignments"]) for row in candidate_rows
    )
    total_completions = sum(
        int(row["adjacent_queue_completions"]) for row in candidate_rows
    )
    total_cancellations = sum(
        int(row["adjacent_queue_cancellations"]) for row in candidate_rows
    )
    report = f"""# E18.8 — gate 7-7-0 adjacent crop queue

## Verdetto

Gate A causale: `{'PASS' if gate_a['passed'] else 'FAIL'}`. Gate B di
convergenza Top-3: `{'PASS' if gate_b['passed'] else 'FAIL'}`. La topologia è
`7-7-0` per entrambi; l'unica mutazione è PASS → missione crop adiacente nello
stesso quadrante.

## Risultati

| KPI | E18.8 queue | E18.6 controllo | Delta |
|---|---:|---:|---:|
| Money | {candidate['money_mean']:.2f} | {control['money_mean']:.2f} | {delta('money'):+.2f}% |
| Move | {candidate['move_actions_mean']:.2f} | {control['move_actions_mean']:.2f} | {delta('move_actions'):+.2f}% |
| PASS | {candidate['pass_actions_mean']:.2f} | {control['pass_actions_mean']:.2f} | {delta('pass_actions'):+.2f}% |
| Produttive normalizzate | {candidate['normalized_productive_actions_mean']:.2f} | {control['normalized_productive_actions_mean']:.2f} | {delta('normalized_productive_actions'):+.2f}% |
| Move/prod. normalizzato | {candidate['normalized_move_per_productive_mean']:.4f} | {control['normalized_move_per_productive_mean']:.4f} | {delta('normalized_move_per_productive'):+.2f}% |
| Crop service | {candidate['crop_service_actions_mean']:.2f} | {control['crop_service_actions_mean']:.2f} | {delta('crop_service_actions'):+.2f}% |
| Harvest riusciti | {candidate['harvest_events_total_mean']:.2f} | {control['harvest_events_total_mean']:.2f} | {delta('harvest_events_total'):+.2f}% |
| Unità raccolte | {candidate['harvested_units_total_mean']:.2f} | {control['harvested_units_total_mean']:.2f} | {delta('harvested_units_total'):+.2f}% |
| Late unwatered/crop | {candidate['late_unwatered_per_crop_tile_mean']:.4f} | {control['late_unwatered_per_crop_tile_mean']:.4f} | {delta('late_unwatered_per_crop_tile'):+.2f}% |

Missioni totali sui 14 match: `{total_assignments}` assegnate,
`{total_completions}` completate, `{total_cancellations}` cancellate. Topologia
candidata: `{gates['exact_candidate_matches']}/14`; controllo:
`{gates['exact_control_matches']}/14`. Record:
`{candidate['wins']}-{control['wins']}`. Delta money matched medio
`{gates['mean_matched_money_delta_percent']:+.2f}%`, peggiore
`{gates['worst_matched_money_delta_percent']:+.2f}%`.

## Gate A causale

```json
{json.dumps(gate_a['checks'], indent=2, sort_keys=True)}
```

## Gate B Top-3

```json
{json.dumps(gate_b['checks'], indent=2, sort_keys=True)}
```

Holdout, final e upload Kaggle non sono autorizzati da questo gate.
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps a reserved seed")
    specs = [
        (index, seed, p0, p1)
        for index, (seed, p0, p1) in enumerate(
            item
            for seed in seeds
            for item in (
                (seed, CANDIDATE, CONTROL),
                (seed, CONTROL, CANDIDATE),
            )
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
        "schema_version": "E18_8_770_ADJACENT_CROP_QUEUE_DEV_GATE_V1",
        "date": "2026-09-04",
        "epistemic_role": "DEVELOPMENT_ONLY_TOPOLOGY_MATCHED_CAUSAL_ABLATION",
        "causal_variable": "PASS_TO_SAME_QUADRANT_ADJACENT_CROP_QUEUE",
        "participants": list(PARTICIPANTS),
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
        "mutation_freeze": {
            "pasture_topology": EXPECTED_TOPOLOGY,
            "market": "E18_6_UNCHANGED",
            "crop_calendar": "E18_6_UNCHANGED",
            "worker_count": "E18_6_UNCHANGED",
            "livestock_cap": "E18_6_UNCHANGED_15",
            "provider_non_pass_commands": "AUTHORITATIVE",
            "allowed_override": (
                "PASS_TO_IN_PLACE_OR_DISTANCE_1_SAME_QUADRANT_HARVEST_OR_WATER"
            ),
        },
        "provenance": {
            "candidate_source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "candidate_source_sha256": prior.common.prior._sha256(SOURCE),
            "candidate_config": str(
                Path(DEFAULT_E18_770_ADJACENT_CROP_QUEUE_CONFIG_PATH).relative_to(
                    ROOT
                )
            ).replace("\\", "/"),
            "candidate_config_sha256": prior.common.prior._sha256(
                Path(DEFAULT_E18_770_ADJACENT_CROP_QUEUE_CONFIG_PATH)
            ),
            "control_source": str(CONTROL_SOURCE.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "control_source_sha256": prior.common.prior._sha256(CONTROL_SOURCE),
            "control_config": str(
                Path(DEFAULT_E18_CONCENTRATED_770_CONFIG_PATH).relative_to(ROOT)
            ).replace("\\", "/"),
            "control_config_sha256": prior.common.prior._sha256(
                Path(DEFAULT_E18_CONCENTRATED_770_CONFIG_PATH)
            ),
            "e18_7_result": str(E18_7_RESULT.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "e18_7_result_sha256": prior.common.prior._sha256(E18_7_RESULT),
            "matched_top3_reference": str(MATCHED_TOP3.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "matched_top3_reference_sha256": prior.common.prior._sha256(
                MATCHED_TOP3
            ),
        },
        "standings": standings,
        "gates": _gates(matches, standings),
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_csv(matches)
    _write_report(payload)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    print(f"wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
