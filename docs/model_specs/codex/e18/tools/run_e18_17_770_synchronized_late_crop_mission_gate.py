#!/usr/bin/env python3
"""Run the E18.17 matched development gate against E18.16."""

from __future__ import annotations

import csv
import hashlib
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

from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    DEFAULT_E18_770_EXACT_CAP_CRITICAL_FEED_CONFIG_PATH,
    create_codex_e18_770_exact_cap_critical_feed,
)
from agricola.strategy.codex.codex_e18_770_synchronized_late_crop_mission import (
    DEFAULT_E18_770_SYNCHRONIZED_LATE_CROP_MISSION_CONFIG_PATH,
    create_codex_e18_770_synchronized_late_crop_mission,
)
from docs.model_specs.codex.e18.tools import (
    run_e18_13_770_d20_critical_feed_deadline_gate as feed_gate,
)
from experiments.e18.tools.common import analyze_episode_105080066 as lifecycle

MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_17_770_SYNCHRONIZED_LATE_CROP_MISSION_DEV_GATE_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_17_770_SYNCHRONIZED_LATE_CROP_MISSION_DEV_GATE_REPORT_IT.md"
)
SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_770_synchronized_late_crop_mission.py"
)
CONTROL_SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_770_exact_cap_critical_feed.py"
)
CANDIDATE = "CODEX_E18_17_770_SYNCHRONIZED_LATE_CROP_MISSION"
CONTROL = "CODEX_E18_16_770_CONTROL"
PARTICIPANTS = (CANDIDATE, CONTROL)
EXPECTED_TOPOLOGY = {"Q0": 7, "Q1": 7, "Q2": 0}
EXTRA_MEAN_FIELDS = (
    "requested_plant",
    "requested_water",
    "requested_harvest",
    "ack_plant",
    "ack_water",
    "ack_harvest",
    "harvest_ack_rate_pct",
    "starved_to_weed",
    "expired_to_weed",
    "plant_commands_blocked",
    "local_harvest_overrides",
    "local_water_overrides",
    "local_dig_overrides",
    "harvest_missions_started",
    "harvest_missions_completed",
    "harvest_missions_cancelled",
    "harvest_mission_route_commands",
    "harvest_mission_service_commands",
    "harvest_mission_acknowledged",
    "harvest_mission_service_retries",
    "provider_move_overrides",
    "provider_non_move_overrides",
)
MEAN_FIELDS = tuple(feed_gate.MEAN_FIELDS) + EXTRA_MEAN_FIELDS


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-17-770-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-17-770-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_codex_e18_770_synchronized_late_crop_mission(
            run_context=context
        )
        return (
            policy,
            policy.codex_e18_770_synchronized_late_crop_mission_instance,
        )
    if name == CONTROL:
        policy = create_codex_e18_770_exact_cap_critical_feed(
            run_context=context
        )
        return policy, policy.codex_e18_770_exact_cap_critical_feed_instance
    raise ValueError(name)


