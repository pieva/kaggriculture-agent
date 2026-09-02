"""Run and freeze the Copilot-native E17.0 baseline on development seeds only."""

from __future__ import annotations

import ast
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import kaggle_environments

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.e17_ledger import (
    E17CommandLedger,
    LEDGER_SCHEMA_VERSION,
    canonical_sha256,
    instrument_policy,
)
from agricola.strategy.copilot.e17_native_3q import (
    POLICY_VERSION,
    create_native_agent,
    native_policy_fingerprint,
)

SEEDS = (26090101, 26090102, 26090103)
SEATS = (0, 1)
EPISODE_STEPS = 720
CODEX_ROUTINE_SHA256 = "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"
SOURCE_PATH = SRC_ROOT / "agricola" / "strategy" / "copilot" / "e17_native_3q.py"
CONFIG_PATH = REPOSITORY_ROOT / "experiments" / "e17" / "configs" / "copilot" / "COPILOT_E17_0_NATIVE_3Q_V1.json"
TOOL_PATH = Path(__file__).resolve()
TEST_PATH = REPOSITORY_ROOT / "experiments" / "e17" / "tests" / "test_copilot_e17_0_native.py"
RUNS_DIR = REPOSITORY_ROOT / "experiments" / "e17" / "artifacts" / "runs" / "copilot" / "e17_0"
DERIVED_DIR = REPOSITORY_ROOT / "experiments" / "e17" / "artifacts" / "derived" / "copilot"
FREEZE_DIR = REPOSITORY_ROOT / "experiments" / "e17" / "artifacts" / "freeze" / "copilot"
METRICS_PATH = DERIVED_DIR / "E17_0_METRICS.json"
FREEZE_MANIFEST_PATH = FREEZE_DIR / "E17_0_FREEZE_MANIFEST.json"
FROZEN_SOURCE_PATH = FREEZE_DIR / "COPILOT_E17_0_NATIVE_3Q_V1.py"
FROZEN_CONFIG_PATH = FREEZE_DIR / "COPILOT_E17_0_NATIVE_3Q_V1.json"


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(
                json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                + "\n"
            )


def _final_observation(env: Any, seat: int) -> dict[str, Any]:
    observation = env.steps[-1][seat].get("observation", {})
    return observation if isinstance(observation, dict) else dict(observation)


def _independence_audit() -> dict[str, Any]:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    prohibited_imports = sorted(
        name
        for name in imports
        if name.startswith("agricola.strategy.codex")
        or name.startswith("agricola.strategy.antigravity")
    )
    prohibited_tokens = [
        token
        for token in (
            "ROUTINE_ACTIONS",
            "codex_v9_routine_data",
            "antigravity_3q",
        )
        if token in source
    ]
    fingerprint = native_policy_fingerprint()
    return {
        "imports": imports,
        "prohibited_imports": prohibited_imports,
        "prohibited_tokens": prohibited_tokens,
        "no_import_other_agent_routine": not prohibited_imports,
        "no_copy_other_agent_action_table": "ROUTINE_ACTIONS" not in source,
        "no_external_planner_dispatcher_or_schedule": not prohibited_tokens,
        "native_routine_fingerprint": fingerprint,
        "codex_routine_fingerprint": CODEX_ROUTINE_SHA256,
        "routine_fingerprint_distinct": fingerprint != CODEX_ROUTINE_SHA256,
    }


def _quadrant_activity(records: list[dict[str, Any]]) -> list[str]:
    productive = {"PLANT", "WATER", "HARVEST", "DIG"}
    return sorted(
        {
            str(record["quadrant_slot"])
            for record in records
            if record.get("quadrant_slot") in {"Q0", "Q1", "Q2"}
            and record.get("requested_command") in productive
        }
    )


