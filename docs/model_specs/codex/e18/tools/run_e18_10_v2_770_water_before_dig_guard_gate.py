#!/usr/bin/env python3
"""Run the safe PASS-only E18.10 V2 gate against E18.9."""

from __future__ import annotations

import csv
import json
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agricola.strategy.codex.codex_e18_770_live_crop_rotation_guard import (
    DEFAULT_E18_770_LIVE_CROP_ROTATION_GUARD_CONFIG_PATH,
    create_codex_e18_770_live_crop_rotation_guard,
)
from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    DEFAULT_E18_770_WATER_BEFORE_DIG_GUARD_V2_CONFIG_PATH,
    create_codex_e18_770_water_before_dig_guard_v2,
)
from docs.model_specs.codex.e18.tools import (
    run_e18_10_770_water_before_dig_guard_gate as prior,
)

CANDIDATE = prior.CANDIDATE
CONTROL = prior.CONTROL
PARTICIPANTS = prior.PARTICIPANTS
MEAN_FIELDS = prior.MEAN_FIELDS
MANIFEST = prior.MANIFEST
MATCHED_TOP3 = prior.MATCHED_TOP3
E18_9_RESULT = prior.E18_9_RESULT
OUTPUT_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_10_V2_770_WATER_BEFORE_DIG_GUARD_DEV_GATE_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_10_V2_770_WATER_BEFORE_DIG_GUARD_DEV_GATE_REPORT_IT.md"
)
SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_770_water_before_dig_guard_v2.py"
)
CONTROL_SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_770_live_crop_rotation_guard.py"
)


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-10-V2-770-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-10-V2-770-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_codex_e18_770_water_before_dig_guard_v2(
            run_context=context
        )
        return policy, policy.codex_e18_770_water_before_dig_guard_v2_instance
    if name == CONTROL:
        policy = create_codex_e18_770_live_crop_rotation_guard(
            run_context=context
        )
        return policy, policy.codex_e18_770_live_crop_rotation_guard_instance
    raise ValueError(name)


def _run_match(seed: int, p0: str, p1: str) -> dict[str, Any]:
    policy0, controller0 = _factory(p0, seed, 0)
    policy1, controller1 = _factory(p1, seed, 1)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([policy0, policy1])
    metrics0 = prior._seat_metrics(env, 0, p0, controller0)
    metrics1 = prior._seat_metrics(env, 1, p1, controller1)
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
        "live_crop_dig_tasks_converted_to_water",
        "water_guard_active_batches",
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
                        "live_crop_dig_tasks_converted_to_water": metrics[
                            "live_crop_dig_tasks_converted_to_water"
                        ],
                        "water_guard_active_batches": metrics[
                            "water_guard_active_batches"
                        ],
                    }
                )


