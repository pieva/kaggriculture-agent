#!/usr/bin/env python3
"""Seat-balanced pre-gate for E18.20 against parent and incumbent."""

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
from docs.model_specs.codex.e18.tools.e18_19_retrying_trajectory_controller import (
    RetryingTrajectoryController,
)
from docs.model_specs.codex.e18.tools.e18_20_wheat_market_netting_controller import (
    WheatMarketNettingController,
)
from docs.model_specs.codex.e18.tools.run_e18_18_770_capacity_trajectory_gate_0b import (
    _snapshot,
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
    / "E18_20_770_WHEAT_MARKET_NETTING_PRE_GATE_V1.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_20_770_WHEAT_MARKET_NETTING_PRE_GATE_REPORT_IT.md"
)

def _wheat_orders(replay: dict[str, Any], seat: int) -> dict[str, int]:
    sold = 0
    bought = 0
    overlapping = 0
    overlapping_turns = 0
    overlapping_from_activation = 0
    overlapping_turns_from_activation = 0
    for records in replay["steps"]:
        record = records[seat]
        orders = (record.get("action") or {}).get("market", []) or []
        turn_sold = sum(
            int(order[2])
            for order in orders
            if order[:2] == ["SELL", "WHEAT"]
        )
        turn_bought = sum(
            int(order[2])
            for order in orders
            if order[:2] == ["BUY_PRODUCT", "WHEAT"]
        )
        sold += turn_sold
        bought += turn_bought
        overlapping += min(turn_sold, turn_bought)
        overlapping_turns += int(turn_sold > 0 and turn_bought > 0)
        day = int(record["observation"].get("day", 0)) + 1
        if day >= WheatMarketNettingController.activation_day:
            overlapping_from_activation += min(turn_sold, turn_bought)
            overlapping_turns_from_activation += int(
                turn_sold > 0 and turn_bought > 0
            )
    return {
        "sell_requested_units": sold,
        "buy_requested_units": bought,
        "same_batch_overlap_units": overlapping,
        "same_batch_overlap_turns": overlapping_turns,
        "same_batch_overlap_units_from_activation": overlapping_from_activation,
        "same_batch_overlap_turns_from_activation": (
            overlapping_turns_from_activation
        ),
    }


def _parent(plan: dict[str, Any], seat: int) -> RetryingTrajectoryController:
    return RetryingTrajectoryController(plan, seat=seat)


