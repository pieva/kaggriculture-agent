"""Development-only validation runner for the Claude E17.1 reactive candidate.

Runs seat 0 and seat 1 against ``INERT_PASS_POLICY`` on the seven E17
development seeds only (never holdout or final-confirmation seeds), records
every run, and checks the admission gates declared in
``docs/model_specs/claude/e17/prompts/E17_CLAUDE_REACTIVE_3Q_INDEPENDENT_BUILD_PROMPT.md``.
"""

from __future__ import annotations

import ast
import hashlib
import json
import shutil
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import kaggle_environments

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.e17_ledger import (
    LEDGER_SCHEMA_VERSION,
    E17CommandLedger,
    canonical_sha256,
    instrument_policy,
)
from agricola.strategy.claude.e17_reactive_3q import (
    DEFAULT_CONFIG_PATH,
    POLICY_VERSION,
    claude_policy_fingerprint,
    create_claude_e17_agent,
)

# Development seeds only (E17_STRATEGY_FROZEN_V1.md Sec. 7); holdout and
# final-confirmation seeds are never referenced here.
DEVELOPMENT_SEEDS = (
    26090101,
    26090102,
    26090103,
    1838889274,
    1619968655,
    710418712,
    562040596,
)
SEATS = (0, 1)
EPISODE_STEPS = 720
DEVELOPMENT_MONEY_TARGET = 50000.0

CODEX_ROUTINE_SHA256 = "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"
SOURCE_PATH = SRC_ROOT / "agricola" / "strategy" / "claude" / "e17_reactive_3q.py"
CONFIG_PATH = DEFAULT_CONFIG_PATH
MODEL_SPEC_PATH = (
    REPOSITORY_ROOT
    / "docs"
    / "model_specs"
    / "claude"
    / "MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE.md"
)
TOOL_PATH = Path(__file__).resolve()
TEST_PATH = (
    REPOSITORY_ROOT / "docs" / "model_specs" / "claude" / "e17" / "tests" / "test_claude_e17_1_reactive.py"
)
RUNS_DIR = REPOSITORY_ROOT / "docs" / "model_specs" / "claude" / "e17" / "artifacts" / "runs" / "e17_1"
DERIVED_DIR = REPOSITORY_ROOT / "docs" / "model_specs" / "claude" / "e17" / "artifacts" / "derived"
FREEZE_DIR = REPOSITORY_ROOT / "docs" / "model_specs" / "claude" / "e17" / "artifacts" / "freeze"
METRICS_PATH = DERIVED_DIR / "E17_1_METRICS.json"
FREEZE_MANIFEST_PATH = FREEZE_DIR / "E17_1_FREEZE_MANIFEST.json"
FROZEN_SOURCE_PATH = FREEZE_DIR / "CLAUDE_E17_1_3Q_REACTIVE_V1.py"
FROZEN_CONFIG_PATH = FREEZE_DIR / "CLAUDE_E17_1_3Q_REACTIVE_V1.json"


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
    prohibited_prefixes = (
        "agricola.strategy.codex",
        "agricola.strategy.antigravity",
        "agricola.strategy.copilot",
    )
    prohibited_imports = sorted(
        name for name in imports if name.startswith(prohibited_prefixes)
    )
    prohibited_tokens = [
        token
        for token in ("ROUTINE_ACTIONS", "codex_v9_routine_data", "antigravity_3q")
        if token in source
    ]
    fingerprint = claude_policy_fingerprint()
    return {
        "imports": imports,
        "prohibited_imports": prohibited_imports,
        "prohibited_tokens": prohibited_tokens,
        "no_import_other_agent_routine": not prohibited_imports,
        "no_copy_other_agent_action_table": "ROUTINE_ACTIONS" not in source,
        "no_external_planner_dispatcher_or_schedule": not prohibited_tokens,
        "claude_policy_fingerprint": fingerprint,
        "codex_v9_routine_fingerprint": CODEX_ROUTINE_SHA256,
        "fingerprint_distinct_from_codex_routine": fingerprint != CODEX_ROUTINE_SHA256,
    }


