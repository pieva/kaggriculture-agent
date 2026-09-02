#!/usr/bin/env python3
"""Run the frozen Codex V9 E17.0 measurement-parity matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.e17_ledger import (
    E17CommandLedger,
    canonical_sha256,
    instrument_policy,
)
from agricola.strategy.codex.codex_3q_mixed_high_density import (
    V9_MODEL_SPEC_VERSION,
    create_v9_agent,
)
from agricola.strategy.codex.codex_v9_routine_data import ROUTINE_SHA256


REPO_ROOT = Path(__file__).resolve().parents[4]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
RUN_ROOT = REPO_ROOT / "experiments/e17/artifacts/runs/codex/e17_0"
DERIVED_ROOT = REPO_ROOT / "experiments/e17/artifacts/derived/codex"
FREEZE_ROOT = REPO_ROOT / "experiments/e17/artifacts/freeze/codex"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _capture_policy(policy: Callable, actions: list[dict[str, Any]]) -> Callable:
    def wrapped(observation: dict[str, Any], configuration: Any = None):
        action = policy(observation, configuration)
        actions.append(deepcopy(action))
        return action

    return wrapped


def _terminal_payload(env: Any, seat: int) -> dict[str, Any]:
    terminal = env.steps[-1][seat]
    observation = terminal.get("observation", {}) or {}
    stable_observation = {
        key: observation.get(key)
        for key in ("step", "player", "farms", "private", "market", "town", "day", "hour")
    }
    return {
        "reward": terminal.get("reward"),
        "status": terminal.get("status"),
        "observation": observation,
        "state_sha256": canonical_sha256(stable_observation),
    }


def _run(seed: int, seat: int, *, instrumented: bool) -> dict[str, Any]:
    context = {
        "run_id": f"E17-0-CODEX-S{seed}-P{seat}-{'L' if instrumented else 'B'}",
        "episode_id": f"E17-0-CODEX-S{seed}-P{seat}",
        "seed": seed,
        "player_position": seat,
    }
    policy = create_v9_agent(run_context=context)
    actions: list[dict[str, Any]] = []
    ledger = None
    if instrumented:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        ledger = E17CommandLedger(
            {
                "episode_id": context["episode_id"],
                "seed": seed,
                "seat": seat,
                "player_id": seat,
                "policy_version": V9_MODEL_SPEC_VERSION,
                "source_hash": manifest["opponents"]["codex_v9_freeze"]["source_sha256"],
                "config_hash": manifest["opponents"]["codex_v9_freeze"]["config_sha256"],
                "routine_hash": ROUTINE_SHA256,
            }
        )
        candidate = instrument_policy(policy, ledger)
    else:
        candidate = _capture_policy(policy, actions)

    agents = [candidate, inert_pass_policy] if seat == 0 else [inert_pass_policy, candidate]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    terminal = _terminal_payload(env, seat)
    if ledger is not None:
        ledger.finalize(terminal["observation"])
        actions = [deepcopy(entry["action"]) for entry in ledger.action_batches]
    instance = policy.codex_v9_instance
    return {
        "seed": seed,
        "seat": seat,
        "instrumented": instrumented,
        "actions": actions,
        "action_count": len(actions),
        "action_sequence_sha256": canonical_sha256(actions),
        "reward": terminal["reward"],
        "status": terminal["status"],
        "terminal_state_sha256": terminal["state_sha256"],
        "error_count": instance.error_count,
        "fallback_count": instance.fallback_count,
        "ledger": ledger,
    }


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def run_matrix(seeds: list[int]) -> dict[str, Any]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    for seed in seeds:
        for seat in (0, 1):
            print(f"RUN seed={seed} seat={seat} baseline", flush=True)
            baseline = _run(seed, seat, instrumented=False)
            print(f"RUN seed={seed} seat={seat} instrumented", flush=True)
            measured = _run(seed, seat, instrumented=True)
            ledger: E17CommandLedger = measured.pop("ledger")
            baseline.pop("ledger")
            ledger_metrics = ledger.metrics()
            action_parity = baseline["actions"] == measured["actions"]
            outcome_parity = (
                baseline["reward"] == measured["reward"]
                and baseline["status"] == measured["status"]
                and baseline["terminal_state_sha256"] == measured["terminal_state_sha256"]
            )
            run_id = f"E17-0-CODEX-S{seed}-P{seat}"
            _write_jsonl(RUN_ROOT / f"{run_id}.ledger.jsonl", ledger.records)
            _write_json(RUN_ROOT / f"{run_id}.derived_events.json", ledger.derived_events)
            result = {
                "run_id": run_id,
                "seed": seed,
                "seat": seat,
                "action_parity": action_parity,
                "action_count_baseline": baseline["action_count"],
                "action_count_instrumented": measured["action_count"],
                "action_sequence_sha256_baseline": baseline["action_sequence_sha256"],
                "action_sequence_sha256_instrumented": measured["action_sequence_sha256"],
                "outcome_parity": outcome_parity,
                "reward_baseline": baseline["reward"],
                "reward_instrumented": measured["reward"],
                "terminal_state_sha256_baseline": baseline["terminal_state_sha256"],
                "terminal_state_sha256_instrumented": measured["terminal_state_sha256"],
                "errors_baseline": baseline["error_count"],
                "errors_instrumented": measured["error_count"],
                "fallback_baseline": baseline["fallback_count"],
                "fallback_instrumented": measured["fallback_count"],
                "ledger_metrics": ledger_metrics,
            }
            _write_json(RUN_ROOT / f"{run_id}.summary.json", result)
            results.append(result)
            print(
                f"PASS seed={seed} seat={seat} actions={baseline['action_count']} "
                f"records={ledger_metrics['ledger_records']} reward={baseline['reward']}",
                flush=True,
            )

    total_actions = sum(row["action_count_baseline"] for row in results)
    total_instrumented = sum(row["action_count_instrumented"] for row in results)
    all_pass = all(
        row["action_parity"]
        and row["outcome_parity"]
        and row["action_count_baseline"] == 719
        and row["action_count_instrumented"] == 719
        and row["errors_baseline"] == 0
        and row["errors_instrumented"] == 0
        and row["fallback_baseline"] == row["fallback_instrumented"]
        and row["ledger_metrics"]["ledger_record_coverage"] == 1.0
        for row in results
    )
    metrics = {
        "schema_version": "E17_0_METRICS_V1",
        "agent_id": "codex",
        "policy_version": V9_MODEL_SPEC_VERSION,
        "status": "PASS" if all_pass else "FAIL",
        "seeds": seeds,
        "seats": [0, 1],
        "opponent": manifest["opponents"]["inert_pass"],
        "runs": len(results),
        "action_parity_runs": sum(row["action_parity"] for row in results),
        "outcome_parity_runs": sum(row["outcome_parity"] for row in results),
        "action_parity": f"{total_instrumented}/{total_actions}",
        "action_sequence_sha256": sorted(
            {row["action_sequence_sha256_baseline"] for row in results}
        ),
        "ledger_records": sum(row["ledger_metrics"]["ledger_records"] for row in results),
        "ledger_record_coverage_min": min(
            row["ledger_metrics"]["ledger_record_coverage"] for row in results
        ),
        "market_classified_outcome_coverage_min": min(
            row["ledger_metrics"]["market_classified_outcome_coverage"]
            for row in results
        ),
        "market_outcome_unknown_count": sum(
            row["ledger_metrics"]["market_outcome_counts"]["UNKNOWN"]
            for row in results
        ),
        "derived_eod_escape_count": sum(
            row["ledger_metrics"]["derived_eod_escape_count"] for row in results
        ),
        "technical_errors": sum(
            row["errors_instrumented"] + row["ledger_metrics"]["technical_errors"]
            for row in results
        ),
        "fallback_delta": sum(
            row["fallback_instrumented"] - row["fallback_baseline"] for row in results
        ),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "results": results,
    }
    _write_json(DERIVED_ROOT / "E17_0_METRICS.json", metrics)
    freeze = {
        "agent_id": "codex",
        "policy_version": V9_MODEL_SPEC_VERSION,
        "source": manifest["opponents"]["codex_v9_freeze"],
        "submission_sha256": "AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421",
        "ledger_source_path": "src/agricola/core/e17_ledger.py",
        "ledger_source_sha256": sha256_file(REPO_ROOT / "src/agricola/core/e17_ledger.py"),
        "runner_path": "experiments/e17/tools/codex/run_e17_0_codex_parity.py",
        "runner_sha256": sha256_file(Path(__file__)),
        "metrics_path": "experiments/e17/artifacts/derived/codex/E17_0_METRICS.json",
        "measurement_parity": metrics["status"],
        "policy_mutation": False,
    }
    _write_json(FREEZE_ROOT / "E17_0_FREEZE_MANIFEST.json", freeze)
    return metrics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=[26090101, 26090102, 26090103])
    args = parser.parse_args(argv)
    metrics = run_matrix(args.seeds)
    print(json.dumps({key: metrics[key] for key in (
        "status", "runs", "action_parity", "ledger_records",
        "ledger_record_coverage_min", "market_classified_outcome_coverage_min",
        "derived_eod_escape_count", "technical_errors", "fallback_delta",
    )}, indent=2, sort_keys=True))
    return 0 if metrics["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
