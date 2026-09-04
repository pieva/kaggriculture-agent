#!/usr/bin/env python3
"""Run the E18.16 exact-cap critical-FEED gate against E18.10 V2."""

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
from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    DEFAULT_E18_770_WATER_BEFORE_DIG_GUARD_V2_CONFIG_PATH,
    create_codex_e18_770_water_before_dig_guard_v2,
)
from docs.model_specs.codex.e18.tools import (
    run_e18_13_770_d20_critical_feed_deadline_gate as feed_gate,
)

MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_16_770_EXACT_CAP_CRITICAL_FEED_DEV_GATE_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_16_770_EXACT_CAP_CRITICAL_FEED_DEV_GATE_REPORT_IT.md"
)
SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_770_exact_cap_critical_feed.py"
)
CONTROL_SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_770_water_before_dig_guard_v2.py"
)
CANDIDATE = "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED"
CONTROL = "CODEX_E18_10_V2_770_CONTROL"
PARTICIPANTS = (CANDIDATE, CONTROL)
EXPECTED_TOPOLOGY = {"Q0": 7, "Q1": 7, "Q2": 0}
MEAN_FIELDS = feed_gate.MEAN_FIELDS


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-16-770-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-16-770-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_codex_e18_770_exact_cap_critical_feed(
            run_context=context
        )
        return policy, policy.codex_e18_770_exact_cap_critical_feed_instance
    if name == CONTROL:
        policy = create_codex_e18_770_water_before_dig_guard_v2(
            run_context=context
        )
        return policy, policy.codex_e18_770_water_before_dig_guard_v2_instance
    raise ValueError(name)


