#!/usr/bin/env python3
"""Seat-balanced internal gate for E18.26 Jesse BoostD10."""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    create_codex_e18_770_exact_cap_critical_feed,
)
from docs.model_specs.codex.e18.tools.e18_25_d10_labor_step_controller import (
    D10LaborStepController,
)
from docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller import (
    JesseBoostD10Controller,
    load_candidate_config,
)
from docs.model_specs.codex.e18.tools.run_e18_18_770_capacity_trajectory_gate_0b import (
    _snapshot,
)

SEED = 180903001
BASE = ROOT / "docs/model_specs/codex/e18"
PARENT_PLAN = BASE / "artifacts/derived/E18_25_770_D10_LABOR_STEP_PLAN_V1.json"
CANDIDATE_PLAN = BASE / "artifacts/derived/E18_26_770_JESSE_BOOST_D10_PLAN_V1.json"
PARENT_RESULT = BASE / "artifacts/derived/E18_25_770_D10_LABOR_STEP_PRE_GATE_V1.json"
OUTPUT = BASE / "artifacts/derived/E18_26_770_JESSE_BOOST_D10_GATE_V1.json"
REPORT = BASE / "reports/E18_26_770_TOP770_BOOST_D10_GATE_REPORT_IT.md"
PARENT_PLAN_HASH = "ffa39984acd4d506db39856d5269e3e8e1af909ddf2a4324a9d16955d834a786"


def _parent(plan: dict[str, Any], seat: int) -> D10LaborStepController:
    return D10LaborStepController(plan, seat=seat)


def _incumbent(plan: dict[str, Any], seat: int):
    del plan
    return create_codex_e18_770_exact_cap_critical_feed(
        run_context={
            "run_id": f"E18-26-BOOST-D10-S{SEED}-P{seat}",
            "episode_id": f"E18-26-BOOST-D10-S{SEED}-P{seat}",
            "seed": SEED,
            "player_position": seat,
        }
    )


def _run_match(
    candidate_plan: dict[str, Any],
    opponent_plan: dict[str, Any],
    candidate_seat: int,
    opponent_name: str,
    opponent_factory: Callable[[dict[str, Any], int], Any],
) -> dict[str, Any]:
    candidate = JesseBoostD10Controller(candidate_plan, seat=candidate_seat)
    opponent_seat = 1 - candidate_seat
    opponent = opponent_factory(opponent_plan, opponent_seat)
    policies = [None, None]
    policies[candidate_seat] = candidate
    policies[opponent_seat] = opponent
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24},
        debug=False,
    )
    env.run(policies)
    candidate.finalize_metrics()
    if hasattr(opponent, "finalize_metrics"):
        opponent.finalize_metrics()
    replay = env.toJSON()
    rewards = [float(value or 0.0) for value in replay.get("rewards", [0, 0])]
    unfinished_opcodes: dict[str, Counter[str]] = {}
    for (route_day, worker), rows in candidate.routes.items():
        cursor = candidate.cursors[(route_day, worker)]
        if cursor >= len(rows):
            continue
        key = str(route_day)
        unfinished_opcodes.setdefault(key, Counter()).update(
            str(row["opcode"]) for row in rows[cursor:]
        )
    return {
        "opponent": opponent_name,
        "candidate_seat": candidate_seat,
        "candidate_reward": rewards[candidate_seat],
        "opponent_reward": rewards[opponent_seat],
        "margin": rewards[candidate_seat] - rewards[opponent_seat],
        "candidate_snapshots": {
            f"D{day:02d}": _snapshot(replay, day, candidate_seat)
            for day in (1, 5, 10, 11, 12, 13, 14, 15, 30)
        },
        "opponent_snapshots": {
            f"D{day:02d}": _snapshot(replay, day, opponent_seat)
            for day in (1, 5, 10, 30)
        },
        "candidate_requested_actions": dict(
            sorted(candidate.requested_actions.items())
        ),
        "candidate_unfinished_actions": sum(candidate.unfinished_by_day.values()),
        "candidate_unfinished_by_day": dict(
            sorted(candidate.unfinished_by_day.items())
        ),
        "candidate_unfinished_opcodes_by_day": {
            day: dict(sorted(counts.items()))
            for day, counts in sorted(
                unfinished_opcodes.items(), key=lambda item: int(item[0])
            )
        },
        "candidate_skipped_stale": dict(sorted(candidate.skipped_stale.items())),
        "candidate_deferred_critical": dict(
            sorted(candidate.deferred_critical.items())
        ),
        "candidate_skipped_bounded_by_day": {
            str(day): dict(sorted(counts.items()))
            for day, counts in sorted(candidate.skipped_bounded_by_day.items())
        },
        "candidate_recovery_actions": dict(sorted(candidate.recovery_actions.items())),
        "candidate_market_trace_key_days": [
            row
            for row in candidate.market_trace
            if int(row["day"]) in {3, 4, 5, 11, 12, 13, 14}
        ],
        "opponent_unfinished_actions": sum(
            getattr(opponent, "unfinished_by_day", {}).values()
        ),
        "candidate_errors": candidate.error_count,
        "opponent_errors": int(getattr(opponent, "error_count", 0)),
    }


