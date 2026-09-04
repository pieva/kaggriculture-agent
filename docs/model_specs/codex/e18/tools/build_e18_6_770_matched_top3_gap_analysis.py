#!/usr/bin/env python3
"""Compare E18.6 only with exact 7-7-0 profiles from the current Top 3."""

from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
TOP3_ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/discovery/"
    / "E18_CURRENT_TOP3_STRATEGY_BENCHMARK_2026_09_04.json"
)
CODEX_ARTIFACT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_6_CONCENTRATED_770_THROUGHPUT_DEV_GATE_V1.json"
)
OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_6_770_MATCHED_TOP3_GAP_ANALYSIS_2026_09_04.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_6_770_MATCHED_TOP3_GAP_ANALYSIS_IT.md"
)

CANDIDATE = "CODEX_E18_6_CONCENTRATED_770"
EXACT_TOPOLOGY = "7-7-0"
MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})
CROP_SERVICE = ("PLANT", "WATER", "HARVEST", "DIG")
METRICS = (
    "unit_actions",
    "move",
    "pass",
    "productive_normalized",
    "move_per_productive_normalized",
    "crop_service",
    "other_productive",
    "plant",
    "water",
    "harvest_commands",
    "dig",
    "peak_workers",
    "peak_crops",
    "late_crop_tile_days",
    "late_unwatered_tile_days",
    "late_unwatered_per_crop_tile",
    "harvest_events",
    "harvested_units",
    "units_per_successful_harvest",
    "harvested_units_per_1000_moves",
    "final_animals",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _codex_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for match in payload["matches"]:
        for seat in (0, 1):
            if match[f"p{seat}"] != CANDIDATE:
                continue
            source = match[f"p{seat}_metrics"]
            actions = source["action_counts"]
            unit_actions = sum(int(value) for value in actions.values())
            move = sum(int(actions.get(opcode, 0)) for opcode in MOVES)
            passes = int(actions.get("PASS", 0))
            productive = unit_actions - move - passes
            crop_service = sum(
                int(actions.get(opcode, 0)) for opcode in CROP_SERVICE
            )
            events = int(source["harvest_events_total"])
            harvested = int(source["harvested_units_total"])
            rows.append(
                {
                    "seed": match["seed"],
                    "seat": seat,
                    "unit_actions": unit_actions,
                    "move": move,
                    "pass": passes,
                    "productive_normalized": productive,
                    "move_per_productive_normalized": move / productive,
                    "crop_service": crop_service,
                    "other_productive": productive - crop_service,
                    "plant": int(actions.get("PLANT", 0)),
                    "water": int(actions.get("WATER", 0)),
                    "harvest_commands": int(actions.get("HARVEST", 0)),
                    "dig": int(actions.get("DIG", 0)),
                    "peak_workers": int(source["peak_hands"]),
                    "peak_crops": int(source["peak_crops"]),
                    "late_crop_tile_days": float(
                        source["crop_tile_days_d21_d30"]
                    ),
                    "late_unwatered_tile_days": float(
                        source["unwatered_tile_days_d21_d30"]
                    ),
                    "late_unwatered_per_crop_tile": float(
                        source["late_unwatered_per_crop_tile"]
                    ),
                    "harvest_events": events,
                    "harvested_units": harvested,
                    "units_per_successful_harvest": harvested / events,
                    "harvested_units_per_1000_moves": float(
                        source["harvested_units_per_1000_moves"]
                    ),
                    "final_animals": int(source["final_animals"]),
                    "verified_livestock_losses": int(
                        source["verified_livestock_losses"]
                    ),
                }
            )
    return rows


def _leader_row(profile: dict[str, Any]) -> dict[str, Any]:
    actions = profile["actions"]
    events = sum(int(value) for value in profile["harvest_events"].values())
    harvested = int(profile["harvested_units_total"])
    crop_service = sum(
        int(actions[opcode.lower()]) for opcode in CROP_SERVICE
    )
    return {
        "episode_id": int(profile["episode_id"]),
        "player": profile["player"],
        "opponent": profile["opponent"],
        "outcome": profile["outcome"],
        "action_shape_sha256": profile["action_shape_sha256"],
        "unit_actions": int(actions["unit_actions"]),
        "move": int(actions["move"]),
        "pass": int(actions["pass"]),
        "productive_normalized": int(actions["productive"]),
        "move_per_productive_normalized": float(
            actions["move_per_productive"]
        ),
        "crop_service": crop_service,
        "other_productive": int(actions["other_productive"]),
        "plant": int(actions["plant"]),
        "water": int(actions["water"]),
        "harvest_commands": int(actions["harvest"]),
        "dig": int(actions["dig"]),
        "peak_workers": int(profile["peak_workers"]),
        "peak_crops": int(profile["peak_crops"]),
        "late_crop_tile_days": float(profile["crop_tile_days_d21_d30"]),
        "late_unwatered_tile_days": float(
            profile["unwatered_tile_days_d21_d30"]
        ),
        "late_unwatered_per_crop_tile": float(
            profile["late_unwatered_per_crop_tile"]
        ),
        "harvest_events": events,
        "harvested_units": harvested,
        "units_per_successful_harvest": harvested / events,
        "harvested_units_per_1000_moves": float(
            profile["harvested_units_per_1000_moves"]
        ),
        "final_animals": int(profile["final_animals"]),
        "harvested_units_by_crop": profile["harvested_units"],
        "action_phases": profile["action_phases"],
        "farm_snapshots": profile["farm_snapshots"],
    }


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "profiles": len(rows),
        **{
            f"{metric}_mean": statistics.mean(
                float(row[metric]) for row in rows
            )
            for metric in METRICS
        },
    }


