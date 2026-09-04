#!/usr/bin/env python3
"""Run the E18.6 concentrated 7-7-0 gate against frozen E18.2."""

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
from agricola.strategy.codex.codex_e18_concentrated_770_throughput import (
    DEFAULT_E18_CONCENTRATED_770_CONFIG_PATH,
    create_codex_e18_concentrated_770_throughput,
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
    / "E18_6_CONCENTRATED_770_THROUGHPUT_DEV_GATE_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_6_CONCENTRATED_770_THROUGHPUT_DEV_GATE_REPORT_IT.md"
)
SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_concentrated_770_throughput.py"
)
CONTROL_SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e18_capacity_governed_v4d.py"
)

CANDIDATE = "CODEX_E18_6_CONCENTRATED_770"
CONTROL = "CODEX_E18_2_CONTROL"
PARTICIPANTS = (CANDIDATE, CONTROL)
EXPECTED_TOPOLOGY = {"Q0": 7, "Q1": 7, "Q2": 0}


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-6-770-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-6-770-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_codex_e18_concentrated_770_throughput(
            run_context=context
        )
        return policy, policy.codex_e18_concentrated_770_instance
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
            if tile.get("kind") == "PLANT":
                counts["crops"] += 1
                if not bool(tile.get("watered_today", False)):
                    counts["unwatered"] += 1
            elif tile.get("kind") == "WEED":
                counts["weeds"] += 1
    return counts


def _lifecycle_metrics(env: Any, seat: int) -> dict[str, float]:
    daily: list[dict[str, float]] = []
    for state in env.steps:
        observation = state[seat].get("observation", {}) or {}
        if int(observation.get("hour", -1)) != 23:
            continue
        surface = _farm_surface(base._farm(state, seat))
        daily.append(
            {
                "display_day": int(observation.get("day", 0)) + 1,
                "crops": float(surface["crops"]),
                "unwatered": float(surface["unwatered"]),
                "weeds": float(surface["weeds"]),
            }
        )
    late = [row for row in daily if row["display_day"] >= 21]
    late_crops = sum(row["crops"] for row in late)
    late_unwatered = sum(row["unwatered"] for row in late)
    return {
        "crop_tile_days_total": sum(row["crops"] for row in daily),
        "crop_tile_days_d21_d30": late_crops,
        "unwatered_tile_days_total": sum(row["unwatered"] for row in daily),
        "unwatered_tile_days_d21_d30": late_unwatered,
        "late_unwatered_per_crop_tile": (
            late_unwatered / late_crops if late_crops else 0.0
        ),
        "weed_tile_days_total": sum(row["weeds"] for row in daily),
        "weed_tile_days_d21_d30": sum(row["weeds"] for row in late),
    }


def _pasture_profile(farm: dict[str, Any]) -> dict[str, dict[str, int]]:
    profile = {
        quadrant: {"built": 0, "filled": 0}
        for quadrant in ("Q0", "Q1", "Q2")
    }
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict) or tile.get("kind") != "PASTURE":
                continue
            quadrant = replay._quadrant(x, y)
            profile[quadrant]["built"] += 1
            if tile.get("animal"):
                profile[quadrant]["filled"] += 1
    return profile


