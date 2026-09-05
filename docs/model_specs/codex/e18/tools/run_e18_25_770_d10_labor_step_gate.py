#!/usr/bin/env python3
"""Seat-balanced pre-gate for the E18.25 D10 labor step."""

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
from docs.model_specs.codex.e18.tools.e18_25_d10_labor_step_controller import (
    D10LaborStepController,
    build_candidate_plan,
)
from docs.model_specs.codex.e18.tools.run_e18_18_770_capacity_trajectory_gate_0b import (
    _snapshot,
)

SEED = 180903001
PARENT_PLAN_HASH = "844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1"
PARENT_PLAN = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_V1.json"
)
PARENT_RESULT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_22_770_WHEAT_JIT_D1_PRE_GATE_V1.json"
)
CANDIDATE_PLAN = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_25_770_D10_LABOR_STEP_PLAN_V1.json"
)
OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_25_770_D10_LABOR_STEP_PRE_GATE_V1.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_25_770_D10_LABOR_STEP_PRE_GATE_REPORT_IT.md"
)


def _parent(plan: dict[str, Any], seat: int) -> WheatJitD1Controller:
    return WheatJitD1Controller(plan, seat=seat)


def _incumbent(plan: dict[str, Any], seat: int):
    del plan
    return create_codex_e18_770_exact_cap_critical_feed(
        run_context={
            "run_id": f"E18-25-PRE-GATE-S{SEED}-P{seat}-INCUMBENT",
            "episode_id": f"E18-25-PRE-GATE-S{SEED}-P{seat}-INCUMBENT",
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
    candidate = D10LaborStepController(candidate_plan, seat=candidate_seat)
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
    return {
        "opponent": opponent_name,
        "candidate_seat": candidate_seat,
        "candidate_reward": rewards[candidate_seat],
        "opponent_reward": rewards[opponent_seat],
        "margin": rewards[candidate_seat] - rewards[opponent_seat],
        "candidate_d10": _snapshot(replay, 10, candidate_seat),
        "opponent_d10": _snapshot(replay, 10, opponent_seat),
        "candidate_final": _snapshot(replay, 30, candidate_seat),
        "opponent_final": _snapshot(replay, 30, opponent_seat),
        "candidate_requested_actions": dict(
            sorted(candidate.requested_actions.items())
        ),
        "candidate_unfinished_actions": sum(candidate.unfinished_by_day.values()),
        "opponent_unfinished_actions": sum(
            getattr(opponent, "unfinished_by_day", {}).values()
        ),
        "candidate_errors": candidate.error_count,
        "opponent_errors": int(getattr(opponent, "error_count", 0)),
    }


def _comparison(matches: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = float(statistics.median(m["candidate_reward"] for m in matches))
    opponent = float(statistics.median(m["opponent_reward"] for m in matches))
    return {
        "candidate_median": candidate,
        "opponent_median": opponent,
        "median_margin": candidate - opponent,
        "matches": matches,
    }


def _productive_counts(daily: dict[str, Any]) -> dict[str, int]:
    excluded = {"NORTH", "SOUTH", "EAST", "WEST", "PASS"}
    return {
        opcode: int(count)
        for opcode, count in daily["action_counts"].items()
        if opcode not in excluded
    }


def _candidate_plan() -> dict[str, Any]:
    if CANDIDATE_PLAN.exists():
        plan = json.loads(CANDIDATE_PLAN.read_text(encoding="utf-8"))
        if (
            plan.get("candidate_id") == "CODEX_E18_25_770_D10_LABOR_STEP_V1"
            and plan["daily"][9]["planned_hands"] == 11
        ):
            return plan
    plan = build_candidate_plan()
    CANDIDATE_PLAN.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE_PLAN.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    return plan


def run() -> dict[str, Any]:
    parent_plan = json.loads(PARENT_PLAN.read_text(encoding="utf-8"))
    if parent_plan.get("plan_sha256") != PARENT_PLAN_HASH:
        raise ValueError("frozen E18.18 plan hash mismatch")
    candidate_plan = _candidate_plan()
    parent_result = json.loads(PARENT_RESULT.read_text(encoding="utf-8"))
    parent_d10 = parent_plan["daily"][9]
    candidate_d10 = candidate_plan["daily"][9]
    parent = _comparison(
        [
            _run_match(candidate_plan, parent_plan, seat, "E18.22", _parent)
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
        int(match["candidate_seat"]): float(match["candidate_reward"])
        for match in parent_result["incumbent_comparison"]["matches"]
    }
    matched_parent_delta_by_seat = {
        str(match["candidate_seat"]): (
            float(match["candidate_reward"])
            - baseline_by_seat[int(match["candidate_seat"])]
        )
        for match in incumbent["matches"]
    }
    all_matches = [*parent["matches"], *incumbent["matches"]]
    checks = {
        "zero_errors": all(
            m["candidate_errors"] == m["opponent_errors"] == 0 for m in all_matches
        ),
        "plan_gate_0a_passed": candidate_plan["gate_0a_passed"] is True,
        "d10_planned_active_units_12": candidate_d10["active_units"] == 12,
        "d10_actual_hands_11": all(
            m["candidate_d10"]["hands"] == 11 for m in all_matches
        ),
        "d10_productive_action_multiset_unchanged": (
            _productive_counts(candidate_d10) == _productive_counts(parent_d10)
        ),
        "biological_plan_unchanged": (
            candidate_plan["snapshots"] == parent_plan["snapshots"]
        ),
        "candidate_exact_770": all(
            m["candidate_final"]["topology"] == {"Q0": 7, "Q1": 7} for m in all_matches
        ),
        "candidate_exact_9_cow_5_sheep": all(
            m["candidate_final"]["animals"] == {"COW": 9, "SHEEP": 5}
            for m in all_matches
        ),
        "matched_parent_delta_positive_both_seats": all(
            delta > 0 for delta in matched_parent_delta_by_seat.values()
        ),
        "incumbent_delta_nonnegative_both_seats": all(
            m["margin"] >= 0 for m in incumbent["matches"]
        ),
    }
    causal_keys = (
        "zero_errors",
        "plan_gate_0a_passed",
        "d10_planned_active_units_12",
        "d10_actual_hands_11",
        "d10_productive_action_multiset_unchanged",
        "biological_plan_unchanged",
        "candidate_exact_770",
        "candidate_exact_9_cow_5_sheep",
        "matched_parent_delta_positive_both_seats",
    )
    return {
        "schema_version": "e18.codex.770_d10_labor_step_pre_gate.v1",
        "candidate": "CODEX_E18_25_770_D10_LABOR_STEP_V1",
        "parent": "CODEX_E18_22_770_WHEAT_JIT_D1_V1",
        "incumbent": "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1",
        "seed": SEED,
        "seats": [0, 1],
        "epistemic_role": "DEVELOPMENT_PRE_GATE_ABLATION",
        "parent_plan_sha256": PARENT_PLAN_HASH,
        "candidate_plan_sha256": candidate_plan["plan_sha256"],
        "d10_plan": {
            "parent_planned_hands": parent_d10["planned_hands"],
            "candidate_planned_hands": candidate_d10["planned_hands"],
            "parent_active_units": parent_d10["active_units"],
            "candidate_active_units": candidate_d10["active_units"],
            "parent_available_action_slots": parent_d10["available_action_slots"],
            "candidate_available_action_slots": candidate_d10["available_action_slots"],
            "planned_action_slots": candidate_d10["planned_action_slots"],
            "action_counts": candidate_d10["action_counts"],
        },
        "competitive_parent_comparison": parent,
        "matched_parent_baseline": {
            "source": str(PARENT_RESULT.relative_to(ROOT)),
            "parent_candidate_median": parent_result["incumbent_comparison"][
                "candidate_median"
            ],
            "candidate_median": incumbent["candidate_median"],
            "median_delta": (
                incumbent["candidate_median"]
                - parent_result["incumbent_comparison"]["candidate_median"]
            ),
            "delta_by_seat": matched_parent_delta_by_seat,
        },
        "incumbent_comparison": incumbent,
        "causal_delta_passed": all(checks[key] for key in causal_keys),
        "incumbent_gate_passed": checks["incumbent_delta_nonnegative_both_seats"],
        "checks": checks,
        "full_gate_1_authorized": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }


def _rows(matches: list[dict[str, Any]]) -> str:
    return "\n".join(
        "| {candidate_seat} | {candidate_reward:.0f} | {opponent_reward:.0f} | "
        "{margin:+.0f} | {candidate_hands} | {opponent_hands} | "
        "{candidate_money:.0f} | {opponent_money:.0f} |".format(
            **match,
            candidate_hands=match["candidate_d10"]["hands"] + 1,
            opponent_hands=match["opponent_d10"]["hands"] + 1,
            candidate_money=match["candidate_d10"]["money"],
            opponent_money=match["opponent_d10"]["money"],
        )
        for match in matches
    )


def _write_report(payload: dict[str, Any]) -> None:
    parent = payload["competitive_parent_comparison"]
    baseline = payload["matched_parent_baseline"]
    incumbent = payload["incumbent_comparison"]
    verdict = "PASS" if payload["causal_delta_passed"] else "FAIL"
    report = f"""# E18.25 — D10 labor step pre-gate

## Verdetto

Delta causale matched contro E18.22: `{verdict}`. Il trattamento porta D10 da
`{payload["d10_plan"]["parent_active_units"]}` a
`{payload["d10_plan"]["candidate_active_units"]}` unità attive, senza cambiare
il multiset di azioni agricole pianificate.

Sul medesimo seed, seat e avversario E18.16, la mediana passa da
`{baseline["parent_candidate_median"]:.1f}` a
`{baseline["candidate_median"]:.1f}`: delta `{baseline["median_delta"]:+.1f}`;
delta per seat `{baseline["delta_by_seat"]}`.

## Stress competitivo diretto contro E18.22

| Seat E18.25 | E18.25 | E18.22 | Margine | Unità D10 E18.25 | Unità D10 opp. | Denaro D10 E18.25 | Denaro D10 opp. |
|---:|---:|---:|---:|---:|---:|---:|---:|
{_rows(parent["matches"])}

Mediana `{parent["candidate_median"]:.1f}` contro
`{parent["opponent_median"]:.1f}`, delta `{parent["median_margin"]:+.1f}`.

## Contro E18.16

| Seat E18.25 | E18.25 | E18.16 | Margine | Unità D10 E18.25 | Unità D10 opp. | Denaro D10 E18.25 | Denaro D10 opp. |
|---:|---:|---:|---:|---:|---:|---:|---:|
{_rows(incumbent["matches"])}

Mediana `{incumbent["candidate_median"]:.1f}` contro
`{incumbent["opponent_median"]:.1f}`, delta `{incumbent["median_margin"]:+.1f}`.

## Check

```json
{json.dumps(payload["checks"], indent=2, sort_keys=True)}
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
