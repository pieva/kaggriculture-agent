#!/usr/bin/env python3
"""Seat-balanced pre-gate for E18.24 against parent and incumbent."""

from __future__ import annotations

import json
import statistics
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "docs/model_specs/codex/e18/tools"
for import_root in (ROOT, TOOLS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    create_codex_e18_770_exact_cap_critical_feed,
)
from docs.model_specs.codex.e18.tools.e18_22_wheat_jit_d1_controller import (
    WheatJitD1Controller,
)
from docs.model_specs.codex.e18.tools.e18_24_deferred_plant_on_water_controller import (
    DeferredPlantOnWaterController,
)
from docs.model_specs.codex.e18.tools.run_e18_18_770_capacity_trajectory_gate_0b import (
    _snapshot,
)
from docs.model_specs.codex.e18.tools.run_e18_20_770_wheat_market_netting_gate import (
    _wheat_orders,
)

SEED = 180903001
EXPECTED_PLAN_SHA256 = (
    "844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1"
)
PLAN = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_V1.json"
)
OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_24_770_DEFERRED_PLANT_ON_WATER_PRE_GATE_V1.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_24_770_DEFERRED_PLANT_ON_WATER_PRE_GATE_REPORT_IT.md"
)


def _parent(plan: dict[str, Any], seat: int) -> WheatJitD1Controller:
    return WheatJitD1Controller(plan, seat=seat)


def _incumbent(plan: dict[str, Any], seat: int):
    del plan
    return create_codex_e18_770_exact_cap_critical_feed(
        run_context={
            "run_id": f"E18-24-PRE-GATE-S{SEED}-P{seat}-INCUMBENT",
            "episode_id": f"E18-24-PRE-GATE-S{SEED}-P{seat}-INCUMBENT",
            "seed": SEED,
            "player_position": seat,
        }
    )


def _run_match(
    plan: dict[str, Any],
    candidate_seat: int,
    opponent_name: str,
    opponent_factory: Callable[[dict[str, Any], int], Any],
) -> dict[str, Any]:
    candidate = DeferredPlantOnWaterController(plan, seat=candidate_seat)
    opponent_seat = 1 - candidate_seat
    opponent = opponent_factory(plan, opponent_seat)
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
    replay = env.toJSON()
    rewards = [float(value or 0.0) for value in replay.get("rewards", [0, 0])]
    candidate_reward = rewards[candidate_seat]
    opponent_reward = rewards[opponent_seat]
    return {
        "opponent": opponent_name,
        "candidate_seat": candidate_seat,
        "candidate_reward": candidate_reward,
        "opponent_reward": opponent_reward,
        "margin": candidate_reward - opponent_reward,
        "candidate_final": _snapshot(replay, 30, candidate_seat),
        "opponent_final": _snapshot(replay, 30, opponent_seat),
        "candidate_wheat_orders": _wheat_orders(replay, candidate_seat),
        "opponent_wheat_orders": _wheat_orders(replay, opponent_seat),
        "deferred_plant_target_count": len(candidate.deferred_plant_targets),
        "resolved_plant_count": len(candidate.resolved_plant_targets),
        "recovered_plant_count": len(candidate.recovered_plant_targets),
        "deferred_plant_metrics": dict(
            sorted(candidate.deferred_plant_metrics.items())
        ),
        "recovered_by_day": dict(sorted(candidate.recovered_by_day.items())),
        "skipped_stale": dict(sorted(candidate.skipped_stale.items())),
        "recovery_actions": dict(sorted(candidate.recovery_actions.items())),
        "requested_actions": dict(sorted(candidate.requested_actions.items())),
        "unfinished_actions": sum(candidate.unfinished_by_day.values()),
        "candidate_errors": candidate.error_count,
        "opponent_errors": int(getattr(opponent, "error_count", 0)),
    }