def _phase_reference(rows: list[dict[str, Any]]) -> dict[str, Any]:
    fields = (
        "move",
        "pass",
        "productive",
        "move_per_productive",
        "plant",
        "water",
        "harvest",
        "dig",
        "other_productive",
    )
    return {
        phase: {
            f"{field}_mean": statistics.mean(
                float(row["action_phases"][phase][field]) for row in rows
            )
            for field in fields
        }
        for phase in ("D01_D10", "D11_D20", "D21_D30")
    }


def _crop_reference(rows: list[dict[str, Any]]) -> dict[str, float]:
    return {
        crop: statistics.mean(
            float(row["harvested_units_by_crop"].get(crop, 0)) for row in rows
        )
        for crop in ("WHEAT", "STRAWBERRY", "MELON", "CARROT", "TOMATO")
    }


def _gap(candidate: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    result = {}
    for metric in METRICS:
        key = f"{metric}_mean"
        baseline = float(reference[key])
        value = float(candidate[key])
        result[metric] = {
            "codex": value,
            "top3_exact_770": baseline,
            "absolute": value - baseline,
            "percent": 100.0 * (value - baseline) / baseline,
        }
    return result


def _hypotheses(gaps: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "priority": 0,
            "id": "NORMALIZE_ACTION_TAXONOMY",
            "observation": (
                "The local gate excludes PICKUP/DROP/PLACE from productive, "
                "while replay productive includes every non-MOVE/non-PASS "
                "unit command."
            ),
            "next_test": (
                "Publish both local-service and normalized productive KPIs; "
                "never compare the two definitions directly."
            ),
        },
        {
            "priority": 1,
            "id": "CONVERT_PASS_TO_LOCAL_CROP_SERVICE",
            "observation": (
                f"PASS gap {gaps['pass']['absolute']:+.1f}; crop-service gap "
                f"{gaps['crop_service']['absolute']:+.1f} per episode."
            ),
            "mechanism": (
                "A worker without provider work is left idle instead of "
                "finishing a compatible local crop task."
            ),
            "next_test": (
                "One-cluster local task queue with PASS replacement only; "
                "topology, market, worker count and crop calendar frozen."
            ),
            "acceptance": "PASS <= 600 and crop_service >= 1800.",
        },
        {
            "priority": 2,
            "id": "PERSISTENT_CROP_LIFECYCLE",
            "observation": (
                f"Late crop tile-days {gaps['late_crop_tile_days']['percent']:+.1f}%, "
                f"late unwatered rate {gaps['late_unwatered_per_crop_tile']['percent']:+.1f}%, "
                f"harvest events {gaps['harvest_events']['percent']:+.1f}%."
            ),
            "mechanism": (
                "The same peak surface is reached, but it is active and "
                "serviced for fewer late-game tile-days."
            ),
            "next_test": (
                "Age-aware WATER/HARVEST deadlines and no DIG unless a "
                "replacement crop is already funded and assignable."
            ),
            "acceptance": (
                "late_crop_tile_days >= 500, late_unwatered rate <= 0.42, "
                "harvest_events >= 300."
            ),
        },
        {
            "priority": 3,
            "id": "LOCAL_ROUTE_COMPLETION",
            "observation": (
                f"MOVE {gaps['move']['percent']:+.1f}% and normalized "
                f"MOVE/productive {gaps['move_per_productive_normalized']['percent']:+.1f}%."
            ),
            "mechanism": (
                "Preserving 7-7-5 provider routes keeps transfers that the "
                "7-7-0 leader schedule avoids."
            ),
            "next_test": (
                "Finish all feasible tasks in the current quadrant before "
                "cross-quadrant reassignment; do not alter task priorities."
            ),
            "acceptance": "MOVE <= 3500 and normalized MOVE/productive <= 1.10.",
        },
        {
            "priority": 4,
            "id": "EXACT_LIVESTOCK_CAP_14",
            "observation": (
                "Codex ends with 15 animal resources for 14 pasture slots "
                "and records one verified loss per match; exact leaders end "
                "with 14."
            ),
            "next_test": "Set the animal resource cap to 14 with zero in-transit surplus.",
            "acceptance": "14 filled pastures, final animals 14, verified losses 0.",
        },
        {
            "priority": 5,
            "id": "WORKER_13_ONLY_AFTER_SCHEDULER",
            "observation": (
                "Exact leaders peak at 13 workers and Codex at 12, but Codex "
                "already issues 2.9% more unit commands and many more PASS."
            ),
            "next_test": (
                "Do not add a worker until priorities 1-4 pass; then run an "
                "isolated 12-vs-13 worker ablation."
            ),
        },
    ]