def _run_once(seed: int, seat: int, episode_id: str) -> tuple[E17CommandLedger, dict[str, Any]]:
    source_hash = _file_sha256(SOURCE_PATH)
    config_hash = _file_sha256(CONFIG_PATH)
    policy = create_native_agent(CONFIG_PATH)
    ledger = E17CommandLedger(
        {
            "episode_id": episode_id,
            "seed": seed,
            "seat": seat,
            "player_id": seat,
            "policy_version": POLICY_VERSION,
            "source_hash": source_hash,
            "config_hash": config_hash,
            "routine_hash": native_policy_fingerprint(),
        }
    )
    instrumented = instrument_policy(policy, ledger)
    agents = [inert_pass_policy, inert_pass_policy]
    agents[seat] = instrumented
    env = kaggle_environments.make(
        "kaggriculture",
        configuration={"episodeSteps": EPISODE_STEPS, "seed": seed},
    )
    env.run(agents)
    final_observation = _final_observation(env, seat)
    ledger.finalize(final_observation)
    terminal = env.steps[-1]
    own = terminal[seat]
    opponent = terminal[1 - seat]
    metrics = ledger.metrics()
    command_counts = Counter(record["requested_command"] for record in ledger.records)
    farms = final_observation.get("farms", []) or []
    farm = farms[seat] if seat < len(farms) else {}
    unlocked = list(farm.get("unlocked_quadrants", []) or [])
    reproducibility_payload = {
        "actions": ledger.action_batches,
        "farm": farm,
        "private": final_observation.get("private", {}),
        "market": final_observation.get("market", {}),
        "own_reward": own.get("reward"),
        "opponent_reward": opponent.get("reward"),
    }
    summary = {
        "schema_version": "E17_0_COPILOT_RUN_SUMMARY_V1",
        "episode_id": episode_id,
        "seed": seed,
        "seat": seat,
        "opponent_id": "INERT_PASS_POLICY",
        "policy_id": POLICY_VERSION,
        "source_sha256": source_hash,
        "config_sha256": config_hash,
        "native_routine_fingerprint": native_policy_fingerprint(),
        "status": own.get("status"),
        "opponent_status": opponent.get("status"),
        "final_money": float(own.get("reward") or 0.0),
        "opponent_final_money": float(opponent.get("reward") or 0.0),
        "recorded_environment_states": len(env.steps),
        "policy_technical_errors": policy.technical_errors,
        "ledger": metrics,
        "command_counts": dict(sorted(command_counts.items())),
        "unlocked_quadrants": unlocked,
        "operated_quadrants": _quadrant_activity(ledger.records),
        "ledger_sha256": canonical_sha256(ledger.records),
        "derived_events_sha256": canonical_sha256(ledger.derived_events),
        "reproducibility_sha256": canonical_sha256(reproducibility_payload),
    }
    return ledger, summary


def _persist_run(ledger: E17CommandLedger, summary: dict[str, Any]) -> dict[str, str]:
    stem = summary["episode_id"]
    ledger_path = RUNS_DIR / f"{stem}.ledger.jsonl"
    events_path = RUNS_DIR / f"{stem}.derived_events.json"
    summary_path = RUNS_DIR / f"{stem}.summary.json"
    _write_jsonl(ledger_path, ledger.records)
    _write_json(
        events_path,
        {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "episode_id": stem,
            "events": ledger.derived_events,
        },
    )
    _write_json(summary_path, summary)
    return {
        "ledger_path": ledger_path.relative_to(REPOSITORY_ROOT).as_posix(),
        "ledger_sha256": _file_sha256(ledger_path),
        "derived_events_path": events_path.relative_to(REPOSITORY_ROOT).as_posix(),
        "derived_events_sha256": _file_sha256(events_path),
        "summary_path": summary_path.relative_to(REPOSITORY_ROOT).as_posix(),
        "summary_sha256": _file_sha256(summary_path),
    }