def _seat_metrics(env: Any, seat: int, name: str, controller: Any) -> dict[str, Any]:
    metrics = base._seat_metrics(env, seat, "E18_GENERIC", controller)
    metrics["technical_errors"] = int(getattr(controller, "error_count", 0))
    metrics["fallbacks"] = int(getattr(controller, "fallback_count", 0))
    metrics["verified_livestock_losses"] = prior._verified_livestock_losses(
        env, seat
    )
    metrics["animal_escapes"] = metrics["verified_livestock_losses"]
    metrics.update(_lifecycle_metrics(env, seat))
    farm = base._farm(env.steps[-1], seat)
    profile = _pasture_profile(farm)
    metrics["final_pastures_by_quadrant"] = {
        quadrant: values["built"] for quadrant, values in profile.items()
    }
    metrics["final_filled_pastures_by_quadrant"] = {
        quadrant: values["filled"] for quadrant, values in profile.items()
    }
    metrics["final_pastures_total"] = sum(
        metrics["final_pastures_by_quadrant"].values()
    )
    metrics["final_filled_pastures_total"] = sum(
        metrics["final_filled_pastures_by_quadrant"].values()
    )
    execution = replay._execution_metrics(env.steps, seat)
    transitions = replay._transition_metrics(env.steps, seat)["counts"]
    metrics["harvested_units_total"] = int(execution["harvested_units_total"])
    metrics["harvest_events_total"] = int(sum(execution["harvest_events"].values()))
    metrics["abandoned_crop_count"] = int(
        transitions.get("expired_to_weed", 0)
        + transitions.get("starved_to_weed", 0)
        + transitions.get("disappeared_without_observed_harvest", 0)
    )
    metrics["harvested_units_per_1000_moves"] = (
        1000.0 * metrics["harvested_units_total"] / metrics["move_actions"]
        if metrics["move_actions"]
        else 0.0
    )
    metrics["score_per_move"] = (
        metrics["money"] / metrics["move_actions"]
        if metrics["move_actions"]
        else 0.0
    )
    if name == CANDIDATE:
        telemetry = controller.telemetry_snapshot()
        metrics.update(
            {
                "topology_cap_breaches": int(telemetry["topology_cap_breaches"]),
                "max_observed_q2_pastures": int(
                    telemetry["max_observed_q2_pastures"]
                ),
                "max_active_reclaimed_crops": int(
                    telemetry["max_active_reclaimed_crops"]
                ),
                "seed_batches_requested": telemetry["seed_batches_requested"],
                "phase_crop_commands": telemetry["phase_crop_commands"],
                "persistent_fill_override_batches": int(
                    telemetry["persistent_fill_override_batches"]
                ),
                "global_rerouting_enabled": bool(
                    telemetry["global_rerouting_enabled"]
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


MEAN_FIELDS = (
    "money",
    "move_actions",
    "productive_actions",
    "pass_actions",
    "move_per_productive",
    "harvested_units_total",
    "harvested_units_per_1000_moves",
    "score_per_move",
    "crop_tile_days_d21_d30",
    "unwatered_tile_days_d21_d30",
    "late_unwatered_per_crop_tile",
    "weed_tile_days_d21_d30",
    "abandoned_crop_count",
    "final_pastures_total",
    "final_filled_pastures_total",
)


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


def _candidate_gate(
    matches: list[dict[str, Any]], standings: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    candidate_rows = _records(matches, CANDIDATE)
    candidate = standings[CANDIDATE]
    control = standings[CONTROL]
    matched_money_deltas = []
    for match in matches:
        seat = 0 if match["p0"] == CANDIDATE else 1
        candidate_money = float(match[f"p{seat}_metrics"]["money"])
        control_money = float(match[f"p{1 - seat}_metrics"]["money"])
        matched_money_deltas.append(
            100.0 * (candidate_money - control_money) / control_money
            if control_money
            else 0.0
        )
    exact_topology = sum(
        row["final_pastures_by_quadrant"] == EXPECTED_TOPOLOGY
        for row in candidate_rows
    )
    filled = sum(row["final_filled_pastures_total"] == 14 for row in candidate_rows)
    checks = {
        "exact_770_topology_all_matches": exact_topology == 14,
        "filled_14_of_14_all_matches": filled == 14,
        "zero_q2_pastures_observed": all(
            int(row["max_observed_q2_pastures"]) == 0 for row in candidate_rows
        ),
        "zero_topology_breaches": all(
            int(row["topology_cap_breaches"]) == 0 for row in candidate_rows
        ),
        "zero_global_rerouting": all(
            row["global_rerouting_enabled"] is False for row in candidate_rows
        ),
        "zero_technical_errors": candidate["technical_errors"] == 0,
        "zero_fallbacks": candidate["fallbacks"] == 0,
        "zero_verified_livestock_losses": candidate[
            "verified_livestock_losses"
        ]
        == 0,
        "move_per_productive_at_most_1_20": candidate[
            "move_per_productive_mean"
        ]
        <= 1.20,
        "move_per_productive_at_least_5pct_better": candidate[
            "move_per_productive_mean"
        ]
        <= control["move_per_productive_mean"] * 0.95,
        "productive_at_least_3000": candidate["productive_actions_mean"] >= 3000,
        "productive_at_least_10pct_above_control": candidate[
            "productive_actions_mean"
        ]
        >= control["productive_actions_mean"] * 1.10,
        "harvested_units_at_least_720": candidate[
            "harvested_units_total_mean"
        ]
        >= 720,
        "harvested_units_at_least_20pct_above_control": candidate[
            "harvested_units_total_mean"
        ]
        >= control["harvested_units_total_mean"] * 1.20,
        "harvest_per_1000_moves_at_least_200": candidate[
            "harvested_units_per_1000_moves_mean"
        ]
        >= 200,
        "late_unwatered_rate_at_least_10pct_better": candidate[
            "late_unwatered_per_crop_tile_mean"
        ]
        <= control["late_unwatered_per_crop_tile_mean"] * 0.90,
        "money_not_below_control_minus_5pct": candidate["money_mean"]
        >= control["money_mean"] * 0.95,
        "worst_matched_money_delta_at_least_minus_5pct": min(
            matched_money_deltas
        )
        >= -5.0,
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "exact_topology_matches": exact_topology,
        "fully_filled_matches": filled,
        "worst_matched_money_delta_percent": min(matched_money_deltas),
        "mean_matched_money_delta_percent": statistics.mean(matched_money_deltas),
        "kpi_reference": "E18_CURRENT_TOP3_STRATEGY_BENCHMARK_2026_09_04",
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
        "final_filled_pastures_by_quadrant",
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
                        "final_filled_pastures_by_quadrant": json.dumps(
                            metrics["final_filled_pastures_by_quadrant"],
                            sort_keys=True,
                        ),
                    }
                )


def _write_report(payload: dict[str, Any]) -> None:
    candidate = payload["standings"][CANDIDATE]
    control = payload["standings"][CONTROL]
    gate = payload["candidate_gate"]
    verdict = "PASS" if gate["passed"] else "FAIL"
    money_delta = 100.0 * (candidate["money_mean"] - control["money_mean"]) / control[
        "money_mean"
    ]
    move_delta = 100.0 * (
        candidate["move_actions_mean"] - control["move_actions_mean"]
    ) / control["move_actions_mean"]
    productive_delta = 100.0 * (
        candidate["productive_actions_mean"] - control["productive_actions_mean"]
    ) / control["productive_actions_mean"]
    ratio_delta = 100.0 * (
        candidate["move_per_productive_mean"]
        - control["move_per_productive_mean"]
    ) / control["move_per_productive_mean"]
    harvest_delta = 100.0 * (
        candidate["harvested_units_total_mean"]
        - control["harvested_units_total_mean"]
    ) / control["harvested_units_total_mean"]
    harvest_efficiency_delta = 100.0 * (
        candidate["harvested_units_per_1000_moves_mean"]
        - control["harvested_units_per_1000_moves_mean"]
    ) / control["harvested_units_per_1000_moves_mean"]
    pass_delta = 100.0 * (
        candidate["pass_actions_mean"] - control["pass_actions_mean"]
    ) / control["pass_actions_mean"]
    late_unwatered_delta = 100.0 * (
        candidate["late_unwatered_per_crop_tile_mean"]
        - control["late_unwatered_per_crop_tile_mean"]
    ) / control["late_unwatered_per_crop_tile_mean"]
    text = f"""# E18.6 — gate 7-7-0 concentrata contro E18.2

## Verdetto

`{verdict}` sui KPI Top-3 aggiornati. La candidata usa pasture `7-7-0`,
converte in crop le cinque celle Q2 della E18.2 e conserva il routing provider
salvo traduzione in-place e fill zootecnico.

La topologia concentrata è tecnicamente realizzabile, ma l'ipotesi di un
guadagno di efficienza non è confermata: la candidata perde tutti i 14 match,
non riduce le move e riduce il lavoro produttivo.

## Risultati

| KPI | E18.6 770 | E18.2 controllo | Delta 770 |
|---|---:|---:|---:|
| Money | {candidate['money_mean']:.2f} | {control['money_mean']:.2f} | {money_delta:+.2f}% |
| Move | {candidate['move_actions_mean']:.2f} | {control['move_actions_mean']:.2f} | {move_delta:+.2f}% |
| Produttive | {candidate['productive_actions_mean']:.2f} | {control['productive_actions_mean']:.2f} | {productive_delta:+.2f}% |
| Move/produttive | {candidate['move_per_productive_mean']:.4f} | {control['move_per_productive_mean']:.4f} | {ratio_delta:+.2f}% |
| PASS | {candidate['pass_actions_mean']:.2f} | {control['pass_actions_mean']:.2f} | {pass_delta:+.2f}% |
| Harvest | {candidate['harvested_units_total_mean']:.2f} | {control['harvested_units_total_mean']:.2f} | {harvest_delta:+.2f}% |
| Harvest/1.000 move | {candidate['harvested_units_per_1000_moves_mean']:.2f} | {control['harvested_units_per_1000_moves_mean']:.2f} | {harvest_efficiency_delta:+.2f}% |
| Late unwatered/crop | {candidate['late_unwatered_per_crop_tile_mean']:.4f} | {control['late_unwatered_per_crop_tile_mean']:.4f} | {late_unwatered_delta:+.2f}% |

Topologia esatta: `{gate['exact_topology_matches']}/14`; fill 14/14:
`{gate['fully_filled_matches']}/14`; perdite verificate:
`{candidate['verified_livestock_losses']}`. Record:
`{candidate['wins']}-{control['wins']}`.

## Lettura causale

Il risparmio geometrico esiste: cinque pasture e quattro animali finali in
meno, con le cinque celle Q2 effettivamente utilizzate come crop. Non diventa
però risparmio logistico. Le move medie restano quasi identiche
(`{move_delta:+.2f}%`), le produttive calano di `{abs(productive_delta):.2f}%`
e i PASS crescono di `{pass_delta:.2f}%`. Il lavoro zootecnico rimosso non è
sostituito da un ciclo crop abbastanza intenso; harvest e harvest per 1.000
move scendono rispettivamente di `{abs(harvest_delta):.2f}%` e
`{abs(harvest_efficiency_delta):.2f}%`.

La piccola riduzione del late-unwatered (`{abs(late_unwatered_delta):.2f}%`)
non raggiunge il target del 10% e non compensa il throughput perso. Il cap di
15 risorse animali per 14 pasture introduce inoltre un transito
sovrannumerario: il verificatore osserva una perdita in ciascun match. È un
difetto di safety da non conservare, ma non spiega da solo il gap economico
medio del `{abs(money_delta):.2f}%`.

La prima esecuzione completa aveva prodotto una topologia invalida `6-5-0`
perché il carrier fill sovrascriveva tre BUILD_PASTURE. È stata corretta
soltanto la precedenza del comando, senza cambiare KPI; quel tentativo non è
usato per la decisione.

## Decisione

E18.6 V1 è `REJECTED_AT_DEVELOPMENT_GATE`. Non consumare holdout o final e non
preparare/uploadare una submission. Il prossimo trattamento non deve essere
un altro overlay geometrico: prima serve un lifecycle scheduler capace di
trasformare il Q2 crop-only in lavoro produttivo e di ridurre davvero le
tratte; un'eventuale 7-7-0 nativa dovrà inoltre usare cap animali 14.

## Check

```json
{json.dumps(gate['checks'], indent=2, sort_keys=True)}
```
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(text, encoding="utf-8")


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
        "schema_version": "E18_6_CONCENTRATED_770_THROUGHPUT_DEV_GATE_V1",
        "date": "2026-09-04",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "causal_variable": "E18_2_775_TO_CONCENTRATED_770_WITH_IN_PLACE_Q2_CROPS",
        "participants": list(PARTICIPANTS),
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
        "pre_gate_correction": {
            "invalid_attempt_completed": True,
            "invalid_final_topology": "6-5-0",
            "invalid_match_count": 14,
            "diagnosis": (
                "Persistent livestock carriers overrode three BUILD_PASTURE "
                "commands before construction completed."
            ),
            "correction_scope": (
                "Carrier fill may override provider work only after all "
                "fourteen target pastures are built."
            ),
            "kpi_thresholds_changed": False,
            "invalid_attempt_used_for_promotion": False,
        },
        "provenance": {
            "candidate_source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "candidate_source_sha256": prior._sha256(SOURCE),
            "candidate_config": str(
                Path(DEFAULT_E18_CONCENTRATED_770_CONFIG_PATH).relative_to(ROOT)
            ).replace("\\", "/"),
            "candidate_config_sha256": prior._sha256(
                Path(DEFAULT_E18_CONCENTRATED_770_CONFIG_PATH)
            ),
            "control_source": str(CONTROL_SOURCE.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "control_source_sha256": prior._sha256(CONTROL_SOURCE),
            "control_config": str(
                Path(DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH).relative_to(ROOT)
            ).replace("\\", "/"),
            "control_config_sha256": prior._sha256(
                Path(DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH)
            ),
        },
        "standings": standings,
        "candidate_gate": _candidate_gate(matches, standings),
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