def build() -> dict[str, Any]:
    top3 = json.loads(TOP3_ARTIFACT.read_text(encoding="utf-8"))
    codex = json.loads(CODEX_ARTIFACT.read_text(encoding="utf-8"))
    profiles = [
        profile
        for profile in top3["profiles"]
        if profile["final_pasture_topology"] == EXACT_TOPOLOGY
    ]
    leaders = [_leader_row(profile) for profile in profiles]
    codex_rows = _codex_rows(codex)
    giulio = [row for row in leaders if row["player"] == "Giulio Ravasio"]
    jesse = [row for row in leaders if row["player"] == "Jesse Bullard"]
    crop = [row for row in leaders if row["player"] == "Crop Dusta"]
    cohorts = {
        "CODEX_E18_6_770": _aggregate(codex_rows),
        "GIULIO_RAVASIO_EXACT_770": _aggregate(giulio),
        "JESSE_BULLARD_EXACT_770": _aggregate(jesse),
        "TOP3_EXACT_770_POOL": _aggregate(leaders),
    }
    gaps = _gap(cohorts["CODEX_E18_6_770"], cohorts["TOP3_EXACT_770_POOL"])
    return {
        "schema_version": "E18_6_770_MATCHED_TOP3_GAP_ANALYSIS_V1",
        "date": "2026-09-04",
        "epistemic_role": "MATCHED_TOPOLOGY_OBSERVATIONAL_DIAGNOSIS",
        "leaderboard_verification": {
            "observed_at": "2026-09-04T11:15:00+02:00",
            "url": "https://www.kaggle.com/competitions/kaggriculture/leaderboard",
            "entries": [
                {"rank": 1, "player": "Crop Dusta", "rating": 3035.3},
                {"rank": 2, "player": "Giulio Ravasio", "rating": 2976.0},
                {"rank": 3, "player": "Jesse Bullard", "rating": 2963.4},
            ],
        },
        "selection": {
            "required_final_pasture_topology": EXACT_TOPOLOGY,
            "codex_profiles": len(codex_rows),
            "top3_exact_profiles": len(leaders),
            "giulio_profiles": len(giulio),
            "jesse_profiles": len(jesse),
            "crop_dusta_profiles": len(crop),
            "crop_dusta_status": "EXCLUDED_NO_EXACT_770_IN_FROZEN_CORPUS",
            "episode_ids": sorted({row["episode_id"] for row in leaders}),
            "matched_head_to_head_episode": 105398563,
        },
        "normalization": {
            "productive_normalized": "all unit commands excluding MOVE and PASS",
            "reason": (
                "Local productive_actions excludes logistics commands, while "
                "the replay benchmark includes them."
            ),
            "money_and_score_compared": False,
        },
        "comparability": {
            "same_final_pasture_topology": True,
            "same_final_pasture_count": 14,
            "same_environment": False,
            "same_opponents": False,
            "causal_claim": (
                "Topology is controlled observationally; strategy gaps are "
                "hypothesis-generating, not causal estimates."
            ),
        },
        "provenance": {
            "top3_artifact": str(TOP3_ARTIFACT.relative_to(ROOT)).replace("\\", "/"),
            "top3_artifact_sha256": _sha256(TOP3_ARTIFACT),
            "codex_artifact": str(CODEX_ARTIFACT.relative_to(ROOT)).replace("\\", "/"),
            "codex_artifact_sha256": _sha256(CODEX_ARTIFACT),
        },
        "cohorts": cohorts,
        "codex_rows": codex_rows,
        "leader_exact_770_rows": leaders,
        "codex_vs_top3_exact_770_gaps": gaps,
        "top3_exact_770_phase_reference": _phase_reference(leaders),
        "top3_exact_770_harvest_mix": _crop_reference(leaders),
        "hypotheses": _hypotheses(gaps),
    }