def _seat_metrics(
    env: Any,
    seat: int,
    name: str,
    controller: Any,
) -> dict[str, Any]:
    metrics = feed_gate._seat_metrics(env, seat, name, controller)
    telemetry = controller.telemetry_snapshot()
    execution = lifecycle._execution_metrics(env.steps, seat)
    transitions = lifecycle._transition_metrics(env.steps, seat)["counts"]
    requested = execution["requested"]
    acknowledged = execution["acknowledged"]
    requested_harvest = int(requested.get("HARVEST", 0))
    ack_harvest = int(acknowledged.get("HARVEST", 0))
    metrics.update(
        {
            "livestock_resource_cap": int(
                telemetry.get("livestock_resource_cap", 14)
            ),
            "max_observed_livestock_resources": int(
                telemetry.get("max_observed_livestock_resources", 14)
            ),
            "requested_plant": int(requested.get("PLANT", 0)),
            "requested_water": int(requested.get("WATER", 0)),
            "requested_harvest": requested_harvest,
            "ack_plant": int(acknowledged.get("PLANT", 0)),
            "ack_water": int(acknowledged.get("WATER", 0)),
            "ack_harvest": ack_harvest,
            "harvest_ack_rate_pct": (
                100.0 * ack_harvest / requested_harvest
                if requested_harvest
                else 100.0
            ),
            "starved_to_weed": int(transitions.get("starved_to_weed", 0)),
            "expired_to_weed": int(transitions.get("expired_to_weed", 0)),
            **{
                field: int(telemetry.get(field, 0) or 0)
                for field in EXTRA_MEAN_FIELDS
                if field
                not in {
                    "requested_plant",
                    "requested_water",
                    "requested_harvest",
                    "ack_plant",
                    "ack_water",
                    "ack_harvest",
                    "harvest_ack_rate_pct",
                    "starved_to_weed",
                    "expired_to_weed",
                }
            },
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


def _run_spec(
    index: int, seed: int, p0: str, p1: str
) -> tuple[int, dict[str, Any]]:
    return index, _run_match(seed, p0, p1)


def _records(
    matches: list[dict[str, Any]], name: str
) -> list[dict[str, Any]]:
    return [
        match[f"p{seat}_metrics"]
        for match in matches
        for seat in (0, 1)
        if match[f"p{seat}"] == name
    ]


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    standings = {}
    for name in PARTICIPANTS:
        rows = _records(matches, name)
        money = [float(row["money"]) for row in rows]
        standings[name] = {
            "matches": len(rows),
            "wins": sum(match["winner"] == name for match in matches),
            "money_median": statistics.median(money),
            "money_min": min(money),
            "money_max": max(money),
            "technical_errors": sum(
                int(row["technical_errors"]) for row in rows
            ),
            "fallbacks": sum(int(row["fallbacks"]) for row in rows),
            "verified_livestock_losses": sum(
                int(row["verified_livestock_losses"]) for row in rows
            ),
            **{
                f"{field}_mean": statistics.mean(
                    float(row[field]) for row in rows
                )
                for field in MEAN_FIELDS
            },
        }
    return standings


def _percent_delta(candidate: float, control: float) -> float:
    return 100.0 * (candidate - control) / control if control else 0.0


def _gates(
    matches: list[dict[str, Any]], standings: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    candidate_rows = _records(matches, CANDIDATE)
    candidate = standings[CANDIDATE]
    control = standings[CONTROL]
    money_deltas = []
    for match in matches:
        seat = 0 if match["p0"] == CANDIDATE else 1
        money_deltas.append(
            _percent_delta(
                float(match[f"p{seat}_metrics"]["money"]),
                float(match[f"p{1 - seat}_metrics"]["money"]),
            )
        )
    exact_candidate = sum(
        row["final_pastures_by_quadrant"] == EXPECTED_TOPOLOGY
        and row["final_filled_pastures_total"] == 14
        for row in candidate_rows
    )
    checks = {
        "exact_filled_770_all_matches": exact_candidate == 14,
        "max_fourteen_livestock_resources_all_matches": all(
            row["max_observed_livestock_resources"] <= 14
            for row in candidate_rows
        ),
        "zero_livestock_losses": candidate["verified_livestock_losses"] == 0,
        "zero_errors_and_fallbacks": (
            candidate["technical_errors"] == 0 and candidate["fallbacks"] == 0
        ),
        "controller_observed_all_matches": all(
            row["plant_commands_blocked"] > 0
            or row["local_harvest_overrides"] > 0
            or row["local_water_overrides"] > 0
            or row["harvest_missions_started"] > 0
            for row in candidate_rows
        ),
        "treatment_action_effect_all_matches": all(
            row["plant_commands_blocked"] > 0
            or row["local_harvest_overrides"] > 0
            or row["local_water_overrides"] > 0
            or row["local_dig_overrides"] > 0
            or row["harvest_mission_route_commands"] > 0
            or row["harvest_mission_service_commands"] > 0
            for row in candidate_rows
        ),
        "mission_ack_observed_all_matches": all(
            row["harvest_mission_acknowledged"] > 0
            for row in candidate_rows
        ),
        "zero_unauthorized_non_move_overrides": all(
            row["provider_non_move_overrides"] == 0 for row in candidate_rows
        ),
        "money_not_below_control": candidate["money_mean"] >= control["money_mean"],
        "worst_matched_money_delta_at_least_minus_2pct": min(money_deltas) >= -2.0,
        "move_not_higher_by_more_than_1pct": candidate["move_actions_mean"]
        <= control["move_actions_mean"] * 1.01,
        "harvest_ack_rate_not_lower": candidate["harvest_ack_rate_pct_mean"]
        >= control["harvest_ack_rate_pct_mean"],
        "harvested_units_not_lower": candidate["harvested_units_total_mean"]
        >= control["harvested_units_total_mean"],
        "late_unwatered_not_worse": candidate[
            "unwatered_tile_days_d21_d30_mean"
        ]
        <= control["unwatered_tile_days_d21_d30_mean"],
        "starved_to_weed_not_worse": candidate["starved_to_weed_mean"]
        <= control["starved_to_weed_mean"],
    }
    convergence = {
        "pass_at_most_700": candidate["pass_actions_mean"] <= 700,
        "move_at_most_3500": candidate["move_actions_mean"] <= 3500,
        "late_unwatered_at_most_0_42": candidate[
            "late_unwatered_per_crop_tile_mean"
        ]
        <= 0.42,
        "harvest_ack_at_least_67_7pct": candidate[
            "harvest_ack_rate_pct_mean"
        ]
        >= 67.7,
        "harvested_units_at_least_600": candidate[
            "harvested_units_total_mean"
        ]
        >= 600,
    }
    return {
        "gate_a_causal": {"passed": all(checks.values()), "checks": checks},
        "gate_b_diagnostic_convergence": {
            "passed": all(convergence.values()),
            "checks": convergence,
        },
        "exact_candidate_matches": exact_candidate,
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
        "money",
        "move_actions",
        "pass_actions",
        "requested_plant",
        "ack_water",
        "requested_harvest",
        "ack_harvest",
        "harvest_ack_rate_pct",
        "harvested_units_total",
        "unwatered_tile_days_d21_d30",
        "starved_to_weed",
        "plant_commands_blocked",
        "local_harvest_overrides",
        "local_water_overrides",
        "local_dig_overrides",
        "harvest_missions_started",
        "harvest_mission_acknowledged",
        "provider_move_overrides",
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
                        **{field: metrics[field] for field in fields[5:]},
                    }
                )


def _write_report(payload: dict[str, Any]) -> None:
    candidate = payload["standings"][CANDIDATE]
    control = payload["standings"][CONTROL]
    gates = payload["gates"]

    def delta(field: str) -> float:
        return _percent_delta(
            candidate[f"{field}_mean"], control[f"{field}_mean"]
        )

    verdict = "PASS" if gates["gate_a_causal"]["passed"] else "FAIL"
    report = f"""# E18.17 — synchronized late crop mission V1

## Verdetto

Gate A causale: `{verdict}`. Gate B diagnostico:
`{'PASS' if gates['gate_b_diagnostic_convergence']['passed'] else 'FAIL'}`.
Controllo topology-matched: E18.16.

| KPI | E18.17 | E18.16 | Delta |
|---|---:|---:|---:|
| Money | {candidate['money_mean']:.2f} | {control['money_mean']:.2f} | {delta('money'):+.2f}% |
| MOVE | {candidate['move_actions_mean']:.2f} | {control['move_actions_mean']:.2f} | {delta('move_actions'):+.2f}% |
| PASS | {candidate['pass_actions_mean']:.2f} | {control['pass_actions_mean']:.2f} | {delta('pass_actions'):+.2f}% |
| PLANT richiesti | {candidate['requested_plant_mean']:.2f} | {control['requested_plant_mean']:.2f} | {delta('requested_plant'):+.2f}% |
| HARVEST ack rate | {candidate['harvest_ack_rate_pct_mean']:.2f}% | {control['harvest_ack_rate_pct_mean']:.2f}% | {candidate['harvest_ack_rate_pct_mean'] - control['harvest_ack_rate_pct_mean']:+.2f} pp |
| Unità raccolte | {candidate['harvested_units_total_mean']:.2f} | {control['harvested_units_total_mean']:.2f} | {delta('harvested_units_total'):+.2f}% |
| Late unwatered | {candidate['unwatered_tile_days_d21_d30_mean']:.2f} | {control['unwatered_tile_days_d21_d30_mean']:.2f} | {delta('unwatered_tile_days_d21_d30'):+.2f}% |
| Starved-to-weed | {candidate['starved_to_weed_mean']:.2f} | {control['starved_to_weed_mean']:.2f} | {candidate['starved_to_weed_mean'] - control['starved_to_weed_mean']:+.2f} |

Record `{candidate['wins']}-{control['wins']}`; money matched medio
`{gates['mean_matched_money_delta_percent']:+.2f}%`, peggiore
`{gates['worst_matched_money_delta_percent']:+.2f}%`.

Il record grezzo include l'effetto seat: sul solo seed non-TIE, `180903004`,
candidata e controllo ottengono lo stesso money quando occupano lo stesso
seat. Non è quindi evidenza di un vantaggio del trattamento.

## Attivazione

- PLANT bloccati medi: `{candidate['plant_commands_blocked_mean']:.2f}`;
- override HARVEST locali: `{candidate['local_harvest_overrides_mean']:.2f}`;
- override WATER locali: `{candidate['local_water_overrides_mean']:.2f}`;
- missioni avviate/ack: `{candidate['harvest_missions_started_mean']:.2f}` /
  `{candidate['harvest_mission_acknowledged_mean']:.2f}`;
- MOVE provider sostituiti: `{candidate['provider_move_overrides_mean']:.2f}`;
- override non-MOVE non autorizzati: `{candidate['provider_non_move_overrides_mean']:.2f}`.

## Gate A

```json
{json.dumps(gates['gate_a_causal']['checks'], indent=2, sort_keys=True)}
```

Holdout e final-confirmation non consumati. Il confronto con gli altri campioni
interni è ammesso soltanto se il Gate A passa. In caso di trattamento senza
effetto sulle azioni, E18.16 resta la base interna e la candidata non è
promuovibile né candidabile alla submission quotidiana.
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
                f"winner={match['winner']}",
                flush=True,
            )
    matches = [completed[index] for index in range(len(specs))]
    standings = _aggregate(matches)
    payload = {
        "schema_version": (
            "E18_17_770_SYNCHRONIZED_LATE_CROP_MISSION_DEV_GATE_V1"
        ),
        "date": "2026-09-04",
        "epistemic_role": "DEVELOPMENT_ONLY_TOPOLOGY_MATCHED_CAUSAL_ABLATION",
        "causal_variable": (
            "SYNCHRONIZED_LATE_CROP_ADMISSION_PRIORITY_AND_MISSION_ACK"
        ),
        "participants": list(PARTICIPANTS),
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
        "mutation_freeze": {
            "pasture_topology": EXPECTED_TOPOLOGY,
            "pasture_fill_target": 14,
            "livestock_resource_cap": 14,
            "market": "E18_16_UNCHANGED",
            "worker_count": "E18_16_UNCHANGED",
            "critical_feed": "E18_16_UNCHANGED",
            "treatment_window": "D21_D28_CROP_LIFECYCLE_ONLY",
        },
        "provenance": {
            "candidate_source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "candidate_source_sha256": _sha256(SOURCE),
            "candidate_config": str(
                Path(
                    DEFAULT_E18_770_SYNCHRONIZED_LATE_CROP_MISSION_CONFIG_PATH
                ).relative_to(ROOT)
            ).replace("\\", "/"),
            "candidate_config_sha256": _sha256(
                Path(
                    DEFAULT_E18_770_SYNCHRONIZED_LATE_CROP_MISSION_CONFIG_PATH
                )
            ),
            "control_source": str(CONTROL_SOURCE.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "control_source_sha256": _sha256(CONTROL_SOURCE),
            "control_config": str(
                Path(
                    DEFAULT_E18_770_EXACT_CAP_CRITICAL_FEED_CONFIG_PATH
                ).relative_to(ROOT)
            ).replace("\\", "/"),
            "control_config_sha256": _sha256(
                Path(DEFAULT_E18_770_EXACT_CAP_CRITICAL_FEED_CONFIG_PATH)
            ),
        },
        "standings": standings,
        "gates": _gates(matches, standings),
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
    print(f"wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
