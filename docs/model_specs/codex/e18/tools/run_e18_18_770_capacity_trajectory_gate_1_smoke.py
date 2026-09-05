#!/usr/bin/env python3
"""Two-seat development smoke for the guarded E18.18 trajectory controller."""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    create_codex_e18_770_exact_cap_critical_feed,
)
from docs.model_specs.codex.e18.tools.e18_18_capacity_trajectory_planner import (
    build_plan,
)
from docs.model_specs.codex.e18.tools.run_e18_18_770_capacity_trajectory_gate_0b import (
    Gate0BController,
    _snapshot,
)

SEED = 180903001
CANDIDATE = "CODEX_E18_18_770_TRAJECTORY_GUARDED"
CONTROL = "CODEX_E18_16_770_CONTROL"
OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_1_SMOKE_V1.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_1_SMOKE_REPORT_IT.md"
)


def _weed_count(farm: dict[str, Any]) -> int:
    return sum(
        isinstance(tile, dict) and tile.get("kind") == "WEED"
        for row in farm.get("tiles", []) or []
        for tile in row
    )


def _control(seed: int, seat: int):
    return create_codex_e18_770_exact_cap_critical_feed(
        run_context={
            "run_id": f"E18-18-SMOKE-S{seed}-P{seat}-CONTROL",
            "episode_id": f"E18-18-SMOKE-S{seed}-P{seat}-CONTROL",
            "seed": seed,
            "player_position": seat,
        }
    )


def _run_match(plan: dict[str, Any], candidate_seat: int) -> dict[str, Any]:
    candidate = Gate0BController(plan, seat=candidate_seat)
    control_seat = 1 - candidate_seat
    policies = [None, None]
    policies[candidate_seat] = candidate
    policies[control_seat] = _control(SEED, control_seat)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24},
        debug=False,
    )
    env.run(policies)
    replay = env.toJSON()
    rewards = [float(value or 0.0) for value in replay.get("rewards", [0, 0])]
    final = _snapshot(replay, 30, candidate_seat)
    final_record = replay["steps"][719][candidate_seat]["observation"]
    candidate_reward = rewards[candidate_seat]
    control_reward = rewards[control_seat]
    return {
        "seed": SEED,
        "candidate_seat": candidate_seat,
        "candidate_reward": candidate_reward,
        "control_reward": control_reward,
        "margin": candidate_reward - control_reward,
        "candidate_final": final,
        "candidate_final_weeds": _weed_count(
            final_record["farms"][candidate_seat]
        ),
        "controller_errors": candidate.error_count,
        "guarded_noops": dict(sorted(candidate.guarded_noops.items())),
    }


def run() -> dict[str, Any]:
    plan = build_plan()
    matches = [_run_match(plan, seat) for seat in (0, 1)]
    checks = {
        "zero_controller_errors": all(
            match["controller_errors"] == 0 for match in matches
        ),
        "exact_final_770_both_seats": all(
            match["candidate_final"]["topology"] == {"Q0": 7, "Q1": 7}
            for match in matches
        ),
        "exact_final_9_cow_5_sheep_both_seats": all(
            match["candidate_final"]["animals"] == {"COW": 9, "SHEEP": 5}
            for match in matches
        ),
        "positive_candidate_reward_both_seats": all(
            match["candidate_reward"] > 0 for match in matches
        ),
        "candidate_median_not_below_control": statistics.median(
            match["candidate_reward"] for match in matches
        )
        >= statistics.median(match["control_reward"] for match in matches),
    }
    return {
        "schema_version": "e18.codex.770_capacity_trajectory_gate_1_smoke.v1",
        "candidate": CANDIDATE,
        "control": CONTROL,
        "seed": SEED,
        "seats": [0, 1],
        "epistemic_role": "DEVELOPMENT_SMOKE_NOT_FULL_GATE_1",
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "plan_sha256": plan["plan_sha256"],
        "passed": all(checks.values()),
        "checks": checks,
        "matches": matches,
    }


def _write_report(payload: dict[str, Any]) -> None:
    rows = "\n".join(
        "| {candidate_seat} | {candidate_reward:.0f} | {control_reward:.0f} | "
        "{margin:+.0f} | {topology} | {animals} | {weeds} |".format(
            **match,
            topology=json.dumps(match["candidate_final"]["topology"], sort_keys=True),
            animals=json.dumps(match["candidate_final"]["animals"], sort_keys=True),
            weeds=match["candidate_final_weeds"],
        )
        for match in payload["matches"]
    )
    failed = [key for key, value in payload["checks"].items() if not value]
    report = f"""# E18.18 — Gate 1 development smoke

## Verdetto

`{'PASS' if payload['passed'] else 'FAIL'}` sul primo seed development in
entrambi i seat. Questo smoke non sostituisce il Gate 1 preregistrato a 14
match.

Check falliti: `{', '.join(failed) if failed else 'nessuno'}`.

| Seat candidato | E18.18 | E18.16 | Margine | Topologia | Animali | Weed finali |
|---:|---:|---:|---:|---|---|---:|
{rows}

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
