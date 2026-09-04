#!/usr/bin/env python3
"""Matched development benchmark for capacity-aware E17.2 V4C."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4C_CONFIG_PATH,
    load_v4_config,
)
from experiments.e17.tools.codex.run_codex_e17_batched_cluster_routing_v4_development import (
    _aggregate,
    _common_gates,
    _run,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUTPUT_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/artifacts/derived/"
    / "E17_2_CAPACITY_AWARE_BATCHED_ROUTING_V4C_DEVELOPMENT_METRICS.json"
)
POLICIES = ("capacity_v4c", "service_routing_v3")


def run_candidate_matrix(
    seeds: list[int],
    *,
    candidate_policy: str,
    config_path: Path,
    schema_version: str,
    output_path: Path,
    require_post_feed_release: bool = False,
) -> dict[str, Any]:
    policies = (candidate_policy, "service_routing_v3")
    rows = [
        _run(seed, seat, policy_name)
        for seed in seeds
        for seat in (0, 1)
        for policy_name in policies
    ]
    by_policy = {
        name: [row for row in rows if row["policy"] == name]
        for name in policies
    }
    aggregates = {
        name: _aggregate(policy_rows)
        for name, policy_rows in by_policy.items()
    }
    candidate = aggregates[candidate_policy]
    control = aggregates["service_routing_v3"]
    lookup = {
        (row["seed"], row["seat"], row["policy"]): row for row in rows
    }
    deltas = [
        lookup[(seed, seat, candidate_policy)]["reward"]
        - lookup[(seed, seat, "service_routing_v3")]["reward"]
        for seed in seeds
        for seat in (0, 1)
    ]
    delta_pct = 100 * (
        candidate["mean_reward"] / control["mean_reward"] - 1
    )
    gates = {
        **_common_gates(candidate),
        "capacity_flush_trigger_present": (
            candidate["capacity_flush_trigger_events"] > 0
        ),
        "d28_explicit_drop_present": candidate["d28_explicit_drop_count"] > 0,
        "batched_harvest_present": candidate["batched_harvest_services"] > 0,
        "move_per_service_below_v3": (
            candidate["move_per_service"] < control["move_per_service"]
        ),
        "mean_reward_not_below_v3": (
            candidate["mean_reward"] >= control["mean_reward"]
        ),
    }
    if require_post_feed_release:
        gates["post_feed_wheat_carrier_release_present"] = (
            candidate["post_feed_wheat_carrier_releases"] > 0
        )
    config = load_v4_config(config_path)
    summary = {
        "schema_version": schema_version,
        "epistemic_role": "DEVELOPMENT_ONLY",
        "candidate": config["model_spec_version"],
        "control": "CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28",
        "causal_family": config["causal_family"],
        "activation_day": config["activation_day"],
        "liquidation_day": config["liquidation_day"],
        "capacity_flush_trigger_ratio": config["capacity_flush_trigger_ratio"],
        "capacity_flush_target_ratio": config["capacity_flush_target_ratio"],
        "seeds": seeds,
        "seats": [0, 1],
        "opponent": "INERT_PASS_POLICY",
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "runs": len(rows),
        "aggregates": aggregates,
        "mean_matched_delta_vs_v3": statistics.mean(deltas),
        "min_matched_delta_vs_v3": min(deltas),
        "delta_pct_vs_v3": delta_pct,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
        "results": rows,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return summary


def run_matrix(seeds: list[int]) -> dict[str, Any]:
    return run_candidate_matrix(
        seeds,
        candidate_policy="capacity_v4c",
        config_path=DEFAULT_V4C_CONFIG_PATH,
        schema_version="E17_2_CAPACITY_AWARE_BATCHED_V4C_DEVELOPMENT_V1",
        output_path=OUTPUT_PATH,
    )


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
    return 0 if summary["aggregates"]["capacity_v4c"]["technical_errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
