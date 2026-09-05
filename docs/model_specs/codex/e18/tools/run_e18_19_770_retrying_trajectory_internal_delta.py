#!/usr/bin/env python3
"""Matched E18.19 versus E18.18 execution-layer delta smoke."""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "docs/model_specs/codex/e18/tools"
for import_root in (ROOT, TOOLS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from docs.model_specs.codex.e18.tools.e18_19_retrying_trajectory_controller import (
    RetryingTrajectoryController,
)
from docs.model_specs.codex.e18.tools.run_e18_18_770_capacity_trajectory_gate_0b import (
    Gate0BController,
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
    / "E18_19_770_RETRYING_TRAJECTORY_INTERNAL_DELTA_V1.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_19_770_RETRYING_TRAJECTORY_INTERNAL_DELTA_REPORT_IT.md"
)


def _run_match(plan: dict[str, Any], candidate_seat: int) -> dict[str, Any]:
    candidate = RetryingTrajectoryController(plan, seat=candidate_seat)
    baseline_seat = 1 - candidate_seat
    baseline = Gate0BController(plan, seat=baseline_seat)
    policies = [None, None]
    policies[candidate_seat] = candidate
    policies[baseline_seat] = baseline
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
    baseline_reward = rewards[baseline_seat]
    return {
        "candidate_seat": candidate_seat,
        "candidate_reward": candidate_reward,
        "baseline_reward": baseline_reward,
        "margin": candidate_reward - baseline_reward,
        "candidate_final": _snapshot(replay, 30, candidate_seat),
        "baseline_final": _snapshot(replay, 30, baseline_seat),
        "candidate_errors": candidate.error_count,
        "baseline_errors": baseline.error_count,
        "recovery_actions": dict(sorted(candidate.recovery_actions.items())),
        "deferred_critical": dict(sorted(candidate.deferred_critical.items())),
        "skipped_stale": dict(sorted(candidate.skipped_stale.items())),
        "unfinished_actions": sum(candidate.unfinished_by_day.values()),
    }


def run() -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan.get("plan_sha256") != EXPECTED_PLAN_SHA256:
        raise ValueError("frozen E18.18 plan hash mismatch")
    matches = [_run_match(plan, seat) for seat in (0, 1)]
    candidate_median = statistics.median(
        match["candidate_reward"] for match in matches
    )
    baseline_median = statistics.median(
        match["baseline_reward"] for match in matches
    )
    checks = {
        "zero_errors": all(
            match["candidate_errors"] == match["baseline_errors"] == 0
            for match in matches
        ),
        "candidate_exact_770": all(
            match["candidate_final"]["topology"] == {"Q0": 7, "Q1": 7}
            for match in matches
        ),
        "candidate_exact_9_cow_5_sheep": all(
            match["candidate_final"]["animals"] == {"COW": 9, "SHEEP": 5}
            for match in matches
        ),
        "candidate_wins_both_seats": all(match["margin"] > 0 for match in matches),
    }
    return {
        "schema_version": "e18.codex.770_retrying_trajectory_internal_delta.v1",
        "candidate": "CODEX_E18_19_770_RETRYING_TRAJECTORY_V1",
        "baseline": "CODEX_E18_18_770_TRAJECTORY_GUARDED",
        "seed": SEED,
        "seats": [0, 1],
        "epistemic_role": "DEVELOPMENT_MATCHED_DELTA_SMOKE",
        "plan_sha256": EXPECTED_PLAN_SHA256,
        "passed": all(checks.values()),
        "checks": checks,
        "candidate_median": candidate_median,
        "baseline_median": baseline_median,
        "median_margin": candidate_median - baseline_median,
        "median_margin_pct": (
            100.0 * (candidate_median - baseline_median) / baseline_median
        ),
        "matches": matches,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
    }


def _write_report(payload: dict[str, Any]) -> None:
    rows = "\n".join(
        "| {candidate_seat} | {candidate_reward:.0f} | {baseline_reward:.0f} | "
        "{margin:+.0f} | {topology} | {animals} | {unfinished_actions} |".format(
            **match,
            topology=json.dumps(match["candidate_final"]["topology"], sort_keys=True),
            animals=json.dumps(match["candidate_final"]["animals"], sort_keys=True),
        )
        for match in payload["matches"]
    )
    report = f"""# E18.19 — delta interno contro E18.18

## Verdetto

`{'PASS' if payload['passed'] else 'FAIL'}` sul delta causale del solo layer di
esecuzione. Seed, piano, topologia, composizione target e mercato sono comuni;
il trattamento E18.19 aggiunge ack, retry limitato e recupero dello stato.

| Seat E18.19 | E18.19 | E18.18 | Margine | Topologia | Animali | Backlog |
|---:|---:|---:|---:|---|---|---:|
{rows}

Mediana E18.19 `{payload['candidate_median']:.1f}`, mediana E18.18
`{payload['baseline_median']:.1f}`, delta `{payload['median_margin']:+.1f}`
(`{payload['median_margin_pct']:+.2f}%`).

Questo PASS dimostra il miglioramento rispetto all'executor E18.18, non la
promozione rispetto all'incumbent E18.16. Fa fede separatamente lo smoke Gate 1
contro E18.16.

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
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