def _number(value: float, digits: int = 1) -> str:
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _write_report(payload: dict[str, Any]) -> None:
    cohorts = payload["cohorts"]
    codex = cohorts["CODEX_E18_6_770"]
    giulio = cohorts["GIULIO_RAVASIO_EXACT_770"]
    jesse = cohorts["JESSE_BULLARD_EXACT_770"]
    pool = cohorts["TOP3_EXACT_770_POOL"]
    gaps = payload["codex_vs_top3_exact_770_gaps"]

    def row(label: str, key: str, digits: int = 1) -> str:
        metric = f"{key}_mean"
        return (
            f"| {label} | {_number(codex[metric], digits)} | "
            f"{_number(giulio[metric], digits)} | {_number(jesse[metric], digits)} | "
            f"{_number(pool[metric], digits)} | {gaps[key]['percent']:+.1f}% |"
        )

    phases = payload["top3_exact_770_phase_reference"]
    crop_mix = payload["top3_exact_770_harvest_mix"]
    report = f"""# E18.6 — gap analysis 7-7-0 topology-matched

## Verdetto

Tenendo fissa la topologia finale `7-7-0`, il gap di E18.6 non è spiegato
dalla geometria. La candidata emette il `2,9%` di comandi unità in più del
pool Giulio/Jesse equivalente, ma produce `-18,1%` di servizio crop,
`+60,5%` PASS, `+4,1%` move e `-36,7%` unità raccolte. Il problema prioritario
è la conversione del tempo-worker in lifecycle crop locale.

Il confronto esatto contiene 14 profili locali Codex, due replay `7-7-0` di
Giulio e quattro di Jesse. Crop Dusta non presenta nessun `7-7-0` negli otto
profili del corpus congelato ed è quindi escluso, non approssimato con altre
topologie. La leaderboard è stata riverificata: Crop `3035,3`, Giulio
`2976,0`, Jesse `2963,4`.

## Confronto normalizzato

`Produttive normalizzate` significa ogni comando unità diverso da MOVE e
PASS. È la sola tassonomia confrontabile: il KPI locale `productive_actions`
esclude PICKUP/DROP/PLACE, quello dei replay li include. Money locale e score
Kaggle non vengono confrontati.

| KPI | Codex 770 | Giulio 770 | Jesse 770 | Pool 770 | Gap Codex |
|---|---:|---:|---:|---:|---:|
| Profili | 14 | 2 | 4 | 6 | — |
{row('Comandi unità', 'unit_actions')}
{row('Move', 'move')}
{row('PASS', 'pass')}
{row('Produttive normalizzate', 'productive_normalized')}
{row('Move/produttive normalizzato', 'move_per_productive_normalized', 3)}
{row('Servizio crop', 'crop_service')}
{row('Altre produttive', 'other_productive')}
{row('PLANT', 'plant')}
{row('WATER', 'water')}
{row('HARVEST comandati', 'harvest_commands')}
{row('DIG', 'dig')}
{row('Peak crop', 'peak_crops')}
{row('Crop tile-days D21–D30', 'late_crop_tile_days')}
{row('Unwatered/crop D21–D30', 'late_unwatered_per_crop_tile', 3)}
{row('Harvest riusciti', 'harvest_events')}
{row('Unità raccolte', 'harvested_units')}
{row('Unità/harvest riuscito', 'units_per_successful_harvest', 3)}
{row('Unità raccolte/1.000 move', 'harvested_units_per_1000_moves')}
{row('Animali finali', 'final_animals')}

## Cosa fanno gli equivalenti Top-3

Giulio e Jesse condividono praticamente lo stesso schedule: `243` PLANT,
`1.168–1.172` WATER, `467` HARVEST e `43` DIG. Nell'episodio `105398563`
si affrontano direttamente con `7-7-0` entrambi e restano a sole sei azioni
produttive di distanza. Questo rende il pattern più credibile di una media
ottenuta mescolando topologie.

La progressione del pool esatto è:

| Fase | Move | PASS | Produttive | Move/prod. | PLANT | WATER | HARVEST |
|---|---:|---:|---:|---:|---:|---:|---:|
| D1–D10 | {_number(phases['D01_D10']['move_mean'])} | {_number(phases['D01_D10']['pass_mean'])} | {_number(phases['D01_D10']['productive_mean'])} | {_number(phases['D01_D10']['move_per_productive_mean'], 3)} | {_number(phases['D01_D10']['plant_mean'])} | {_number(phases['D01_D10']['water_mean'])} | {_number(phases['D01_D10']['harvest_mean'])} |
| D11–D20 | {_number(phases['D11_D20']['move_mean'])} | {_number(phases['D11_D20']['pass_mean'])} | {_number(phases['D11_D20']['productive_mean'])} | {_number(phases['D11_D20']['move_per_productive_mean'], 3)} | {_number(phases['D11_D20']['plant_mean'])} | {_number(phases['D11_D20']['water_mean'])} | {_number(phases['D11_D20']['harvest_mean'])} |
| D21–D30 | {_number(phases['D21_D30']['move_mean'])} | {_number(phases['D21_D30']['pass_mean'])} | {_number(phases['D21_D30']['productive_mean'])} | {_number(phases['D21_D30']['move_per_productive_mean'], 3)} | {_number(phases['D21_D30']['plant_mean'])} | {_number(phases['D21_D30']['water_mean'])} | {_number(phases['D21_D30']['harvest_mean'])} |

Il lifecycle cresce invece di spegnersi: le produttive passano da `666` a
`1.265` e poi `1.384`, mentre i PASS scendono da `236` a `172` e `122`.
Il raccolto medio è Wheat `{_number(crop_mix['WHEAT'])}`, Strawberry
`{_number(crop_mix['STRAWBERRY'])}`, Melon `{_number(crop_mix['MELON'])}` e
Carrot `{_number(crop_mix['CARROT'])}`; Tomato non viene usato in questo
regime esatto.

## Gap causali candidati, in ordine

1. **Tassonomia prima del tuning.** Pubblicare sempre productive locale e
   normalizzata: il vecchio confronto Top-3 sovrastimava il gap perché
   confrontava definizioni diverse.
2. **PASS → servizio crop locale.** Mantenendo invariati topologia, market,
   worker e calendario, assegnare un solo task compatibile nello stesso
   cluster quando il provider produrrebbe PASS. Gate: PASS `≤600`, crop
   service `≥1.800`.
3. **Lifecycle persistente.** Il peak crop è vicino (`-5,0%`), ma i crop
   tile-days tardi sono `-10,7%`, gli harvest riusciti `-31,7%` e il tasso
   late-unwatered `+24,5%`. Servono deadline WATER/HARVEST age-aware e DIG
   soltanto con reimpianto finanziato. Gate: late crop tile-days `≥500`,
   unwatered/crop `≤0,42`, harvest riusciti `≥300`.
4. **Completamento locale delle rotte.** A parità di `7-7-0`, Codex fa
   `+4,1%` move. Dopo il PASS replacement, completare i task fattibili nel
   quadrante prima di un trasferimento. Gate: move `≤3.500`, rapporto
   normalizzato `≤1,10`.
5. **Cap animali esatto.** Portare il cap da 15 a 14: i leader chiudono con
   14 animali, Codex con 15 e una perdita verificata per match.
6. **Tredicesimo worker solo dopo.** I leader arrivano a 13 e Codex a 12,
   ma Codex emette già più comandi totali e molti più PASS. Aggiungere capacità
   prima di correggere lo scheduler rischia di aggiungere inattività; il
   confronto 12-vs-13 deve restare un'ablation separata.

## Limiti

La topologia è controllata, ma gli ambienti non lo sono: Codex gioca localmente
contro E18.2, Giulio e Jesse giocano replay live. Il confronto identifica gap
e ipotesi, non stima l'effetto causale di una modifica. Il prossimo esperimento
deve cambiare una sola priorità alla volta sulla nostra `7-7-0`, usando gli
stessi seed e seat del gate E18.6.
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")


def main() -> int:
    payload = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_report(payload)
    print(f"wrote {OUTPUT}")
    print(f"wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