def _state_reactivity_check() -> dict[str, Any]:
    """Two observations at the same step, differing only in whether the
    farmer stands on an unwatered PLANT tile, must yield a different and
    explainable farmer command (WATER vs. something else)."""

    agent = create_claude_e17_agent()
    configuration = {
        "episodeSteps": EPISODE_STEPS,
        "turnsPerDay": 24,
        "boardSize": 10,
        "maxMarketOrdersPerTurn": 10,
        "shedCapacity": 100,
    }
    tiles = [[None if y < 5 and x < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    farm = {
        "money": 3000.0,
        "farmer": [4, 4],
        "hands": [],
        "tiles": tiles,
        "unlocked_quadrants": ["NW"],
        "hires_today": 0,
    }
    base_observation = {
        "step": 100,
        "day": 100 // 24,
        "hour": 100 % 24,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
        "market": {"inventory": {}, "prices": {"WHEAT": 25}},
    }
    baseline_action = agent(deepcopy(base_observation), configuration)

    thirsty_observation = deepcopy(base_observation)
    thirsty_observation["farms"][0]["tiles"][4][4] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 3,
        "watered_today": False,
        "consecutive_unwatered": 1,
        "yield_units": 1,
        "max_lifespan_step": 10_000,
        "fertilized_until_day": -1,
    }
    thirsty_action = agent(thirsty_observation, configuration)

    explained = thirsty_action["farmer"] == ["WATER"]
    differs = baseline_action["farmer"] != thirsty_action["farmer"]
    return {
        "same_step": 100,
        "baseline_farmer_command": baseline_action["farmer"],
        "thirsty_farmer_command": thirsty_action["farmer"],
        "differs": differs,
        "explained_by_urgent_water_guard": explained,
        "pass": bool(differs and explained),
    }


def _ledger_action_parity_check() -> dict[str, Any]:
    """The E17 ledger wrapper must never change the wrapped policy's action."""

    reference = create_claude_e17_agent()
    wrapped_policy = create_claude_e17_agent()
    ledger = E17CommandLedger(
        {
            "episode_id": "E17-1-CLAUDE-PARITY-CHECK",
            "seed": DEVELOPMENT_SEEDS[0],
            "seat": 0,
            "policy_version": POLICY_VERSION,
            "source_hash": "SOURCE",
            "config_hash": "CONFIG",
            "routine_hash": claude_policy_fingerprint(),
        }
    )
    wrapped = instrument_policy(wrapped_policy, ledger)
    configuration = {
        "episodeSteps": EPISODE_STEPS,
        "turnsPerDay": 24,
        "boardSize": 10,
        "maxMarketOrdersPerTurn": 10,
        "shedCapacity": 100,
    }
    tiles = [[None if y < 5 and x < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    mismatches = 0
    for step in (0, 1, 24, 48, 100):
        farm = {
            "money": 3000.0 + step,
            "farmer": [4, 4],
            "hands": [[3, 3]] if step > 24 else [],
            "tiles": tiles,
            "unlocked_quadrants": ["NW"],
            "hires_today": 0,
        }
        observation = {
            "step": step,
            "day": step // 24,
            "hour": step % 24,
            "player": 0,
            "farms": [farm, deepcopy(farm)],
            "private": {"shed": {}, "seeds": {}, "inventories": [{}, {}]},
            "market": {"inventory": {}, "prices": {"WHEAT": 25}},
        }
        wrapped_action = wrapped(deepcopy(observation), configuration)
        reference_action = reference(deepcopy(observation), configuration)
        if wrapped_action != reference_action:
            mismatches += 1
    return {
        "steps_checked": 5,
        "mismatches": mismatches,
        "ledger_records": len(ledger.records),
        "ledger_errors": len(ledger.errors),
        "pass": mismatches == 0 and not ledger.errors,
    }


def _quadrant_activity(records: list[dict[str, Any]]) -> list[str]:
    productive = {"PLANT", "WATER", "HARVEST", "DIG", "BUILD_COOP", "BUILD_PASTURE", "PLACE", "FEED"}
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
    policy = create_claude_e17_agent(config_path=CONFIG_PATH)
    ledger = E17CommandLedger(
        {
            "episode_id": episode_id,
            "seed": seed,
            "seat": seat,
            "player_id": seat,
            "policy_version": POLICY_VERSION,
            "source_hash": source_hash,
            "config_hash": config_hash,
            "routine_hash": claude_policy_fingerprint(),
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
    invalid_batches = sum(
        1
        for entry in ledger.action_batches
        if not isinstance(entry.get("action", {}).get("farmer"), list)
        or not entry["action"]["farmer"]
        or len(entry["action"].get("market", [])) > 10
    )
    reproducibility_payload = {
        "actions": ledger.action_batches,
        "farm": farm,
        "private": final_observation.get("private", {}),
        "market": final_observation.get("market", {}),
        "own_reward": own.get("reward"),
        "opponent_reward": opponent.get("reward"),
    }
    summary = {
        "schema_version": "E17_1_CLAUDE_RUN_SUMMARY_V1",
        "episode_id": episode_id,
        "seed": seed,
        "seat": seat,
        "opponent_id": "INERT_PASS_POLICY",
        "policy_id": POLICY_VERSION,
        "source_sha256": source_hash,
        "config_sha256": config_hash,
        "claude_policy_fingerprint": claude_policy_fingerprint(),
        "status": own.get("status"),
        "opponent_status": opponent.get("status"),
        "final_money": float(own.get("reward") or 0.0),
        "opponent_final_money": float(opponent.get("reward") or 0.0),
        "recorded_environment_states": len(env.steps),
        "policy_technical_errors": policy.technical_errors,
        "invalid_batches": invalid_batches,
        "ledger": metrics,
        "command_counts": dict(sorted(command_counts.items())),
        "unlocked_quadrants": unlocked,
        "max_quadrants": len(unlocked),
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
    reactivity = _state_reactivity_check()
    ledger_parity = _ledger_action_parity_check()

    run_summaries: list[dict[str, Any]] = []
    run_artifacts: list[dict[str, str]] = []

    for seed in DEVELOPMENT_SEEDS:
        for seat in SEATS:
            episode_id = f"E17-1-CLAUDE-S{seed}-P{seat}"
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
            primary["reproducibility"]["pass"] = all(primary["reproducibility"].values())
            run_artifacts.append(_persist_run(ledger, primary))
            run_summaries.append(primary)
            print(
                f"{episode_id}: money={primary['final_money']:.0f} "
                f"records={primary['ledger']['ledger_records']} "
                f"coverage={primary['ledger']['ledger_record_coverage']:.3f} "
                f"quadrants={primary['unlocked_quadrants']} "
                f"escapes={primary['ledger']['derived_eod_escape_count']} "
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
    invalid_batches = sum(item["invalid_batches"] for item in run_summaries)
    escapes = sum(item["ledger"]["derived_eod_escape_count"] for item in run_summaries)
    max_quadrants_all = [item["max_quadrants"] for item in run_summaries]

    gates = {
        "development_matrix_complete": len(run_summaries)
        == len(DEVELOPMENT_SEEDS) * len(SEATS),
        "technical_errors_zero": technical_errors == 0,
        "invalid_batches_zero": invalid_batches == 0,
        "ledger_record_coverage_100_percent": total_records == total_emitted
        and total_records > 0,
        "animal_escapes_zero": escapes == 0,
        "max_quadrants_equal_3_all_runs": all(q == 3 for q in max_quadrants_all),
        "development_mean_final_money_ge_target": mean(money) >= DEVELOPMENT_MONEY_TARGET,
        "deterministic_reproducibility": all(
            item["reproducibility"]["pass"] for item in run_summaries
        ),
        "state_reactivity_test_pass": reactivity["pass"],
        "ledger_action_parity_pass": ledger_parity["pass"],
        "source_config_freeze": source_hash == freeze_source_hash
        and config_hash == freeze_config_hash,
        "no_import_other_agent_routine": independence["no_import_other_agent_routine"],
        "no_copy_other_agent_action_table": independence["no_copy_other_agent_action_table"],
        "no_external_planner_dispatcher_or_schedule": independence[
            "no_external_planner_dispatcher_or_schedule"
        ],
        "fingerprint_distinct_from_codex_routine": independence[
            "fingerprint_distinct_from_codex_routine"
        ],
        "holdout_not_consumed": True,
        "final_confirmation_not_consumed": True,
        "no_post_hoc_seed_removal": [item["seed"] for item in run_summaries]
        == [seed for seed in DEVELOPMENT_SEEDS for _seat in SEATS],
    }
    economic_gates_pass = gates["development_mean_final_money_ge_target"] and gates[
        "max_quadrants_equal_3_all_runs"
    ]
    technical_gate_pass = all(
        value for key, value in gates.items()
        if key not in {"development_mean_final_money_ge_target", "max_quadrants_equal_3_all_runs"}
    )
    gate_pass = technical_gate_pass and economic_gates_pass

    aggregate = {
        "schema_version": "E17_1_CLAUDE_METRICS_V1",
        "experiment_id": "E17.1",
        "agent_owner": "CLAUDE",
        "policy_id": POLICY_VERSION,
        "role": "REACTIVE_INDEPENDENT_CANDIDATE",
        "opponent_id": "INERT_PASS_POLICY",
        "development_seeds": list(DEVELOPMENT_SEEDS),
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
            "market_classified_outcome_coverage": (
                total_market_classified / total_market if total_market else 1.0
            ),
            "derived_eod_escape_count": escapes,
            "technical_errors": technical_errors,
            "invalid_batches": invalid_batches,
        },
        "independence_audit": independence,
        "state_reactivity_check": reactivity,
        "ledger_action_parity_check": ledger_parity,
        "source_sha256": source_hash,
        "config_sha256": config_hash,
        "claude_policy_fingerprint": claude_policy_fingerprint(),
        "gates": gates,
        "technical_gate_status": "PASS" if technical_gate_pass else "FAIL",
        "economic_gate_status": "PASS" if economic_gates_pass else "FAIL",
        "gate_status": "PASS" if gate_pass else "FAIL",
        "runs": run_summaries,
    }
    _write_json(METRICS_PATH, aggregate)

    freeze_manifest = {
        "schema_version": "E17_1_CLAUDE_FREEZE_MANIFEST_V1",
        "experiment_id": "E17.1",
        "agent_owner": "CLAUDE",
        "policy_id": POLICY_VERSION,
        "status": "FROZEN_PASS" if gate_pass else "FROZEN_WITH_FAILED_GATES",
        "model_spec": {
            "path": MODEL_SPEC_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
            "sha256": _file_sha256(MODEL_SPEC_PATH),
        },
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
        "claude_policy_fingerprint": claude_policy_fingerprint(),
        "independence_audit": independence,
        "development_matrix": {
            "seeds": list(DEVELOPMENT_SEEDS),
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
    print(f"TECHNICAL_GATE_STATUS={aggregate['technical_gate_status']}")
    print(f"ECONOMIC_GATE_STATUS={aggregate['economic_gate_status']}")
    print(f"GATE_STATUS={aggregate['gate_status']}")
    print(f"METRICS={METRICS_PATH.relative_to(REPOSITORY_ROOT).as_posix()}")
    print(f"FREEZE={FREEZE_MANIFEST_PATH.relative_to(REPOSITORY_ROOT).as_posix()}")
    return 0 if technical_gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
