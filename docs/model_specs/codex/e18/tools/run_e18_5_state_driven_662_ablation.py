#!/usr/bin/env python3
"""Run the E18.5 6-6-2 versus 7-7-2 move-efficiency ablation."""

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
from agricola.strategy.codex.codex_e18_state_driven_662_ablation import (
    create_codex_e18_state_driven_662_ablation,
)
from docs.model_specs.codex.e18.tools import (
    run_e18_4_state_driven_772_v2_gate as v2_gate,
)

MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
REFERENCE_772_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_4_STATE_DRIVEN_772_V2_DEV_GATE.json"
)
OUTPUT_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
OUTPUT_PARTIAL = OUTPUT_JSON.with_suffix(".partial.json")
OUTPUT_REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_REPORT_IT.md"
)
CANDIDATE = "CODEX_E18_5_STATE_DRIVEN_662"
CONTROL = "CODEX_E18_2_CONTROL"
PARTICIPANTS = (CANDIDATE, CONTROL)


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-5-662-ABLATION-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-5-662-ABLATION-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_codex_e18_state_driven_662_ablation(run_context=context)
        return policy, policy.codex_e18_state_driven_662_instance
    if name == CONTROL:
        policy = create_codex_e18_capacity_governed_v4d(run_context=context)
        return policy, policy.codex_e18_capacity_governed_instance
    raise ValueError(name)


