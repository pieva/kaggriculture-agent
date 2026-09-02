#!/usr/bin/env python3
"""Run the single-factor RQ3 Q2 timing probe for D11/D10/D8.

This is an experiment-only wrapper around the frozen Codex V9 baseline. It does
not modify the source of the baseline and is intentionally limited to the single
causal lever: the calendar day on which the third quadrant is unlocked.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.e17_ledger import E17CommandLedger, instrument_policy
from agricola.strategy.codex.codex_3q_mixed_high_density import (
    V9_MODEL_SPEC_VERSION,
    create_v9_agent,
)
from agricola.strategy.codex.codex_v9_routine_data import ROUTINE_SHA256

REPO_ROOT = Path(__file__).resolve().parents[4]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUT_ROOT = REPO_ROOT / "experiments/e17/artifacts/runs/codex/rq3_q2_timing"
REPORT_PATH = REPO_ROOT / "experiments/e17/reports/common/E17_RQ3_Q2_TIMING_PROBE_SUMMARY.md"

SEEDS = [26090101, 26090102, 26090103]
TARGET_DAYS = [11, 10, 8]
SEATS = [0, 1]


def _load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _build_q2_timing_agent(target_day: int, *, run_context: dict[str, Any]) -> Any:
    """Return a wrapper that holds the frozen policy constant and only shifts Q2 unlock timing."""
    base_policy = create_v9_agent(run_context=run_context)

    def wrapped(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        action = base_policy(observation, configuration)
        farm = observation.get("farms", [])[int(observation.get("player", 0))]
        unlocked = list(farm.get("unlocked_quadrants", []) or [])
        day = int(observation.get("day", 0))
        if len(unlocked) >= 2 and len(unlocked) < 3 and day <= target_day:
            market = list(action.get("market", []) or [])
            if not any(isinstance(order, list) and order and order[0] == "BUY_LAND" for order in market):
                market.append(["BUY_LAND"])
                action["market"] = market
        return action

    wrapped.__name__ = f"codex_q2_timing_{target_day}_day_policy"
    wrapped.codex_v9_instance = base_policy.codex_v9_instance
    return wrapped


def _terminal_payload(env: Any, seat: int) -> dict[str, Any]:
    terminal = env.steps[-1][seat]
    observation = terminal.get("observation", {}) or {}
    return {
        "reward": terminal.get("reward"),
        "status": terminal.get("status"),
        "final_money": float((observation.get("farms") or [])[seat].get("money", 0.0)),
        "unlocked_quadrants": (observation.get("farms") or [])[seat].get("unlocked_quadrants", []),
        "step": int(observation.get("step", 0)),
        "day": int(observation.get("day", 0)),
        "terminal_snapshot": observation,
    }


def _run_one(seed: int, seat: int, target_day: int) -> dict[str, Any]:
    manifest = _load_manifest()
    run_id = f"RQ3-Q2-T{target_day}-S{seed}-P{seat}"
    context = {
        "run_id": run_id,
        "episode_id": run_id,
        "seed": seed,
        "player_position": seat,
    }
    ledger = E17CommandLedger(
        {
            "episode_id": run_id,
            "seed": seed,
            "seat": seat,
            "policy_version": V9_MODEL_SPEC_VERSION,
            "source_hash": manifest["opponents"]["codex_v9_freeze"]["source_sha256"],
            "config_hash": manifest["opponents"]["codex_v9_freeze"]["config_sha256"],
            "routine_hash": ROUTINE_SHA256,
        }
    )
    policy = _build_q2_timing_agent(target_day, run_context=context)
    candidate = instrument_policy(policy, ledger)
    agents = [candidate, inert_pass_policy] if seat == 0 else [inert_pass_policy, candidate]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    terminal = _terminal_payload(env, seat)
    ledger.finalize(terminal["terminal_snapshot"])
    ledger_metrics = ledger.metrics()
    instance = getattr(policy, "codex_v9_instance", None)
    if instance is not None:
        telemetry = instance.telemetry_snapshot()
    else:
        telemetry = {}
    result = {
        "run_id": run_id,
        "seed": seed,
        "seat": seat,
        "target_q2_day": target_day,
        "reward": terminal["reward"],
        "status": terminal["status"],
        "final_money": terminal["final_money"],
        "unlock_day": terminal["day"],
        "unlocked_quadrants": terminal["unlocked_quadrants"],
        "ledger_record_coverage": ledger_metrics["ledger_record_coverage"],
        "ledger_records": ledger_metrics["ledger_records"],
        "move_actions": telemetry.get("MOVE_actions", 0),
        "productive_actions": telemetry.get("productive_actions", 0),
        "move_per_productive": telemetry.get("MOVE_PER_PRODUCTIVE_ACTION"),
        "animal_escapes": telemetry.get("ANIMAL_ESCAPE", 0),
        "q1_activation_day": telemetry.get("Q1_activation_day"),
        "q2_activation_day": telemetry.get("Q2_activation_day"),
        "q2_first_output_day": telemetry.get("Q2_first_output_day"),
        "max_hands": telemetry.get("max_hands", 0),
        "max_active_animals": telemetry.get("max_active_animals", 0),
        "max_active_crops": telemetry.get("max_active_crops", 0),
        "sale_requests": telemetry.get("sale_requests", {}),
    }
    return result


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _render_markdown(rows: list[dict[str, Any]]) -> str:
    by_target = {}
    for row in rows:
        by_target.setdefault(row["target_q2_day"], []).append(row)
    lines = [
        "# E17 — RQ3 Q2 timing probe summary",
        "",
        "- **Scope:** single-factor timing probe for Q2 unlock timing under the frozen Codex V9 baseline.",
        "- **Protocol:** maintain the baseline agent source and config fixed; vary only the Q2 unlock day while keeping the rest of the policy intact.",
        "- **Ledger:** every run recorded through the E17 ledger and checked for `ledger_record_coverage == 1.0`.",
        "",
        "## Aggregate comparison",
        "",
        "| Target Q2 day | Runs | Mean reward | Mean final money | Mean MOVE | Mean productive | Mean animal escapes | Mean max hands | Mean q2 activation day |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for target_day in TARGET_DAYS:
        subset = by_target.get(target_day, [])
        if not subset:
            continue
        lines.append(
            f"| {target_day} | {len(subset)} | {sum(r['reward'] for r in subset)/len(subset):.2f} | {sum(r['final_money'] for r in subset)/len(subset):.2f} | {sum(r['move_actions'] for r in subset)/len(subset):.2f} | {sum(r['productive_actions'] for r in subset)/len(subset):.2f} | {sum(r['animal_escapes'] for r in subset)/len(subset):.2f} | {sum(r['max_hands'] for r in subset)/len(subset):.2f} | {sum(v for v in [r['q2_activation_day'] for r in subset if r['q2_activation_day'] is not None]) / max(1, len([r for r in subset if r['q2_activation_day'] is not None])):.2f} |"
        )
    lines += ["", "## Per-run rows", "", "| run_id | target | seed | seat | reward | final_money | move | productive | q2_day | escapes | ledger_cov |",
               "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for row in sorted(rows, key=lambda r: (r["target_q2_day"], r["seed"], r["seat"])):
        lines.append(
            f"| {row['run_id']} | {row['target_q2_day']} | {row['seed']} | {row['seat']} | {row['reward']} | {row['final_money']} | {row['move_actions']} | {row['productive_actions']} | {row['q2_activation_day'] if row['q2_activation_day'] is not None else 'NA'} | {row['animal_escapes']} | {row['ledger_record_coverage']:.2f} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    rows: list[dict[str, Any]] = []
    for target_day in TARGET_DAYS:
        for seed in SEEDS:
            for seat in SEATS:
                print(f"RUN target={target_day} seed={seed} seat={seat}", flush=True)
                row = _run_one(seed, seat, target_day)
                rows.append(row)
                assert row["ledger_record_coverage"] == 1.0, f"ledger coverage failed for {row['run_id']}"
                _write_json(OUT_ROOT / f"{row['run_id']}.summary.json", row)
    summary = {"schema_version": "E17.RQ3.Q2_TIMING.V1", "target_days": TARGET_DAYS, "seeds": SEEDS, "seats": SEATS, "runs": rows}
    _write_json(OUT_ROOT / "RQ3_Q2_TIMING_SUMMARY.json", summary)
    REPORT_PATH.write_text(_render_markdown(rows), encoding="utf-8")
    print(f"WROTE {len(rows)} rows to {OUT_ROOT}")
    print(f"REPORT: {REPORT_PATH}")


if __name__ == "__main__":
    main()