def _incumbent(plan: dict[str, Any], seat: int):
    del plan
    return create_codex_e18_770_exact_cap_critical_feed(
        run_context={
            "run_id": f"E18-20-PRE-GATE-S{SEED}-P{seat}-INCUMBENT",
            "episode_id": f"E18-20-PRE-GATE-S{SEED}-P{seat}-INCUMBENT",
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
    candidate = WheatMarketNettingController(plan, seat=candidate_seat)
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
        "market_adjustments": dict(
            sorted(candidate.wheat_market_adjustments.items())
        ),
        "skipped_stale": dict(sorted(candidate.skipped_stale.items())),
        "unfinished_actions": sum(candidate.unfinished_by_day.values()),
        "candidate_errors": candidate.error_count,
        "opponent_errors": int(getattr(opponent, "error_count", 0)),
    }


def _median(matches: list[dict[str, Any]], field: str) -> float:
    return float(statistics.median(match[field] for match in matches))


def run() -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan.get("plan_sha256") != EXPECTED_PLAN_SHA256:
        raise ValueError("frozen E18.18 plan hash mismatch")
    parent_matches = [
        _run_match(plan, seat, "E18.19", _parent) for seat in (0, 1)
    ]
    incumbent_matches = [
        _run_match(plan, seat, "E18.16", _incumbent) for seat in (0, 1)
    ]
    all_matches = [*parent_matches, *incumbent_matches]
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
        "zero_candidate_same_batch_wheat_overlap": all(
            match["candidate_wheat_orders"][
                "same_batch_overlap_units_from_activation"
            ]
            == 0
            for match in all_matches
        ),
        "parent_delta_nonnegative_both_seats": all(
            match["margin"] >= 0 for match in parent_matches
        ),
        "incumbent_gate_nonnegative_both_seats": all(
            match["margin"] >= 0 for match in incumbent_matches
        ),
    }
    parent_candidate_median = _median(parent_matches, "candidate_reward")
    parent_opponent_median = _median(parent_matches, "opponent_reward")
    incumbent_candidate_median = _median(incumbent_matches, "candidate_reward")
    incumbent_opponent_median = _median(incumbent_matches, "opponent_reward")
    return {
        "schema_version": "e18.codex.770_wheat_market_netting_pre_gate.v1",
        "candidate": "CODEX_E18_20_770_WHEAT_MARKET_NETTING_V1",
        "parent": "CODEX_E18_19_770_RETRYING_TRAJECTORY_V1",
        "incumbent": "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1",
        "seed": SEED,
        "seats": [0, 1],
        "epistemic_role": "DEVELOPMENT_PRE_GATE_ABLATION",
        "plan_sha256": EXPECTED_PLAN_SHA256,
        "causal_delta_passed": all(
            checks[key]
            for key in (
                "zero_errors",
                "candidate_exact_770",
                "candidate_exact_9_cow_5_sheep",
                "zero_candidate_same_batch_wheat_overlap",
                "parent_delta_nonnegative_both_seats",
            )
        ),
        "incumbent_gate_passed": checks[
            "incumbent_gate_nonnegative_both_seats"
        ],
        "checks": checks,
        "parent_comparison": {
            "candidate_median": parent_candidate_median,
            "opponent_median": parent_opponent_median,
            "median_margin": parent_candidate_median - parent_opponent_median,
            "matches": parent_matches,
        },
        "incumbent_comparison": {
            "candidate_median": incumbent_candidate_median,
            "opponent_median": incumbent_opponent_median,
            "median_margin": incumbent_candidate_median - incumbent_opponent_median,
            "matches": incumbent_matches,
        },
        "full_gate_1_authorized": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }


def _table(matches: list[dict[str, Any]]) -> str:
    return "\n".join(
        "| {candidate_seat} | {candidate_reward:.0f} | {opponent_reward:.0f} | "
        "{margin:+.0f} | {sell} | {buy} | {overlap} |".format(
            **match,
            sell=match["candidate_wheat_orders"]["sell_requested_units"],
            buy=match["candidate_wheat_orders"]["buy_requested_units"],
            overlap=match["candidate_wheat_orders"]["same_batch_overlap_units"],
        )
        for match in matches
    )


def _write_report(payload: dict[str, Any]) -> None:
    parent = payload["parent_comparison"]
    incumbent = payload["incumbent_comparison"]
    report = f"""# E18.20 — Wheat market netting pre-gate

## Verdetto

Delta causale E18.19:
`{'PASS' if payload['causal_delta_passed'] else 'FAIL'}`.
Gate incumbent E18.16:
`{'PASS' if payload['incumbent_gate_passed'] else 'FAIL'}`.

## Contro E18.19

| Seat E18.20 | E18.20 | E18.19 | Margine | SELL W | BUY W | Overlap |
|---:|---:|---:|---:|---:|---:|---:|
{_table(parent['matches'])}

Mediana `{parent['candidate_median']:.1f}` contro
`{parent['opponent_median']:.1f}`, delta `{parent['median_margin']:+.1f}`.

## Contro E18.16

| Seat E18.20 | E18.20 | E18.16 | Margine | SELL W | BUY W | Overlap |
|---:|---:|---:|---:|---:|---:|---:|
{_table(incumbent['matches'])}

Mediana `{incumbent['candidate_median']:.1f}` contro
`{incumbent['opponent_median']:.1f}`, delta
`{incumbent['median_margin']:+.1f}`.

Il netting rimuove soltanto le quantità Wheat comprate e vendute nello stesso
batch. La variante che allineava anche la riserva SELL all'orizzonte D+2 è
stata respinta nel pre-gate perché riduceva il churn ma peggiorava il money.

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
