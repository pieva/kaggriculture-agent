#!/usr/bin/env python3
"""Run Antigravity E17.0 native baseline construction on development seeds."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any, Callable

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.e17_ledger import E17CommandLedger, canonical_sha256, instrument_policy
from agricola.strategy.antigravity.antigravity_e17_native_3q import (
    E17_NATIVE_MODEL_SPEC_VERSION,
    create_e17_native_agent,
)


REPO_ROOT = Path(__file__).resolve().parents[5]
RUN_ROOT = REPO_ROOT / "docs/model_specs/antigravity/e17/artifacts/runs/e17_0_native"
DERIVED_ROOT = REPO_ROOT / "docs/model_specs/antigravity/e17/artifacts/derived"
FREEZE_ROOT = REPO_ROOT / "docs/model_specs/antigravity/e17/artifacts/freeze"
CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/antigravity/e17/configs/ANTIGRAVITY_E17_0_NATIVE_3Q_BASELINE_CONFIG.json"
)
SOURCE_PATH = (
    REPO_ROOT
    / "src/agricola/strategy/antigravity/antigravity_e17_native_3q.py"
)
ENTRYPOINT_PATH = (
    REPO_ROOT
    / "src/agricola/strategy/antigravity/agent_e17_native_3q.py"
)
LEDGER_PATH = REPO_ROOT / "src/agricola/core/e17_ledger.py"
FORBIDDEN_IMPORT_TOKENS = (
    "agricola.strategy.codex",
    "agricola.strategy.copilot",
    "ROUTINE_ACTIONS",
    "codex_v9_routine_data",
)
CODEX_ROUTINE_SHA = "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _capture_policy(policy: Callable, actions: list[dict[str, Any]]) -> Callable:
    def wrapped(observation: dict[str, Any], configuration: Any = None):
        action = policy(observation, configuration)
        actions.append(deepcopy(action))
        return action

    return wrapped


def _stable_observation(observation: dict[str, Any]) -> dict[str, Any]:
    return {
        key: observation.get(key)
        for key in ("step", "player", "farms", "private", "market", "town", "day", "hour")
    }


def _terminal_payload(env: Any, seat: int) -> dict[str, Any]:
    terminal = env.steps[-1][seat]
    observation = terminal.get("observation", {}) or {}
    return {
        "reward": terminal.get("reward"),
        "status": terminal.get("status"),
        "observation": observation,
        "state_sha256": canonical_sha256(_stable_observation(observation)),
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


def _audit_source() -> dict[str, Any]:
    text = SOURCE_PATH.read_text(encoding="utf-8")
    forbidden_hits = [token for token in FORBIDDEN_IMPORT_TOKENS if token in text]
    return {
        "source_path": str(SOURCE_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "entrypoint_path": str(ENTRYPOINT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "source_sha256": sha256_file(SOURCE_PATH),
        "entrypoint_sha256": sha256_file(ENTRYPOINT_PATH),
        "forbidden_tokens": forbidden_hits,
        "no_import_other_agent_routine": not forbidden_hits,
        "no_copy_other_agent_action_table": not forbidden_hits,
    }


def _run(seed: int, seat: int, *, instrumented: bool) -> dict[str, Any]:
    context = {
        "run_id": f"E17-0-AG-S{seed}-P{seat}-{'L' if instrumented else 'B'}",
        "episode_id": f"E17-0-AG-S{seed}-P{seat}",
        "seed": seed,
        "player_position": seat,
    }
    policy = create_e17_native_agent(run_context=context, config_path=CONFIG_PATH)
    actions: list[dict[str, Any]] = []
    ledger = None
    if instrumented:
        ledger = E17CommandLedger(
            {
                "episode_id": context["episode_id"],
                "seed": seed,
                "seat": seat,
                "player_id": seat,
                "policy_version": E17_NATIVE_MODEL_SPEC_VERSION,
                "source_hash": sha256_file(SOURCE_PATH),
                "config_hash": sha256_file(CONFIG_PATH),
                "routine_hash": policy.antigravity_e17_native_instance.routine_hash,
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
    instance = policy.antigravity_e17_native_instance
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
        "telemetry": instance.telemetry_snapshot(),
        "routine_hash": instance.routine_hash,
        "ledger": ledger,
    }


def run_matrix(seeds: list[int]) -> dict[str, Any]:
    audit = _audit_source()
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
            run_id = f"E17-0-AG-S{seed}-P{seat}"
            plain_vs_instrumented_actions = baseline["actions"] == measured["actions"]
            plain_vs_instrumented_terminal = (
                baseline["reward"] == measured["reward"]
                and baseline["status"] == measured["status"]
                and baseline["terminal_state_sha256"] == measured["terminal_state_sha256"]
            )
            result = {
                "run_id": run_id,
                "seed": seed,
                "seat": seat,
                "plain_vs_instrumented_actions": plain_vs_instrumented_actions,
                "plain_vs_instrumented_terminal": plain_vs_instrumented_terminal,
                "action_count_baseline": baseline["action_count"],
                "action_count_instrumented": measured["action_count"],
                "action_sequence_sha256_baseline": baseline["action_sequence_sha256"],
                "action_sequence_sha256_instrumented": measured["action_sequence_sha256"],
                "reward_baseline": baseline["reward"],
                "reward_instrumented": measured["reward"],
                "terminal_state_sha256_baseline": baseline["terminal_state_sha256"],
                "terminal_state_sha256_instrumented": measured["terminal_state_sha256"],
                "errors_baseline": baseline["error_count"],
                "errors_instrumented": measured["error_count"],
                "fallback_baseline": baseline["fallback_count"],
                "fallback_instrumented": measured["fallback_count"],
                "routine_hash": measured["routine_hash"],
                "telemetry": measured["telemetry"],
                "ledger_metrics": ledger_metrics,
            }
            _write_jsonl(RUN_ROOT / f"{run_id}.ledger.jsonl", ledger.records)
            _write_json(RUN_ROOT / f"{run_id}.derived_events.json", ledger.derived_events)
            _write_json(RUN_ROOT / f"{run_id}.summary.json", result)
            results.append(result)
            print(
                f"PASS seed={seed} seat={seat} actions={measured['action_count']} "
                f"records={ledger_metrics['ledger_records']} reward={measured['reward']}",
                flush=True,
            )

    rewards = [float(row["reward_instrumented"] or 0.0) for row in results]
    routine_hashes = sorted({row["routine_hash"] for row in results})
    all_pass = all(
        row["plain_vs_instrumented_actions"]
        and row["plain_vs_instrumented_terminal"]
        and row["errors_baseline"] == 0
        and row["errors_instrumented"] == 0
        and row["ledger_metrics"]["ledger_record_coverage"] == 1.0
        and int(row["telemetry"]["max_quadrants"]) >= 3
        and row["telemetry"]["Q2_activation_day"] is not None
        for row in results
    )
    metrics = {
        "schema_version": "E17_0_ANTIGRAVITY_NATIVE_METRICS_V1",
        "agent_id": "antigravity",
        "policy_version": E17_NATIVE_MODEL_SPEC_VERSION,
        "status": "PASS" if all_pass else "FAIL",
        "construction_mode": "NATIVE_BASELINE_CONSTRUCTION",
        "seeds": seeds,
        "seats": [0, 1],
        "opponent_id": "INERT_PASS_POLICY",
        "opponent_entrypoint": "agricola.core.benchmark_opponents.inert_pass_policy",
        "runs": len(results),
        "plain_vs_instrumented_action_parity_runs": sum(
            row["plain_vs_instrumented_actions"] for row in results
        ),
        "plain_vs_instrumented_terminal_parity_runs": sum(
            row["plain_vs_instrumented_terminal"] for row in results
        ),
        "three_quadrant_activation_runs": sum(
            int(row["telemetry"]["max_quadrants"]) >= 3 for row in results
        ),
        "three_quadrant_activation_required_runs": len(results),
        "q2_activation_recorded_runs": sum(
            row["telemetry"]["Q2_activation_day"] is not None for row in results
        ),
        "ledger_records": sum(row["ledger_metrics"]["ledger_records"] for row in results),
        "ledger_record_coverage_min": min(
            row["ledger_metrics"]["ledger_record_coverage"] for row in results
        ),
        "classified_outcome_coverage_min": min(
            row["ledger_metrics"]["classified_outcome_coverage"] for row in results
        ),
        "market_classified_outcome_coverage_min": min(
            row["ledger_metrics"]["market_classified_outcome_coverage"] for row in results
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
        "reward_mean": mean(rewards),
        "reward_median": median(rewards),
        "reward_min": min(rewards),
        "reward_max": max(rewards),
        "reward_std": pstdev(rewards),
        "routine_hashes": routine_hashes,
        "routine_hash_distinct_from_codex": all(
            routine_hash != CODEX_ROUTINE_SHA for routine_hash in routine_hashes
        ),
        "no_import_audit": audit,
        "source_config_freeze": {
            "source_path": str(SOURCE_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
            "source_sha256": sha256_file(SOURCE_PATH),
            "entrypoint_path": str(ENTRYPOINT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
            "entrypoint_sha256": sha256_file(ENTRYPOINT_PATH),
            "config_path": str(CONFIG_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
            "config_sha256": sha256_file(CONFIG_PATH),
        },
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "results": results,
    }
    _write_json(DERIVED_ROOT / "E17_0_METRICS.json", metrics)
    freeze = {
        "agent_id": "antigravity",
        "policy_version": E17_NATIVE_MODEL_SPEC_VERSION,
        "source_path": str(SOURCE_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "source_sha256": sha256_file(SOURCE_PATH),
        "entrypoint_path": str(ENTRYPOINT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "entrypoint_sha256": sha256_file(ENTRYPOINT_PATH),
        "config_path": str(CONFIG_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "config_sha256": sha256_file(CONFIG_PATH),
        "ledger_source_path": str(LEDGER_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "ledger_source_sha256": sha256_file(LEDGER_PATH),
        "runner_path": str(Path(__file__).relative_to(REPO_ROOT)).replace("\\", "/"),
        "runner_sha256": sha256_file(Path(__file__)),
        "metrics_path": "docs/model_specs/antigravity/e17/artifacts/derived/E17_0_METRICS.json",
        "native_baseline_construction": True,
        "policy_optimization": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "routine_hash": routine_hashes[0] if len(routine_hashes) == 1 else routine_hashes,
    }
    _write_json(FREEZE_ROOT / "E17_0_FREEZE_MANIFEST.json", freeze)
    return metrics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=[26090101, 26090102, 26090103])
    args = parser.parse_args(argv)
    metrics = run_matrix(args.seeds)
    summary = {
        key: metrics[key]
        for key in (
            "status",
            "runs",
            "ledger_records",
            "ledger_record_coverage_min",
            "market_classified_outcome_coverage_min",
            "derived_eod_escape_count",
            "technical_errors",
            "fallback_delta",
            "routine_hash_distinct_from_codex",
        )
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if metrics["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