def _seat_metrics(
    env: Any,
    seat: int,
    name: str,
    controller: Any,
) -> dict[str, Any]:
    metrics = feed_gate._seat_metrics(env, seat, name, controller)
    telemetry = controller.telemetry_snapshot()
    metrics.update(
        {
            "livestock_resource_cap": int(
                telemetry.get("livestock_resource_cap", 15)
            ),
            "max_observed_livestock_resources": int(
                telemetry.get("max_observed_livestock_resources", 15)
            ),
            "clamped_animal_units": sum(
                int(value)
                for value in (
                    telemetry.get("clamped_animal_units", {}) or {}
                ).values()
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
    control_rows = _records(matches, CONTROL)
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
    exact_control = sum(
        row["final_pastures_by_quadrant"] == EXPECTED_TOPOLOGY
        and row["final_filled_pastures_total"] == 14
        for row in control_rows
    )
    checks = {
        "exact_filled_770_candidate_all_matches": exact_candidate == 14,
        "exact_filled_770_control_all_matches": exact_control == 14,
        "max_fourteen_livestock_resources_all_matches": all(
            row["max_observed_livestock_resources"] <= 14
            for row in candidate_rows
        ),
        "animal_clamp_activated_all_matches": all(
            row["clamped_animal_units"] >= 1 for row in candidate_rows
        ),
        "one_critical_feed_override_each_match": all(
            row["move_to_critical_feed_overrides"] == 1
            for row in candidate_rows
        ),
        "zero_candidate_livestock_losses": candidate[
            "verified_livestock_losses"
        ]
        == 0,
        "control_loss_reproduced_each_match": control[
            "verified_livestock_losses"
        ]
        == 14,
        "zero_errors_and_fallbacks": (
            candidate["technical_errors"] == 0 and candidate["fallbacks"] == 0
        ),
        "zero_topology_breaches": all(
            row["topology_cap_breaches"] == 0 for row in candidate_rows
        ),
        "only_registered_mutations": all(
            row["market_mutation"]
            and row["livestock_cap_mutation"]
            and not row["worker_count_mutation"]
            and not row["crop_lifecycle_mutation"]
            and row["route_delay_commands"] == 1
            for row in candidate_rows
        ),
        "money_not_below_control": candidate["money_mean"]
        >= control["money_mean"],
        "worst_matched_money_delta_at_least_minus_2pct": min(money_deltas)
        >= -2.0,
        "move_not_higher_by_more_than_0_5pct": candidate["move_actions_mean"]
        <= control["move_actions_mean"] * 1.005,
        "water_not_lower_by_more_than_0_5pct": candidate["water_actions_mean"]
        >= control["water_actions_mean"] * 0.995,
        "crop_service_not_lower_by_more_than_0_5pct": candidate[
            "crop_service_actions_mean"
        ]
        >= control["crop_service_actions_mean"] * 0.995,
        "late_unwatered_not_worse_by_more_than_0_5pct": candidate[
            "late_unwatered_per_crop_tile_mean"
        ]
        <= control["late_unwatered_per_crop_tile_mean"] * 1.005,
        "harvest_events_not_lower_by_more_than_0_5pct": candidate[
            "harvest_events_total_mean"
        ]
        >= control["harvest_events_total_mean"] * 0.995,
        "harvested_units_not_lower_by_more_than_0_5pct": candidate[
            "harvested_units_total_mean"
        ]
        >= control["harvested_units_total_mean"] * 0.995,
    }
    gate_b_checks = {
        "pass_at_most_600": candidate["pass_actions_mean"] <= 600,
        "crop_service_at_least_1800": candidate[
            "crop_service_actions_mean"
        ]
        >= 1800,
        "move_at_most_3500": candidate["move_actions_mean"] <= 3500,
        "late_unwatered_at_most_0_42": candidate[
            "late_unwatered_per_crop_tile_mean"
        ]
        <= 0.42,
        "harvest_events_at_least_300": candidate[
            "harvest_events_total_mean"
        ]
        >= 300,
    }
    return {
        "gate_a_causal": {"passed": all(checks.values()), "checks": checks},
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
        "money",
        "move_actions",
        "water_actions",
        "harvest_events_total",
        "harvested_units_total",
        "verified_livestock_losses",
        "max_observed_livestock_resources",
        "clamped_animal_units",
        "move_to_critical_feed_overrides",
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

    report = f"""# E18.16 — cap 14 + critical FEED

## Verdetto

Gate A: `{'PASS' if gates['gate_a_causal']['passed'] else 'FAIL'}`. Gate B
Top-3: `{'PASS' if gates['gate_b_top3_convergence']['passed'] else 'FAIL'}`.
Controllo E18.10 V2.

| KPI | E18.16 | E18.10 V2 | Delta |
|---|---:|---:|---:|
| Money | {candidate['money_mean']:.2f} | {control['money_mean']:.2f} | {delta('money'):+.2f}% |
| Perdite | {candidate['verified_livestock_losses']} | {control['verified_livestock_losses']} | n/a |
| MOVE | {candidate['move_actions_mean']:.2f} | {control['move_actions_mean']:.2f} | {delta('move_actions'):+.2f}% |
| PASS | {candidate['pass_actions_mean']:.2f} | {control['pass_actions_mean']:.2f} | {delta('pass_actions'):+.2f}% |
| WATER | {candidate['water_actions_mean']:.2f} | {control['water_actions_mean']:.2f} | {delta('water_actions'):+.2f}% |
| Crop service | {candidate['crop_service_actions_mean']:.2f} | {control['crop_service_actions_mean']:.2f} | {delta('crop_service_actions'):+.2f}% |
| Harvest | {candidate['harvest_events_total_mean']:.2f} | {control['harvest_events_total_mean']:.2f} | {delta('harvest_events_total'):+.2f}% |
| Unità | {candidate['harvested_units_total_mean']:.2f} | {control['harvested_units_total_mean']:.2f} | {delta('harvested_units_total'):+.2f}% |

Record `{candidate['wins']}-{control['wins']}`; money matched medio
`{gates['mean_matched_money_delta_percent']:+.2f}%`, peggiore
`{gates['worst_matched_money_delta_percent']:+.2f}%`.

## Interpretazione causale

Il quindicesimo animale era ammesso dal buffer legacy: 14 risorse erano già
presenti a D12 H2, ma un ulteriore `BUY_ANIMAL SHEEP 1` a D12 H3 passava sotto
il cap 15. Con il solo cap, la morte D20 obbligava a ricomprare un rimpiazzo;
con il solo FEED, il surplus restava nello shed e il worst era `-2,85%`.
E18.16 impedisce entrambi gli sprechi e porta il worst a
`{gates['worst_matched_money_delta_percent']:+.2f}%`.

## Gate A

```json
{json.dumps(gates['gate_a_causal']['checks'], indent=2, sort_keys=True)}
```

Holdout, final-confirmation e upload Kaggle non sono autorizzati.
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
        "schema_version": "E18_16_770_EXACT_CAP_CRITICAL_FEED_DEV_GATE_V1",
        "date": "2026-09-04",
        "epistemic_role": "DEVELOPMENT_ONLY_TOPOLOGY_MATCHED_CAUSAL_ABLATION",
        "causal_variable": "COHERENT_14_SLOT_LIVESTOCK_SAFETY",
        "participants": list(PARTICIPANTS),
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
        "mutation_freeze": {
            "pasture_topology": EXPECTED_TOPOLOGY,
            "market": "BUY_ANIMAL_CLAMP_AT_14_ONLY",
            "worker_routes": "ONE_D20_MOVE_DELAYED_FOR_FEED_ONLY",
            "worker_count": "E18_10_V2_UNCHANGED",
            "livestock_cap": 14,
            "crop_lifecycle": "E18_10_V2_UNCHANGED",
        },
        "provenance": {
            "candidate_source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "candidate_source_sha256": _sha256(SOURCE),
            "candidate_config": str(
                Path(DEFAULT_E18_770_EXACT_CAP_CRITICAL_FEED_CONFIG_PATH).relative_to(
                    ROOT
                )
            ).replace("\\", "/"),
            "candidate_config_sha256": _sha256(
                Path(DEFAULT_E18_770_EXACT_CAP_CRITICAL_FEED_CONFIG_PATH)
            ),
            "control_source": str(CONTROL_SOURCE.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "control_source_sha256": _sha256(CONTROL_SOURCE),
            "control_config": str(
                Path(DEFAULT_E18_770_WATER_BEFORE_DIG_GUARD_V2_CONFIG_PATH).relative_to(
                    ROOT
                )
            ).replace("\\", "/"),
            "control_config_sha256": _sha256(
                Path(DEFAULT_E18_770_WATER_BEFORE_DIG_GUARD_V2_CONFIG_PATH)
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