def _comparison(matches: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = float(
        statistics.median(match["candidate_reward"] for match in matches)
    )
    opponent = float(
        statistics.median(match["opponent_reward"] for match in matches)
    )
    return {
        "candidate_median": candidate,
        "opponent_median": opponent,
        "median_margin": candidate - opponent,
        "matches": matches,
    }


def run() -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan.get("plan_sha256") != EXPECTED_PLAN_SHA256:
        raise ValueError("frozen E18.18 plan hash mismatch")
    parent = _comparison(
        [_run_match(plan, seat, "E18.22", _parent) for seat in (0, 1)]
    )
    incumbent = _comparison(
        [_run_match(plan, seat, "E18.16", _incumbent) for seat in (0, 1)]
    )
    all_matches = [*parent["matches"], *incumbent["matches"]]
    checks = {
        "zero_errors": all(
            match["candidate_errors"] == match["opponent_errors"] == 0
            for match in all_matches
        ),
        "candidate_exact_770": all(
            match["candidate_final"]["topology"] == {"Q0": 7, "Q1": 7}
            for match in all_matches
        ),
        "candidate_exact_9_cow_5_sheep": all(
            match["candidate_final"]["animals"] == {"COW": 9, "SHEEP": 5}
            for match in all_matches
        ),
        "all_d11_locked_plants_recovered": all(
            match["deferred_plant_target_count"] == 11
            and match["recovered_plant_count"] == 11
            for match in all_matches
        ),
        "harvest_skips_below_parent_baseline": all(
            match["skipped_stale"].get("HARVEST", 0) < 40
            for match in incumbent["matches"]
        ),
        "parent_delta_nonnegative_both_seats": all(
            match["margin"] >= 0 for match in parent["matches"]
        ),
        "incumbent_gate_nonnegative_both_seats": all(
            match["margin"] >= 0 for match in incumbent["matches"]
        ),
    }
    causal_delta_passed = all(
        checks[key]
        for key in (
            "zero_errors",
            "candidate_exact_770",
            "candidate_exact_9_cow_5_sheep",
            "all_d11_locked_plants_recovered",
            "harvest_skips_below_parent_baseline",
            "parent_delta_nonnegative_both_seats",
        )
    )
    return {
        "schema_version": "e18.codex.770_deferred_plant_on_water_pre_gate.v1",
        "candidate": "CODEX_E18_24_770_DEFERRED_PLANT_ON_WATER_V1",
        "parent": "CODEX_E18_22_770_WHEAT_JIT_D1_V1",
        "incumbent": "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1",
        "seed": SEED,
        "seats": [0, 1],
        "epistemic_role": "DEVELOPMENT_PRE_GATE_ABLATION",
        "plan_sha256": EXPECTED_PLAN_SHA256,
        "parent_comparison": parent,
        "incumbent_comparison": incumbent,
        "causal_delta_passed": causal_delta_passed,
        "incumbent_gate_passed": checks[
            "incumbent_gate_nonnegative_both_seats"
        ],
        "checks": checks,
        "full_gate_1_authorized": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }


def _rows(matches: list[dict[str, Any]]) -> str:
    return "\n".join(
        "| {candidate_seat} | {candidate_reward:.0f} | {opponent_reward:.0f} | "
        "{margin:+.0f} | {recovered_plant_count} | {harvest} | {plant} |".format(
            **match,
            harvest=match["skipped_stale"].get("HARVEST", 0),
            plant=match["skipped_stale"].get("PLANT", 0),
        )
        for match in matches
    )


def _write_report(payload: dict[str, Any]) -> None:
    parent = payload["parent_comparison"]
    incumbent = payload["incumbent_comparison"]
    report = f"""# E18.24 — Deferred PLANT on WATER pre-gate

## Verdetto

Delta causale E18.22:
`{'PASS' if payload['causal_delta_passed'] else 'FAIL'}`.
Gate incumbent E18.16:
`{'PASS' if payload['incumbent_gate_passed'] else 'FAIL'}`.

## Contro E18.22

| Seat E18.24 | E18.24 | E18.22 | Margine | PLANT recuperati | HARVEST skip | PLANT skip storico |
|---:|---:|---:|---:|---:|---:|---:|
{_rows(parent['matches'])}

Mediana `{parent['candidate_median']:.1f}` contro
`{parent['opponent_median']:.1f}`, delta `{parent['median_margin']:+.1f}`.

## Contro E18.16

| Seat E18.24 | E18.24 | E18.16 | Margine | PLANT recuperati | HARVEST skip | PLANT skip storico |
|---:|---:|---:|---:|---:|---:|---:|
{_rows(incumbent['matches'])}

Mediana `{incumbent['candidate_median']:.1f}` contro
`{incumbent['opponent_median']:.1f}`, delta
`{incumbent['median_margin']:+.1f}`.

## Check

```json
{json.dumps(payload['checks'], indent=2, sort_keys=True)}
```
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")


def main() -> int:
    payload = run()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_report(payload)
    print(json.dumps(payload, indent=2))
    return 0 if payload["causal_delta_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
