"""Frozen E16 episode runner, manifest writer, and E0 instrumentation gate."""

from __future__ import annotations

import importlib.util
import json
import platform
import subprocess
import sys
import time
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import kaggle_environments

from agricola.e16.analysis import (
    compute_stage_b_gate,
    load_episode_results,
    validate_complete_matrix,
)
from agricola.e16.config import (
    DEFAULT_CONFIG_PATH,
    REPO_ROOT,
    ConfigError,
    build_run_matrix,
    load_frozen_config,
    resolve_cell,
    sha256_file,
    validate_run_identity,
)
from agricola.e16.telemetry import (
    EngineEventLedger,
    derive_episode_telemetry,
    validate_ledger_schema,
    write_jsonl,
)
from agricola.evaluation.runner import resolve_agent

RESULTS_ROOT = REPO_ROOT / "results" / "e16"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load_treatment(config: dict[str, Any], cell_config: dict[str, Any]) -> Callable:
    path = REPO_ROOT / config["treatment_build_path"]
    module_name = f"e16_treatment_{time.time_ns()}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ConfigError(f"cannot load treatment build: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "create_agent"):
        raise ConfigError("treatment build does not expose create_agent")
    return module.create_agent(cell_config)


def _engine_version() -> str:
    return f"kaggle-environments={getattr(kaggle_environments, '__version__', 'unknown')};python={platform.python_version()}"


def run_frozen_episode(
    config: dict[str, Any],
    *,
    stage: str,
    cell_id: str,
    seed: int,
    treatment_seat: int,
    episode_steps: int = 720,
    c_star: int | None = None,
    training: bool = True,
) -> dict[str, Any]:
    if training:
        validate_run_identity(config, seed=seed, treatment_seat=treatment_seat)
    cell = resolve_cell(config, "stage_a" if stage == "e0" else stage, cell_id, c_star)
    treatment = _load_treatment(config, cell)
    opponent = resolve_agent(str(REPO_ROOT / config["opponent_path"]))
    agents = [treatment, opponent] if treatment_seat == 0 else [opponent, treatment]
    episode_id = (
        f"E16-E0-{cell_id}-S{seed}-P{treatment_seat}"
        if stage == "e0"
        else f"{config.get('replication_id', 'E16') if stage == 'stage_a' else 'E16'}-{cell_id}-S{seed}-P{treatment_seat}"
    )
    metadata = {
        "design_id": config["design_id"],
        "stage": stage,
        "cell_id": cell_id,
        "episode_id": episode_id,
        "seed": seed,
        "treatment_seat": treatment_seat,
        "treatment_build_sha256": config["treatment_build_sha256"],
        "opponent_sha256": config["opponent_sha256"],
        "engine_version": _engine_version(),
        "configuration_sha256": config["configuration_sha256"],
    }
    env = kaggle_environments.make(
        "kaggriculture", configuration={"episodeSteps": episode_steps, "seed": seed}
    )
    started = time.perf_counter()
    with EngineEventLedger(metadata) as instrumentor:
        env.run(agents)
    elapsed = time.perf_counter() - started
    last = env.steps[-1]
    treatment_state = last[treatment_seat]
    opponent_seat = 1 - treatment_seat
    completed = (
        treatment_state.get("status") == "DONE"
        and last[opponent_seat].get("status") == "DONE"
        and len(env.steps) == episode_steps
    )
    telemetry = derive_episode_telemetry(
        env.steps, instrumentor.events, treatment_seat, cell, episode_steps
    )
    result = {
        "design_id": config["design_id"],
        "evidence_role": "TRAINING" if training else "E0_NON_ANALYTIC_SMOKE",
        "stage": stage,
        "cell_id": cell_id,
        "episode_id": episode_id,
        "seed": seed,
        "treatment_seat": treatment_seat,
        "cell_config": cell,
        "completed": completed,
        "treatment_status": treatment_state.get("status"),
        "opponent_status": last[opponent_seat].get("status"),
        "total_steps": len(env.steps),
        "elapsed_seconds": elapsed,
        "telemetry": telemetry,
        "treatment_build_sha256": config["treatment_build_sha256"],
        "opponent_sha256": config["opponent_sha256"],
        "configuration_sha256": config["configuration_sha256"],
        "engine_version": metadata["engine_version"],
        "completed_at": utc_now(),
    }
    return {"result": result, "ledger": instrumentor.events}


