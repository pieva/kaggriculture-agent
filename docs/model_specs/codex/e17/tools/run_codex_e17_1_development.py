#!/usr/bin/env python3
"""Validate and freeze the Codex E17.1 reactive candidate on development seeds."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import statistics
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.e17_ledger import E17CommandLedger, instrument_policy
from agricola.strategy.codex.codex_3q_mixed_high_density import create_v9_agent
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    DEFAULT_REACTIVE_CONFIG_PATH,
    REACTIVE_MODEL_SPEC_VERSION,
    create_codex_e17_reactive_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
SOURCE_PATH = REPO_ROOT / "src/agricola/strategy/codex/codex_e17_reactive_guarded.py"
RUN_ROOT = REPO_ROOT / "docs/model_specs/codex/e17/artifacts/runs/e17_1_development"
DERIVED_PATH = (
    REPO_ROOT / "docs/model_specs/codex/e17/artifacts/derived/E17_1_DEVELOPMENT_METRICS.json"
)
FREEZE_ROOT = REPO_ROOT / "docs/model_specs/codex/e17/artifacts/freeze/e17_1"


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


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


def _terminal(env: Any, seat: int) -> dict[str, Any]:
    state = env.steps[-1][seat]
    return {
        "reward": float(state.get("reward") or 0.0),
        "status": state.get("status"),
        "observation": state.get("observation", {}) or {},
    }


def _run_policy(
    factory: Callable[..., Callable],
    *,
    seed: int,
    seat: int,
    label: str,
    with_ledger: bool,
) -> dict[str, Any]:
    context = {
        "run_id": f"E17-1-{label}-S{seed}-P{seat}",
        "episode_id": f"E17-1-{label}-S{seed}-P{seat}",
        "seed": seed,
        "player_position": seat,
    }
    policy = factory(run_context=context)
    ledger = None
    candidate = policy
    if with_ledger:
        ledger = E17CommandLedger(
            {
                "episode_id": context["episode_id"],
                "seed": seed,
                "seat": seat,
                "player_id": seat,
                "policy_version": REACTIVE_MODEL_SPEC_VERSION,
                "source_hash": _sha256_file(SOURCE_PATH),
                "config_hash": _sha256_file(DEFAULT_REACTIVE_CONFIG_PATH),
                "routine_hash": "PARENT_V9_C2466262",
            }
        )
        candidate = instrument_policy(policy, ledger)
    agents = [candidate, inert_pass_policy] if seat == 0 else [inert_pass_policy, candidate]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    terminal = _terminal(env, seat)
    if ledger is not None:
        ledger.finalize(terminal["observation"])
    if hasattr(policy, "codex_e17_instance"):
        instance = policy.codex_e17_instance
        telemetry = instance.telemetry_snapshot()
        errors = instance.error_count + instance.base_policy.codex_v9_instance.error_count
        fallbacks = instance.fallback_count + instance.base_policy.codex_v9_instance.fallback_count
    else:
        instance = policy.codex_v9_instance
        telemetry = instance.telemetry_snapshot()
        errors = instance.error_count
        fallbacks = instance.fallback_count
    return {
        "reward": terminal["reward"],
        "status": terminal["status"],
        "errors": errors,
        "fallbacks": fallbacks,
        "telemetry": telemetry,
        "ledger": ledger,
    }


def run_development(seeds: list[int]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for seed in seeds:
        for seat in (0, 1):
            print(f"RUN seed={seed} seat={seat} V9", flush=True)
            baseline = _run_policy(
                create_v9_agent,
                seed=seed,
                seat=seat,
                label="V9",
                with_ledger=False,
            )
            print(f"RUN seed={seed} seat={seat} REACTIVE", flush=True)
            reactive = _run_policy(
                create_codex_e17_reactive_agent,
                seed=seed,
                seat=seat,
                label="CODEX-REACTIVE",
                with_ledger=True,
            )
            ledger: E17CommandLedger = reactive.pop("ledger")
            ledger_metrics = ledger.metrics()
            run_id = f"E17-1-CODEX-REACTIVE-S{seed}-P{seat}"
            _write_jsonl(RUN_ROOT / f"{run_id}.ledger.jsonl", ledger.records)
            _write_json(RUN_ROOT / f"{run_id}.derived_events.json", ledger.derived_events)
            row = {
                "run_id": run_id,
                "seed": seed,
                "seat": seat,
                "opponent": "INERT_PASS_POLICY",
                "baseline_reward": baseline["reward"],
                "reactive_reward": reactive["reward"],
                "reward_delta": reactive["reward"] - baseline["reward"],
                "baseline_status": baseline["status"],
                "reactive_status": reactive["status"],
                "baseline_errors": baseline["errors"],
                "reactive_errors": reactive["errors"],
                "baseline_fallbacks": baseline["fallbacks"],
                "reactive_fallbacks": reactive["fallbacks"],
                "reactive_override_batches": reactive["telemetry"]["reactive_override_batches"],
                "reactive_override_reasons": reactive["telemetry"]["reactive_override_reasons"],
                "max_quadrants": reactive["telemetry"]["max_quadrants"],
                "max_hands": reactive["telemetry"]["max_hands"],
                "max_active_animals": reactive["telemetry"]["max_active_animals"],
                "q1_activation_day": reactive["telemetry"]["Q1_activation_day"],
                "q2_activation_day": reactive["telemetry"]["Q2_activation_day"],
                "ledger_metrics": ledger_metrics,
            }
            _write_json(RUN_ROOT / f"{run_id}.summary.json", row)
            rows.append(row)
            print(
                f"DONE base={baseline['reward']:.0f} reactive={reactive['reward']:.0f} "
                f"delta={row['reward_delta']:+.0f} overrides={row['reactive_override_batches']}",
                flush=True,
            )

    rewards = [row["reactive_reward"] for row in rows]
    base_rewards = [row["baseline_reward"] for row in rows]
    total_escapes = sum(
        int(row["ledger_metrics"]["derived_eod_escape_count"]) for row in rows
    )
    technical_errors = sum(
        int(row["reactive_errors"]) + int(row["ledger_metrics"]["technical_errors"])
        for row in rows
    )
    gate = {
        "technical_errors_zero": technical_errors == 0,
        "fallbacks_zero": all(row["reactive_fallbacks"] == 0 for row in rows),
        "animal_escapes_zero": total_escapes == 0,
        "ledger_record_coverage_full": all(
            row["ledger_metrics"]["ledger_record_coverage"] == 1.0 for row in rows
        ),
        "three_quadrants_all_runs": all(row["max_quadrants"] >= 3 for row in rows),
        "mean_final_money_at_least_50000": statistics.mean(rewards) >= 50000,
        "reactivity_unit_tests_required": True,
    }
    passed = all(gate.values())
    metrics = {
        "schema_version": "E17_1_CODEX_REACTIVE_DEVELOPMENT_METRICS_V1",
        "candidate_id": "CODEX_E17_1_3Q_REACTIVE_GUARDED_V1",
        "policy_version": REACTIVE_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY",
        "status": "PASS" if passed else "FAIL",
        "epistemic_role": "DEVELOPMENT_ONLY",
        "seeds": seeds,
        "seats": [0, 1],
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "runs": len(rows),
        "reactive_mean_final_money": statistics.mean(rewards),
        "reactive_median_final_money": statistics.median(rewards),
        "reactive_min_final_money": min(rewards),
        "reactive_max_final_money": max(rewards),
        "baseline_mean_final_money": statistics.mean(base_rewards),
        "mean_delta_vs_v9": statistics.mean(rewards) - statistics.mean(base_rewards),
        "positive_delta_runs": sum(row["reward_delta"] > 0 for row in rows),
        "neutral_delta_runs": sum(row["reward_delta"] == 0 for row in rows),
        "negative_delta_runs": sum(row["reward_delta"] < 0 for row in rows),
        "reactive_override_batches": sum(
            row["reactive_override_batches"] for row in rows
        ),
        "derived_eod_escape_count": total_escapes,
        "technical_errors": technical_errors,
        "gate": gate,
        "results": rows,
    }
    _write_json(DERIVED_PATH, metrics)
    if passed:
        FREEZE_ROOT.mkdir(parents=True, exist_ok=True)
        frozen_source = FREEZE_ROOT / SOURCE_PATH.name
        frozen_config = FREEZE_ROOT / DEFAULT_REACTIVE_CONFIG_PATH.name
        shutil.copy2(SOURCE_PATH, frozen_source)
        shutil.copy2(DEFAULT_REACTIVE_CONFIG_PATH, frozen_config)
        freeze = {
            "schema_version": "E17_1_CODEX_REACTIVE_FREEZE_V1",
            "candidate_id": metrics["candidate_id"],
            "policy_version": REACTIVE_MODEL_SPEC_VERSION,
            "status": "FROZEN_FOR_REACTIVE_TOURNAMENT",
            "epistemic_role": "DEVELOPMENT_FREEZE",
            "source_path": str(SOURCE_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
            "source_sha256": _sha256_file(SOURCE_PATH),
            "config_path": str(DEFAULT_REACTIVE_CONFIG_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
            "config_sha256": _sha256_file(DEFAULT_REACTIVE_CONFIG_PATH),
            "frozen_source_path": str(frozen_source.relative_to(REPO_ROOT)).replace("\\", "/"),
            "frozen_source_sha256": _sha256_file(frozen_source),
            "frozen_config_path": str(frozen_config.relative_to(REPO_ROOT)).replace("\\", "/"),
            "frozen_config_sha256": _sha256_file(frozen_config),
            "development_metrics_path": str(DERIVED_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
            "development_metrics_sha256": _sha256_file(DERIVED_PATH),
            "holdout_consumed": False,
            "final_confirmation_consumed": False,
        }
        _write_json(FREEZE_ROOT / "E17_1_FREEZE_MANIFEST.json", freeze)
    return metrics


def main(argv: list[str] | None = None) -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=manifest["seed_policy"]["development"],
    )
    args = parser.parse_args(argv)
    forbidden = set(manifest["seed_policy"]["holdout"]["seeds"]) | set(
        manifest["seed_policy"]["final_confirmation"]["seeds"]
    )
    if forbidden.intersection(args.seeds):
        raise SystemExit("holdout/final seeds are forbidden in development")
    metrics = run_development(args.seeds)
    print(
        json.dumps(
            {
                key: metrics[key]
                for key in (
                    "status",
                    "runs",
                    "reactive_mean_final_money",
                    "baseline_mean_final_money",
                    "mean_delta_vs_v9",
                    "reactive_override_batches",
                    "derived_eod_escape_count",
                    "technical_errors",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if metrics["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