def _seat_metrics(env: Any, seat: int, name: str, controller: Any) -> dict[str, Any]:
    metrics = v2_gate._seat_metrics(
        env,
        seat,
        v2_gate.CANDIDATE if name == CANDIDATE else v2_gate.CONTROL,
        controller,
    )
    target = (
        {"Q0": 6, "Q1": 6, "Q2": 2}
        if name == CANDIDATE
        else {"Q0": 7, "Q1": 7, "Q2": 5}
    )
    metrics["target_pastures_by_quadrant"] = target
    metrics["final_empty_target_pastures"] = sum(
        max(
            0,
            target[quadrant]
            - int(metrics["final_filled_pastures_by_quadrant"][quadrant]),
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
        "move_actions",
        "productive_actions",
        "move_per_productive",
        "pass_actions",
        "harvested_units_total",
        "mean_units_per_harvest",
        "crop_tile_days_d21_d30",
        "weed_tile_days_d21_d30",
        "final_empty_target_pastures",
        "route_thrashing_violations",
        "pass_on_actionable_violations",
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


def _gate(
    matches: list[dict[str, Any]],
    standings: dict[str, dict[str, Any]],
    reference_772: dict[str, Any],
) -> dict[str, Any]:
    candidate = _records(matches, CANDIDATE)
    candidate_move = _mean(candidate, "move_actions")
    control_move = float(reference_772["move_actions_mean"])
    candidate_productive = _mean(candidate, "productive_actions")
    control_productive = float(reference_772["productive_actions_mean"])
    candidate_ratio = (
        candidate_move / candidate_productive
        if candidate_productive
        else float("inf")
    )
    control_ratio = control_move / control_productive if control_productive else 0.0
    exact = sum(
        row["final_pastures_by_quadrant"] == {"Q0": 6, "Q1": 6, "Q2": 2}
        for row in candidate
    )
    filled = sum(row["final_empty_target_pastures"] == 0 for row in candidate)
    checks = {
        "move_actions_at_least_5pct_lower": candidate_move <= control_move * 0.95,
        "move_per_productive_at_least_5pct_lower": candidate_ratio
        <= control_ratio * 0.95,
        "productive_actions_at_least_90pct_control": candidate_productive
        >= control_productive * 0.90,
        "exact_662_topology_all_matches": exact == len(candidate),
        "all_14_target_pastures_filled": filled == len(candidate),
        "zero_pass_on_actionable": sum(
            int(row["pass_on_actionable_violations"]) for row in candidate
        )
        == 0,
        "zero_route_thrashing": sum(
            int(row["route_thrashing_violations"]) for row in candidate
        )
        == 0,
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
        "candidate_move_per_productive": candidate_ratio,
        "control_move_per_productive": control_ratio,
        "move_delta_percent": (
            (candidate_move - control_move) / control_move * 100
            if control_move
            else 0.0
        ),
        "move_per_productive_delta_percent": (
            (candidate_ratio - control_ratio) / control_ratio * 100
            if control_ratio
            else 0.0
        ),
        "productive_delta_percent": (
            (candidate_productive - control_productive) / control_productive * 100
            if control_productive
            else 0.0
        ),
        "exact_topology_matches": exact,
        "fully_filled_matches": filled,
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
        "productive_actions",
        "move_per_productive",
        "harvested_units_total",
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
    candidate = payload["standings"][CANDIDATE]
    control = payload["frozen_772_reference"]["standings"]
    gate = payload["efficiency_gate"]
    failed = [name for name, passed in gate["checks"].items() if not passed]

    def delta_percent(key: str) -> float:
        baseline = float(control[key])
        return (
            (float(candidate[key]) - baseline) / baseline * 100
            if baseline
            else 0.0
        )

    report = f"""# E18.5 — ablation topologica 6-6-2

## Decisione

**Efficiency gate: {'PASS' if gate['passed'] else 'FAIL'}**. La candidata resta
development-only e nessun upload Kaggle è autorizzato.

## Confronto diretto

| KPI medio vs E18.2 | 6-6-2 | 7-7-2 frozen | Delta 6-6-2 |
|---|---:|---:|---:|
| Move | {candidate['move_actions_mean']:.2f} | {control['move_actions_mean']:.2f} | {gate['move_delta_percent']:+.2f}% |
| Productive | {candidate['productive_actions_mean']:.2f} | {control['productive_actions_mean']:.2f} | {gate['productive_delta_percent']:+.2f}% |
| Move/productive | {gate['candidate_move_per_productive']:.4f} | {gate['control_move_per_productive']:.4f} | {gate['move_per_productive_delta_percent']:+.2f}% |
| Money | {candidate['money_mean']:.2f} | {control['money_mean']:.2f} | {delta_percent('money_mean'):+.2f}% |
| Harvested units | {candidate['harvested_units_total_mean']:.2f} | {control['harvested_units_total_mean']:.2f} | {delta_percent('harvested_units_total_mean'):+.2f}% |
| Late weed tile-days | {candidate['weed_tile_days_d21_d30_mean']:.2f} | {control['weed_tile_days_d21_d30_mean']:.2f} | {delta_percent('weed_tile_days_d21_d30_mean'):+.2f}% |

## Check falliti

{chr(10).join(f'- `{name}`' for name in failed) if failed else '- Nessuno.'}

## Integrità

- match development: {payload['match_count']};
- topologia 6-6-2 esatta: {gate['exact_topology_matches']}/{payload['match_count']};
- fill 14/14: {gate['fully_filled_matches']}/{payload['match_count']};
- holdout/final: non consumati;
- errori/fallback/perdite: {candidate['technical_errors']}/{candidate['fallbacks']}/{candidate['verified_livestock_losses']}.
"""
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text(report, encoding="utf-8")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    frozen_772 = json.loads(REFERENCE_772_JSON.read_text(encoding="utf-8"))
    reference_772 = frozen_772["standings"][v2_gate.CANDIDATE]
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
    if OUTPUT_PARTIAL.exists():
        partial = json.loads(OUTPUT_PARTIAL.read_text(encoding="utf-8"))
        if partial.get("seeds") != seeds:
            raise RuntimeError("partial artifact uses a different development sample")
        completed = {
            int(index): match
            for index, match in partial.get("completed", {}).items()
        }
        print(f"resuming from {len(completed)}/{len(specs)} completed matches")
    pending_specs = [spec for spec in specs if spec[0] not in completed]
    with ProcessPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(_run_spec, index, seed, p0, p1): index
            for index, seed, p0, p1 in pending_specs
        }
        for future in as_completed(futures):
            index, match = future.result()
            completed[index] = match
            OUTPUT_PARTIAL.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT_PARTIAL.write_text(
                json.dumps(
                    {
                        "schema_version": "E18_5_662_PARTIAL_V1",
                        "seeds": seeds,
                        "completed": completed,
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            print(
                f"[{len(completed):02d}/{len(specs)}] seed={match['seed']} "
                f"{match['p0']} vs {match['p1']} winner={match['winner']}",
                flush=True,
            )
    matches = [completed[index] for index in range(len(specs))]
    standings = _aggregate(matches)
    gate = _gate(matches, standings, reference_772)
    payload = {
        "schema_version": "E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "date": "2026-09-04",
        "causal_variable": "PASTURE_TOPOLOGY_772_TO_662_AND_CAP_16_TO_14_ONLY",
        "participants": list(PARTICIPANTS),
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
        "frozen_772_reference": {
            "artifact": str(REFERENCE_772_JSON.relative_to(ROOT)).replace("\\", "/"),
            "same_development_seeds": frozen_772["seeds"] == seeds,
            "same_seats": frozen_772["seats"] == [0, 1],
            "common_opponent": CONTROL,
            "standings": reference_772,
        },
        "standings": standings,
        "efficiency_gate": gate,
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv(matches)
    _write_report(payload)
    OUTPUT_PARTIAL.unlink(missing_ok=True)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    print(f"wrote {OUTPUT_REPORT}")
    print(f"Efficiency gate: {'PASS' if gate['passed'] else 'FAIL'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
