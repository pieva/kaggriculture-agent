#!/usr/bin/env python3
"""Matched development ablation of D27 versus frozen V4D D28."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.observation_contract import stable_payload_hash
from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4D_CONFIG_PATH,
    create_codex_e17_batched_cluster_routing_v4,
)
from agricola.strategy.codex.codex_e17_post_feed_capacity_routing_v5_d27 import (
    DEFAULT_V5_D27_CONFIG_PATH,
    create_codex_e17_post_feed_capacity_routing_v5_d27,
)
from experiments.e17.tools.codex.run_codex_e17_batched_cluster_routing_v4_development import (
    _aggregate,
    _common_gates,
    _telemetry,
)
from experiments.e17.tools.codex.run_codex_e17_service_routing_v3_development import (
    _capture,
    _counts,
    _eod_losses,
    _farm,
    _terminal_residual,
    _unlock_timing,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUTPUT_PATH = (
    REPO_ROOT
    / "experiments/e17/artifacts/derived/codex/"
    / "E17_2_D27_HANDOFF_ABLATION_DEVELOPMENT_METRICS.json"
)
CANDIDATE_SOURCE_PATH = (
    REPO_ROOT
    / "src/agricola/strategy/codex/"
    / "codex_e17_post_feed_capacity_routing_v5_d27.py"
)
CONTROL_SOURCE_PATH = (
    REPO_ROOT / "src/agricola/strategy/codex/codex_e17_batched_cluster_routing_v4.py"
)
POLICIES = ("d27_candidate", "v4d_d28_control")
EXPECTED_FREEZE = {
    "candidate_source": "38F78316A2CE6E44258C3A972A8FFBE3AF672F07F0883924459A6F4B946CB0D8",
    "candidate_config": "028D5F4175DA9757C639C49DAA6CCD58031C94D9C806CE343DB95A0A6B11F717",
    "control_source": "9350F8B327B972C703136EB6411F03C74B2A80F6A75A9D99C3E4CA614A60B2A4",
    "control_config": "CA7A6E13CF991185E823325D8220E0682388AC18EB446BB206C0A30ACAB45595",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _freeze_hashes() -> dict[str, str]:
    return {
        "candidate_source": _sha256(CANDIDATE_SOURCE_PATH),
        "candidate_config": _sha256(DEFAULT_V5_D27_CONFIG_PATH),
        "control_source": _sha256(CONTROL_SOURCE_PATH),
        "control_config": _sha256(DEFAULT_V4D_CONFIG_PATH),
    }


def _make_policy(name: str, context: dict[str, Any]):
    if name == "d27_candidate":
        return create_codex_e17_post_feed_capacity_routing_v5_d27(
            run_context=context
        )
    return create_codex_e17_batched_cluster_routing_v4(
        run_context=context,
        config_path=DEFAULT_V4D_CONFIG_PATH,
    )


def _run(seed: int, seat: int, policy_name: str) -> dict[str, Any]:
    context = {
        "run_id": f"E17-D27-{policy_name}-S{seed}-P{seat}",
        "episode_id": f"E17-D27-{policy_name}-S{seed}-P{seat}",
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
    telemetry = _telemetry("post_feed_v4d", policy)
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
                _farm(state[seat].get("observation", {}) or {}, seat).get("hands", [])
                or []
            )
            for state in env.steps
        ),
        "unlock_timing": _unlock_timing(env.steps, seat),
        "final_quadrants": _counts(farm),
        "terminal_residual": _terminal_residual(observation.get("private", {}) or {}),
        **telemetry,
    }
    print(
        f"{policy_name:16s} seed={seed} p{seat} reward={row['reward']:.0f} "
        f"move/service={row['move_per_service']:.3f} "
        f"ledger={row['ledger_record_count']} escapes={row['strict_eod_escapes']}",
        flush=True,
    )
    return row


def run_matrix(seeds: list[int]) -> dict[str, Any]:
    freeze_hashes = _freeze_hashes()
    if freeze_hashes != EXPECTED_FREEZE:
        raise RuntimeError(
            "freeze mismatch; preregister again before execution: "
            f"expected={EXPECTED_FREEZE}, actual={freeze_hashes}"
        )
    rows = [
        _run(seed, seat, policy)
        for seed in seeds
        for seat in (0, 1)
        for policy in POLICIES
    ]
    by_policy = {
        policy: [row for row in rows if row["policy"] == policy]
        for policy in POLICIES
    }
    candidate = _aggregate(by_policy["d27_candidate"])
    control = _aggregate(by_policy["v4d_d28_control"])
    lookup = {
        (row["seed"], row["seat"], row["policy"]): row for row in rows
    }
    matched = []
    for seed in seeds:
        for seat in (0, 1):
            candidate_row = lookup[(seed, seat, "d27_candidate")]
            control_row = lookup[(seed, seat, "v4d_d28_control")]
            delta = candidate_row["reward"] - control_row["reward"]
            matched.append(
                {
                    "seed": seed,
                    "seat": seat,
                    "candidate_reward": candidate_row["reward"],
                    "control_reward": control_row["reward"],
                    "delta": delta,
                    "delta_pct": 100 * delta / control_row["reward"],
                    "action_stream_diverged": candidate_row["action_stream_sha256"]
                    != control_row["action_stream_sha256"],
                }
            )
    nonnegative = sum(item["delta"] >= 0 for item in matched)
    gates = {
        **_common_gates(candidate),
        "mean_reward_not_below_v4d_d28": (
            candidate["mean_reward"] >= control["mean_reward"]
        ),
        "at_least_four_of_six_matched_nonnegative": nonnegative >= 4,
        "worst_matched_delta_pct_at_least_minus_two": min(
            item["delta_pct"] for item in matched
        )
        >= -2.0,
        "move_per_service_not_above_v4d_d28": (
            candidate["move_per_service"] <= control["move_per_service"]
        ),
        "all_action_streams_diverged": all(
            item["action_stream_diverged"] for item in matched
        ),
        "candidate_unit_ledger_larger_than_control": (
            candidate["unit_ledger_record_count"]
            > control["unit_ledger_record_count"]
        ),
        "post_feed_capacity_mechanism_observed": (
            candidate["capacity_flush_trigger_events"] > 0
            and candidate["post_feed_wheat_carrier_releases"] > 0
        ),
    }
    summary = {
        "schema_version": "E17_2_D27_HANDOFF_ABLATION_DEVELOPMENT_V1",
        "epistemic_role": "DEVELOPMENT_ONLY",
        "causal_family": "ISOLATED_ROUTING_HANDOFF_DAY_D28_TO_D27",
        "candidate": "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V5-D27",
        "control": "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28",
        "freeze_hashes": freeze_hashes,
        "seeds": seeds,
        "seats": [0, 1],
        "opponent": "INERT_PASS_POLICY",
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "runs": len(rows),
        "aggregates": {"d27_candidate": candidate, "v4d_d28_control": control},
        "mean_reward_delta": candidate["mean_reward"] - control["mean_reward"],
        "mean_reward_delta_pct": 100
        * (candidate["mean_reward"] / control["mean_reward"] - 1),
        "matched_nonnegative": nonnegative,
        "matched_total": len(matched),
        "min_matched_delta": min(item["delta"] for item in matched),
        "min_matched_delta_pct": min(item["delta_pct"] for item in matched),
        "matched_comparisons": matched,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
        "market_stress_admission": "PASS" if all(gates.values()) else "BLOCKED",
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
        "--seeds", nargs="+", type=int, default=manifest["seed_policy"]["e17_0_seeds"]
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
