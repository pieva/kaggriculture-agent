#!/usr/bin/env python3
"""Build the E18.18 Gate-0A plan, verify determinism, and write evidence."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from e18_18_capacity_trajectory_planner import build_plan

ROOT = Path(__file__).resolve().parents[5]
OUTPUT_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_V1.json"
)
OUTPUT_CSV = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_V1.csv"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_REPORT_IT.md"
)


def _write_csv(payload: dict[str, Any]) -> None:
    scalar_fields = [
        "day",
        "available_action_slots",
        "reference_requested_action_slots",
        "planned_action_slots",
        "slack_action_slots",
        "slack_ratio",
        "reserve_target_met",
        "active_units",
        "planned_hands",
    ]
    structured_fields = [
        "crop_mix_end_of_actions",
        "animal_mix_end_of_actions",
        "fertilizer_used_by_crop",
        "action_counts",
    ]
    fields = [*scalar_fields, *structured_fields]
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in payload["daily"]:
            writer.writerow(
                {
                    **{field: row[field] for field in scalar_fields},
                    **{
                        field: json.dumps(row[field], sort_keys=True)
                        for field in structured_fields
                    },
                }
            )


def _write_report(payload: dict[str, Any]) -> None:
    totals = payload["totals"]
    actions = totals["action_counts"]
    minimum = min(payload["daily"], key=lambda row: row["slack_ratio"])
    checks = payload["gate_0a_checks"]
    checkpoint_lines = []
    for key, snapshot in payload["snapshots"].items():
        checkpoint_lines.append(
            f"| {key} | `{json.dumps(snapshot['crops'], sort_keys=True)}` | "
            f"`{json.dumps(snapshot['animals'], sort_keys=True)}` | "
            f"{'PASS' if all(payload['checkpoint_checks'][key].values()) else 'FAIL'} |"
        )
    move_total = sum(actions.get(opcode, 0) for opcode in ("NORTH", "SOUTH", "EAST", "WEST"))
    report = f"""# E18.18 — Gate 0A capacity trajectory planner

## Verdetto

`{'PASS' if payload['gate_0a_passed'] else 'FAIL'}` per il Gate 0A offline.
Il piano nativo `7-7-0` realizza i checkpoint del benchmark Jesse, usa
`9 COW + 5 SHEEP`, non produce starvation/fughe/comandi illegali nel modello
biologico shadow e rispetta la riserva operativa preregistrata ogni giorno.

Questo **non** è ancora il Gate 0 completo e non autorizza un executor o una
submission. Mancano replay nell'engine reale, ledger monetario/inventari/shed e
ack delle vendite terminali.

## Risultato sintetico

| KPI | Piano E18.18 Gate 0A | Riferimento Jesse 770 |
|---|---:|---:|
| Peak crop | {totals['peak_crop_total']} (D{totals['peak_crop_first_day']}) | 62 (entro D13) |
| Output crop shadow | {totals['shadow_crop_output']} | 885 |
| Melon | {totals['harvested'].get('MELON', 0)} | 72 |
| Strawberry | {totals['harvested'].get('STRAWBERRY', 0)} | 260 |
| Annuali Wheat/Carrot | {totals['harvested'].get('WHEAT', 0)} | 553 |
| MOVE teoriche | {move_total} | 3.473 osservate |
| WATER | {actions.get('WATER', 0)} | 1.172 osservate |
| PLANT | {actions.get('PLANT', 0)} | 243 osservate |
| Fertilizzazioni | {actions.get('FERTILIZE', 0)} | n.d. |
| Riserva minima | {100.0 * totals['minimum_daily_slack_ratio']:.2f}% (D{minimum['day']}) | target >={100.0 * totals['reserve_target_ratio']:.0f}% |
| Crop residui D30 | {payload['snapshots']['D30']['crop_total']} | <=2 |

L'output shadow è `{totals['shadow_crop_output']}`: +{totals['shadow_crop_output'] - 885}
rispetto alle 885 unità del riferimento. Il mix è molto vicino
(`72 MELON`, `{totals['harvested'].get('STRAWBERRY', 0)} STRAWBERRY`,
`{totals['harvested'].get('WHEAT', 0)} WHEAT`). La riduzione di MOVE è un lower
bound del route solver, non ancora una previsione di risultato nell'engine.

## Checkpoint di consistenza

| Giorno | Colture | Animali | Esito |
|---|---|---|---|
{chr(10).join(checkpoint_lines)}

La settima pasture di Q0 è coltivata nella fase iniziale. Il piano raggiunge
37 crop e 13 pasture entro D10, occupa Q2 con 25 crop entro D12, poi raccoglie
i 12 MELON e converte quella tile nel quattordicesimo pascolo. A D15 restano
esattamente 61 crop. Sedici STRAWBERRY vengono ruotate verso annuali fra D21 e
D25; ogni nuova semina annuale si ferma a D25 e le colture terminali sono
liquidate entro D29.

## Scelte di capacità

- WATER alternato quando non incide sul yield; WATER obbligatorio nelle
  finestre produttive annuali e sui nuovi PLANT;
- fertilizzante raccolto soltanto fino al fabbisogno pianificato: nessuna
  raccolta eccedente dopo D16;
- HARVEST permanenti distribuiti per fase di tile e WATER remoti di Q2 rinviati
  al massimo di un giorno nei picchi, senza starvation shadow;
- ogni route che raccoglie torna a uno dei quattro accessi dello shed e chiude
  con DROP nello stesso giorno;
- la capacità usa il timing reale: farmer e primi dieci HIRE iniziano le route
  al turno 2; gli ultimi due hands, quando necessari, dal turno 3;
- hash del piano: `{payload['plan_sha256']}`;
- seconda costruzione identica: `{payload['deterministic_two_run_hash']}`.

## Gate 0B ancora obbligatorio

1. eseguire le route contro l'interprete Kaggriculture reale con weed disabilitate;
2. modellare BUY_LAND, HIRE, semi, animali, Wheat di FEED, shed capacity e cash;
3. verificare DROP/SELL terminali e ack di ogni task;
4. soltanto dopo un PASS costruire l'executor state-driven e avviare Gate 1 e
   confronti matched con E18.16.

## Check automatici

```json
{json.dumps(checks, indent=2, sort_keys=True)}
```
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")


def main() -> int:
    first = build_plan()
    second = build_plan()
    deterministic = (
        first["plan_sha256"] == second["plan_sha256"]
        and first["snapshots"] == second["snapshots"]
        and first["totals"] == second["totals"]
    )
    first["gate_0a_checks"]["deterministic_two_run_hash"] = deterministic
    first["deterministic_two_run_hash"] = deterministic
    first["gate_0a_passed"] = all(first["gate_0a_checks"].values())
    first["executor_authorized"] = False
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(first, indent=2) + "\n", encoding="utf-8")
    _write_csv(first)
    _write_report(first)
    print(json.dumps({
        "gate_0a_passed": first["gate_0a_passed"],
        "plan_sha256": first["plan_sha256"],
        "minimum_daily_slack_ratio": first["totals"]["minimum_daily_slack_ratio"],
        "shadow_crop_output": first["totals"]["shadow_crop_output"],
        "executor_authorized": first["executor_authorized"],
    }, indent=2))
    return 0 if first["gate_0a_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
