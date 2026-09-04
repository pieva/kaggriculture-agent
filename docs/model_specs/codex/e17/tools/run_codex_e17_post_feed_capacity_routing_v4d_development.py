#!/usr/bin/env python3
"""Matched development benchmark for post-feed capacity flush V4D."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4D_CONFIG_PATH,
)
from experiments.e17.tools.codex.run_codex_e17_capacity_aware_batched_routing_v4c_development import (
    run_candidate_matrix,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUTPUT_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/artifacts/derived/"
    / "E17_2_POST_FEED_CAPACITY_ROUTING_V4D_DEVELOPMENT_METRICS.json"
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
    summary = run_candidate_matrix(
        args.seeds,
        candidate_policy="post_feed_v4d",
        config_path=DEFAULT_V4D_CONFIG_PATH,
        schema_version="E17_2_POST_FEED_CAPACITY_V4D_DEVELOPMENT_V1",
        output_path=OUTPUT_PATH,
        require_post_feed_release=True,
    )
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "results"},
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if summary["aggregates"]["post_feed_v4d"]["technical_errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