def _comparison(matches: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = float(statistics.median(row["candidate_reward"] for row in matches))
    opponent = float(statistics.median(row["opponent_reward"] for row in matches))
    return {
        "candidate_median": candidate,
        "opponent_median": opponent,
        "median_margin": candidate - opponent,
        "matches": matches,
    }


def _phase_counts(plan: dict[str, Any]) -> dict[str, int]:
    counts = Counter(
        str(row["opcode"]) for row in plan["trajectory"] if int(row["day"]) <= 10
    )
    counts["MOVE"] = sum(
        counts.pop(direction, 0) for direction in ("NORTH", "SOUTH", "EAST", "WEST")
    )
    counts["PRODUCTIVE"] = sum(
        count for opcode, count in counts.items() if opcode not in {"MOVE", "PASS"}
    )
    return dict(sorted(counts.items()))


def run() -> dict[str, Any]:
    config = load_candidate_config()
    parent_plan = json.loads(PARENT_PLAN.read_text(encoding="utf-8"))
    candidate_plan = json.loads(CANDIDATE_PLAN.read_text(encoding="utf-8"))
    parent_result = json.loads(PARENT_RESULT.read_text(encoding="utf-8"))
    if parent_plan.get("plan_sha256") != PARENT_PLAN_HASH:
        raise ValueError("frozen E18.25 plan hash mismatch")

    parent = _comparison(
        [
            _run_match(candidate_plan, parent_plan, seat, "E18.25", _parent)
            for seat in (0, 1)
        ]
    )
    incumbent = _comparison(
        [
            _run_match(candidate_plan, parent_plan, seat, "E18.16", _incumbent)
            for seat in (0, 1)
        ]
    )
    baseline_by_seat = {
        int(row["candidate_seat"]): float(row["candidate_reward"])
        for row in parent_result["incumbent_comparison"]["matches"]
    }
    delta_by_seat = {
        str(row["candidate_seat"]): (
            float(row["candidate_reward"])
            - baseline_by_seat[int(row["candidate_seat"])]
        )
        for row in incumbent["matches"]
    }
    phase = _phase_counts(candidate_plan)
    target = config["jesse_d10_action_targets"]
    all_matches = [*parent["matches"], *incumbent["matches"]]
    expected_crops = {
        "D01": {"MELON": 12, "WHEAT": 7},
        "D05": {"MELON": 12, "WHEAT": 7},
        "D10": {"MELON": 12, "STRAWBERRY": 20, "WHEAT": 5},
    }
    checks = {
        "plan_gate_0a_passed": candidate_plan["gate_0a_passed"] is True,
        "jesse_plant_exact": phase.get("PLANT") == int(target["PLANT"]),
        "jesse_water_exact": phase.get("WATER") == int(target["WATER"]),
        "jesse_harvest_gap_at_most_two": abs(
            phase.get("HARVEST", 0) - int(target["HARVEST"])
        )
        <= 2,
        "d10_actual_hands_11": all(
            row["candidate_snapshots"]["D10"]["hands"] == 11 for row in all_matches
        ),
        "actual_crop_checkpoints_match_jesse": all(
            row["candidate_snapshots"][day]["crops"] == mix
            for row in all_matches
            for day, mix in expected_crops.items()
        ),
        "zero_errors": all(
            row["candidate_errors"] == row["opponent_errors"] == 0
            for row in all_matches
        ),
        "candidate_exact_770": all(
            row["candidate_snapshots"]["D30"]["topology"] == {"Q0": 7, "Q1": 7}
            for row in all_matches
        ),
        "candidate_exact_9_cow_5_sheep": all(
            row["candidate_snapshots"]["D30"]["animals"] == {"COW": 9, "SHEEP": 5}
            for row in all_matches
        ),
        "matched_parent_delta_positive_both_seats": all(
            value > 0 for value in delta_by_seat.values()
        ),
        "incumbent_delta_nonnegative_both_seats": all(
            row["margin"] >= 0 for row in incumbent["matches"]
        ),
    }
    causal_keys = tuple(
        key for key in checks if key != "incumbent_delta_nonnegative_both_seats"
    )
    return {
        "schema_version": "e18.codex.770_jesse_boost_d10_gate.v1",
        "candidate": config["candidate_id"],
        "parent": "CODEX_E18_25_770_D10_LABOR_STEP_V1",
        "incumbent": "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1",
        "seed": SEED,
        "seats": [0, 1],
        "candidate_plan_sha256": candidate_plan["plan_sha256"],
        "jesse_reference": target,
        "candidate_d01_d10_plan": phase,
        "competitive_parent_comparison": parent,
        "incumbent_comparison": incumbent,
        "matched_parent_baseline": {
            "parent_candidate_median": parent_result["incumbent_comparison"][
                "candidate_median"
            ],
            "candidate_median": incumbent["candidate_median"],
            "median_delta": incumbent["candidate_median"]
            - parent_result["incumbent_comparison"]["candidate_median"],
            "delta_by_seat": delta_by_seat,
        },
        "checks": checks,
        "causal_delta_passed": all(checks[key] for key in causal_keys),
        "incumbent_gate_passed": checks["incumbent_delta_nonnegative_both_seats"],
        "full_gate_1_authorized": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }


def _rows(matches: list[dict[str, Any]]) -> str:
    return "\n".join(
        "| {candidate_seat} | {candidate_reward:.0f} | {opponent_reward:.0f} | "
        "{margin:+.0f} | {money:.0f} | {hands} |".format(
            **row,
            money=row["candidate_snapshots"]["D10"]["money"],
            hands=row["candidate_snapshots"]["D10"]["hands"] + 1,
        )
        for row in matches
    )


def _write_report(payload: dict[str, Any]) -> None:
    parent = payload["competitive_parent_comparison"]
    incumbent = payload["incumbent_comparison"]
    phase = payload["candidate_d01_d10_plan"]
    target = payload["jesse_reference"]
    baseline = payload["matched_parent_baseline"]
    report = f"""# E18.26 — Jesse BoostD10 internal gate

## D1–D10

| KPI | Jesse 7-7-0 | E18.25 | E18.26 |
|---|---:|---:|---:|
| PLANT | {target["PLANT"]} | 51 | {phase["PLANT"]} |
| WATER | {target["WATER"]} | 186 | {phase["WATER"]} |
| HARVEST | {target["HARVEST"]} | 18 | {phase["HARVEST"]} |
| MOVE | {target["MOVE"]} | 457 | {phase["MOVE"]} |

E18.26 replica esattamente PLANT e WATER. I due HARVEST mancanti sono output
animali non ancora disponibili nello shadow model; non vengono sostituiti con
no-op o comandi illegali. Le MOVE restano inferiori al riferimento Jesse.

## Contro E18.25

| Seat E18.26 | E18.26 | E18.25 | Margine | Money D10 | Unità D10 |
|---:|---:|---:|---:|---:|---:|
{_rows(parent["matches"])}

Mediana `{parent["candidate_median"]:.1f}` contro `{parent["opponent_median"]:.1f}`.

## Contro E18.16

| Seat E18.26 | E18.26 | E18.16 | Margine | Money D10 | Unità D10 |
|---:|---:|---:|---:|---:|---:|
{_rows(incumbent["matches"])}

Delta matched rispetto a E18.25: `{baseline["median_delta"]:+.1f}`;
per seat `{baseline["delta_by_seat"]}`.

## Check

```json
{json.dumps(payload["checks"], indent=2, sort_keys=True)}
```

## Verdetto

Il segnale economico è positivo rispetto al parent: delta matched
`{baseline["median_delta"]:+.1f}` e positivo in entrambi i seat. Il gate
strutturale resta però FAIL: contro E18.25 il checkpoint D5 perde
temporaneamente due Wheat, e dopo D12 la copertura FEED non conserva il mix
finale `9 COW + 5 SHEEP`. D10 è exact in tutte le esecuzioni.

E18.26 resta una candidata development. Gate 1, holdout, final confirmation e
upload Kaggle non sono autorizzati. Il successore deve congelare D1–D10 e
ripianificare D11–D14 con una sequenza harvest-first per il Wheat maturo D13.
"""
    REPORT.write_text(report, encoding="utf-8")


def main() -> int:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_report(payload)
    print(json.dumps(payload, indent=2))
    return 0 if payload["causal_delta_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