def _probe_agent(
    observation: dict[str, Any], configuration: Any = None
) -> dict[str, Any]:
    if int(observation.get("step", 0)) == 0:
        return {
            "farmer": ["WATER"],
            "hands": [],
            "market": [["HIRE"], ["BUY_SEED", "WHEAT", 1000], ["SELL", "MILK", 2]],
        }
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _pass_agent(
    observation: dict[str, Any], configuration: Any = None
) -> dict[str, Any]:
    return {"farmer": ["PASS"], "hands": [], "market": []}


def run_instrumentation_probe(
    config: dict[str, Any], treatment_seat: int = 0
) -> list[dict[str, Any]]:
    metadata = {
        "design_id": config["design_id"],
        "stage": "e0_probe",
        "cell_id": "INSTRUMENTATION_PROBE",
        "episode_id": "E16-E0-INSTRUMENTATION-PROBE",
        "seed": 271828182,
        "treatment_seat": treatment_seat,
        "treatment_build_sha256": config["treatment_build_sha256"],
        "opponent_sha256": config["opponent_sha256"],
        "engine_version": _engine_version(),
        "configuration_sha256": config["configuration_sha256"],
    }
    env = kaggle_environments.make(
        "kaggriculture", configuration={"episodeSteps": 6, "seed": metadata["seed"]}
    )
    agents = (
        [_probe_agent, _pass_agent]
        if treatment_seat == 0
        else [_pass_agent, _probe_agent]
    )
    with EngineEventLedger(metadata) as instrumentor:
        env.run(agents)
    return instrumentor.events


def _check_cash_reconciliation(events: list[dict[str, Any]]) -> bool:
    checked = 0
    for event in events:
        if (
            event["actor_or_order_type"] != "market_order"
            or not event["executed_quantity"]
        ):
            continue
        op = event["requested_payload"][0]
        expected = float(event["realized_value"])
        observed = float(event["cash_after"]) - float(event["cash_before"])
        if op != "SELL":
            observed = -observed
        if abs(observed - expected) > 1e-9:
            return False
        checked += 1
    return checked > 0