def main() -> int:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    FREEZE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_PATH, FROZEN_SOURCE_PATH)
    shutil.copyfile(CONFIG_PATH, FROZEN_CONFIG_PATH)

    source_hash = _file_sha256(SOURCE_PATH)
    config_hash = _file_sha256(CONFIG_PATH)
    freeze_source_hash = _file_sha256(FROZEN_SOURCE_PATH)
    freeze_config_hash = _file_sha256(FROZEN_CONFIG_PATH)
    independence = _independence_audit()
    run_summaries: list[dict[str, Any]] = []
    run_artifacts: list[dict[str, str]] = []

    for seed in SEEDS:
        for seat in SEATS:
            episode_id = f"E17-0-COPILOT-S{seed}-P{seat}"
            ledger, primary = _run_once(seed, seat, episode_id)
            _repeat_ledger, repeated = _run_once(seed, seat, episode_id)
            primary["reproducibility"] = {
                "action_sequence_match": primary["ledger"]["action_sequence_sha256"]
                == repeated["ledger"]["action_sequence_sha256"],
                "ledger_match": primary["ledger_sha256"] == repeated["ledger_sha256"],
                "terminal_match": primary["reproducibility_sha256"]
                == repeated["reproducibility_sha256"],
                "final_money_match": primary["final_money"] == repeated["final_money"],
            }
            primary["reproducibility"]["pass"] = all(
                primary["reproducibility"].values()
            )
            run_artifacts.append(_persist_run(ledger, primary))
            run_summaries.append(primary)
            print(
                f"{episode_id}: money={primary['final_money']:.0f} "
                f"records={primary['ledger']['ledger_records']} "
                f"coverage={primary['ledger']['ledger_record_coverage']:.3f} "
                f"3q={primary['operated_quadrants']} "
                f"repro={primary['reproducibility']['pass']}",
                flush=True,
            )

    total_records = sum(item["ledger"]["ledger_records"] for item in run_summaries)
    total_emitted = sum(item["ledger"]["emitted_commands"] for item in run_summaries)
    total_market = sum(item["ledger"]["market_records"] for item in run_summaries)
    total_market_classified = sum(
        sum(
            item["ledger"]["market_outcome_counts"][outcome]
            for outcome in ("EXECUTED", "NOT_EXECUTED")
        )
        for item in run_summaries
    )
    money = [item["final_money"] for item in run_summaries]
    technical_errors = sum(
        item["policy_technical_errors"] + item["ledger"]["technical_errors"]
        for item in run_summaries
    ) + sum(item["status"] != "DONE" for item in run_summaries)
    escapes = sum(item["ledger"]["derived_eod_escape_count"] for item in run_summaries)
    gates = {
        "development_matrix_complete": len(run_summaries) == len(SEEDS) * len(SEATS),
        "technical_errors_zero": technical_errors == 0,
        "ledger_record_coverage_100_percent": total_records == total_emitted and total_records > 0,
        "derived_eod_escape_count_zero": escapes == 0,
        "three_quadrant_operation_all_runs": all(
            item["operated_quadrants"] == ["Q0", "Q1", "Q2"]
            for item in run_summaries
        ),
        "deterministic_reproducibility": all(
            item["reproducibility"]["pass"] for item in run_summaries
        ),
        "source_config_freeze": source_hash == freeze_source_hash
        and config_hash == freeze_config_hash,
        "no_import_other_agent_routine": independence["no_import_other_agent_routine"],
        "no_copy_other_agent_action_table": independence["no_copy_other_agent_action_table"],
        "no_external_planner_dispatcher_or_schedule": independence["no_external_planner_dispatcher_or_schedule"],
        "routine_fingerprint_distinct": independence["routine_fingerprint_distinct"],
        "holdout_not_consumed": True,
        "final_confirmation_not_consumed": True,
        "no_post_hoc_seed_removal": [item["seed"] for item in run_summaries]
        == [seed for seed in SEEDS for _seat in SEATS],
    }
    gate_pass = all(gates.values())
    aggregate = {
        "schema_version": "E17_0_COPILOT_METRICS_V1",
        "experiment_id": "E17.0",
        "agent_owner": "COPILOT",
        "policy_id": POLICY_VERSION,
        "baseline_role": "NATIVE_BASELINE_CONSTRUCTION",
        "opponent_id": "INERT_PASS_POLICY",
        "development_seeds": list(SEEDS),
        "seats": list(SEATS),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "episode_count": len(run_summaries),
        "final_money": {
            "mean": mean(money),
            "median": median(money),
            "min": min(money),
            "max": max(money),
            "population_stddev": pstdev(money),
        },
        "ledger": {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "records": total_records,
            "emitted_commands": total_emitted,
            "record_coverage": total_records / total_emitted if total_emitted else 0.0,
            "market_records": total_market,
            "market_classified_outcome_coverage": total_market_classified / total_market if total_market else 1.0,
            "derived_eod_escape_count": escapes,
            "technical_errors": technical_errors,
        },
        "independence_audit": independence,
        "source_sha256": source_hash,
        "config_sha256": config_hash,
        "native_routine_fingerprint": native_policy_fingerprint(),
        "gates": gates,
        "gate_status": "PASS" if gate_pass else "FAIL",
        "runs": run_summaries,
    }
    _write_json(METRICS_PATH, aggregate)

    freeze_manifest = {
        "schema_version": "E17_0_COPILOT_FREEZE_MANIFEST_V1",
        "experiment_id": "E17.0",
        "agent_owner": "COPILOT",
        "policy_id": POLICY_VERSION,
        "status": "FROZEN_PASS" if gate_pass else "FROZEN_WITH_FAILED_GATES",
        "source": {
            "path": SOURCE_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
            "sha256": source_hash,
            "frozen_path": FROZEN_SOURCE_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
            "frozen_sha256": freeze_source_hash,
        },
        "config": {
            "path": CONFIG_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
            "sha256": config_hash,
            "frozen_path": FROZEN_CONFIG_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
            "frozen_sha256": freeze_config_hash,
        },
        "tool": {
            "path": TOOL_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
            "sha256": _file_sha256(TOOL_PATH),
        },
        "test": {
            "path": TEST_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
            "sha256": _file_sha256(TEST_PATH),
        },
        "ledger_schema": {
            "version": LEDGER_SCHEMA_VERSION,
            "path": "src/agricola/core/e17_ledger.py",
            "sha256": _file_sha256(SRC_ROOT / "agricola" / "core" / "e17_ledger.py"),
        },
        "opponent": {
            "id": "INERT_PASS_POLICY",
            "path": "src/agricola/core/benchmark_opponents.py",
            "sha256": _file_sha256(SRC_ROOT / "agricola" / "core" / "benchmark_opponents.py"),
        },
        "native_routine_fingerprint": native_policy_fingerprint(),
        "independence_audit": independence,
        "development_matrix": {
            "seeds": list(SEEDS),
            "seats": list(SEATS),
            "opponent": "INERT_PASS_POLICY",
            "failed_run_replacement": "FORBIDDEN",
        },
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "metrics": {
            "path": METRICS_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
            "sha256": _file_sha256(METRICS_PATH),
        },
        "run_artifacts": run_artifacts,
        "gates": gates,
        "gate_status": aggregate["gate_status"],
    }
    _write_json(FREEZE_MANIFEST_PATH, freeze_manifest)
    print(f"GATE_STATUS={aggregate['gate_status']}")
    print(f"METRICS={METRICS_PATH.relative_to(REPOSITORY_ROOT).as_posix()}")
    print(f"FREEZE={FREEZE_MANIFEST_PATH.relative_to(REPOSITORY_ROOT).as_posix()}")
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