def _write_report(payload: dict[str, Any]) -> None:
    candidate = payload["standings"][CANDIDATE]
    control = payload["standings"][CONTROL]
    gates = payload["gates"]
    gate_a = gates["gate_a_causal"]
    gate_b = gates["gate_b_top3_convergence"]
    rows = prior._records(payload["matches"], CANDIDATE)

    def delta(field: str) -> float:
        return prior._percent_delta(
            candidate[f"{field}_mean"], control[f"{field}_mean"]
        )

    converted = sum(
        int(row["live_crop_dig_tasks_converted_to_water"]) for row in rows
    )
    report = f"""# E18.10 V2 — safe PASS-only WATER-before-DIG

## Verdetto

Gate A causale: `{'PASS' if gate_a['passed'] else 'FAIL'}`. Gate B Top-3:
`{'PASS' if gate_b['passed'] else 'FAIL'}`. La V2 converte soltanto un PASS
finale di E18.9 in WATER in-place ed esclude lo shed access `(4,5)`.

## Risultati

| KPI | E18.10 V2 | E18.9 controllo | Delta |
|---|---:|---:|---:|
| Money | {candidate['money_mean']:.2f} | {control['money_mean']:.2f} | {delta('money'):+.2f}% |
| Move | {candidate['move_actions_mean']:.2f} | {control['move_actions_mean']:.2f} | {delta('move_actions'):+.2f}% |
| PASS | {candidate['pass_actions_mean']:.2f} | {control['pass_actions_mean']:.2f} | {delta('pass_actions'):+.2f}% |
| WATER | {candidate['water_actions_mean']:.2f} | {control['water_actions_mean']:.2f} | {delta('water_actions'):+.2f}% |
| DIG | {candidate['dig_actions_mean']:.2f} | {control['dig_actions_mean']:.2f} | {delta('dig_actions'):+.2f}% |
| Crop service | {candidate['crop_service_actions_mean']:.2f} | {control['crop_service_actions_mean']:.2f} | {delta('crop_service_actions'):+.2f}% |
| Late crop tile-days | {candidate['crop_tile_days_d21_d30_mean']:.2f} | {control['crop_tile_days_d21_d30_mean']:.2f} | {delta('crop_tile_days_d21_d30'):+.2f}% |
| Late unwatered/crop | {candidate['late_unwatered_per_crop_tile_mean']:.4f} | {control['late_unwatered_per_crop_tile_mean']:.4f} | {delta('late_unwatered_per_crop_tile'):+.2f}% |
| Harvest riusciti | {candidate['harvest_events_total_mean']:.2f} | {control['harvest_events_total_mean']:.2f} | {delta('harvest_events_total'):+.2f}% |
| Unità raccolte | {candidate['harvested_units_total_mean']:.2f} | {control['harvested_units_total_mean']:.2f} | {delta('harvested_units_total'):+.2f}% |

PASS→WATER totali sui 14 match: `{converted}`. Topologia/fill candidata:
`{gates['exact_candidate_matches']}/14`; controllo:
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

Holdout, final e upload Kaggle non sono autorizzati.
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
    standings = prior._aggregate(matches)
    hash_file = prior.prior.prior.prior.common.prior._sha256
    payload = {
        "schema_version": "E18_10_V2_770_WATER_BEFORE_DIG_GUARD_DEV_GATE_V1",
        "date": "2026-09-04",
        "epistemic_role": "DEVELOPMENT_ONLY_TOPOLOGY_MATCHED_CAUSAL_ABLATION",
        "causal_variable": "E18_9_PASS_TO_PROTECTED_LIVE_CROP_WATER",
        "participants": list(PARTICIPANTS),
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
        "mutation_freeze": {
            "pasture_topology": prior.EXPECTED_TOPOLOGY,
            "market": "E18_9_UNCHANGED",
            "worker_routes": "E18_9_UNCHANGED",
            "worker_count": "E18_9_UNCHANGED",
            "livestock_cap": "E18_9_UNCHANGED_15",
            "excluded_shared_logistics_targets": [[4, 5]],
            "allowed_change": "FINAL_E18_9_PASS_TO_IN_PLACE_WATER_ONLY",
        },
        "provenance": {
            "candidate_source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "candidate_source_sha256": hash_file(SOURCE),
            "candidate_config": str(
                Path(
                    DEFAULT_E18_770_WATER_BEFORE_DIG_GUARD_V2_CONFIG_PATH
                ).relative_to(ROOT)
            ).replace("\\", "/"),
            "candidate_config_sha256": hash_file(
                Path(DEFAULT_E18_770_WATER_BEFORE_DIG_GUARD_V2_CONFIG_PATH)
            ),
            "control_source": str(CONTROL_SOURCE.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "control_source_sha256": hash_file(CONTROL_SOURCE),
            "control_config": str(
                Path(
                    DEFAULT_E18_770_LIVE_CROP_ROTATION_GUARD_CONFIG_PATH
                ).relative_to(ROOT)
            ).replace("\\", "/"),
            "control_config_sha256": hash_file(
                Path(DEFAULT_E18_770_LIVE_CROP_ROTATION_GUARD_CONFIG_PATH)
            ),
            "e18_9_result": str(E18_9_RESULT.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "e18_9_result_sha256": hash_file(E18_9_RESULT),
            "matched_top3_reference": str(MATCHED_TOP3.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "matched_top3_reference_sha256": hash_file(MATCHED_TOP3),
        },
        "standings": standings,
        "gates": prior._gates(matches, standings),
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