def run_e0(config_path: Path | str = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    config = load_frozen_config(config_path)
    e0 = config["e0"]
    smokes = [
        run_frozen_episode(
            config,
            stage="e0",
            cell_id=e0["smoke_cell"],
            seed=int(e0["smoke_seed"]),
            treatment_seat=seat,
            episode_steps=int(e0["episode_steps"]),
            training=False,
        )
        for seat in (0, 1)
    ]
    probe_events = [
        event
        for seat in (0, 1)
        for event in run_instrumentation_probe(config, treatment_seat=seat)
    ]
    all_events = [event for smoke in smokes for event in smoke["ledger"]]
    all_events.extend(probe_events)
    statuses = {event["execution_status"] for event in all_events}
    lifecycle = {
        status for event in all_events for status in event["lifecycle_statuses"]
    }
    treatment_market = [
        event
        for smoke in smokes
        for event in smoke["ledger"]
        if event["actor_role"] == "treatment"
        and event["actor_or_order_type"] == "market_order"
    ]
    unit_events = [
        event for event in all_events if event["actor_or_order_type"] != "market_order"
    ]
    treatment_water = [
        event
        for smoke in smokes
        for event in smoke["ledger"]
        if event["actor_role"] == "treatment"
        and event["actor_or_order_type"] != "market_order"
        and isinstance(event["engine_applied_payload"], list)
        and event["engine_applied_payload"]
        and event["engine_applied_payload"][0] == "WATER"
    ]
    smoke_metrics = [smoke["result"]["telemetry"] for smoke in smokes]

    def watering_metrics_reconcile(metrics: dict[str, Any]) -> bool:
        denominator = int(metrics["watering_need_denominator"])
        effects = int(metrics["successful_watering_effects"])
        expected_rate = effects / denominator if denominator else 0.0
        daily_rates = metrics["daily_watering_execution_rate"]
        productive_days = [
            day
            for day, needs in metrics["daily_watering_need_denominator"].items()
            if needs
        ]
        expected_continuity = (
            sum(float(daily_rates[day]) >= 0.50 for day in productive_days)
            / len(productive_days)
            if productive_days
            else 0.0
        )
        return (
            abs(metrics["watering_execution_rate"] - expected_rate) < 1e-12
            and abs(metrics["watering_continuity"] - expected_continuity) < 1e-12
        )

    checks = {
        "event_ledger_present": bool(all_events),
        "event_ledger_schema": not validate_ledger_schema(all_events),
        "requested_executed_distinction": any(
            event["requested_payload"] != event["executed_payload"]
            for event in all_events
        ),
        "accepted_status": "accepted" in lifecycle,
        "partial_status": "partially_executed" in statuses,
        "executed_status": "executed" in statuses,
        "failed_status": "failed" in statuses,
        "no_op_status": "no_op" in statuses,
        "realized_price_reconciliation": all(
            event["realized_price"] is None
            or abs(
                event["realized_price"] * event["executed_quantity"]
                - event["realized_value"]
            )
            < 1e-9
            for event in all_events
        ),
        "realized_value_reconciliation": any(
            event["realized_value"] for event in all_events
        ),
        "cash_before_after_reconciliation": _check_cash_reconciliation(probe_events),
        "inventory_flow_reconciliation": any(
            event["actor_or_order_type"] == "market_order"
            and event["execution_status"] in {"executed", "partially_executed"}
            and event["relevant_state_before"] != event["relevant_state_after"]
            for event in all_events
        ),
        "failure_reason_coverage": all(
            event["failure_or_noop_reason"]
            for event in all_events
            if event["execution_status"] in {"failed", "no_op", "partially_executed"}
        ),
        "treatment_build_hash": sha256_file(REPO_ROOT / config["treatment_build_path"])
        == config["treatment_build_sha256"],
        "opponent_hash": sha256_file(REPO_ROOT / config["opponent_path"])
        == config["opponent_sha256"],
        "configuration_hash": config["configuration_sha256"]
        == sha256_file(Path(config_path)),
        "unit_player_attribution": bool(unit_events)
        and all(event["player"] in {0, 1} for event in unit_events),
        "unit_seat_consistency": all(
            event["seat"] == event["player"]
            and event["attribution_status"] == "attributed"
            for event in unit_events
        ),
        "treatment_opponent_separation": all(
            {event["actor_role"] for event in smoke["ledger"]}
            == {"treatment", "opponent"}
            for smoke in smokes
        ),
        "both_treatment_seats": {smoke["result"]["treatment_seat"] for smoke in smokes}
        == {0, 1},
        "watering_attribution": bool(treatment_water)
        and all(
            event["player"] == event["treatment_seat"] for event in treatment_water
        ),
        "watering_metric_bounds": all(
            0.0 <= metrics["watering_execution_rate"] <= 1.0
            and 0.0 <= metrics["watering_continuity"] <= 1.0
            for metrics in smoke_metrics
        ),
        "watering_metric_reconciliation": all(
            watering_metrics_reconcile(metrics) for metrics in smoke_metrics
        ),
        "quadrants_owned_numeric_semantics": all(
            isinstance(event["quadrants_owned"], int) for event in treatment_market
        ),
        "quadrants_hard_cap": all(
            (event["quadrants_owned"] or 0) <= 2
            for smoke in smokes
            for event in smoke["ledger"]
            if event["actor_role"] == "treatment"
        ),
        "t0_detection": all(
            smoke["result"]["telemetry"]["t0_step"] is not None for smoke in smokes
        ),
        "seat_detection": all(
            event["treatment_seat"] == smoke["result"]["treatment_seat"]
            for smoke in smokes
            for event in smoke["ledger"]
        ),
        "seed_detection": all(
            event["seed"] == e0["smoke_seed"]
            for smoke in smokes
            for event in smoke["ledger"]
        ),
        "cell_config_allowlist": all(
            set(smoke["result"]["cell_config"])
            >= {
                "watering_dispatch_priority",
                "crop_working_set_target",
                "livestock_headcount_target",
                "pasture_allocation_target",
            }
            for smoke in smokes
        ),
    }
    report = {
        "design_id": config["design_id"],
        "evidence_role": "E0_NON_ANALYTIC_SMOKE",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "smoke_episode": smokes[0]["result"],
        "smoke_episodes": [smoke["result"] for smoke in smokes],
        "event_count": len(all_events),
        "generated_at": utc_now(),
    }
    instrumentation_dir = RESULTS_ROOT / "instrumentation"
    instrumentation_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(instrumentation_dir / "E16_E0_EVENT_LEDGER.jsonl", all_events)
    (instrumentation_dir / "E16_E0_RESULT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


def git_state() -> tuple[str, bool]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return "UNAVAILABLE", True


def write_implementation_manifest(
    config: dict[str, Any], e0_status: str
) -> dict[str, Any]:
    commit, dirty = git_state()
    manifest = {
        "design_id": config["design_id"],
        "evidence_role": "TRAINING",
        "git_commit": commit,
        "git_dirty_state": dirty,
        "treatment_build_path": config["treatment_build_path"],
        "treatment_build_sha256": config["treatment_build_sha256"],
        "opponent_path": config["opponent_path"],
        "opponent_sha256": config["opponent_sha256"],
        "engine_version": _engine_version(),
        "environment_version": getattr(kaggle_environments, "__version__", "unknown"),
        "config_path": config["configuration_path"],
        "config_sha256": config["configuration_sha256"],
        "telemetry_schema_version": config["telemetry_schema_version"],
        "seed_list": config["seed_list"],
        "seat_protocol": config["seat_protocol"],
        "stage_a_cell_ids": list(config["stage_a_cells"]),
        "stage_b_cell_ids": list(config["stage_b_cells"]),
        "instrumentation_gate_status": e0_status,
        "repair_reasons": config.get("repair_reasons", []),
        "semantic_clarification_path": config.get("semantic_clarification_path"),
        "semantic_clarification_sha256": config.get("semantic_clarification_sha256"),
        "predecessor_config_sha256": config.get("predecessor_config_sha256"),
        "predecessor_treatment_build_sha256": config.get(
            "predecessor_treatment_build_sha256"
        ),
        "corrected_replication_id": config.get("replication_id"),
        "corrected_stage_a_results_path": config.get("corrected_stage_a_results_path"),
        "original_stage_a_status": "PRESERVED_28_COMPLETED",
        "stage_a_status": "E16_A_R1_PLANNED_NOT_RUN",
        "stage_b_gate_status": "NOT_COMPUTED",
        "stage_b_status": "BLOCKED_PENDING_CORRECTED_GATE",
        "generated_at": utc_now(),
    }
    path = RESULTS_ROOT / "manifests" / "E16_IMPLEMENTATION_MANIFEST.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def write_planned_stage_a_manifest(config: dict[str, Any]) -> dict[str, Any]:
    rows = build_run_matrix(config, "stage_a")
    manifest = {
        "design_id": config["design_id"],
        "evidence_role": "TRAINING",
        "status": "PLANNED_NOT_RUN",
        "episode_count": len(rows),
        "no_replacement_seed": True,
        "runs": rows,
    }
    if config.get("replication_id") == "E16-A-R1":
        path = (
            REPO_ROOT
            / config["corrected_stage_a_results_path"]
            / "E16_STAGE_A_R1_RUN_MANIFEST.json"
        )
    else:
        path = RESULTS_ROOT / "stage_a" / "E16_STAGE_A_RUN_MANIFEST.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def write_planned_stage_b_manifest(
    config: dict[str, Any], c_star: int, gate: dict[str, Any]
) -> dict[str, Any]:
    rows = build_run_matrix(config, "stage_b", c_star=c_star)
    manifest = {
        "design_id": config["design_id"],
        "evidence_role": "TRAINING",
        "status": "PLANNED_NOT_RUN",
        "episode_count": len(rows),
        "selected_C_star": c_star,
        "gate_input_hashes": gate["input_result_hashes"],
        "no_replacement_seed": True,
        "runs": rows,
    }
    path = RESULTS_ROOT / "stage_b" / "E16_STAGE_B_RUN_MANIFEST.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing.get("selected_C_star") != c_star:
            raise ConfigError("existing Stage B manifest has a different C*")
        return existing
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def write_pretraining_artifacts(
    config: dict[str, Any], e0_report: dict[str, Any]
) -> None:
    write_planned_stage_a_manifest(config)
    analysis_dir = RESULTS_ROOT / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    (analysis_dir / "E16_STAGE_A_ANALYSIS.md").write_text(
        "# E16 Stage A Analysis\n\nSTATUS: NOT_RUN\n\nStage A was intentionally not executed during implementation/E0.\n",
        encoding="utf-8",
    )
    gate = {
        "design_id": config["design_id"],
        "eligible_cells": [],
        "metrics_by_cell": {},
        "selected_C_star": None,
        "gate_status": "NOT_COMPUTED_STAGE_A_NOT_RUN",
        "input_result_hashes": {},
        "analysis_code_hash": sha256_file(
            REPO_ROOT / "src" / "agricola" / "e16" / "analysis.py"
        ),
        "timestamp": e0_report["generated_at"],
    }
    (analysis_dir / "E16_STAGE_B_GATE.json").write_text(
        json.dumps(gate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def save_training_episode(config: dict[str, Any], payload: dict[str, Any]) -> None:
    result = payload["result"]
    stage_dir = (
        REPO_ROOT / config["corrected_stage_a_results_path"]
        if result["stage"] == "stage_a" and config.get("replication_id") == "E16-A-R1"
        else RESULTS_ROOT / result["stage"]
    )
    stage_dir.mkdir(parents=True, exist_ok=True)
    result_path = stage_dir / f"{result['episode_id']}.json"
    if result_path.exists():
        raise ConfigError(
            f"run already exists; automatic rerun forbidden: {result_path.name}"
        )
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_jsonl(stage_dir / f"{result['episode_id']}.events.jsonl", payload["ledger"])
    manifest_name = (
        "E16_STAGE_A_R1_RUN_MANIFEST.json"
        if result["stage"] == "stage_a" and config.get("replication_id") == "E16-A-R1"
        else f"E16_{result['stage'].upper()}_RUN_MANIFEST.json"
    )
    manifest_path = stage_dir / manifest_name
    if not manifest_path.is_file():
        raise ConfigError(f"missing frozen run manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    matches = [
        row
        for row in manifest["runs"]
        if row["cell_id"] == result["cell_id"]
        and row["seed"] == result["seed"]
        and row["treatment_seat"] == result["treatment_seat"]
    ]
    if len(matches) != 1:
        raise ConfigError("episode identity is absent or duplicated in frozen manifest")
    matches[0].update(
        {
            "status": "COMPLETED"
            if result["completed"]
            else "RETAINED_GAMEPLAY_FAILURE",
            "result_path": str(result_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "result_sha256": sha256_file(result_path),
            "completed_at": result["completed_at"],
        }
    )
    statuses = {row["status"] for row in manifest["runs"]}
    manifest["status"] = "COMPLETED" if "PLANNED" not in statuses else "PARTIAL"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def require_e0_pass(config: dict[str, Any]) -> None:
    manifest_path = RESULTS_ROOT / "manifests" / "E16_IMPLEMENTATION_MANIFEST.json"
    if not manifest_path.is_file():
        raise ConfigError("E16 TRAINING is blocked until E0 is recorded")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("instrumentation_gate_status") != "PASS":
        raise ConfigError("E16 TRAINING is blocked because E0 did not pass")
    if manifest.get("config_sha256") != config["configuration_sha256"]:
        raise ConfigError("E0 manifest does not match the current frozen configuration")
    if manifest.get("treatment_build_sha256") != config["treatment_build_sha256"]:
        raise ConfigError("E0 manifest does not match the current treatment build")


def load_verified_stage_b_gate(
    config: dict[str, Any], gate_path: Path
) -> dict[str, Any]:
    """Recompute the gate from hashed Stage A inputs before authorizing Stage B."""

    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    if gate.get("gate_status") != "STAGE_B_AUTHORIZED":
        raise ConfigError("Stage B requested without positive frozen gate")
    stage_a_root = (
        REPO_ROOT / config["corrected_stage_a_results_path"]
        if config.get("replication_id") == "E16-A-R1"
        else RESULTS_ROOT / "stage_a"
    )
    rows, hashes = load_episode_results(stage_a_root)
    validate_complete_matrix(rows, build_run_matrix(config, "stage_a"))
    analysis_path = REPO_ROOT / "src" / "agricola" / "e16" / "analysis.py"
    recomputed = compute_stage_b_gate(
        rows,
        hashes,
        sha256_file(analysis_path),
        gate.get("timestamp", ""),
    )
    if gate != recomputed:
        raise ConfigError("Stage B gate does not match deterministic recomputation")
    return gate


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Run exact frozen E16 TRAINING episodes"
    )
    parser.add_argument("--stage", choices=("stage_a", "stage_b"), required=True)
    parser.add_argument("--cell", required=True)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--seat", required=True, type=int)
    parser.add_argument(
        "--gate", type=Path, default=RESULTS_ROOT / "analysis" / "E16_STAGE_B_GATE.json"
    )
    args = parser.parse_args(argv)
    config = load_frozen_config()
    require_e0_pass(config)
    c_star = None
    if args.stage == "stage_b":
        gate = load_verified_stage_b_gate(config, args.gate)
        c_star = gate.get("selected_C_star")
        write_planned_stage_b_manifest(config, c_star, gate)
    payload = run_frozen_episode(
        config,
        stage=args.stage,
        cell_id=args.cell,
        seed=args.seed,
        treatment_seat=args.seat,
        c_star=c_star,
    )
    save_training_episode(config, payload)
    print(json.dumps(payload["result"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
