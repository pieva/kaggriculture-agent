#!/usr/bin/env python3
"""Matched development ablation for E17.2 V4A batching and V4B affinity."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.observation_contract import stable_payload_hash
from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4A_CONFIG_PATH,
    DEFAULT_V4B_CONFIG_PATH,
    DEFAULT_V4C_CONFIG_PATH,
    DEFAULT_V4D_CONFIG_PATH,
    create_codex_e17_batched_cluster_routing_v4,
    load_v4_config,
)
from agricola.strategy.codex.codex_e17_reactive_service_routing_v3 import (
    create_codex_e17_reactive_service_routing_v3,
)
from experiments.e17.tools.codex.run_codex_e17_service_routing_v3_development import (
    _capture,
    _counts,
    _eod_losses,
    _farm,
    _terminal_residual,
    _unlock_timing,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUTPUT_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/artifacts/derived/"
    / "E17_2_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_METRICS.json"
)
POLICIES = ("batched_v4a", "clustered_v4b", "service_routing_v3")
CLASSIFIED = {"EXECUTED", "NOT_EXECUTED", "UNKNOWN"}


def _make_policy(name: str, context: dict[str, Any]):
    if name == "batched_v4a":
        return create_codex_e17_batched_cluster_routing_v4(
            run_context=context,
            config_path=DEFAULT_V4A_CONFIG_PATH,
        )
    if name == "clustered_v4b":
        return create_codex_e17_batched_cluster_routing_v4(
            run_context=context,
            config_path=DEFAULT_V4B_CONFIG_PATH,
        )
    if name == "capacity_v4c":
        return create_codex_e17_batched_cluster_routing_v4(
            run_context=context,
            config_path=DEFAULT_V4C_CONFIG_PATH,
        )
    if name == "post_feed_v4d":
        return create_codex_e17_batched_cluster_routing_v4(
            run_context=context,
            config_path=DEFAULT_V4D_CONFIG_PATH,
        )
    return create_codex_e17_reactive_service_routing_v3(run_context=context)


def _telemetry(name: str, policy: Any) -> dict[str, Any]:
    if name == "service_routing_v3":
        instance = policy.codex_e17_service_routing_v3_instance
        telemetry = instance.telemetry_snapshot()
        extras = {
            "deferred_drop_opportunities": 0,
            "batched_harvest_services": 0,
            "deadline_drop_assignments": 0,
            "cluster_initial_assignments": 0,
            "cluster_sticky_assignments": 0,
            "cluster_switches": 0,
            "cluster_switch_rate": 0.0,
            "max_carried_sellable_units": 0,
            "capacity_flush_trigger_events": 0,
            "capacity_flush_active_batches": 0,
            "post_feed_wheat_carrier_releases": 0,
        }
    else:
        instance = policy.codex_e17_batched_cluster_routing_instance
        telemetry = instance.telemetry_snapshot()
        extras = {
            key: telemetry[key]
            for key in (
                "deferred_drop_opportunities",
                "batched_harvest_services",
                "deadline_drop_assignments",
                "cluster_initial_assignments",
                "cluster_sticky_assignments",
                "cluster_switches",
                "cluster_switch_rate",
                "max_carried_sellable_units",
                "capacity_flush_trigger_events",
                "capacity_flush_active_batches",
                "post_feed_wheat_carrier_releases",
            )
        }
    unit_records = telemetry["ledger_records"]
    market_records = telemetry["market_ledger_records"]
    return {
        "errors": instance.error_count,
        "fallbacks": instance.fallback_count,
        "routing_commands": telemetry["routing_commands"],
        "service_commands": telemetry["service_commands"],
        "move_per_service": telemetry["move_per_service"],
        "action_counts": telemetry["action_counts"],
        "task_counts": telemetry["task_counts"],
        "ledger_record_count": len(unit_records),
        "ledger_classified_count": sum(
            record.get("outcome") in CLASSIFIED for record in unit_records
        ),
        "execution_outcomes": telemetry["execution_outcomes"],
        "d28_explicit_drop_count": sum(
            record.get("day") == 28
            and record.get("requested")
            and record["requested"][0] == "DROP"
            for record in unit_records
        ),
        "coordinated_market_batches": telemetry["coordinated_market_batches"],
        "coordinated_sell_orders": telemetry["coordinated_sell_orders"],
        "coordinated_sell_units_requested": telemetry[
            "coordinated_sell_units_requested"
        ],
        "non_sell_preservation_failures": telemetry[
            "non_sell_preservation_failures"
        ],
        "market_ledger_record_count": len(market_records),
        "market_ledger_classified_count": sum(
            record.get("outcome") in CLASSIFIED for record in market_records
        ),
        "market_execution_outcomes": telemetry["market_execution_outcomes"],
        **extras,
    }


def _run(seed: int, seat: int, policy_name: str) -> dict[str, Any]:
    context = {
        "run_id": f"E17-ROUTING-V4-{policy_name}-S{seed}-P{seat}",
        "episode_id": f"E17-ROUTING-V4-{policy_name}-S{seed}-P{seat}",
        "seed": seed,
        "player_position": seat,
    }
    policy = _make_policy(policy_name, context)
    actions: list[dict[str, Any]] = []
    agents = (
        [_capture(policy, actions), inert_pass_policy]
        if seat == 0
        else [inert_pass_policy, _capture(policy, actions)]
    )
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    terminal = env.steps[-1]
    observation = terminal[seat].get("observation", {}) or {}
    farm = _farm(observation, seat)
    escapes, crop_losses = _eod_losses(env.steps, seat)
    telemetry = _telemetry(policy_name, policy)
    row = {
        "seed": seed,
        "seat": seat,
        "policy": policy_name,
        "reward": float(terminal[seat].get("reward") or 0.0),
        "status": terminal[seat].get("status"),
        "opponent_reward": float(terminal[1 - seat].get("reward") or 0.0),
        "action_batches": len(actions),
        "action_stream_sha256": stable_payload_hash(actions),
        "invalid_action_shapes": sum(
            1
            for action in actions
            if not isinstance(action, dict)
            or not isinstance(action.get("farmer"), list)
            or not action.get("farmer")
            or not isinstance(action.get("hands", []), list)
            or not isinstance(action.get("market", []), list)
            or len(action.get("market", []) or []) > 10
        ),
        "strict_eod_escapes": escapes,
        "strict_eod_crop_losses": crop_losses,
        "max_hands": max(
            len(
                _farm(state[seat].get("observation", {}) or {}, seat).get(
                    "hands", []
                )
                or []
            )
            for state in env.steps
        ),
        "unlock_timing": _unlock_timing(env.steps, seat),
        "final_quadrants": _counts(farm),
        "terminal_residual": _terminal_residual(
            observation.get("private", {}) or {}
        ),
        **telemetry,
    }
    print(
        f"{policy_name:20s} seed={seed} p{seat} reward={row['reward']:.0f} "
        f"move/service={row['move_per_service']:.3f} "
        f"batch={row['batched_harvest_services']} "
        f"switch={row['cluster_switch_rate']:.3f} "
        f"residual={row['terminal_residual']['sellable_units']}",
        flush=True,
    )
    return row


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    unit_records = sum(row["ledger_record_count"] for row in rows)
    unit_classified = sum(row["ledger_classified_count"] for row in rows)
    market_records = sum(row["market_ledger_record_count"] for row in rows)
    market_classified = sum(
        row["market_ledger_classified_count"] for row in rows
    )
    routing = sum(row["routing_commands"] for row in rows)
    services = sum(row["service_commands"] for row in rows)
    cluster_sticky = sum(row["cluster_sticky_assignments"] for row in rows)
    cluster_switches = sum(row["cluster_switches"] for row in rows)
    action_counts = sum((Counter(row["action_counts"]) for row in rows), Counter())
    return {
        "runs": len(rows),
        "mean_reward": statistics.mean(row["reward"] for row in rows),
        "routing_commands": routing,
        "service_commands": services,
        "move_per_service": routing / services if services else None,
        "action_counts": dict(action_counts),
        "strict_eod_escapes": sum(row["strict_eod_escapes"] for row in rows),
        "strict_eod_crop_losses": sum(
            row["strict_eod_crop_losses"] for row in rows
        ),
        "terminal_sellable_residual_units": sum(
            row["terminal_residual"]["sellable_units"] for row in rows
        ),
        "technical_errors": sum(row["errors"] for row in rows),
        "fallbacks": sum(row["fallbacks"] for row in rows),
        "invalid_action_shapes": sum(row["invalid_action_shapes"] for row in rows),
        "non_sell_preservation_failures": sum(
            row["non_sell_preservation_failures"] for row in rows
        ),
        "unit_ledger_record_count": unit_records,
        "unit_ledger_classification_coverage": (
            unit_classified / unit_records if unit_records else 1.0
        ),
        "unit_execution_outcomes": dict(
            sum((Counter(row["execution_outcomes"]) for row in rows), Counter())
        ),
        "market_ledger_record_count": market_records,
        "market_ledger_classification_coverage": (
            market_classified / market_records if market_records else 1.0
        ),
        "market_execution_outcomes": dict(
            sum(
                (Counter(row["market_execution_outcomes"]) for row in rows),
                Counter(),
            )
        ),
        "d28_explicit_drop_count": sum(
            row["d28_explicit_drop_count"] for row in rows
        ),
        "deferred_drop_opportunities": sum(
            row["deferred_drop_opportunities"] for row in rows
        ),
        "batched_harvest_services": sum(
            row["batched_harvest_services"] for row in rows
        ),
        "deadline_drop_assignments": sum(
            row["deadline_drop_assignments"] for row in rows
        ),
        "cluster_initial_assignments": sum(
            row["cluster_initial_assignments"] for row in rows
        ),
        "cluster_sticky_assignments": cluster_sticky,
        "cluster_switches": cluster_switches,
        "cluster_switch_rate": (
            cluster_switches / (cluster_sticky + cluster_switches)
            if cluster_sticky + cluster_switches
            else 0.0
        ),
        "max_carried_sellable_units": max(
            row["max_carried_sellable_units"] for row in rows
        ),
        "capacity_flush_trigger_events": sum(
            row["capacity_flush_trigger_events"] for row in rows
        ),
        "capacity_flush_active_batches": sum(
            row["capacity_flush_active_batches"] for row in rows
        ),
        "post_feed_wheat_carrier_releases": sum(
            row["post_feed_wheat_carrier_releases"] for row in rows
        ),
        "coordinated_market_batches": sum(
            row["coordinated_market_batches"] for row in rows
        ),
        "coordinated_sell_orders": sum(
            row["coordinated_sell_orders"] for row in rows
        ),
        "coordinated_sell_units_requested": sum(
            row["coordinated_sell_units_requested"] for row in rows
        ),
    }


def _common_gates(aggregate: dict[str, Any]) -> dict[str, bool]:
    return {
        "technical_errors_zero": aggregate["technical_errors"] == 0,
        "fallbacks_zero": aggregate["fallbacks"] == 0,
        "invalid_action_shapes_zero": aggregate["invalid_action_shapes"] == 0,
        "animal_escapes_zero": aggregate["strict_eod_escapes"] == 0,
        "unit_ledger_coverage_one": (
            aggregate["unit_ledger_classification_coverage"] == 1.0
        ),
        "market_ledger_coverage_one": (
            aggregate["market_ledger_classification_coverage"] == 1.0
        ),
        "non_sell_orders_preserved": (
            aggregate["non_sell_preservation_failures"] == 0
        ),
        "terminal_sellable_residual_zero": (
            aggregate["terminal_sellable_residual_units"] == 0
        ),
    }


def run_matrix(seeds: list[int]) -> dict[str, Any]:
    rows = [
        _run(seed, seat, policy_name)
        for seed in seeds
        for seat in (0, 1)
        for policy_name in POLICIES
    ]
    by_policy = {
        name: [row for row in rows if row["policy"] == name]
        for name in POLICIES
    }
    aggregates = {
        name: _aggregate(policy_rows)
        for name, policy_rows in by_policy.items()
    }
    lookup = {
        (row["seed"], row["seat"], row["policy"]): row for row in rows
    }
    v4a_deltas = [
        lookup[(seed, seat, "batched_v4a")]["reward"]
        - lookup[(seed, seat, "service_routing_v3")]["reward"]
        for seed in seeds
        for seat in (0, 1)
    ]
    v4b_deltas = [
        lookup[(seed, seat, "clustered_v4b")]["reward"]
        - lookup[(seed, seat, "batched_v4a")]["reward"]
        for seed in seeds
        for seat in (0, 1)
    ]
    v4a = aggregates["batched_v4a"]
    v4b = aggregates["clustered_v4b"]
    v3 = aggregates["service_routing_v3"]
    v4a_gates = {
        **_common_gates(v4a),
        "batched_harvest_present": v4a["batched_harvest_services"] > 0,
        "d28_explicit_drop_zero": v4a["d28_explicit_drop_count"] == 0,
        "move_per_service_below_v3": (
            v4a["move_per_service"] < v3["move_per_service"]
        ),
        "mean_reward_not_below_v3": v4a["mean_reward"] >= v3["mean_reward"],
    }
    v4b_delta_pct = 100 * (v4b["mean_reward"] / v4a["mean_reward"] - 1)
    v4b_gates = {
        **_common_gates(v4b),
        "cluster_sticky_assignments_present": (
            v4b["cluster_sticky_assignments"] > 0
        ),
        "cluster_switch_rate_not_above_v4a": (
            v4b["cluster_switch_rate"] <= v4a["cluster_switch_rate"]
        ),
        "move_per_service_not_above_v4a": (
            v4b["move_per_service"] <= v4a["move_per_service"]
        ),
        "mean_reward_delta_at_least_minus_half_pct": v4b_delta_pct >= -0.5,
    }
    config_a = load_v4_config(DEFAULT_V4A_CONFIG_PATH)
    config_b = load_v4_config(DEFAULT_V4B_CONFIG_PATH)
    summary = {
        "schema_version": "E17_2_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_V1",
        "epistemic_role": "DEVELOPMENT_ONLY",
        "policies": list(POLICIES),
        "candidate_a": config_a["model_spec_version"],
        "candidate_b": config_b["model_spec_version"],
        "control": "CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28",
        "activation_day": 28,
        "liquidation_day": 29,
        "seeds": seeds,
        "seats": [0, 1],
        "opponent": "INERT_PASS_POLICY",
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "runs": len(rows),
        "aggregates": aggregates,
        "v4a_mean_matched_delta_vs_v3": statistics.mean(v4a_deltas),
        "v4a_min_matched_delta_vs_v3": min(v4a_deltas),
        "v4a_delta_pct_vs_v3": 100
        * (v4a["mean_reward"] / v3["mean_reward"] - 1),
        "v4b_mean_matched_delta_vs_v4a": statistics.mean(v4b_deltas),
        "v4b_min_matched_delta_vs_v4a": min(v4b_deltas),
        "v4b_delta_pct_vs_v4a": v4b_delta_pct,
        "gates": {"v4a": v4a_gates, "v4b": v4b_gates},
        "v4a_all_gates_pass": all(v4a_gates.values()),
        "v4b_all_gates_pass": all(v4b_gates.values()),
        "results": rows,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=manifest["seed_policy"]["e17_0_seeds"],
    )
    args = parser.parse_args(argv)
    forbidden = set(manifest["seed_policy"]["holdout"]["seeds"]) | set(
        manifest["seed_policy"]["final_confirmation"]["seeds"]
    )
    if forbidden.intersection(args.seeds):
        raise SystemExit("holdout/final seeds are forbidden in development")
    if not set(args.seeds).issubset(set(manifest["seed_policy"]["development"])):
        raise SystemExit("only manifest development seeds are allowed")
    summary = run_matrix(args.seeds)
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "results"},
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if all(
        aggregate["technical_errors"] == 0
        for aggregate in summary["aggregates"].values()
    ) else 1


if __name__ == "__main__":
    sys.exit(main())
